from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Announcement
from .forms import AnnouncementForm

class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcements/announcement_list.html'
    context_object_name = 'announcements'
    paginate_by = 10
    
    def get_queryset(self):
        return Announcement.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pinned_announcements'] = Announcement.objects.filter(is_pinned=True)
        return context

class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'announcements/announcement_detail.html'
    context_object_name = 'announcement'

class AnnouncementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/announcement_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Оголошення успішно створено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('announcements:announcement_detail', kwargs={'pk': self.object.pk})

class AnnouncementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/announcement_form.html'
    
    def test_func(self):
        announcement = self.get_object()
        return self.request.user.is_moderator() and (
            self.request.user == announcement.author or 
            self.request.user.is_admin()
        )
    
    def form_valid(self, form):
        messages.success(self.request, 'Оголошення успішно оновлено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('announcements:announcement_detail', kwargs={'pk': self.object.pk})

class AnnouncementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcement
    template_name = 'announcements/announcement_confirm_delete.html'
    
    def test_func(self):
        announcement = self.get_object()
        return self.request.user.is_moderator() and (
            self.request.user == announcement.author or 
            self.request.user.is_admin()
        )
    
    def get_success_url(self):
        return reverse_lazy('announcements:announcement_list')

class PinAnnouncementView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_moderator()
    
    def post(self, request, pk):
        announcement = get_object_or_404(Announcement, pk=pk)
        announcement.is_pinned = not announcement.is_pinned
        announcement.save()
        
        action = "закріплено" if announcement.is_pinned else "відкріплено"
        messages.success(request, f'Оголошення {action}!')
        return redirect('announcements:announcement_detail', pk=pk)

class AnnouncementTypeListView(ListView):
    model = Announcement
    template_name = 'announcements/announcement_type_list.html'
    context_object_name = 'announcements'
    paginate_by = 10
    
    def get_queryset(self):
        announcement_type = self.kwargs.get('announcement_type')
        return Announcement.objects.filter(
            announcement_type=announcement_type
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Отримуємо відображення типу
        type_choices = dict([
            ('tournament', 'Турніри'),
            ('server', 'Новини сервера'),
            ('rules', 'Правила'),
            ('update', 'Оновлення'),
        ])
        context['type_name'] = type_choices.get(self.kwargs.get('announcement_type'), 'Невідомий тип')
        context['announcement_type'] = self.kwargs.get('announcement_type')
        return context

class LatestAnnouncementsView(ListView):
    model = Announcement
    template_name = 'announcements/latest_announcements.html'
    context_object_name = 'announcements'
    paginate_by = 10
    
    def get_queryset(self):
        return Announcement.objects.all().order_by('-created_at')