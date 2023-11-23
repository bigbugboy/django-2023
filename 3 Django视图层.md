# 3 Django视图层



Django视图层功能：

- 处理对应URL的请求，并返回响应数据；
- 这个请求-响应的过程中可能涉及到两个部分，
    - 1. 和模型层打交道，访问数据库数据，把数据响应给浏览器；
    - 2. 和模板层打交道， 视图层将某些数据传递给html模版文件，渲染后在把内容响应给浏览器





------

## 视图函数中的request

视图函数中的request参数非常重要。通过源码我们知道这个参数是 WSGIRequest类的实例化对象。

在视图函数中，我们可以通过request参数获取和请求有关的所有信息。

**通过type查看request参数的类型**

~~~python
from django.shortcuts import HttpResponse


def test(request: WSGIRequest):
    print(request)					# <WSGIRequest: GET '/app01/test?name=liuxu'>
    print(type(request))			 'django.core.handlers.wsgi.WSGIRequest'>
    return HttpResponse('test')
~~~



**request参数的常用属性和方法**

| 属性/方法                      | 描述                                                         |
| ------------------------------ | ------------------------------------------------------------ |
| `request.path`                 | 请求的路径部分，不包括域名、查询参数和其他组件。             |
| `request.path_info`            | 请求的完整路径，包括域名、查询参数和其他组件。               |
| `request.get_full_path()`      | 返回完整的请求路径URI                                        |
| `request.build_absolute_uri()` | 返回完整的请求路径，包括路径、查询参数和其他组件             |
| `request.method`               | 请求的 HTTP 方法，如 GET、POST 等。                          |
| `request.scheme`               | 请求协议 HTTP或者HTTPS                                       |
| `request.GET`                  | 包含所有的 GET 请求参数，以字典形式返回。                    |
| `request.POST`                 | 包含所有的 POST 请求参数，以字典形式返回。                   |
| `request.FILES`                | 包含所有的上传文件，以字典形式返回。                         |
| `request.body`                 | 请求体原始数据                                               |
| `request.session`              | 对象，表示当前会话的状态和数据。可以使用该对象读取或写入会话数据。 |
| `request.COOKIES`              | 包含所有的 cookie，以字典形式返回。                          |
| `request.user`                 | 表示当前经过身份验证的用户的对象。                           |
| `request.is_ajax()`            | 检查请求是否是 AJAX 请求，返回布尔值。                       |
| `request.is_secure()`          | 检查请求是否通过 HTTPS 安全连接进行。                        |





**Demo：request对象上常用的属性和方法**

~~~python
from django.shortcuts import HttpResponse


def test(request):
    print(request.path)	
    print(request.path_info)
    print(request.get_full_path())
    print(request.build_absolute_uri())

    print(request.method)
    print(request.scheme)

    return HttpResponse('test')
~~~

>比如：浏览器访问：http://127.0.0.1:8000/app01/test?name=liuxu 打印信息如下，
>
>/app01/test
>/app01/test
>/app01/test?name=liuxu
>http://127.0.0.1:8000/app01/test?name=liuxu
>GET
>http



**补充：通过类型提示的方式，查看request对象的所有属性和方法**。

~~~python
from django.shortcuts import HttpResponse

from django.core.handlers.wsgi import WSGIRequest


def test(request: WSGIRequest):
    print(request.path)	
    print(request.path_info)
    print(request.get_full_path())
    print(request.build_absolute_uri())

    print(request.method)
    print(request.scheme)

    return HttpResponse('test')
~~~







------

## 视图函数中的其他参数

视图函数中除了request之外，还可能有其他参数，比如：路径参数和自定义参数。并且他们都是按照关键字传参的方式，交给视图函数的。

如果你对 Python 函数传参不熟悉，推荐先了解如下知识点：

- 位置参数
- 关键字参数
- 不定长参数，*args, **kwargs



**request是位置参数，必须放在第一个位置**。如下两个视图函数，

