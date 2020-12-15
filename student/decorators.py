from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from .models import Student

def picture_required(function):
    def _function(request,*args, **kwargs):
        if request.user.student.picture.url == "/media/profile_images/default.jpg":
            return redirect('user_picture')
        return function(request, *args, **kwargs)
    return _function