from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import User
from .forms import CustomUserCreationForm, UserProfileForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Реєстрація успішна! Тепер ви можете увійти.')
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        # Перевіряємо, чи користувач переглядає свій профіль чи іншого
        context['is_own_profile'] = self.request.user == user
        
        # Додаємо доповнення до профілю
        context['posts'] = user.posts.all()[:10] if hasattr(user, 'posts') else []
        context['portfolio_items'] = user.portfolio_items.filter(is_approved=True)[:6] if hasattr(user, 'portfolio_items') else []
        context['gallery_items'] = user.gallery_items.filter(is_approved=True)[:6] if hasattr(user, 'gallery_items') else []
        context['topics'] = user.forum_topics.all()[:5] if hasattr(user, 'forum_topics') else []
        
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Профіль успішно оновлено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'pk': self.object.pk})

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        
        # Фільтрація за роллю
        role_filter = self.request.GET.get('role', '')
        if role_filter:
            queryset = queryset.filter(role=role_filter)
        
        # Пошук за іменем
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(username__icontains=search_query)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_filter'] = self.request.GET.get('role', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context

class UserRoleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['role']
    template_name = 'accounts/user_role_update.html'
    
    def test_func(self):
        return self.request.user.is_admin()
    
    def form_valid(self, form):
        messages.success(self.request, f'Роль користувача {self.object.username} оновлено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('accounts:user_list')

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    
    def test_func(self):
        # Тільки адміністратори можуть видаляти користувачів
        return self.request.user.is_admin()
    
    def get_success_url(self):
        return reverse_lazy('accounts:user_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cannot_delete_self'] = self.object == self.request.user
        return context