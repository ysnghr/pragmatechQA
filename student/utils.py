from student.models import *
from django.utils.text import slugify
import os

def FilterComments(question_obj):
    filtered_comments = []
    tempComments = list(question_obj.comment_set.all())
    
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

def GetImagesData(question_obj):
    image_list = list(question_obj.questionimage_set.all())
    
    mockFiles = []
    file_urls =[]

    for eachImage in image_list:
        mockFiles.append({
            'name': os.path.basename(eachImage.image.name),
            'size': eachImage.image.size,  
            'type' : 'image/jpeg',          
        })

        file_urls.append(eachImage.image.url)

    return (mockFiles, file_urls)

def GetPreviousImages(question_obj):
    image_list = list(question_obj.questionimage_set.all())
    
    temp = []

    for eachImage in image_list:
        temp.append({
            'image_object': eachImage,
            'image_url': eachImage.image.url,        
        })

    return temp

def GetTagsData(question_obj):
    tag_list = list(map(str, question_obj.tags.all()))    
    tag_data = ",".join(tag_list)
    

    return tag_data

def GetTagsData(question_obj):
    tag_list = list(map(str, question_obj.tags.all()))    
    tag_data = ",".join(tag_list)
    

    return tag_data

def GetUniqueSlug(artTitle):
    slug = slugify(artTitle.replace('ı', 'i').replace('ə', 'e').replace('ş', 's').replace('ç', 'c').replace('ğ', 'g').replace('ü', 'u').replace('ö', 'o'))
    ran = randrange(10000, 99999)
    unique_slug = f'{slug}-{str(ran)}'
    while Question.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{slug}-{str(ran)}'
        ran = randrange(10000, 99999)
    return unique_slug
