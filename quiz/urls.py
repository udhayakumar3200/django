from django.urls import path
from .views import QuizListCreateAPIView,QuizRetrieveUpdateDestroyAPIView,UserAnswersAPIView

urlpatterns = [
    # path('quizzes/', QuizApi.as_view({"get":"list"})), path('quizzes/', QuizListCreateAPIView.as_view(), name='quiz-list-create'),
    path('quizzes/', QuizListCreateAPIView.as_view(), name='quiz-list-create'),
    path('quizzes/<int:pk>/', QuizRetrieveUpdateDestroyAPIView.as_view(), name='quiz-detail'),
    path('useranswer/',UserAnswersAPIView.as_view(),name='user_answer')
]
