from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Survey, Question, Choice
from .forms import SurveyForm, QuestionForm, ChoiceForm, SurveyResponseForm

class SurveyListView(ListView):
    model = Survey
    template_name = 'surveys/survey_list.html'
    context_object_name = 'surveys'
    paginate_by = 10
    
    def get_queryset(self):
        return Survey.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_surveys_count'] = Survey.objects.filter(is_active=True).count()
        return context

class ActiveSurveyListView(ListView):
    model = Survey
    template_name = 'surveys/active_surveys.html'
    context_object_name = 'surveys'
    paginate_by = 10
    
    def get_queryset(self):
        return Survey.objects.filter(is_active=True).order_by('-created_at')

class SurveyDetailView(DetailView):
    model = Survey
    template_name = 'surveys/survey_detail.html'
    context_object_name = 'survey'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = self.get_object()
        context['questions_count'] = survey.questions.count()
        
        # Якщо багатосторінкове опитування
        if survey.is_multi_page:
            context['pages'] = survey.questions.values_list('page', flat=True).distinct().order_by('page')
        
        return context

class SurveyTakeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk, is_active=True)
        
        # Перевіряємо, чи користувач вже проходив опитування
        if hasattr(request.user, 'survey_responses') and request.user.survey_responses.filter(survey=survey).exists():
            messages.warning(request, 'Ви вже проходили це опитування.')
            return redirect('surveys:survey_results', pk=pk)
        
        if survey.is_multi_page:
            # Переходимо на першу сторінку
            return redirect('surveys:survey_page', survey_id=pk, page=1)
        else:
            # Одно сторінкове опитування
            questions = survey.questions.all().order_by('order')
            form = SurveyResponseForm(questions=questions)
            
            # Зберігаємо survey_id в сесії
            request.session['current_survey_id'] = pk
            
            return render(request, 'surveys/survey_take.html', {
                'survey': survey,
                'form': form,
                'questions': questions
            })
    
    def post(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk, is_active=True)
        questions = survey.questions.all().order_by('order')
        form = SurveyResponseForm(request.POST, questions=questions)
        
        if form.is_valid():
            # Зберігаємо відповіді
            for question in questions:
                selected_choice_id = form.cleaned_data.get(f'question_{question.id}')
                if selected_choice_id:
                    choice = Choice.objects.get(id=selected_choice_id)
                    choice.votes += 1
                    choice.save()
            
            messages.success(request, 'Дякуємо за участь в опитуванні!')
            return redirect('surveys:survey_results', pk=pk)
        
        return render(request, 'surveys/survey_take.html', {
            'survey': survey,
            'form': form,
            'questions': questions
        })

class SurveyPageView(LoginRequiredMixin, View):
    def get(self, request, survey_id, page):
        survey = get_object_or_404(Survey, pk=survey_id, is_active=True)
        
        if not survey.is_multi_page:
            return redirect('surveys:survey_take', pk=survey_id)
        
        questions = survey.questions.filter(page=page).order_by('order')
        total_pages = survey.questions.values_list('page', flat=True).distinct().count()
        
        # Зберігаємо survey_id в сесії
        request.session['current_survey_id'] = survey_id
        request.session['current_page'] = page
        
        form = SurveyResponseForm(questions=questions)
        
        return render(request, 'surveys/survey_page.html', {
            'survey': survey,
            'form': form,
            'questions': questions,
            'current_page': page,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        })
    
    def post(self, request, survey_id, page):
        survey = get_object_or_404(Survey, pk=survey_id, is_active=True)
        questions = survey.questions.filter(page=page).order_by('order')
        
        form = SurveyResponseForm(request.POST, questions=questions)
        
        if form.is_valid():
            # Зберігаємо відповіді для поточної сторінки в сесії
            if 'survey_responses' not in request.session:
                request.session['survey_responses'] = {}
            
            for question in questions:
                selected_choice_id = form.cleaned_data.get(f'question_{question.id}')
                if selected_choice_id:
                    request.session['survey_responses'][str(question.id)] = selected_choice_id
            
            request.session.modified = True
            
            total_pages = survey.questions.values_list('page', flat=True).distinct().count()
            
            if page < total_pages:
                return redirect('surveys:survey_page', survey_id=survey_id, page=page + 1)
            else:
                # Це остання сторінка, зберігаємо всі відповіді
                responses = request.session.get('survey_responses', {})
                for question_id, choice_id in responses.items():
                    choice = Choice.objects.get(id=choice_id)
                    choice.votes += 1
                    choice.save()
                
                # Очищаємо сесію
                if 'survey_responses' in request.session:
                    del request.session['survey_responses']
                
                messages.success(request, 'Дякуємо за участь в опитуванні!')
                return redirect('surveys:survey_results', pk=survey_id)
        
        return render(request, 'surveys/survey_page.html', {
            'survey': survey,
            'form': form,
            'questions': questions,
            'current_page': page,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        })

