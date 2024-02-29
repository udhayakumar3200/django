# from django.shortcuts import render
# from rest_framework import status
# from rest_framework.request import Request
# from rest_framework.response import Response
# from rest_framework.generics import ListAPIView
# from rest_framework.viewsets import ModelViewSet
# from .serializers import QuizSerializer,QuestionSerializer
# from .models import Quiz,Question

# class QuizApi(ModelViewSet):
#     serializer_class = QuizSerializer
#     def get_queryset(self):
#         quiz_id = self.request.query_params.get('quiz_id', None)
#         print(quiz_id)
#         sel_quizes = Question.objects.filter(type = quiz_id)
#         print(sel_quizes)
#         context = super().get_serializer_context()
#         context.update({"request":self.request})
#         return sel_quizes
    
    
#     def post(self,request:Request,format=None):
        
    
#     #  def get_queryset(self):
#     #     quiz_id = self.kwargs.get('id')
#     #     return Quiz.objects.filter(id=quiz_id).prefetch_related('questions')[:1]


from rest_framework import generics
from .models import Quiz
from .serializers import QuizSerializer,UserAnswerSerializer
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import UserAnswers,Quiz,Question,Answer



class QuizListCreateAPIView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    
class UserAnswersAPIView(APIView):
    def post(self, request:Request,format=None):
        serializer = UserAnswerSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            quiz_id = serializer.validated_data['quiz_id']
            answers = serializer.validated_data['answers']
            question_ids = Question.objects.filter(quiz_id=quiz_id).order_by('id').values_list('id',flat=True)
            ans_fix = []
            objects = []
            score = 0
            ans_bool = False
            print("printing user : ",user)
            print("quiz_id : ",quiz_id)
            print("question_ids : ",question_ids)
            print("user answer serializer : ",serializer.validated_data)
            print("answer : ",answers," len: ",len(answers))
            for i,q in enumerate(question_ids):
                print("inside for i value : ",i)
                temp_ans = Answer.objects.filter(question_id=q)
                ans_bool = False

                for ans in temp_ans:
                    if ans.text == answers[i]:
                        if ans.is_correct:
                            print("answer id : ",ans.id)
                            ans_fix.append(ans.id)
                            ans_bool = True
                            score += 1
                        else:
                            print("wrong answer : ",ans.id)
                            ans_fix.append(ans.id)
                            # ans_bool = False
                            
                    else:
                        print("one of the answer was out of the options") 
                        # ans_bool = False
                                   
                temp_ans = Answer.objects.none() 
                
                obj = UserAnswers(user=user,quiz_id=quiz_id,question=Question.objects.get(id=question_ids[i]),
                                  answer=Answer.objects.get(id=ans_fix[i]),is_correct=ans_bool)
                objects.append(obj)
            print("Final Objects : ",objects)    
            UserAnswers.objects.bulk_create(objects)
            
            # UserAnswers.objects.all().delete()
            
            
            
            return Response({"message":"Test submitted successfully..!",
                             "score":score
                             },status=status.HTTP_201_CREATED) 
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  
        
        
    def delete(self,request:Request,format=None):
        serializer = UserAnswerSerializer(data=request.data)
        UserAnswers.objects.all().delete()   
        return Response("Deleted",status=status.HTTP_200_OK)    
        
           


