from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Список портфоліо
    path('', views.PortfolioListView.as_view(), name='portfolio_list'),
    
    # Портфоліо конкретного користувача
    path('user/<int:user_id>/', views.UserPortfolioListView.as_view(), name='user_portfolio'),
    
    # Деталі елемента портфоліо
    path('item/<int:pk>/', views.PortfolioItemDetailView.as_view(), name='portfolio_item_detail'),
    
    # Керування портфоліо
    path('create/', views.PortfolioItemCreateView.as_view(), name='portfolio_item_create'),
    path('item/<int:pk>/edit/', views.PortfolioItemUpdateView.as_view(), name='portfolio_item_update'),
    path('item/<int:pk>/delete/', views.PortfolioItemDeleteView.as_view(), name='portfolio_item_delete'),
    
    # Пошук портфоліо
    path('search/', views.PortfolioSearchView.as_view(), name='portfolio_search'),
    
    # Перегляд за ролями
    path('role/<str:role>/', views.PortfolioByRoleListView.as_view(), name='portfolio_by_role'),
    
    # Перегляд за типом
    path('type/<str:item_type>/', views.PortfolioByTypeListView.as_view(), name='portfolio_by_type'),
    
    # Перегляд за картами
    path('map/<str:game_map>/', views.PortfolioByMapListView.as_view(), name='portfolio_by_map'),
    
    # Модерація портфоліо (для адмінів/модераторів)
    path('moderation/', views.PortfolioModerationListView.as_view(), name='portfolio_moderation'),
    path('item/<int:pk>/approve/', views.ApprovePortfolioItemView.as_view(), name='approve_portfolio_item'),
    path('item/<int:pk>/reject/', views.RejectPortfolioItemView.as_view(), name='reject_portfolio_item'),
]