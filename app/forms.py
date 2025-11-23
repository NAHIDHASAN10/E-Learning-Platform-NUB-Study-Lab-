from django import forms
from .models import *

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = ProfileModel
#         fields = '__all__'
#         fields = ['user']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = DepartmentModel
        fields = '__all__'
        

class CourseRegistrationForm(forms.ModelForm):
    class Meta:
        model = CourseRegistrationModel
        fields = '__all__'
        exclude =  ['user', 'department']
        
             
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = "__all__"
