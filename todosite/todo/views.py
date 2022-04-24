from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
## import todo form and models

from .forms import *
from .models import *

from django.http import HttpResponse   
from django.contrib.auth import login, authenticate
from .forms import SignupForm  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage 
from django.contrib.auth import get_user_model 
from django.http import HttpResponseRedirect 

from django.views.generic import (ListView, CreateView,UpdateView, DeleteView,)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
  
def signup(request):  
	if request.method == 'POST':  
		form = SignupForm(request.POST)  
		if form.is_valid():  
			# save form in the memory not in database  
			user = form.save(commit=False)  
			user.is_active = False  
			user.save()  
			# to get the domain of the current site  
			current_site = get_current_site(request)  
			mail_subject = 'Activation link has been sent to your email id'  
			message = render_to_string('acc_active_email.html', {  
				'user': user,  
				'domain': current_site.domain,  
				'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
				'token':account_activation_token.make_token(user),  
			})  
			to_email = form.cleaned_data.get('email')  
			email = EmailMessage(  
						mail_subject, message, to=[to_email]  
			)  
			email.send()  
			return HttpResponse('Please confirm your email address to complete the registration')  
	else:  
		form = SignupForm()  
	return render(request, 'signup.html', {'form': form}) 


def activate(request, uidb64, token):  
	User = get_user_model()  
	try:  
		uid = force_str(urlsafe_base64_decode(uidb64))  
		user = User.objects.get(pk=uid)  
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
		user = None  
	if user is not None and account_activation_token.check_token(user, token):  
		user.is_active = True  
		user.save()  
		return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
	else:  
		return HttpResponse('Activation link is invalid!')  



def Login(request):
	print('helllloooooo')
	if request.method == 'POST':
		print('hiiiii')
		# AuthenticationForm_can_also_be_used__
  
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' wecome {username} !!')
			print('111111111111')
			return redirect('index')
		else:
			messages.info(request, f'account done not exit plz sign in')
	form = AuthenticationForm()
	all_todo_items = ToDoList.objects.all()
	return render(request, 'todolist.html',
	{'all_items':all_todo_items})
	#return render(request, 'todolist.html')


def logout_view(request):
	logout(request)


class ListListView(ListView):
    model = ToDoList
    template_name = "todo/index.html"


class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_category_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context


class ListCreate(CreateView):
    model = ToDoList
    fields = ["category"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        return context

class ItemCreate(CreateView):
    model = ToDoItem
    fields = [
        "todo_list_category",
        "title",
        "description",
        "due_date",
    ]

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_category_id])

class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "todo_list_category",
        "title",
        "description",
        "due_date",
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list_category
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_category_id])


class ListDelete(DeleteView):
    model = ToDoList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("index")

class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list_category
        return context

