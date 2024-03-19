from .models import CandidateAnswer

class ReuseFun():
    def is_attended(self,userId,examId):
        print("printing : userid: ",userId," exam Id: ",examId)
        data=CandidateAnswer.objects.filter(user_id=userId,exam_id=examId)
        print(data)
        if data.exists():
            attended_quizes = CandidateAnswer.objects.filter(user_id=userId,exam_id=examId).values_list('exam_id',flat=True)
            # print("attended quizes : ",attended_quizes)
            if len(attended_quizes) != 0:
                print("returning true")
                return True
            else:
                print("returning false")
                return False
        else:
            print("main else")
            return False    
        
    def get_score(userId,examId):
        questions = CandidateAnswer.objects.filter(user_id=userId,exam_id=examId).values_list('is_correct',flat=True)
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
            