- 第1个视图函数先定义的request形参，再定义的args和kwargs。则test1函数被调用时第一个实参会赋值给我形参request, 多余的位置实参会按照元组的形式给args，多余的关键词参数会按照字典的形式给kwargs。
- 第2个视图函数没有单独定义request形参，直接另一的args和kwargs，则test2函数被调用时，所有的位置参数按照元组的形式给args，所有的关键词参数会按照字典的形式给kwargs。

~~~python
from django.shortcuts import HttpResponse

from django.core.handlers.wsgi import WSGIRequest


def test1(request, *args, **kwargs):
    print(request)
    print(args)
    print(kwargs)
    return HttpResponse('test')


def test2(*args, **kwargs):
    print(args)
    print(kwargs)
    return HttpResponse('test')
~~~



**使用路径转换器，或者使用re_path分组后得到的路径值都会按照关键字的传参方式交给视图函数**。比如，在path中使用路径转换器，访问的URL是 `http://127.0.0.1:8000/app03/test3/2023/12`，那么kwargs这个字典就会有两个键值对（`{'year': 2023, 'month': 12}`），如果你把year和month单独定义在视图函数中，此时kwargs就是空字典了。

~~~python
# app03.views.py
from django.shortcuts import HttpResponse


def test3(request, *args, **kwargs):
    print(request)
    # print(year, month)
    print(args)
    print(kwargs)

    return HttpResponse('test')



# app03.urls.py
urlpatterns = [
    path('test3/<int:year>/<int:month>', test3),
]
~~~



**补充**：

- 如果视图函数中，定义了request参数，那么 args 将永远为空元组

- 路径函数中使用kwargs也会按照关键字传参的方式交给视图函数，且优先级大于路径转换器。







------

## HTTP协议的基本概念

- 基础内容参考视频（第三章前5节）：https://www.51zxw.net/List.aspx?cid=1003#!fenye=1
- 参考视频的PPT给到大家

需要掌握的知识点：URI 请求方式 请求头 响应头 响应体 状态码等

常见的请求方式：

| 序号 | 方法   | 描述                                         |
| ---- | ------ | -------------------------------------------- |
| 1    | GET    | 获取指定资源数据，如：浏览器访问URL是GET请求 |
| 3    | POST   | 新建数据                                     |
| 4    | PUT    | 修改数据                                     |
| 5    | DELETE | 删除数据                                     |
| 9    | PATCH  | 是对 PUT 方法的补充，进行局部更新 。         |



**补充：HTTP协议简介**

软件架构分类：CS（客户端-服务端）、BS（浏览器-服务端）；浏览器是特殊的客户端

在浏览器的网址栏内输入网址，简单来说发生了四件事：

- 浏览器向服务端发送请求
- 服务端接收请求
- 服务端返回响应内容
- 浏览器接收响应，并将响应内容按照一定规则渲染在页面上

浏览器要和不同的服务端打交道，因此需要浏览器和服务端遵循一定的规则，这个规则就是**HTTP协议**。

**HTTP，用来规定服务端和浏览器之间交互数据的格式。**如果是BS软件，就必须准许HTTP协议，否则只能是自己写客户端的app。

**HTTP四大特性**

- 基于响应请求
- 基于TCP/IP协议作用在应用层的协议
- 无状态，（为了保存状态，后来出现了cookie\session\token技术）
- 无\短链接；一次请求一次响应，之后就断开连接，没有关系；（后来出现长链接，双方建立连接后默认不断开：websocket）

**请求数据格式**

```python
# 请求首行\r\n请求头\r\n\r\n请求体\r\n

请求首行：标识HTTP协议版本，当前请求方式
请求头：一大堆k, v键值对
请求体：并不是所有的请求方式都有get没有post有 存放的是post请求提交的敏感数据

# 请求方式
get请求：向服务端要数据		
post请求：向服务端提交数据

# 补充；
url：统一资源定位单位，即所谓的网址
```

**响应数据格式**

```python
# 响应首行\r\n响应头\r\n\r\n响应体\r\n

响应首行：标识HTTP协议版本，响应状态码
响应头：一大堆k, v键值对
响应体：返回给浏览器展示给用户的数据

# 响应状态码：一串表示复杂状态或者描述信息的数字
1xx：服务端已经成功接收到了你的数据正在处理，你可以继续提交额外的数据
2xx：服务端成功响应了你想要的数据(200 OK请求成功)
3xx：重定向(301,302)
4xx：请求错误（404，资源不存在；403，没有访问权限）
5xx：服务器内部存错（500）
```





