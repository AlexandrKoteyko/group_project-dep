from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    # Головна галерея
    path('', views.GalleryListView.as_view(), name='gallery_list'),
    
    # Медіа за типом
    path('type/<str:media_type>/', views.MediaByTypeListView.as_view(), name='media_by_type'),
    
    # Деталі медіа
    path('media/<int:pk>/', views.MediaDetailView.as_view(), name='media_detail'),
    
    # Завантажити медіа
    path('upload/', views.MediaUploadView.as_view(), name='media_upload'),
    
    # Керування медіа
    path('media/<int:pk>/edit/', views.MediaUpdateView.as_view(), name='media_update'),
    path('media/<int:pk>/delete/', views.MediaDeleteView.as_view(), name='media_delete'),
    
    # Лайки для медіа
    path('media/<int:pk>/like/', views.LikeMediaView.as_view(), name='like_media'),
    
    # Модерація галереї (для адмінів/модераторів)
    path('moderation/', views.GalleryModerationListView.as_view(), name='gallery_moderation'),
    path('media/<int:pk>/approve/', views.ApproveMediaView.as_view(), name='approve_media'),
    path('media/<int:pk>/reject/', views.RejectMediaView.as_view(), name='reject_media'),
    
    # Галерея користувача
    path('user/<int:user_id>/', views.UserGalleryListView.as_view(), name='user_gallery'),
    
    # Популярні медіа
    path('popular/', views.PopularMediaListView.as_view(), name='popular_media'),
    
    # Останні завантаження
    path('latest/', views.LatestMediaListView.as_view(), name='latest_media'),
    
    # Пошук у галереї
    path('search/', views.GallerySearchView.as_view(), name='gallery_search'),
]