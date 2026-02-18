from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    # Список оголошень
    path('', views.AnnouncementListView.as_view(), name='announcement_list'),
    
    # Деталі оголошення
    path('announcement/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement_detail'),
    
    # Керування оголошеннями (для адмінів/модераторів)
    path('create/', views.AnnouncementCreateView.as_view(), name='announcement_create'),
    path('announcement/<int:pk>/edit/', views.AnnouncementUpdateView.as_view(), name='announcement_update'),
    path('announcement/<int:pk>/delete/', views.AnnouncementDeleteView.as_view(), name='announcement_delete'),
    path('announcement/<int:pk>/pin/', views.PinAnnouncementView.as_view(), name='announcement_pin'),
    
    # Оголошення за типом
    path('type/<str:announcement_type>/', views.AnnouncementTypeListView.as_view(), name='announcement_by_type'),
    
    # Останні оголошення
    path('latest/', views.LatestAnnouncementsView.as_view(), name='latest_announcements'),
]