class SurveySubmitView(LoginRequiredMixin, View):
    def post(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk)
        # Логіка збереження фінальних відповідей для багатосторінкових опитувань
        messages.success(request, 'Опитування завершено!')
        return redirect('surveys:survey_results', pk=pk)

class SurveyResultsView(DetailView):
    model = Survey
    template_name = 'surveys/survey_results.html'
    context_object_name = 'survey'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = self.get_object()
        
        # Збираємо результати по кожному питанню
        results = []
        for question in survey.questions.all().order_by('page', 'order'):
            choices_data = []
            for choice in question.choices.all():
                choices_data.append({
                    'text': choice.text,
                    'votes': choice.votes,
                    'percentage': (choice.votes / sum(c.votes for c in question.choices.all()) * 100) if question.choices.all() else 0
                })
            
            results.append({
                'question': question,
                'choices': choices_data,
                'total_votes': sum(c.votes for c in question.choices.all())
            })
        
        context['results'] = results
        return context

class SurveyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'surveys/survey_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Опитування створено! Тепер додайте питання.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('surveys:question_add', kwargs={'survey_id': self.object.pk})

class SurveyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'surveys/survey_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Опитування успішно оновлено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('surveys:survey_detail', kwargs={'pk': self.object.pk})

class SurveyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Survey
    template_name = 'surveys/survey_confirm_delete.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('surveys:survey_list')

class QuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'surveys/question_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def dispatch(self, request, *args, **kwargs):
        self.survey = get_object_or_404(Survey, pk=self.kwargs['survey_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey'] = self.survey
        return context
    
    def form_valid(self, form):
        form.instance.survey = self.survey
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Питання додано! Тепер додайте варіанти відповідей.')
        return reverse_lazy('surveys:choice_add', kwargs={'question_id': self.object.pk})

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'surveys/question_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey'] = self.object.survey
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Питання оновлено!')
        return reverse_lazy('surveys:survey_detail', kwargs={'pk': self.object.survey.pk})

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    template_name = 'surveys/question_confirm_delete.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('surveys:survey_detail', kwargs={'pk': self.object.survey.pk})

class ChoiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Choice
    form_class = ChoiceForm
    template_name = 'surveys/choice_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def dispatch(self, request, *args, **kwargs):
        self.question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.question
        context['survey'] = self.question.survey
        return context
    
    def form_valid(self, form):
        form.instance.question = self.question
        messages.success(self.request, 'Варіант відповіді додано!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('surveys:question_update', kwargs={'pk': self.question.pk})

class ChoiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Choice
    form_class = ChoiceForm
    template_name = 'surveys/choice_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.object.question
        context['survey'] = self.object.question.survey
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Варіант відповіді оновлено!')
        return reverse_lazy('surveys:question_update', kwargs={'pk': self.object.question.pk})

class ChoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Choice
    template_name = 'surveys/choice_confirm_delete.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('surveys:question_update', kwargs={'pk': self.object.question.pk})