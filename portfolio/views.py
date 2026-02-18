from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import PortfolioItem
from .forms import PortfolioItemForm

User = get_user_model()

class PortfolioListView(ListView):
    model = PortfolioItem
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'portfolio_items'
    paginate_by = 12
    
    def get_queryset(self):
        # Показуємо тільки схвалені елементи
        return PortfolioItem.objects.filter(is_approved=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_types'] = PortfolioItem.ITEM_TYPES
        context['roles'] = PortfolioItem.ROLES
        return context

class UserPortfolioListView(ListView):
    model = PortfolioItem
    template_name = 'portfolio/user_portfolio.html'
    context_object_name = 'portfolio_items'
    paginate_by = 12
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        
        # Якщо користувач переглядає свій портфоліо, показуємо всі елементи
        if self.request.user == user:
            return PortfolioItem.objects.filter(user=user).order_by('-created_at')
        # Інакше показуємо тільки схвалені
        return PortfolioItem.objects.filter(user=user, is_approved=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['portfolio_user'] = get_object_or_404(User, pk=user_id)
        return context

class PortfolioItemDetailView(DetailView):
    model = PortfolioItem
    template_name = 'portfolio/portfolio_item_detail.html'
    context_object_name = 'portfolio_item'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolio_item = self.get_object()
        
        # Додаємо подібні елементи
        similar_items = PortfolioItem.objects.filter(
            user=portfolio_item.user,
            is_approved=True
        ).exclude(pk=portfolio_item.pk).order_by('-created_at')[:4]
        context['similar_items'] = similar_items
        
        # Перевіряємо, чи користувач може редагувати
        context['can_edit'] = (
            self.request.user == portfolio_item.user or 
            self.request.user.is_moderator()
        )
        
        return context

class PortfolioItemCreateView(LoginRequiredMixin, CreateView):
    model = PortfolioItem
    form_class = PortfolioItemForm
    template_name = 'portfolio/portfolio_item_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        
        # Автоматично схвалюємо для модераторів
        if self.request.user.is_moderator():
            form.instance.is_approved = True
            messages.success(self.request, 'Елемент портфоліо успішно створено та схвалено!')
        else:
            messages.success(self.request, 'Елемент портфоліо створено! Він з\'явиться після перевірки модератором.')
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('portfolio:portfolio_item_detail', kwargs={'pk': self.object.pk})

class PortfolioItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PortfolioItem
    form_class = PortfolioItemForm
    template_name = 'portfolio/portfolio_item_form.html'
    
    def test_func(self):
        portfolio_item = self.get_object()
        return self.request.user == portfolio_item.user or self.request.user.is_moderator()
    
    def form_valid(self, form):
        # Скидаємо статус схвалення при редагуванні (крім модераторів)
        if not self.request.user.is_moderator():
            form.instance.is_approved = False
            messages.info(self.request, 'Елемент портфоліо оновлено. Він знову потребує перевірки модератором.')
        else:
            messages.success(self.request, 'Елемент портфоліо успішно оновлено!')
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('portfolio:portfolio_item_detail', kwargs={'pk': self.object.pk})

class PortfolioItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PortfolioItem
    template_name = 'portfolio/portfolio_item_confirm_delete.html'
    
    def test_func(self):
        portfolio_item = self.get_object()
        return self.request.user == portfolio_item.user or self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('portfolio:portfolio_list')

class PortfolioSearchView(ListView):
    model = PortfolioItem
    template_name = 'portfolio/portfolio_search.html'
    context_object_name = 'portfolio_items'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return PortfolioItem.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(game_map__icontains=query) |
                Q(weapon__icontains=query)
            ).filter(is_approved=True).order_by('-created_at')
        return PortfolioItem.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class PortfolioByRoleListView(ListView):
    model = PortfolioItem
    template_name = 'portfolio/portfolio_by_role.html'
    context_object_name = 'portfolio_items'
    paginate_by = 12
    
    def get_queryset(self):
        role = self.kwargs.get('role')
        return PortfolioItem.objects.filter(
            role=role, 
            is_approved=True
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        role = self.kwargs.get('role')
        
        # Знаходимо назву ролі
        role_name = dict(PortfolioItem.ROLES).get(role, 'Невідома роль')
        context['role_name'] = role_name
        context['current_role'] = role
        
        return context

class PortfolioByTypeListView(ListView):
    model = PortfolioItem
    template_name = 'portfolio/portfolio_by_type.html'
    context_object_name = 'portfolio_items'
    paginate_by = 12
    
    def get_queryset(self):
        item_type = self.kwargs.get('item_type')
        return PortfolioItem.objects.filter(
            item_type=item_type, 
            is_approved=True
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_type = self.kwargs.get('item_type')
        
        # Знаходимо назву типу
        type_name = dict(PortfolioItem.ITEM_TYPES).get(item_type, 'Невідомий тип')
        context['type_name'] = type_name
        context['current_type'] = item_type
        
        return context

class PortfolioByMapListView(ListView):
    model = PortfolioItem
    template_name = 'portfolio/portfolio_by_map.html'
    context_object_name = 'portfolio_items'
    paginate_by = 12
    
    def get_queryset(self):
        game_map = self.kwargs.get('game_map')
        return PortfolioItem.objects.filter(
            game_map__icontains=game_map, 
            is_approved=True
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_map'] = self.kwargs.get('game_map')
        return context

class PortfolioModerationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = PortfolioItem
    template_name = 'portfolio/portfolio_moderation.html'
    context_object_name = 'portfolio_items'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_queryset(self):
        return PortfolioItem.objects.filter(is_approved=False).order_by('-created_at')

class ApprovePortfolioItemView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_moderator()
    
    def post(self, request, pk):
        portfolio_item = get_object_or_404(PortfolioItem, pk=pk)
        portfolio_item.is_approved = True
        portfolio_item.save()
        
        messages.success(request, f'Елемент портфоліо "{portfolio_item.title}" схвалено!')
        return redirect('portfolio:portfolio_moderation')

class RejectPortfolioItemView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PortfolioItem
    template_name = 'portfolio/portfolio_item_reject.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('portfolio:portfolio_moderation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_reject'] = True
        return context