from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    # Список матеріалів
    path('', views.MaterialListView.as_view(), name='material_list'),
    
    # Матеріали за категорією
    path('category/<str:category>/', views.MaterialCategoryListView.as_view(), name='material_by_category'),
    
    # Деталі матеріалу
    path('material/<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),
    path('material/<int:pk>/download/', views.MaterialDownloadView.as_view(), name='material_download'),
    
    # Керування матеріалами (для адмінів/модераторів)
    path('create/', views.MaterialCreateView.as_view(), name='material_create'),
    path('material/<int:pk>/edit/', views.MaterialUpdateView.as_view(), name='material_update'),
    path('material/<int:pk>/delete/', views.MaterialDeleteView.as_view(), name='material_delete'),
    
    # Пошук матеріалів
    path('search/', views.MaterialSearchView.as_view(), name='material_search'),
    
    # Популярні матеріали
    path('popular/', views.PopularMaterialListView.as_view(), name='popular_materials'),
    
    # Завантажити файл
    path('upload/', views.MaterialUploadView.as_view(), name='material_upload'),
]