
from rest_framework import serializers
from .models import Quiz, Question, Answer,UserAnswers

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['text', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    is_attended = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    

    class Meta:
        model = Quiz
        fields = ['name', 'questions','is_attended','score']
        
    def get_is_attended(self,obj:Quiz):
        request = self.context.get('request')
        print("serializer request : ",request)
        if request is None:
            print("is attended none")
            return None
        else:
            attended_quizes = UserAnswers.objects.filter(user_id=request.user.id).values_list('quiz_id',flat=True)
            print("attended quiz list : ",attended_quizes)
            print("print obj : ",obj.id)
            if obj.id in attended_quizes:
                print("Quiz attended")
                return True
            else:
                print("Quiz not attended")    
                return False
            
    def get_score(self,obj:Quiz):
        request = self.context.get('request')
        print("quiz id get score : ",obj.id)
        questions = UserAnswers.objects.filter(quiz_id=obj.id,is_correct=True).values_list('is_correct',flat=True)
        print("questions : ",len(questions))    
        return len(questions)
        
        

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = Question.objects.create(quiz=quiz, **question_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)
        return quiz
    
class UserAnswerSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField(required=True)
    answers = serializers.ListField(
        child=serializers.CharField(),required=False
    )