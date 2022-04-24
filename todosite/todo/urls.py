from django.urls import path  
from .views import *
from django.views.generic import TemplateView

urlpatterns = [  
    path('signup/', signup, name = 'signup'),  
    # path('form/', index, name = 'index'),  
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        activate, name='activate'), 
    path('login/', Login, name ='loginuser'), 
    path("", ListListView.as_view(), name="index"),
    path("list/<int:list_id>/",ItemListView.as_view(), name="list"),
      # CRUD patterns for ToDoLists
    path("list/add/", ListCreate.as_view(), name="list-add"),
    # CRUD patterns for ToDoItems
    path("list/<int:list_id>/item/add/", ItemCreate.as_view(), name="item-add",),
    path("list/<int:list_id>/item/<int:pk>/",ItemUpdate.as_view(), name="item-update",),
    path("list/<int:pk>/delete/", ListDelete.as_view(), name="list-delete"),
    path("list/<int:list_id>/item/<int:pk>/delete/", ItemDelete.as_view(), name="item-delete",),
    
]  