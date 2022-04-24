from django import forms
from .models import *

 
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User  
  
class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2')  


# class TodoForm(forms.ModelForm):
# 	class Meta:
# 		model = Todo
# 		fields="__all__"

class TaskForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = "__all__"

