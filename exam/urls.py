from django.urls import path
from .views import ExamApi,ExamEnum,GetExamApi

urlpatterns =[
    path('',ExamApi.as_view({'get':'list'}),name='exam_api'),
    path('exam_enum/',ExamEnum.as_view(),name='exam_enum'),
    path('get_exam/',GetExamApi.as_view(),name='exam_exam')
    
]