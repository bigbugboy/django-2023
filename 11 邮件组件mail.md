# 11 邮件组件mail



## mail的配置和基本使用

**视图函数使用mail组件**

~~~python
from django.shortcuts import HttpResponse
from django.core.mail import send_mail


def index(request):
    send_mail(
        'Subject here',				# 配置邮件主题
        'Here is the message.',		# 邮件内容
        'from@qq.com',				# 配置发件人
        ['xu.liu@example.com'],	    # 支持配置多个收件人
    )
    return HttpResponse('ok')

~~~



**settings.py配置邮件服务信息**（QQ邮箱为例）

~~~python
EMAIL_HOST = "smtp.qq.com"					# 配置邮件服务器
EMAIL_PORT = 25								# 邮件服务端口
EMAIL_HOST_USER = "xxx@qq.com"				# 发件人账号
EMAIL_HOST_PASSWORD = "ncwsycmyqsytggfa"	# 发件人密码（授权码）

~~~



**获取QQ邮箱授权码**

- 登录网页QQ邮箱，登录
- 点击进入设置页面，找到 邮箱设置下面的【账号】tab页
- 找到 **POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务**，并提示操作获取授权码

![image-20231010180235538](./django_tut.assets/image-20231010180235538.png)









## 模拟注册账号发激活邮件

注册账号后，用户一般会收到激活邮件，在邮件中点击激活链接，完成账号的激活。

**注册逻辑的视图函数和模板文件**

- 视图函数

~~~python
def register(request):
    if request.method == 'POST':
        print(request.POST)
        u = models.User.objects.create(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            age=int(request.POST.get('age')),
            birthday=request.POST.get('birthday')
        )
        return HttpResponse('ok')
    return render(request, 'register.html')

~~~

- 模板文件

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>注册页面</h1>
<form action="/app01/register" method="post" enctype="application/x-www-form-urlencoded">
  <p>用户名: <input type="text" name="username"></p>
  <p>密码: <input type="password" name="password"></p>
  <p>确认密码: <input type="password" name="re_password"></p>
  <p>年龄: <input type="text" name="age"></p>
  <p>出生日期: <input type="date" name="birthday"></p>
  <input type="submit" value="注册">
    {% csrf_token %}
</form>

</body>
</html>
~~~



**QQ邮箱发邮件，激活链接**

- 视图函数

~~~python
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
        send_mail(
            'Subject here',
            f'http://127.0.0.1:8000/app01/activate_account?user={u.username}',
            '1505797244@qq.com',
            ['xu.liu@example.net'],
        )

        return HttpResponse('请查收邮件并点击链接激活账号')
    return render(request, 'register.html')
~~~

- 账号激活接口。用户点击激活链接，完成激活

~~~python
# 简单版
def activate_account(request):
    username = request.GET.get('user')
    if models.User.objects.filter(username=username, status=False).exists():
        models.User.objects.filter(
            username=username, status=False).update(status=True)
        return HttpResponse('激活成功')
    return HttpResponse('该账号无需激活')
~~~



**使用多线程，单独发邮件**

~~~python
def send_email(user):
    send_mail(
        'Subject here',
        f'http://127.0.0.1:8000/app01/activate_account?user={user.username}',
        '1505797244@qq.com',
        ['xu.liu@example.net'],
    )

    
from threading import Thread

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
~~~



