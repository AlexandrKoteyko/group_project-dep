from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    # Категорії форуму
    path('', views.CategoryListView.as_view(), name='category_list'),
    
    # Теми за категорією
    path('category/<int:category_id>/', views.TopicListView.as_view(), name='topic_by_category'),
    
    # Темы
    path('topic/create/', views.TopicCreateView.as_view(), name='topic_create'),
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('topic/<int:pk>/edit/', views.TopicUpdateView.as_view(), name='topic_update'),
    path('topic/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic_delete'),
    path('topic/<int:pk>/close/', views.CloseTopicView.as_view(), name='topic_close'),
    path('topic/<int:pk>/pin/', views.PinTopicView.as_view(), name='topic_pin'),
    
    # Повідомлення в темах
    path('topic/<int:topic_id>/message/', views.MessageCreateView.as_view(), name='add_message'),
    path('message/<int:pk>/edit/', views.MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),
    
    # Пошук по форуму
    path('search/', views.ForumSearchView.as_view(), name='forum_search'),
    
    # Останні активні теми
    path('latest/', views.LatestTopicsView.as_view(), name='latest_topics'),
]