------

## 获取查询参数

在HTTP协议中，**查询参数（Query  Parameters）是在URL中用于向服务器传递数据的一种方式**。查询参数通常用于GET请求，并将数据附加在URL的尾部，按照键值对的形式表示。查询参数以问号（?）开始，然后是一个或多个键值对，每个键值对之间用&符号分隔。

以下是一个示例URL，其中包含查询参数：

~~~
http://127.0.0.1:8001/app03/test?name=liuxu&age=18
~~~

在Django获取查询参数的方式有两种（request.get_full_path()、request.GET）。两种方式都可以获取查询参数，但是第一个需要我们手动解析数据，一般我们使用第二种方式获取查询参数。



**使用request.GET获取查询参数**

~~~python
from django.core.handlers.wsgi import WSGIRequest

def test4(request: WSGIRequest, *args, **kwargs):
    print(request.GET)
    print(request.GET.get('name'))		# 获取最后一个值
    print(request.GET.getlist('name'))	# 获取一个列表
    print(request.GET.urlencode())		# 获取urlencode编码格式的值
    return HttpResponse('test')
~~~

注意：使用request.GET拿到的数据类型都是字符串。

提示：在浏览器的地址栏访问URL的方式，使用的请求方式是 GET



**GET常用方法汇总**（部分）

| 属性/方法                                   | 描述                                                         |
| ------------------------------------------- | ------------------------------------------------------------ |
| `request.GET`                               | 包含所有的 GET 请求参数，以字典形式返回。                    |
| `request.GET.get(key, default=None)`        | 获取指定键的对应值，如果键不存在则返回默认值。               |
| `request.GET.getlist(key)`                  | 获取指定键的所有值，返回一个列表。                           |
| `request.GET.keys()`                        | 返回包含所有参数键的列表。                                   |
| `request.GET.values()`                      | 返回包含所有参数值的列表。                                   |
| `request.GET.items()`                       | 返回包含所有参数键值对的列表。                               |
| `request.GET.urlencode()`                   | 将 GET 请求参数编码为 URL 查询字符串的形式。                 |
| `request.GET.__contains__(key)`             | 检查指定键是否存在于 GET 请求参数中，返回布尔值（Python 3 中使用 `key in request.GET` 语法）。 |
| `request.GET.copy()`                        | 创建 GET 请求参数的副本，返回一个新的字典。                  |
| `request.GET.setlist(key, list)`            | 设置指定键的值为给定的列表，可用于更新 GET 请求参数。        |
| `request.GET.update(query_dict)`            | 使用给定的 QueryDict 对象更新 GET 请求参数。                 |
| `request.GET.pop(key, default=None)`        | 弹出并返回指定键的值，如果键不存在则返回默认值。             |
| `request.GET.popitem()`                     | 弹出并返回 GET 请求参数的任意键值对。                        |
| `request.GET.clear()`                       | 清空 GET 请求参数。                                          |
| `request.GET.setdefault(key, default=None)` | 获取指定键的值，如果键不存在则设置默认值并返回。             |





------

## 获取form表单提交的查询参数

form表单其实是前端HTML中的一个标签，功能是用来向服务器提交数据的。form表单支持的请求方式：

- GET（默认的方式）
- POST

比如，编写一个index.html页面，使用form表单发送GET请求

**index.html**

~~~html
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>

<form action="http://127.0.0.1:8000/app03/test5">
    <p>姓名：<input type="text" name="name"></p>
    <p>年龄：<input type="text" name="age"></p>
    <input type="submit" value="提交">
</form>

</body>
</html>
~~~

其中：

- action 表示朝哪个URL发请求
- form表单默认是GET请求，数据放在URL上发送给服务端（即查询参数）
- `input` 标签中的 `name` 字段指定URL上查询参数的key名，input输入框输入的数据是value值



视图函数，form表单使用GET方式提交的数据，后端可以从`request.GET` 获取。

