from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView, CreateView, UpdateView
from .models import ToDoList, ToDoItem
from django.urls import reverse

# Create your views here.
#def add_quick_todo_task(request, todo_task):

    #return HttpResponseRedirect("placeholder")

#def home(request):
    #return render(request, 'test/home.html')
    #return HttpResponseRedirect("placeholder")


class ListListView(ListView):
    model = ToDoList
    template_name = "test/index.html"

class ItemListView(ListView):
    model = ToDoItem
    template_name = "test/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context
    
class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self, **kwargs):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        return context

class ItemCreate(CreateView):
    model = ToDoItem
    fields = [
        "todo_list",
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
        return reverse("test:list", args=[self.object.todo_list_id])

class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("test:list", args=[self.object.todo_list_id])