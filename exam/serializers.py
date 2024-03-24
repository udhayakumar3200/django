
from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField

from djangoapp.models import Profile
from exam.reuse_functions import ReuseFun
from .models import Exam,Ques,CandidateAnswer,Scores


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
        return ReuseFun.get_score(request.user.id,obj.id)
        
        
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
    

class ScoreBoardSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Scores
        fields = ['score','name']
        
    def get_name(self,obj):
        request = self.context.get('request')
        if request is None:
            
            return None
        else :
            name = Profile.objects.get(user_id=obj.user_id).username
            print("profile tab : ",name,":::::objjj:", obj.user_id)
            return name
    
    # {
    #     "rank":1,
    #     "name": "dd",
    #     "Score":5,
    # }