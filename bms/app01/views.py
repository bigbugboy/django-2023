from django.shortcuts import HttpResponse, render
from django.core.mail import send_mail
from threading import Thread

from . import models


def index(request):
    send_mail(
        'Subject here',
        'Here is the message.',
        '1505797244@qq.com',
        ['xu.liu@example.net'],
    )
    return HttpResponse('ok')


def send_email(user):
    send_mail(
        'Subject here',
        f'http://127.0.0.1:8000/app01/activate_account?user={user.username}',
        '1505797244@qq.com',
        ['xu.liu@example.net'],
    )


def register(request):
    if request.method == 'POST':
        print(request.POST)
        u = models.User.objects.create(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            age=int(request.POST.get('age')),
            birthday=request.POST.get('birthday')
        )
        # 独立线程发邮件，用户体验感更好
        t = Thread(target=send_email, args=[u])
        t.start()

        return HttpResponse('请查收邮件并点击链接激活账号')
    return render(request, 'register.html')


def activate_account(request):
    username = request.GET.get('user')
    if models.User.objects.filter(username=username, status=False).exists():
        models.User.objects.filter(username=username, status=False).update(status=True)
        return HttpResponse('激活成功')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'liuxu' and password == '12345':
            res = HttpResponse('login success')
            res.cookies['xxx'] = 'QWERT'
            return res
        else:
            return HttpResponse('login failed')


def home(request):
    return HttpResponse('home')


def vip(request):
    return HttpResponse('vip page')
