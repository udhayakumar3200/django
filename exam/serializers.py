
from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField

from exam.reuse_functions import ReuseFun
from .models import Exam,Ques,CandidateAnswer

class CreateExamSerializer(serializers.Serializer):
    category_name = serializers.CharField(max_length=100,required=True)
    subCategory_name = serializers.CharField(max_length=100,required=True)
    exam_name = serializers.CharField(max_length=100,required=True)
    duration = serializers.DurationField(required=True)
    questions = serializers.ListField(child=serializers.JSONField(default=dict))    
    
class GetSubcategoryExamSerializer(serializers.ModelSerializer):
    is_attended = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    class Meta:
        model = Exam
        fields = [
            'id',
            'exam_name',
            'is_attended',
            'score'
        ]
    
    def get_is_attended(self,obj:Exam):
        request = self.context.get('request')
        if request is None:
            return None
        else:
            return ReuseFun().is_attended(request.user.id,obj.id)
    
                    
    def get_score(self,obj:Exam):
        request = self.context.get('request')
        print("score : ",request)
        questions = CandidateAnswer.objects.filter(user_id=request.user.id,exam_id=obj.id).values_list('is_correct',flat=True)
        print("questiooo : ",questions)        
        total_questions = len(questions)
        correct_questions = 0
        wrong_questions = 0
        unattended_questions = 0
        negative_mark = 0
        total_mark = 0
        for val in questions:
            if val == True:
               correct_questions += 1
            elif val == False:
                wrong_questions += 1
            else:
                unattended_questions += 1
        
        negative_mark = 0.66 * wrong_questions
        print("tot:",total_questions," corr:",correct_questions," wrong :",wrong_questions," unatt:",unattended_questions)
        print("negative mark : ",negative_mark)
        total_mark = correct_questions - negative_mark
        print("total mark : ",total_mark)
        return total_mark
        
        
class GetExamSerializer(serializers.Serializer):
    exam_id = serializers.IntegerField()  
    questions = serializers.CharField()
    answers = serializers.ListField(child=serializers.JSONField(default=dict))    
    
    # answers = serializers.ListField(child = serializers.JSONField(default=dict))       
    
    
class AnswerSerializer(serializers.Serializer):
    a = serializers.CharField(required=False)
    b = serializers.CharField(required=False)
    c = serializers.CharField(required=False)
    d = serializers.CharField(required=False)

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    correct_option = AnswerSerializer()
    your_answer = serializers.SerializerMethodField()

    class Meta:
        model = Ques
        fields = ('question', 'answers', 'correct_option','your_answer')
        
   
            
        
    def to_representation(self, instance):
        data =  super().to_representation(instance)   
        # print("Data : ",data)
        # print("self : ",self) 
        # print("instance : ",instance.id)
        request = self.context.get('request')
        is_attended = self.context.get('is_attended')
        
        # exam_id = request.GET.get('exam_id')
        # print("user : ",request.user.id)
        print("is attended : ",is_attended)
        if is_attended:
            print("inside if condition")
            data['your_answer'] = self.get_your_answer(instance)
        else:
            print("inside else condition")
            
            data.pop('your_answer',None)   
        

        return data
    
    def get_your_answer(self,instance):
        request = self.context.get('request')
        data = CandidateAnswer.objects.filter(user_id = request.user.id,question_id = instance.id)
        if data.exists():
            your_ans = CandidateAnswer.objects.get(user_id = request.user.id,question_id = instance.id).answer
            return your_ans
        else :
            return None
    
    
        
        

class ExamDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True,source='ques_set')
    is_attended = serializers.SerializerMethodField()
    

    class Meta:
        model = Exam
        fields = ('id', 'questions','duration','is_attended')
        
    def get_is_attended(self,obj):
        request = self.context.get('request')
        if request is None:
            return None
        else:
            return ReuseFun().is_attended(request.user.id,obj.id)
        
   
        
class SubmitAnswerSerializer(serializers.Serializer):
    exam_id = serializers.IntegerField(required = True)
    answers = serializers.ListField(child=serializers.CharField(),required=False)
    
    
    