~~~python
def test5(request: WSGIRequest):
    print(request.GET.get('name'), type(request.GET.get('name')))
    print(request.GET.get('age'), type(request.GET.get('age')))
    return HttpResponse('test')
~~~







------

## 获取form表单提交的请求体数据

在HTTP协议中，客户端向服务端提交数据时，一般会选择使用POST请求，并把数据放在请求体中。

demo：使用form表单发送POST请求

- **demo-form-post.html**

~~~html
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>


<form action="http://127.0.0.1:8000/app03/test6" method="post">
    <p>姓名：<input type="text" name="name"></p>
    <p>年龄：<input type="text" name="age"></p>
    <input type="submit" value="提交">
</form>

</body>
</html>
~~~

其中：

- method=""post"表示发送POST请求，method默认值是GET，即form表单默认发送GET请求。



- 视图函数，**使用 request.body 获取表单数据**

~~~python
def test6(request: WSGIRequest):
    print(request.body)				# b'name=liuxu&age=20'
    return HttpResponse('test')
~~~

>扩展：form表单发送POST请求时，默认请求体数据的编码格式是 `application/x-www-form-urlencoded`，可简称为 `urlencoded`。所以此时从body中拿到的数据是：`b'name=liuxu&age=20'`



- 视图函数，**使用 request.POST获取表单数据**

~~~python
def test6(request: WSGIRequest):
    print(request.body)				# b'name=liuxu&age=20'
    name = request.POST.get('name')
    age = request.POST.get('age')
    print(name, age)
    return HttpResponse('test')
~~~

request.POST的使用方式和request.GET相同，它本省也是一个字典，可以按照字典的取值方式获取客户端发送POST请求时在请求体中传过来的数据。



**CSFT校验失败**

上述页面，在浏览器输入数据，点击提交会报错（CSRF）。这种报错的原因我们暂时不解释，先采用临时的解决方法。临时的解决方法：在django的配置文件中注释一行配置即可。注释后即可发送POST类型的请求。

~~~python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
~~~







------

## form表单编码格式

form表单发送POST请求，请求体中支持的数据格式有三种，

- text/plain
- application/x-www-form-urlencoded
- multipart/form-data

使用form表单时，可以修改 `enctype`的值为这三个中的一个，默认是 urlencoded



**纯文本**。如果请求体数据编码为`text/plain`

- 请求头中：`Content-Type: text/plain`

- 请求体的数据格式为：`b'name=liuxu\r\nage=20\r\n'`
- 此时无法使用 `request.POST` 获取请求体数据，只能使用 `request.body`

~~~python
def test6(request: WSGIRequest):
    print(request.body)					# b'name=liuxu\r\nage=20\r\n'
    name = request.POST.get('name')
    age = request.POST.get('age')
    print(name, age)				# None, None
    return HttpResponse('test')
~~~



**Urlencoded**。请求体数据按照URL上的查询参数的格式编码

- 请求头中：`Content-Type: application/x-www-form-urlencoded`
- 请求体的数据格式为：`b'name=liuxu&age=20'`
- 此时会选择使用 `request.POST` 获取请求体数据，一般不会使用 `request.body` 手动解析数据



**form-data**。这种格式主要用于上传文件的需求，但是也可以上传非文件数据

- 请求体中：`Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryx8xYcBFZBnQSRDi0`
- 请求体数据格式为：`b'------WebKitFormBoundaryx8xYcBFZBnQSRDi0\r\nContent-Disposition: form-data; name="name"\r\n\r\nliuxu\r\n------WebKitFormBoundaryx8xYcBFZBnQSRDi0\r\nContent-Disposition: form-data; name="age"\r\n\r\n20\r\n------WebKitFormBoundaryx8xYcBFZBnQSRDi0--\r\n'`
- 此时，使用 `request.POST`  获取非文件数据，使用 `request.FILES` 获取文件数据。



**总结：**

在 Django 中，不论何种格式的请求体数据，都可以使用 `request.body` 来获取。但这种方式拿到的是一个字节字符串，包含HTTP请求的原始数据。大多数情况下，我们不会直接使用 `request.body` 来获取请求体数据。针对不同格式的请求体数据，有专门的方法来提取数据。    







