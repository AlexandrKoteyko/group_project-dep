from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Головна сторінка
    path('', views.HomeView.as_view(), name='home'),
    
    # Про сайт
    path('about/', views.AboutView.as_view(), name='about'),
    
    # Правила спільноти
    path('rules/', views.RulesView.as_view(), name='rules'),
    
    # Контакти
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/success/', views.ContactSuccessView.as_view(), name='contact_success'),
    
    # Допомога/FAQ
    path('help/', views.HelpView.as_view(), name='help'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    
    # Статистика сайту
    path('stats/', views.StatsView.as_view(), name='stats'),
    
    # Пошук по всьому сайту
    path('search/', views.GlobalSearchView.as_view(), name='global_search'),
    
    # Статус сайту
    path('status/', views.StatusView.as_view(), name='status'),
    
    # Карта сайту
    path('sitemap/', views.SitemapView.as_view(), name='sitemap'),
    
    # API інформація
    path('api/', views.APIInfoView.as_view(), name='api_info'),
    
    # Підтримка/Донати
    path('support/', views.SupportView.as_view(), name='support'),
    
    # Помилка 404 кастомна
    path('404/', views.Custom404View.as_view(), name='custom_404'),
    
    # Помилка 500 кастомна
    path('500/', views.Custom500View.as_view(), name='custom_500'),
]