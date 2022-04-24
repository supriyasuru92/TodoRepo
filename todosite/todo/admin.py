from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# class Todo(admin.ModelAdmin):
# 	list_display = ['title', 'details','date']
# 	search_fields = ('title', 'details','date',)
	# autocomplete_fields = ('title', 'details','date',)


admin.site.register(ToDoList)
admin.site.register(ToDoItem)