------

## 获取form表单上传的文件

form表单一个非常重要的功能就是上传文件

- **form表单上传文件，必须使用POST方式。请求体数据编码，必须使用 form-data格式**
- **文件数据使用 request.FILES 接收**



上传的字段是文件时，需要修改 `input`标签的 `type`属性值为 `file`

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<h1>上传文件</h1>
<form action="http://127.0.0.1:8000/app03/test7" method="post" enctype="multipart/form-data">
    <p> 请选择文件: <input type="file" name="file"></p>
    <input type="submit" value="上传">
</form>

</body>
</html>
~~~

**视图函数**。`request.FILES.get("")` 按照前端传过来的key来获取第一个文件 

~~~python
def test7(request: WSGIRequest):
    print(request.body)
    print(request.POST.get('file'))
    print(request.FILES.get('file'), type(request.FILES.get('file')))
    
    # 保存文件
    file = request.FILES.get('file')
    with open(file.name, "wb") as f:
        for line in file.chunks():  # 分多次读内容并写到本地文件
            f.write(line)

    return HttpResponse('test')
~~~







------

## 获取form表单上传的多个文件

可以同时上传多个文件可以同时上传多个文件。



**前端上传的多个文件使用的是不同的key**

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<h1>上传文件</h1>
<form action="http://127.0.0.1:8000/app03/test8" method="post" enctype="multipart/form-data">
    <p> 请选择文件1: <input type="file" name="file1"></p>
    <p> 请选择文件1: <input type="file" name="file2"></p>
    <input type="submit" value="上传">
</form>

</body>
</html>
~~~

后端视图。使用`request.FILES.get("")` 接收数据

~~~python
def test8(request: WSGIRequest):
    print(request.FILES.get('file1'))
    print(request.FILES.get('file1'))
    
    # 保存文件
    for key in ['file1', 'file2']:
        file = request.FILES.get(key)
        with open(file.name, "wb") as f:
            for line in file.chunks():  # 分多次读内容并写到本地文件
                f.write(line)

    return HttpResponse('test')
~~~

**前端上传的多个文件使用的是相同的key**

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<h1>上传文件</h1>
<form action="http://127.0.0.1:8000/app03/test9" method="post" enctype="multipart/form-data">
    <p> 请选择文件: <input type="file" name="file1"></p>
    <input type="submit" value="上传">
</form>

</body>
</html>
~~~

后端视图。使用`request.FILES.getlist("")` 接收数据

~~~python
def test9(request: WSGIRequest):
    print(request.FILES.get('file1'))
    
    # 保存文件
    files = request.FILES.getlist('file')
    for file in files:
        with open(file.name, "wb") as f:
            for line in file.chunks():  # 分多次读内容并写到本地文件
                f.write(line)

    return HttpResponse('test')
~~~







------

## 获取form表单上传的文件和普通数据

form表单支持非文件数据（普通数据）和文件同时上传，此时上传方式是POST, 编码方式必须是 `form-data`

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<h1>上传头像</h1>
<form action="http://127.0.0.1:8000/app03/test10" method="post" enctype="multipart/form-data">
    <p>用户名: <input type="text" name="name"></p>
    <p> 请选择头像: <input type="file" name="file"></p>
    <input type="submit" value="上传">
</form>

</body>
</html>
~~~

**视图函数**。文件数据使用 `request.FILES` 接收，非文件数据使用 `request.POST`  接收.

~~~python
def test10(request: WSGIRequest):
    print(request.body)
    print(request.POST.get('name'))
    print(request.FILES.get('file'))
    
    # 保存文件
    file = request.FILES.get('file')
    with open(file.name, "wb") as f:
        for line in file.chunks():  # 分多次读内容并写到本地文件
            f.write(line)

    return HttpResponse('test')
~~~









------

## 使用postman发送请求

除了使用浏览器（form表单）发送网络请求外，还有很多可以发送网络请求的客户端。

在开发过程中，经常使用的一个客户端工具大概就是postman了。postman是一个软件，可以免费使用。

