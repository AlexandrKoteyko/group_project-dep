from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Topic, Message, ForumCategory
from .forms import TopicForm, MessageForm

class CategoryListView(ListView):
    model = ForumCategory
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'

class TopicListView(ListView):
    model = Topic
    template_name = 'forum/topic_list.html'
    context_object_name = 'topics'
    paginate_by = 20
    
    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        queryset = Topic.objects.all()
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'category_id' in self.kwargs:
            context['category'] = get_object_or_404(ForumCategory, pk=self.kwargs['category_id'])
        return context

class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'forum/topic_form.html'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Тему успішно створено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('forum:topic_detail', kwargs={'pk': self.object.pk})

class TopicDetailView(DetailView):
    model = Topic
    template_name = 'forum/topic_detail.html'
    context_object_name = 'topic'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message_form'] = MessageForm()
        context['messages'] = self.object.messages.all().order_by('created_at')
        return context

class TopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'forum/topic_form.html'
    
    def test_func(self):
        topic = self.get_object()
        return self.request.user == topic.created_by or self.request.user.is_moderator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Тему успішно оновлено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('forum:topic_detail', kwargs={'pk': self.object.pk})

class TopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Topic
    template_name = 'forum/topic_confirm_delete.html'
    
    def test_func(self):
        topic = self.get_object()
        return self.request.user == topic.created_by or self.request.user.is_moderator()
    
    def get_success_url(self):
        category_id = self.object.category.id
        return reverse_lazy('forum:topic_by_category', kwargs={'category_id': category_id})

class CloseTopicView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        topic = get_object_or_404(Topic, pk=self.kwargs['pk'])
        return self.request.user.is_moderator()
    
    def post(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        topic.is_closed = not topic.is_closed
        topic.save()
        
        action = "закрито" if topic.is_closed else "відкрито"
        messages.success(request, f'Тему {action}!')
        return redirect('forum:topic_detail', pk=pk)

class PinTopicView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        topic = get_object_or_404(Topic, pk=self.kwargs['pk'])
        return self.request.user.is_moderator()
    
    def post(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        topic.is_pinned = not topic.is_pinned
        topic.save()
        
        action = "закріплено" if topic.is_pinned else "відкріплено"
        messages.success(request, f'Тему {action}!')
        return redirect('forum:topic_detail', pk=pk)

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'forum/message_form.html'
    
    def form_valid(self, form):
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_id'])
        if topic.is_closed and not self.request.user.is_moderator():
            messages.error(self.request, 'Ця тема закрита для нових повідомлень.')
            return redirect('forum:topic_detail', pk=topic.pk)
        
        form.instance.topic = topic
        form.instance.author = self.request.user
        messages.success(self.request, 'Повідомлення додано!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('forum:topic_detail', kwargs={'pk': self.kwargs['topic_id']})

class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'forum/message_form.html'
    
    def test_func(self):
        message = self.get_object()
        return self.request.user == message.author or self.request.user.is_moderator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Повідомлення оновлено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('forum:topic_detail', kwargs={'pk': self.object.topic.pk})

class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'forum/message_confirm_delete.html'
    
    def test_func(self):
        message = self.get_object()
        return self.request.user == message.author or self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('forum:topic_detail', kwargs={'pk': self.object.topic.pk})

class ForumSearchView(ListView):
    model = Topic
    template_name = 'forum/search_results.html'
    context_object_name = 'topics'
    paginate_by = 20
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Topic.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(messages__text__icontains=query)
            ).distinct().order_by('-created_at')
        return Topic.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class LatestTopicsView(ListView):
    model = Topic
    template_name = 'forum/latest_topics.html'
    context_object_name = 'topics'
    paginate_by = 20
    
    def get_queryset(self):
        return Topic.objects.all().order_by('-created_at')