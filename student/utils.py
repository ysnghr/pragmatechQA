from student.models import *

def FilterComments(question_obj):
    filtered_comments = []
    tempComments = list(question_obj.comment_set.all())
    # print(tempComments))
    
    # Eger sualin cavabi varsa 1 - ci yere push edir
    if(Comment.objects.filter(id = question_obj.answer).exists()):
        filtered_comments.append(Comment.objects.filter(id = question_obj.answer).first())


    for i in range(0, len(tempComments)):
        if(tempComments[i].id == question_obj.answer):
            continue
        max = tempComments[i]
        max_index = i
        for j in range(i, len(tempComments)):
            if(tempComments[j].id == question_obj.answer):
                continue
            if((max.get_upvote() - max.get_downvote()) < (tempComments[j].get_upvote() - tempComments[j].get_downvote() )):
                max = tempComments[j]
                max_index = j
        temp = tempComments[i]
        tempComments[i] = max
        filtered_comments.append(max)
        tempComments[max_index] = temp

        
    
    
    return filtered_comments

    