使用 postman 发送HTTP网络请求，可以非常方便的选择请求方式，请求体数据格式等。

postman官网：https://www.postman.com/

> 提示：请到postman官网下载该软件。



- 模拟各种请求方式的请求，GET、POST、PUT、DELETE等
- 模拟各种请求体编码格式：urlencoded、form-data、json、xml等



补充：除了postman之外，一般还用使用 apifox、curl等客户端工具。







------

## 获取JSON格式的请求体数据

前后端分离开发模式是目前最主流的开发方式，这种模式下，前后端传递数据大多数使用基于json格式的数据（即请求体数据编码格式为json）。此时如何获取请求体中的json数据呢？

**request.POST 可以非常方便地获取请求体中的数据，但它只能获取form表单提交的请求体数据**（并且是`urlencoded`格式）。

如果想获取客户端在请求体中传过来的 json 数据，需要自己使用 `json` 模块解析数据

**前端发送数据**：

- 使用postman模拟模拟前端发送POST请求，请求体数据格式为json的数据

**视图函数接收数据**

~~~python
import json

def test11(request: WSGIRequest):
    print(request.POST)		# request.POST 不会解析json格式的数据

    try:
        data = json.loads(request.body)
        print(data)
        HttpResponse('success')
    except json.JSONDecodeError:
        return HttpResponse('Invalid JSON format')
~~~

- 补充：这种情况下，最好判断下请求方式为POST，再从请求体中解析数据







------

## 响应 JSON格式的数据

在视图函数内可以响应任何格式的数据，比如 json（前后端分离开发时最常用的一个数据格式）。

**手动序列化**。我们可以把python的数据结构使用json模块序列化为json数据，然后再通过Httpresponse响应给浏览器。

~~~python
import json
from django.shortcuts import HttpResponse

def test12(request):
    data = {
        "name": "liuxu",
        "age": 18,
        "is_boy": True,
    }
    return HttpResponse(
        content=json.dumps(data),			# 使用json手动序列化
        content_type="application/json"		# 告诉客户端响应内容是json格式的数据，方便客户端处理数据。
    )

~~~

>扩展：python中有很多序列化模块，比如pickle，但是在前后端交互时我们不使用pickle，常用的是json







------

## 响应三件套之HttpResponse

HttpResponse是一个类，视图函数内的返回值都是它的对象。

使用时，可以直接返回它的实例化对象，也可以拿到实例化对象，修改对象的属性后，再返回该对象。

~~~python
from django.shortcuts import HttpResponse


def test13(request):
    response = HttpResponse(
        status=200,											# 指定响应状态码
        content="<h1 style='color:red'>hello</h1>",			# 响应的内容
        content_type="plain/text",							# 响应内容的类型
        headers={"xxx": "yyy"}								# 增加响应头
    )
    return response
~~~

- status默认是200
- content要求是bytes, 如果不是也会自动转换
- content_type默认是text/html，如果content是html文档则会自动渲染出页面







------

## 响应三件套之render

render是用来渲染模板的，把模板文件和模板需要的数据渲染到一块，然后响应给浏览器。

模板文件：templates/info.html

~~~html
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>

<!-- 此处的 {{}} 就是模板语法标识符 -->
<h1>about, {{student}}</h1>	

</body>
</html>
~~~

>需要配置：（先了解，后面第四章再详细介绍如何使用）
>
>- 在app01中新建文件夹 templates，把模板文件放在其中
>- 修改项目配置文件 settings.py
>
>~~~python
>INSTALLED_APPS = [
>    'django.contrib.admin',
>    'django.contrib.auth',
>    'django.contrib.contenttypes',
>    'django.contrib.sessions',
>    'django.contrib.messages',
>    'django.contrib.staticfiles',
>    # 'app01',  # 简洁配置
>    'app01.apps.App01Config',   # 完整配置(推荐)
>]
>~~~

views.py

~~~python
from django.shortcuts import render


def test14(request):
    return render(request, "info.html"， context={"student": "liuxu"})
~~~

其中：

- django会默认在app内部寻找 `templates`文件夹，从中按照提供的文件名字找到模板。

