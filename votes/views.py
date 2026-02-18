from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from .models import Vote, VoteOption, UserVote
from .forms import VoteForm, VoteOptionForm, UserVoteForm

class VoteListView(ListView):
    model = Vote
    template_name = 'votes/vote_list.html'
    context_object_name = 'votes'
    paginate_by = 10
    
    def get_queryset(self):
        return Vote.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['active_count'] = Vote.objects.filter(is_active=True).count()
        context['expired_count'] = Vote.objects.filter(is_active=False).count()
        return context

class ActiveVoteListView(ListView):
    model = Vote
    template_name = 'votes/active_votes.html'
    context_object_name = 'votes'
    paginate_by = 10
    
    def get_queryset(self):
        now = timezone.now()
        return Vote.objects.filter(
            is_active=True
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gt=now)
        ).order_by('-created_at')

class VoteByTypeListView(ListView):
    model = Vote
    template_name = 'votes/vote_by_type.html'
    context_object_name = 'votes'
    paginate_by = 10
    
    def get_queryset(self):
        vote_type = self.kwargs.get('vote_type')
        return Vote.objects.filter(vote_type=vote_type).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vote_type = self.kwargs.get('vote_type')
        
        # Знаходимо назву типу
        type_choices = dict([
            ('highlight', 'Найкращий хайлайт дня'),
            ('post', 'Топ пост тижня'),
            ('weapon', 'Краще a1 чи a4?'),
            ('other', 'Інше'),
        ])
        context['type_name'] = type_choices.get(vote_type, 'Невідомий тип')
        context['current_type'] = vote_type
        return context

class VoteDetailView(DetailView):
    model = Vote
    template_name = 'votes/vote_detail.html'
    context_object_name = 'vote'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vote = self.get_object()
        
        # Перевіряємо, чи користувач вже голосував
        if self.request.user.is_authenticated:
            user_vote = UserVote.objects.filter(user=self.request.user, vote=vote).first()
            context['user_vote'] = user_vote
            context['has_voted'] = user_vote is not None
        
        # Перевіряємо, чи активне голосування
        now = timezone.now()
        context['is_active'] = vote.is_active and (vote.end_date is None or vote.end_date > now)
        
        return context

class VoteCastView(LoginRequiredMixin, View):
    def post(self, request, pk):
        vote = get_object_or_404(Vote, pk=pk)
        
        # Перевіряємо, чи активне голосування
        now = timezone.now()
        if not vote.is_active or (vote.end_date and vote.end_date <= now):
            messages.error(request, 'Це голосування вже закрите.')
            return redirect('votes:vote_detail', pk=pk)
        
        # Перевіряємо, чи користувач вже голосував
        if UserVote.objects.filter(user=request.user, vote=vote).exists():
            messages.error(request, 'Ви вже голосували в цьому опитуванні.')
            return redirect('votes:vote_detail', pk=pk)
        
        option_id = request.POST.get('option')
        if not option_id:
            messages.error(request, 'Будь ласка, оберіть варіант відповіді.')
            return redirect('votes:vote_detail', pk=pk)
        
        option = get_object_or_404(VoteOption, pk=option_id, vote=vote)
        
        # Зберігаємо голос
        UserVote.objects.create(user=request.user, vote=vote, option=option)
        option.votes += 1
        option.save()
        
        messages.success(request, 'Ваш голос враховано!')
        return redirect('votes:vote_results', pk=pk)

class VoteResultsView(DetailView):
    model = Vote
    template_name = 'votes/vote_results.html'
    context_object_name = 'vote'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vote = self.get_object()
        
        # Збираємо результати
        options = vote.options.all().order_by('-votes')
        total_votes = sum(option.votes for option in options)
        
        results = []
        for option in options:
            percentage = (option.votes / total_votes * 100) if total_votes > 0 else 0
            results.append({
                'option': option,
                'percentage': percentage,
            })
        
        context['results'] = results
        context['total_votes'] = total_votes
        
        # Перевіряємо, чи користувач голосував
        if self.request.user.is_authenticated:
            context['user_voted'] = UserVote.objects.filter(user=self.request.user, vote=vote).exists()
        
        return context

class VoteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vote
    form_class = VoteForm
    template_name = 'votes/vote_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Голосування створено! Тепер додайте варіанти відповідей.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('votes:option_add', kwargs={'vote_id': self.object.pk})

class VoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vote
    form_class = VoteForm
    template_name = 'votes/vote_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Голосування успішно оновлено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('votes:vote_detail', kwargs={'pk': self.object.pk})

class VoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vote
    template_name = 'votes/vote_confirm_delete.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('votes:vote_list')

class VoteOptionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = VoteOption
    form_class = VoteOptionForm
    template_name = 'votes/option_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def dispatch(self, request, *args, **kwargs):
        self.vote = get_object_or_404(Vote, pk=self.kwargs['vote_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vote'] = self.vote
        return context
    
    def form_valid(self, form):
        form.instance.vote = self.vote
        messages.success(self.request, 'Варіант відповіді додано!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('votes:vote_detail', kwargs={'pk': self.vote.pk})

class VoteOptionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VoteOption
    form_class = VoteOptionForm
    template_name = 'votes/option_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vote'] = self.object.vote
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Варіант відповіді оновлено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('votes:vote_detail', kwargs={'pk': self.object.vote.pk})

class VoteOptionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VoteOption
    template_name = 'votes/option_confirm_delete.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('votes:vote_detail', kwargs={'pk': self.object.vote.pk})

class PopularVoteListView(ListView):
    model = Vote
    template_name = 'votes/popular_votes.html'
    context_object_name = 'votes'
    paginate_by = 10
    
    def get_queryset(self):
        # Отримуємо голосування з найбільшою кількістю голосів
        votes = Vote.objects.annotate(
            total_votes=Count('options__votes')
        ).order_by('-total_votes')[:20]
        return votes

class DailyVoteView(ListView):
    model = Vote
    template_name = 'votes/daily_vote.html'
    context_object_name = 'votes'
    paginate_by = 10
    
    def get_queryset(self):
        # Голосування за сьогодні
        today = timezone.now().date()
        return Vote.objects.filter(created_at__date=today).order_by('-created_at')

class WeeklyVoteView(ListView):
    model = Vote
    template_name = 'votes/weekly_vote.html'
    context_object_name = 'votes'
    paginate_by = 10
    
    def get_queryset(self):
        # Голосування за останній тиждень
        week_ago = timezone.now() - timezone.timedelta(days=7)
        return Vote.objects.filter(created_at__gte=week_ago).order_by('-created_at')