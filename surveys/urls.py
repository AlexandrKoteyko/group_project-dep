from django.urls import path
from . import views

app_name = 'surveys'

urlpatterns = [
    # Список опитувань
    path('', views.SurveyListView.as_view(), name='survey_list'),
    
    # Активні опитування
    path('active/', views.ActiveSurveyListView.as_view(), name='active_surveys'),
    
    # Деталі опитування
    path('survey/<int:pk>/', views.SurveyDetailView.as_view(), name='survey_detail'),
    
    # Проходження опитування
    path('survey/<int:pk>/take/', views.SurveyTakeView.as_view(), name='survey_take'),
    path('survey/<int:survey_id>/page/<int:page>/', views.SurveyPageView.as_view(), name='survey_page'),
    path('survey/<int:pk>/submit/', views.SurveySubmitView.as_view(), name='survey_submit'),
    
    # Результати опитування
    path('survey/<int:pk>/results/', views.SurveyResultsView.as_view(), name='survey_results'),
    
    # Керування опитуваннями (для адмінів/модераторів)
    path('create/', views.SurveyCreateView.as_view(), name='survey_create'),
    path('survey/<int:pk>/edit/', views.SurveyUpdateView.as_view(), name='survey_update'),
    path('survey/<int:pk>/delete/', views.SurveyDeleteView.as_view(), name='survey_delete'),
    
    # Питання та варіанти
    path('survey/<int:survey_id>/question/add/', views.QuestionCreateView.as_view(), name='question_add'),
    path('question/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('question/<int:question_id>/choice/add/', views.ChoiceCreateView.as_view(), name='choice_add'),
    path('choice/<int:pk>/edit/', views.ChoiceUpdateView.as_view(), name='choice_update'),
    path('choice/<int:pk>/delete/', views.ChoiceDeleteView.as_view(), name='choice_delete'),
]