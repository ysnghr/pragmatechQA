from django import template
from student.models import *
from taggit.models import Tag, TaggedItem

register = template.Library()

@register.filter
def downvote_check(question, student):
    temp = question.action_set.filter(student = student).first()
    if not temp:
        return 0
    return 0 if temp.action_type == 1 else 1

@register.filter
def upvote_check(question, student):
    temp = question.action_set.filter(student = student).first()
    if not temp:
        return 0
    return 0 if temp.action_type == 0 else 1