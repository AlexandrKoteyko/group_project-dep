from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import FileResponse
import os
from .models import Material
from .forms import MaterialForm

class MaterialListView(ListView):
    model = Material
    template_name = 'materials/material_list.html'
    context_object_name = 'materials'
    paginate_by = 12
    
    def get_queryset(self):
        return Material.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Додаємо підрахунок матеріалів по категоріях
        context['categories'] = Material.CATEGORY_CHOICES
        context['category_counts'] = {}
        for category_value, category_name in Material.CATEGORY_CHOICES:
            context['category_counts'][category_value] = Material.objects.filter(category=category_value).count()
        return context

class MaterialCategoryListView(ListView):
    model = Material
    template_name = 'materials/material_category_list.html'
    context_object_name = 'materials'
    paginate_by = 12
    
    def get_queryset(self):
        category = self.kwargs.get('category')
        return Material.objects.filter(category=category).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('category')
        
        # Знаходимо назву категорії
        category_name = dict(Material.CATEGORY_CHOICES).get(category, 'Невідома категорія')
        context['category_name'] = category_name
        context['current_category'] = category
        
        return context

class MaterialDetailView(DetailView):
    model = Material
    template_name = 'materials/material_detail.html'
    context_object_name = 'material'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Додаємо подібні матеріали
        material = self.get_object()
        similar_materials = Material.objects.filter(
            category=material.category
        ).exclude(pk=material.pk).order_by('-created_at')[:4]
        context['similar_materials'] = similar_materials
        
        return context

class MaterialDownloadView(View):
    def get(self, request, pk):
        material = get_object_or_404(Material, pk=pk)
        
        if material.file:
            # Збільшуємо лічильник завантажень
            material.downloads += 1
            material.save()
            
            # Віддаємо файл для завантаження
            file_path = material.file.path
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        else:
            messages.error(request, 'Файл не знайдено.')
            return redirect('materials:material_detail', pk=pk)

class MaterialCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'materials/material_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Матеріал успішно створено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('materials:material_detail', kwargs={'pk': self.object.pk})

class MaterialUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'materials/material_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Матеріал успішно оновлено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('materials:material_detail', kwargs={'pk': self.object.pk})

class MaterialDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Material
    template_name = 'materials/material_confirm_delete.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('materials:material_list')

class MaterialSearchView(ListView):
    model = Material
    template_name = 'materials/material_search.html'
    context_object_name = 'materials'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Material.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query)
            ).order_by('-created_at')
        return Material.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class PopularMaterialListView(ListView):
    model = Material
    template_name = 'materials/popular_materials.html'
    context_object_name = 'materials'
    paginate_by = 12
    
    def get_queryset(self):
        return Material.objects.all().order_by('-downloads')

class MaterialUploadView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'materials/material_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_upload'] = True
        return context