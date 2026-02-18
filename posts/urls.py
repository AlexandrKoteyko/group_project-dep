from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # Список постів та головна сторінка
    path('', views.PostListView.as_view(), name='post_list'),
    path('feed/', views.PostFeedView.as_view(), name='post_feed'),
    
    # Створення поста
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    
    # Деталі, редагування, видалення поста
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Коментарі
    path('post/<int:pk>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    
    # Лайки
    path('post/<int:pk>/like/', views.LikePostView.as_view(), name='like_post'),
    path('comment/<int:pk>/like/', views.LikeCommentView.as_view(), name='like_comment'),
    
    # Хештеги
    path('hashtag/<str:hashtag>/', views.HashtagPostListView.as_view(), name='hashtag_posts'),
    path('hashtags/', views.HashtagListView.as_view(), name='hashtag_list'),
    
    # Пін поста
    path('post/<int:pk>/pin/', views.PinPostView.as_view(), name='pin_post'),
    
    # Пости конкретного користувача
    path('user/<int:user_id>/', views.UserPostListView.as_view(), name='user_posts'),
]