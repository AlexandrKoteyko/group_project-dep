from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import MediaItem
from .forms import MediaItemForm

User = get_user_model()

class GalleryListView(ListView):
    model = MediaItem
    template_name = 'gallery/gallery_list.html'
    context_object_name = 'media_items'
    paginate_by = 12
    
    def get_queryset(self):
        # Показуємо тільки схвалені медіа
        return MediaItem.objects.filter(is_approved=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_types'] = MediaItem.MEDIA_TYPES
        context['featured'] = MediaItem.objects.filter(is_approved=True).order_by('-likes')[:4]
        return context

class MediaByTypeListView(ListView):
    model = MediaItem
    template_name = 'gallery/media_by_type.html'
    context_object_name = 'media_items'
    paginate_by = 12
    
    def get_queryset(self):
        media_type = self.kwargs.get('media_type')
        return MediaItem.objects.filter(
            media_type=media_type,
            is_approved=True
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        media_type = self.kwargs.get('media_type')
        
        # Знаходимо назву типу
        type_name = dict(MediaItem.MEDIA_TYPES).get(media_type, 'Невідомий тип')
        context['type_name'] = type_name
        context['current_type'] = media_type
        return context

class MediaDetailView(DetailView):
    model = MediaItem
    template_name = 'gallery/media_detail.html'
    context_object_name = 'media_item'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        media_item = self.get_object()
        
        # Перевіряємо, чи може користувач редагувати
        context['can_edit'] = (
            self.request.user == media_item.user or 
            self.request.user.is_moderator()
        )
        
        # Додаємо схожі медіа
        context['similar_media'] = MediaItem.objects.filter(
            media_type=media_item.media_type,
            is_approved=True
        ).exclude(pk=media_item.pk)[:6]
        
        return context

class MediaUploadView(LoginRequiredMixin, CreateView):
    model = MediaItem
    form_class = MediaItemForm
    template_name = 'gallery/media_upload.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        
        # Автоматично схвалюємо для модераторів
        if self.request.user.is_moderator():
            form.instance.is_approved = True
            messages.success(self.request, 'Медіа успішно завантажено та схвалено!')
        else:
            messages.success(self.request, 'Медіа завантажено! Воно з\'явиться після перевірки модератором.')
        
        return super().form_valid(form)
    
    def get_success_url(self):
        if self.object.is_approved:
            return reverse_lazy('gallery:media_detail', kwargs={'pk': self.object.pk})
        else:
            return reverse_lazy('gallery:gallery_list')

class MediaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MediaItem
    form_class = MediaItemForm
    template_name = 'gallery/media_upload.html'
    
    def test_func(self):
        media_item = self.get_object()
        return self.request.user == media_item.user or self.request.user.is_moderator()
    
    def form_valid(self, form):
        # Скидаємо статус схвалення при редагуванні (крім модераторів)
        if not self.request.user.is_moderator():
            form.instance.is_approved = False
            messages.info(self.request, 'Медіа оновлено. Воно знову потребує перевірки модератором.')
        else:
            messages.success(self.request, 'Медіа успішно оновлено!')
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('gallery:media_detail', kwargs={'pk': self.object.pk})

class MediaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MediaItem
    template_name = 'gallery/media_confirm_delete.html'
    
    def test_func(self):
        media_item = self.get_object()
        return self.request.user == media_item.user or self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('gallery:gallery_list')

class LikeMediaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        media_item = get_object_or_404(MediaItem, pk=pk)
        
        # Проста логіка лайків (без збереження хто лайкнув)
        media_item.likes += 1
        media_item.save()
        
        # Для AJAX запитів
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'likes': media_item.likes
            })
        
        return redirect('gallery:media_detail', pk=pk)

class GalleryModerationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = MediaItem
    template_name = 'gallery/gallery_moderation.html'
    context_object_name = 'media_items'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_queryset(self):
        return MediaItem.objects.filter(is_approved=False).order_by('-created_at')

class ApproveMediaView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_moderator()
    
    def post(self, request, pk):
        media_item = get_object_or_404(MediaItem, pk=pk)
        media_item.is_approved = True
        media_item.save()
        
        messages.success(request, f'Медіа "{media_item.title or media_item.file.name}" схвалено!')
        return redirect('gallery:gallery_moderation')

class RejectMediaView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MediaItem
    template_name = 'gallery/media_reject.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('gallery:gallery_moderation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_reject'] = True
        return context

class UserGalleryListView(ListView):
    model = MediaItem
    template_name = 'gallery/user_gallery.html'
    context_object_name = 'media_items'
    paginate_by = 12
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        
        # Якщо користувач переглядає свою галерею, показуємо всі медіа
        if self.request.user == user:
            return MediaItem.objects.filter(user=user).order_by('-created_at')
        # Інакше показуємо тільки схвалені
        return MediaItem.objects.filter(user=user, is_approved=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['gallery_user'] = get_object_or_404(User, pk=user_id)
        return context

class PopularMediaListView(ListView):
    model = MediaItem
    template_name = 'gallery/popular_media.html'
    context_object_name = 'media_items'
    paginate_by = 12
    
    def get_queryset(self):
        return MediaItem.objects.filter(is_approved=True).order_by('-likes')

class LatestMediaListView(ListView):
    model = MediaItem
    template_name = 'gallery/latest_media.html'
    context_object_name = 'media_items'
    paginate_by = 12
    
    def get_queryset(self):
        return MediaItem.objects.filter(is_approved=True).order_by('-created_at')

class GallerySearchView(ListView):
    model = MediaItem
    template_name = 'gallery/gallery_search.html'
    context_object_name = 'media_items'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return MediaItem.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(user__username__icontains=query)
            ).filter(is_approved=True).order_by('-created_at')
        return MediaItem.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context