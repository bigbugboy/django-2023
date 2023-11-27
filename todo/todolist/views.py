from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from . import models


def todolist(request, *args):
    # https://ricocc.com/todo/
    today = datetime.today()
    todos = models.TodoList.objects.filter(
        created_at__year=today.year,
        created_at__month=today.month,
        created_at__day=today.day,
    ).all()
    return render(request, 'todo.html', context={'todos': todos})


def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title').strip()
        if title:
            models.TodoList.objects.create(title=title)
        else:
            messages.error(request, '💡请输入内容！')
        return redirect('todolist')



def change_status(request, pk):
    todo = get_object_or_404(models.TodoList, pk=pk)
    todo.status = not todo.status
    todo.save()
    return JsonResponse({'status': todo.status})


def delete_todo(request, pk):
    models.TodoList.objects.filter(pk=pk).delete()
    return JsonResponse({'delete': True})

