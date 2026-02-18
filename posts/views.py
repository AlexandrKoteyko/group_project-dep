from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Post, Comment, Hashtag
from .forms import PostForm, CommentForm, HashtagForm

class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Post.objects.filter(is_pinned=False).order_by('-created_at')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pinned_posts'] = Post.objects.filter(is_pinned=True)
        context['trending_hashtags'] = Hashtag.objects.all()[:10]  # Топ-10 хештегів
        return context

class PostFeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_feed.html'
    context_object_name = 'posts'
    paginate_by = 20
    
    def get_queryset(self):
        # Показуємо пости від користувачів, на яких підписаний поточний користувач
        # Поки що просто всі пости
        return Post.objects.filter(is_pinned=False).order_by('-created_at')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        
        # Обробка хештегів
        hashtags_text = form.cleaned_data.get('hashtags', '')
        if hashtags_text:
            # Видаляємо символ # якщо він є і розділяємо по комах
            hashtag_names = [name.strip().lower().replace('#', '') for name in hashtags_text.split(',') if name.strip()]
            for name in hashtag_names:
                if name:  # Перевіряємо, що не пустий
                    hashtag, created = Hashtag.objects.get_or_create(name=name)
                    self.object.hashtags.add(hashtag)
        
        messages.success(self.request, 'Пост успішно створено!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.pk})

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        context['can_edit'] = (
            self.request.user == self.object.author or 
            self.request.user.is_moderator()
        )
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_moderator()
    
    def form_valid(self, form):
        # Оновлюємо хештеги
        response = super().form_valid(form)
        
        # Очищаємо старі хештеги
        self.object.hashtags.clear()
        
        # Додаємо нові хештеги
        hashtags_text = form.cleaned_data.get('hashtags', '')
        if hashtags_text:
            hashtag_names = [name.strip().lower().replace('#', '') for name in hashtags_text.split(',') if name.strip()]
            for name in hashtag_names:
                if name:
                    hashtag, created = Hashtag.objects.get_or_create(name=name)
                    self.object.hashtags.add(hashtag)
        
        messages.success(self.request, 'Пост успішно оновлено!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('posts:post_list')

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comment_form.html'
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Коментар додано!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.kwargs['pk']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comment_form.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_moderator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Коментар оновлено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'posts/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.post.pk})

class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        
        # Для AJAX запитів
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            from django.http import JsonResponse
            return JsonResponse({
                'liked': liked,
                'likes_count': post.likes.count()
            })
        
        return redirect('posts:post_detail', pk=pk)

class LikeCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        # Тут можна додати логіку для лайків коментарів, якщо потрібно
        return redirect('posts:post_detail', pk=comment.post.pk)

class HashtagPostListView(ListView):
    model = Post
    template_name = 'posts/hashtag_posts.html'
    context_object_name = 'posts'
    paginate_by = 20
    
    def get_queryset(self):
        hashtag_name = self.kwargs.get('hashtag')
        hashtag = get_object_or_404(Hashtag, name=hashtag_name.lower())
        return hashtag.posts.filter(is_pinned=False).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hashtag'] = self.kwargs.get('hashtag')
        return context

class HashtagListView(ListView):
    model = Hashtag
    template_name = 'posts/hashtag_list.html'
    context_object_name = 'hashtags'
    paginate_by = 50
    
    def get_queryset(self):
        return Hashtag.objects.all().order_by('name')

class PinPostView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_moderator()
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.is_pinned = not post.is_pinned
        post.save()
        
        action = "закріплено" if post.is_pinned else "відкріплено"
        messages.success(request, f'Пост {action}!')
        return redirect('posts:post_detail', pk=pk)

class UserPostListView(ListView):
    model = Post
    template_name = 'posts/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 20
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Post.objects.filter(author_id=user_id).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        context['profile_user'] = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        return context