- `context`参数是为about模板提供的数据。在渲染该模板时，需要哪个变量就在`context`这个字典中找，找到就把该变量连同`{{}}`一块替换掉。找不到则渲染为空白。

- 使用render时，常用三个参数：request(必须)，template_name 模板文件名(必须)，context需要的数据(非必须)。



**扩展**：`render`把模板和数据整合在一起，然后得到一个 `HttpResponse` 对象。

~~~python
def render(
    request, template_name, context=None, content_type=None, status=None, using=None
):
    """
    Return an HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    content = loader.render_to_string(template_name, context, request, using=using)
    return HttpResponse(content, content_type, status)
~~~









------

## 响应三件套之redirect

redirect的作用是做重定向，即可是外部网站，也可以是内部路由。

redirect是一个函数，执行该函数会返回一个HttpResponse的子类。

本质上，在视图函数内使用redirect做返回值也是HttpResponse的对象。

~~~python
# 重定向外部链接
from django.shortcuts import redirect


def demo_redirect(request):
    return redirect(to="http://www.baidu.com")
~~~

- to参数直接赋值一个完整的外部链接



重定向内部路由有两种方式：

- 方式1：直接拼写需要重定向的url（以 `/` 开头）

~~~python
# app03.urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("apple", views.apple),
    path("test15", views.test15),
]


# app03.views.py
from django.shortcuts import redirect


def test15(request):
    # 手动重定向的url, 注意：以/开头
    return redirect(to="/app03/apple")	


def apple(request):
    return HttpResponse(
        status=200,
        content="<h1 style='color:red'>红苹果</h1>",
    )
~~~



- 方式2：给path定义名字，需要跳转到这个path对应的URL时直接使用名字即可

~~~python
# app03.urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("applexxxxxxxx", views.applex，name='apple'),	# 使用起名字的方式标识这个路由		
    path("test16", views.test16)	
]


# app03.views.py
from django.shortcuts import redirect


def test16(request):
    return redirect(to="apple")		# 直接使用上面起的名字


def applex(request):
    return HttpResponse(
        status=200,
        content="<h1 style='color:red'>红苹果</h1>",
    )
~~~

**总结**：

- 方法1的优点是简单直接，缺点：(1)手动拼接URL容易出错；(2)如果URL的定义发生了变化则需要手动修改代码
- 方法2的有点是解决了方法1的缺点



**扩展**：redirect()可以使用参数 `permanen` 设置重定向的类型

- `permanen=False`，表示临时重定向（默认设置）
- `permanen=True`，表示永久重定向



**思考：**

- **如果重定向的URL中包含动态参数，使用方法1该如何实现，使用方法2该如何实现？**







## JsonResponse响应json数据

django为我们封装了一个现成的response对象，专门用来响应json数据。

~~~python
from django.http import JsonResponse


def test17(request):
    data = {
        "name": "刘旭",
        "age": 18,
        "is_boy": True,
    }
    ll = [1, 2, 3, 4, 5]
    return JsonResponse(data)				
    # return JsonResponse(ll, safe=False)		# 如果最外层是列表，需要使用safe=False

~~~

>扩展1：JsonResponse内还可以使用json_dumps_params，作为参数直接传给 json.dumps()
>
>扩展2：前端JS 序列化和反序列化一般使用：JSON.stringify()、JSON.parse()







------

## 写一个注册功能

- 前端是form表单，用户提交用户名、密码、图像
- 后端接收数据，做注册校验，保存头像文件



- 前端html， templates/register.html

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>注册页面</h1>
<form action="/app01/register" method="post" enctype="multipart/form-data">
  <p>用户名: <input type="text" name="username"></p>
  <p>密码: <input type="password" name="password"></p>
  <p>确认密码: <input type="password" name="re_password"></p>
  <p>头像: <input type="file" name="file"></p>
  <input type="submit" value="注册">
</form>

</body>
</html>
~~~



- 后端代码

~~~python
# app03/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("register", views.register),
]


# app03/views.py
from django.shortcuts import render, HttpResponse
from django.http.request import HttpRequest


DB = {
    "LIUXU": "123456"
}


def register(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        avatar_file = request.FILES.get("file")
        if username in DB:
            return HttpResponse("用户名已存在")
        if password != re_password:
            return HttpResponse("两次密码输入不一致")
        if avatar_file is None:
            return HttpResponse("请选择头像图片")

        DB[username] = password
        return HttpResponse("注册成功")

    return render(request, "register.html")
~~~

>==注意：实际开发中，密码需要加密之后保存数据库，不能保存明文。==







------

## 写一个登录功能

- 前端是form表单，提交数据：用户名和密码
- 后端接收数据，做登录校验逻辑



- 前端html页面 templates/login.html

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<h1>登录</h1>
<form action="/app01/login" method="post">
  <p>用户名：<input type="text" name="username"></p>
  <p>密码：<input type="password" name="password"></p>
  <input type="submit" value="登录">
</form>

</body>
</html>
~~~

- 后端代码

~~~python
# app03/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("login", views.login),
]



# app03/views.py
from django.shortcuts import render, HttpResponse
from django.http.request import HttpRequest


# 模拟数据库
DB = {
    "LIUXU": "123456"
}


def login(request: HttpRequest):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username not in DB:
            return HttpResponse("用户名不存在")
        if password != DB[username]:
            return HttpResponse("密码错误")

        return HttpResponse("登录成功")

    return render(request, "login.html")
~~~





## 使用hashlib实现密码加密

- **注册功能-视图函数**

~~~python
import hashlib

from django.shortcuts import render, HttpResponse
from django.http.request import HttpRequest


DB = {
    "LIUXU": "123456"
}


def register(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        avatar_file = request.FILES.get("file")
        if username in DB:
            return HttpResponse("用户名已存在")
        if password != re_password:
            return HttpResponse("两次密码输入不一致")
        if avatar_file is None:
            return HttpResponse("请选择头像图片")
		
        encrypted_password = hashlib.md5(password.encode()).hexdigest()
        DB[username] = encrypted_password
        return HttpResponse("注册成功")

    return render(request, "register.html")
~~~



- 登录功能-视图函数

~~~python
import hashlib

from django.shortcuts import render, HttpResponse
from django.http.request import HttpRequest


# 模拟数据库
# "e10adc3949ba59abbe56e057f20f883e" 是 "123456" 使用md5加密后的密文
DB = {
    "LIUXU": "e10adc3949ba59abbe56e057f20f883e"
}


def login(request: HttpRequest):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username not in DB:
            return HttpResponse("用户名不存在")
        encrypted_password = hashlib.md5(password.encode()).hexdigest()
        if encrypted_password != DB[username]:
            return HttpResponse("密码错误")

        return HttpResponse("登录成功")

    return render(request, "login.html")
~~~







------

## 写一个下载文件功能

当使用Django实现文件下载功能时，你可以按照以下步骤进行操作：

1. 首先，在`views.py`文件中创建一个名为`file_list`的视图函数，该函数用于显示文件列表页面。

```python
# views.py
import os
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render

def file_list(request):
    # 获取文件列表
    file_directory = os.path.join(settings.MEDIA_ROOT, 'files')
    files = os.listdir(file_directory)

    return render(request, 'file_list.html', {'files': files})
```

创建一个`file_list.html`模板文件，用于显示文件列表。

```html
<!-- file_list.html -->
<ul>
    {% for file in files %}
    <li><a href="{% url 'download' file %}">{{ file }}</a></li>
    {% endfor %}
</ul>
```

创建一个名为`download`的视图函数，该函数用于处理文件下载请求。

```python
# views.py
import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render

def download(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'files', filename)

    if os.path.exists(file_path):
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        raise Http404('File not found')
```

在`urls.py`文件中定义URL模式，将`file_list`和`download`视图函数与相应的URL路径进行关联。

1. ```python
    # urls.py
    from django.urls import path
    from .views import file_list, download
    
    urlpatterns = [
        path('files/', file_list, name='file_list'),
        path('download/<str:filename>/', download, name='download'),
    ]
    ```

现在，当用户访问`/files/`路径时，将显示文件列表页面，其中包含文件的下载链接。当用户点击链接时，将触发文件下载，浏览器会下载相应的文件。



