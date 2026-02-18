from django.urls import path
from . import views

app_name = 'votes'

urlpatterns = [
    # Список голосувань
    path('', views.VoteListView.as_view(), name='vote_list'),
    
    # Активні голосування
    path('active/', views.ActiveVoteListView.as_view(), name='active_votes'),
    
    # Голосування за типом
    path('type/<str:vote_type>/', views.VoteByTypeListView.as_view(), name='vote_by_type'),
    
    # Деталі голосування
    path('vote/<int:pk>/', views.VoteDetailView.as_view(), name='vote_detail'),
    
    # Проголосувати
    path('vote/<int:pk>/cast/', views.VoteCastView.as_view(), name='vote_cast'),
    
    # Результати голосування
    path('vote/<int:pk>/results/', views.VoteResultsView.as_view(), name='vote_results'),
    
    # Керування голосуваннями (для адмінів/модераторів)
    path('create/', views.VoteCreateView.as_view(), name='vote_create'),
    path('vote/<int:pk>/edit/', views.VoteUpdateView.as_view(), name='vote_update'),
    path('vote/<int:pk>/delete/', views.VoteDeleteView.as_view(), name='vote_delete'),
    
    # Варіанти для голосування
    path('vote/<int:vote_id>/option/add/', views.VoteOptionCreateView.as_view(), name='option_add'),
    path('option/<int:pk>/edit/', views.VoteOptionUpdateView.as_view(), name='option_update'),
    path('option/<int:pk>/delete/', views.VoteOptionDeleteView.as_view(), name='option_delete'),
    
    # Популярні голосування
    path('popular/', views.PopularVoteListView.as_view(), name='popular_votes'),
    
    # Голосування дня/тижня
    path('daily/', views.DailyVoteView.as_view(), name='daily_vote'),
    path('weekly/', views.WeeklyVoteView.as_view(), name='weekly_vote'),
]