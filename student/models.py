from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from random import randrange
from PIL import Image
from taggit.managers import TaggableManager
from ckeditor.fields import  RichTextField
from django.contrib.auth.models import User
from taggit.models import Tag
from django.dispatch import receiver
from django.db.models.signals import post_delete

# Create your models here.

class TagInfo(models.Model):
    tag = models.OneToOneField(Tag, on_delete=models.CASCADE) 
    description = models.TextField(verbose_name="Məzmun")

    class Meta:
        """Meta definition for StudyGroup."""

        verbose_name = 'TagInfo'
        verbose_name_plural = 'TagInfos'

    def __str__(self):
        """Unicode representation of StudyGroup."""
        return self.description

class StudyGroup(models.Model):
    """Model definition for StudyGroup."""
    name = models.CharField(verbose_name=("Ad"), max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for StudyGroup."""

        verbose_name = 'StudyGroup'
        verbose_name_plural = 'StudyGroups'

    def __str__(self):
        """Unicode representation of StudyGroup."""
        return self.name


class Student(models.Model):
    """Model definition for Student."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    picture = models.ImageField(verbose_name=("Şəkil"), upload_to='profile_images', default="profile_images/default.jpg")
    study_group = models.ForeignKey(StudyGroup ,verbose_name=("Qrup"), on_delete = models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    level = models.IntegerField(default=0)

    class Meta:
        """Meta definition for Student."""

        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        """Unicode representation of Student."""
        return self.user.first_name + " " + self.user.last_name

    def get_tags(self):
        ans = dict()
        for question in self.question_set.all():
            for tag in question.tags.all():
                ans[tag] = ans.setdefault(tag, 0) + 1
        return ans

    def save(self):
        super().save()
        if self.picture.path:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
    
    
class Setting(models.Model):
    """Model definition for Setting."""

    communityRules = models.TextField(verbose_name="Qaydalar")

    class Meta:
        """Meta definition for Setting."""

        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'

    def __str__(self):
        """Unicode representation of Setting."""
        return self.communityRules


class FAQ(models.Model):
    """Model definition for FAQ."""

    title = models.CharField(verbose_name = "Başlıq", max_length = 255)
    content = models.TextField(verbose_name = "Məzmun")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for FAQ."""

        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        """Unicode representation of FAQ."""
        return self.title


class Question(models.Model):
    """Model definition for Question."""

    title = models.CharField(verbose_name="Başlıq", max_length=50) #Client Side REQUIRED + MAX_LENGTH = 50
    tags = TaggableManager() # Client Side REQUIRED + REGEX
    content = RichTextField(verbose_name="Məzmun") # Client Side REQUIRED
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default = 1) # Bu Tes ucundur Productionda silinecek.
    view = models.IntegerField(verbose_name="Baxış sayı", default = 0 )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)   
    slug = models.SlugField(unique=True, editable=False, max_length=130)
    answer =  models.IntegerField(verbose_name="Cavab Commentin İDsi", null=True)

    class Meta:
        """Meta definition for Question."""

        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        """Unicode representation of Question."""
        return self.title

    def get_downvote(self):
        return len(self.action_set.filter(action_type = 0).all())

    def get_upvote(self):
        return len(self.action_set.filter(action_type = 1).all())

    def get_comment_count(self):
        return len(self.comment_set.all())

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i').replace('ə', 'e').replace('ş', 's').replace('ç', 'c').replace('ğ', 'g').replace('ü', 'u').replace('ö', 'o'))
        ran = randrange(10000, 99999)
        unique_slug = f'{slug}-{str(ran)}'
        while Question.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{str(ran)}'
            ran = randrange(10000, 99999)
        return unique_slug
        
    def actions(self, action_num, stud, vote1, vote2):
        if not vote1:
            action=Action.objects.create(student=stud, question=self, type=0, action_type=action_num)
            self.student.level = self.student.level + 1 if action_num==1 else self.student.level - 2
            self.student.save()
            if vote2:
                self.student.level = self.student.level + 2 if action_num==1 else self.student.level - 1
                self.student.save()
                self.action_set.filter(action_type=1 if action_num==0 else 0).filter(student=stud).delete()
        else:
            self.student.level = self.student.level - 1 if action_num==1 else self.student.level + 2
            self.student.save()
            self.action_set.filter(action_type=action_num).filter(student=stud).delete() 
        return action_num
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        return super(Question, self).save(*args, **kwargs)


class QuestionImage(models.Model):
    """Model definition for QuestionImage."""

    image = models.ImageField(verbose_name="Sualın şəkli", upload_to = "question_images" )
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # Bu Tes ucundur Productionda silinecek.


    class Meta:
        """Meta definition for QuestionImage."""

        verbose_name = 'QuestionImage'
        verbose_name_plural = 'QuestionImage'

    def __str__(self):
        """Unicode representation of QuestionImage."""
        return f'[ {self.question.title} ] - {self.image.name}'
    
@receiver(post_delete, sender = QuestionImage)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 

class Comment(models.Model):
    """Model definition for Comment."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField(verbose_name=("Məzmun"), null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Comment."""

        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


    def get_downvote(self):
        return len(self.action_set.filter(action_type = 0).all())


    def get_upvote(self):
        return len(self.action_set.filter(action_type = 1).all())

    def actions(self, action_num, stud, vote1, vote2):
        if not vote1:
            action = Action.objects.create(student = stud, comment = self, type=1, action_type = action_num)
            self.student.level = self.student.level + 1 if action_num==1 else self.student.level - 2
            self.student.save()
            if vote2:
                self.student.level = self.student.level + 2 if action_num==1 else self.student.level - 1
                self.student.save()
                self.action_set.filter(action_type = 1 if action_num == 0 else 0).filter(student = stud).delete()
        else:
            self.student.level = self.student.level - 1 if action_num==1 else self.student.level + 2
            self.student.save()
            self.action_set.filter(action_type = action_num).filter(student = stud).delete() 
        return action_num


    def __str__(self):
        """Unicode representation of Comment."""
        return f'Q:/{self.question.title} / - C:/{self.content[0:20]}.../'


class CommentImage(models.Model):
    """Model definition for CommentImage."""

    image = models.ImageField(verbose_name="Commentin şəkli", upload_to = "comment_images" )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


    class Meta:
        """Meta definition for CommentImage."""

        verbose_name = 'CommentImage'
        verbose_name_plural = 'CommentImage'

    def __str__(self):
        """Unicode representation of CommentImage."""
        return f'[Question:  {self.comment.question.title} ] - [Comment:  {self.comment.content} ] - {self.image.name}'
   

    def get_downvote(self):
        return len(self.action_set.filter(action_type = 0).all())

    def get_upvote(self):
        return len(self.action_set.filter(action_type = 1).all())

@receiver(post_delete, sender = CommentImage)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 

class Action(models.Model):
    """Model definition for Action."""
    action_choices = (
        (0, 'Downvote'),
        (1, 'Upvote'),
    )
    type_choices = (
        (0, 'Sual'),
        (1, 'Komment'),
    )

    student = models.ForeignKey(Student, verbose_name="Tələbə", on_delete = models.PROTECT) 
    question = models.ForeignKey(Question, verbose_name="Sual", on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, verbose_name="Komment", on_delete=models.CASCADE, blank=True, null=True)
    type = models.BooleanField(verbose_name=("Tip"), choices = type_choices)
    action_type = models.BooleanField(choices = action_choices)  # False - 'Downvote', True - 'Upvote',
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Action."""

        verbose_name = 'Action'
        verbose_name_plural = 'Actions'

    def __str__(self):
        """Unicode representation of Action."""
        return self.get_action_type_display()