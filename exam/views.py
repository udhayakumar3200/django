from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from exam.reuse_functions import ReuseFun
from .models import Ques,Category,SubCategory,Exam,CandidateAnswer,Scores
from .serializers import CreateExamSerializer,GetSubcategoryExamSerializer,SubmitAnswerSerializer,ExamDetailSerializer,ScoreBoardSerializer

class ExamApi(ModelViewSet):
    serializer_class = GetSubcategoryExamSerializer
    # api to get the exams using sub category
    def get_queryset(self):
        # id = None
        id = self.request.GET.get('id')
        print("id : ",id)
        exams = Exam.objects.filter(subCategory_id = id)
        print("exams : ",exams)
        context = super().get_serializer_context()
        context.update({"request": self.request})      
        return exams
    # Response(dd,status=status.HTTP_200_OK)
       
    def post(self,request:Request,format=None):
        serializer = CreateExamSerializer(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            print('serializer valid : ',serializer.data)
            category = serializer.validated_data['category_name']
            subCategory = serializer.validated_data['subCategory_name']
            exam =  serializer.validated_data['exam_name']
            objects = []
                        
            # Creating instance:
            category_instance = Category.objects.get_or_create(category_name=category)
            subCategory_instance = SubCategory.objects.get_or_create(category=category_instance[0], subCategory_name = subCategory)
            exam_instance = Exam.objects.get_or_create(category=category_instance[0],subCategory = subCategory_instance[0],exam_name = exam)
            questions = serializer.validated_data['questions']
            print(f"get or create : {category_instance},{subCategory_instance}")
            
            for items in questions:
                objects.append(Ques(category_id = category_instance[0].id,
                subCategory_id = subCategory_instance[0].id,
                exam_id = exam_instance[0].id,
                question = items['question'],
                answers =items['answers'],
                correct_option = items['correct_option']
                ))
            print("objects : ",objects)
            Ques.objects.bulk_create(objects) 
            
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
class GetExamApi(APIView):
    # to get the particular exam
    def get(self, request, format=None):
        exam_id = request.GET.get('exam_id')
        print("Exam id : ",exam_id)
        exam = Exam.objects.get(id=exam_id)
        print("Exam : ",exam)
        is_att = ReuseFun().is_attended(request.user.id,exam_id)
        print(":::::::: ",is_att)
        serializer = ExamDetailSerializer(exam,context={'request': request,'is_attended':is_att})
        return Response(serializer.data)
    
    # to submit answers
    def post(self,request,format=None):
        serializer = SubmitAnswerSerializer(data=request.data)
        if serializer.is_valid():
            print("serializer data : ",serializer.validated_data)
            exam_id = serializer.validated_data['exam_id']
            user_answers = serializer.validated_data['answers']
            question_ids = Ques.objects.filter(exam_id=exam_id).order_by('id').values_list('id',flat=True)
            print("question_ids len : ",len(question_ids))
            print("user ans len : ",len(user_answers))
            if len(user_answers) == len(question_ids) : 
                category_id = Exam.objects.get(id=exam_id).category.id
                subCategory_id = Exam.objects.get(id=exam_id).subCategory.id
                print("category id : ",category_id," subcat : ",subCategory_id)
                print("question_ids : ",question_ids)
                data = []
                for i,q in enumerate(user_answers):
                    ques = Ques.objects.get(id=question_ids[i])
                    answer = None
                    correct = None
                    if user_answers[i] != "none":
                        for ind in range(4):
                            ans, = ques.answers[ind].keys()
                            if ans == user_answers[i]:
                                answer = ques.answers[ind]
                                print("answer : ",answer)
                                if answer == ques.correct_option:
                                    correct = True
                                    print("correct : ", correct)
                                else:
                                    correct = False    
                    else:
                        print("main else")
                        answer = {}
                        correct = None                                
                    temp_data = CandidateAnswer(user=request.user,category=Category.objects.get(id=category_id),subCategory=SubCategory.objects.get(id=subCategory_id), 
                                                exam=Exam.objects.get(id=exam_id),
                                                question = ques,
                                                answer = answer,
                                                is_correct=correct)
                    data.append(temp_data)
                    print("final data : ",data)

                CandidateAnswer.objects.bulk_create(data)
                total_mark = ReuseFun.get_score(request.user.id,exam_id)
                # print("test : ",Exam.objects.get(id=exam_id),":::",total_mark,":::",request.user.id)
                # score_data = Scores(user=request.user,exam=Exam.objects.get(id=exam_id),score=total_mark)
                # print("score data: ",score_data)
                Scores.objects.create(user=request.user,exam=Exam.objects.get(id=exam_id),score=total_mark)
                data = {
                    "test":"Submitted successfully",
                    "socre":total_mark
                }
                
                return Response(data=data,status=status.HTTP_201_CREATED)
            else:
                return Response("please send all answers in order",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
        
class ExamEnum(APIView):
    def get(self,request:Request,format=None):
        objects = []
        categories = []
        categories = Category.objects.all()
        print("category : ",categories.values_list('category_name',flat=True))
        print("category 2: ",categories.values_list('id',flat=True))
 
        for category in categories:
            category_data = {
                'category': {category.id : category.category_name},
                'sub_categories': []
            }    
            sub_categories = SubCategory.objects.filter(category=category)
            print("sub_categories :",sub_categories)   
            for subcategory in sub_categories:
                category_data['sub_categories'].append({subcategory.id:subcategory.subCategory_name})
            objects.append(category_data)
        print("final object : ",objects)
        return Response(objects,status=status.HTTP_200_OK)
    
class ScoreBoardApi(APIView):
    def get(self,request:Request,format=None):
        examId = self.request.GET.get('exam_id')
        data = []
        print("self : ",examId)
        obj = Scores.objects.filter(exam_id = examId).order_by('-score')
        print("score : ",obj)
        serializer = ScoreBoardSerializer(obj,many=True,context={'request':request})
        print("Serializer data : ",serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)
            
    
