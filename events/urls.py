from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Список подій
    path('', views.EventListView.as_view(), name='event_list'),
    
    # Майбутні та минулі події
    path('upcoming/', views.UpcomingEventListView.as_view(), name='upcoming_events'),
    path('past/', views.PastEventListView.as_view(), name='past_events'),
    
    # Деталі події
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    
    # Керування подіями (для адмінів/модераторів)
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    
    # Календар подій
    path('calendar/', views.EventCalendarView.as_view(), name='event_calendar'),
    
    # Реєстрація на подію
    path('event/<int:pk>/register/', views.EventRegisterView.as_view(), name='event_register'),
    
    # Події за типом
    path('type/<str:event_type>/', views.EventTypeListView.as_view(), name='event_by_type'),
]