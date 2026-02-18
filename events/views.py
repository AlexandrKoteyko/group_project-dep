from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Event
from .forms import EventForm
from django.views import View

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    paginate_by = 10
    context_object_name = 'events'
    
    def get_queryset(self):
        return Event.objects.filter(is_active=True).order_by('date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['upcoming_events'] = Event.objects.filter(
            is_active=True, 
            date__gte=now
        ).order_by('date')[:5]
        context['past_events'] = Event.objects.filter(
            is_active=True, 
            date__lt=now
        ).order_by('-date')[:5]
        return context

class UpcomingEventListView(ListView):
    model = Event
    template_name = 'events/upcoming_events.html'
    paginate_by = 10
    context_object_name = 'events'
    
    def get_queryset(self):
        now = timezone.now()
        return Event.objects.filter(
            is_active=True, 
            date__gte=now
        ).order_by('date')

class PastEventListView(ListView):
    model = Event
    template_name = 'events/past_events.html'
    paginate_by = 10
    context_object_name = 'events'
    
    def get_queryset(self):
        now = timezone.now()
        return Event.objects.filter(
            is_active=True, 
            date__lt=now
        ).order_by('-date')

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['is_upcoming'] = self.object.date > now
        return context

class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def form_valid(self, form): 
        messages.success(self.request, 'Подію успішно створено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.object.pk})

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Подію успішно оновлено!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('events:event_detail', kwargs={'pk': self.object.pk})

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    
    def test_func(self):
        return self.request.user.is_moderator()
    
    def get_success_url(self):
        return reverse_lazy('events:event_list')

class EventCalendarView(TemplateView):
    template_name = 'events/event_calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.filter(is_active=True)
        context['events'] = events
        return context

class EventRegisterView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        
        ####
        
        messages.success(request, f'Ви успішно зареєструвалися на подію "{event.title}"!')
        return redirect('events:event_detail', pk=pk)

class EventTypeListView(ListView):
    model = Event
    template_name = 'events/event_type_list.html'
    paginate_by = 10
    context_object_name = 'events'
    
    def get_queryset(self):
        event_type = self.kwargs.get('event_type')
        return Event.objects.filter(
            is_active=True,
            event_type=event_type
        ).order_by('date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_type'] = dict(Event.EVENT_TYPES).get(self.kwargs.get('event_type'), 'Невідомий тип')
        return context