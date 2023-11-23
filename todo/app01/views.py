from datetime import date

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages

from . import models


def todolist(request, *args):
    # https://ricocc.com/todo/
    todos = models.Todo.objects.filter(created_at=date.today()).all()
    msgs = [m for m in get_messages(request)]
    tip = msgs[0] if msgs else ''
    print(1)
    print(tip)
    return render(request, 'todo.html', {'todos': todos, 'tip': tip})


def todo_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title.strip():
            models.Todo.objects.create(title=title)
        else:
            messages.add_message(request, messages.WARNING, '💡请输入内容！')
        return redirect('/app01/todo')


def todo_status(request, pk):
    todo = models.Todo.objects.filter(pk=pk).first()
    if todo:
        todo.status = int(not todo.status)
        todo.save()
        return redirect(to='/app01/todo')


def todo_delete(request, pk):
    models.Todo.objects.filter(pk=pk).delete()
    return redirect(to='/app01/todo')

