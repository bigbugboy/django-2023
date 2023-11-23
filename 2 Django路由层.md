# 2 Django路由层

django路由层的功能：

- 路由分发，把URL匹配对应的视图函数。核心代码书写在**urls.py**文件





## 路由函数path

路由层中的路由匹配函数很重要，我们就从这个点入手，开始了解Django路由的工作方式。

Django中路由函数有两个（path、re_path），path是常用的一个，并且它的整体使用方式re_path的几乎一致，所以我们先来介绍 path的基本使用。

使用 path 函数，可以传递4个参数（route和view是必须使用的，后两个不是必须的）：

- **route，就是待匹配URL。写的什么就匹配什么**
- **view，就是视图函数。通过 route匹配到的请求，交给该视图函数处理，视图函数都会收到一个表示请求的参数request，作为第一个位置参数。 视图函数的返回值响应给浏览器**
- kwargs，传给视图函数的参数，kwargs就是一个字典，**每个键值按照关键字参数的形式传给视图函数**
- name，给path起名字。用于URL的反向解析和重定向（暂了解，后面在视图层再详细介绍）

~~~python
from django.contrib import admin
from django.shortcuts import HttpResponse, redirect

from django.urls import path


def hello(request, a, b):
    print(a)	# 形参a和b的名字需要和path里面kwargs中的key保持一致
    print(b)	# 因此，形参a和b的位置关系不会影响a和b的值
    return HttpResponse('hello world')


def hello123(request):
    return redirect('http://www.baidu.com')

def ttt(request):
    return HttpResponse('ttt')


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('hello/abc', ttt),
    path('hello', hello, kwargs={'a': 10, 'b': 20}),
    path('hello123', hello123),
]
~~~







## 处理动态URL

想象一下，我们有一个博客网站，它提供了如下一些URL，比如：

- 查询一个年份下的所有文章列表，URL：articles/动态的年份。比如：articles/2023
- 查询一个年份，一个月份下的所有文章，URL：articles/年份/月份。比如：articles/2023/11

那好，遇到这样的需求，该如何编写path和视图函数呢？



Django帮我们想好了，使用动态路由即可实现。

第一步：定义route时，给URL中动态的变量起一个名字，并且用 `<>` 包起来。比如：`articles/<year>`

第二步：定义视图函数时，需要多一个位置参数，名字就是上面定义的变量名。比如：`year`

>解释：这两步完成后，如果访问浏览器的URL被匹配到，比如：articles/2023， django就会把2023赋值给变量year, 此时在视图函数中就可以使用year变量了。



**URL中定义一个动态变量**

~~~python
from django.contrib import admin
from django.shortcuts import HttpResponse, redirect

from django.urls import path


def hello(request, a, b):
    print(a)  # 形参a和b的名字需要path里面kwargs中的key保持一致
    print(b)  # 因此，形参a和b的位置关系不会影响a和b的值
    return HttpResponse('hello world')


def hello123(request):
    return redirect('http://www.baidu.com')


def ttt(request):
    return HttpResponse('ttt')


def year_archive(request, year):
    return HttpResponse(f'{year} 所有的文章列表')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('hello/abc', ttt),
    path('hello/<a>', hello, kwargs={'a': 10, 'b': 20}),
    path('hello123', hello123),
    path("articles/<year>", year_archive),
]
~~~



**URL中定义多个动态变量**。定义多个变量名，并使用<>分别包裹即可。

~~~python
from django.contrib import admin
from django.shortcuts import HttpResponse, redirect

from django.urls import path


def year_archive(request, year):
    return HttpResponse(f'{year} 所有的文章列表')


def month_archive(request, year, month):
    return HttpResponse(f'{year}年{month}月所有的文章列表')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/abc', ttt),
    path('hello/<a>', hello, kwargs={'a': 10, 'b': 20}),
    path('hello123', hello123),
    
    path("articles/<year>", year_archive),
    path("articles/<year>/<month>", month_archive),
]
~~~





## 路由冲突及其解决办法

上面的动态路由很方便，比如说，按照所有的年份分档，只需要写一个视图函数就好了。

但你可曾遇到，我们有了一个新需求，2023年是一个非常重要的年份，我们要推一个特殊的页面出来，此时就需要单独出一个页面了。



你写的代码可能是如下这样的。但是当你访问 articels/2023后，你却看不到你想要的页面。

~~~python
from django.contrib import admin
from django.shortcuts import HttpResponse, redirect

from django.urls import path


def year_archive(request, year):
    return HttpResponse(f'{year} 所有的文章列表')


def month_archive(request, year, month):
    return HttpResponse(f'{year}年{month}月所有的文章列表')


def special_case_2023(request):
    return HttpResponse('this is a special case 2023, welcome!!!')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/abc', ttt),
    path('hello/<a>', hello, kwargs={'a': 10, 'b': 20}),
    path('hello123', hello123),
    
    path("articles/<year>", year_archive),
    path("articles/<year>/<month>", month_archive),
    path("articles/2023", special_case_2023),
]
~~~



**问题的原因**

在浏览器发请求后，django内部首先会做URL的匹配。匹配是按照在urlpatterns中定义的先后顺序的，即从上往下一个path一个paht的匹配，只要匹配成功就不再往下匹配了。

那就好了，浏览器请求的URL是，articles/2023：

- 从上往下匹配，匹配上的第一个就是 `path("articles/<year>", year_archive)`
- 于是你看到的页面永远都是 year_archive 这个视图函数的结果。



**解决方法**

很简单，把具体的 URL匹配规则放在抽象的URL匹配规则前面。这样从上往下匹配时，遇到 articles/2023就会第一个匹配到special_case_2023。

~~~python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/abc', ttt),
    path('hello/<a>', hello, kwargs={'a': 10, 'b': 20}),
    path('hello123', hello123),
    
    path("articles/2023", special_case_2023),
    path("articles/<year>", year_archive),
    path("articles/<year>/<month>", month_archive),
]
~~~







## 路径转换器

不知道大家有没有发现一个问题，上面的例子中，我们使用 `articles/<year>` 的方式来匹配动态路由中的变量`year`，然后在视图函数中就会对应一个同名的形参  `year`。那你知道这个参数是什么类型的吗，是字符串还是数字？

其实，这种方式拿到的形参，他们的类型都是字符串。并且有个特别的名词来形容这种取值的方式，他就是**路径转换器（path converter）**。路径转换器默认都会转为字符串。

~~~python
def year_archive(request, year):
    print(type(year))	# <class 'str'>
    return HttpResponse(f'{year} 所有的文章列表')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/abc', ttt),
    path('hello/<a>', hello, kwargs={'a': 10, 'b': 20}),
    path('hello123', hello123),
    
    path("articles/2023", special_case_2023),
    path("articles/<str:year>", year_archive),
    path("articles/<year>/<month>", month_archive),
]

# 比如,
# 		path("articles/<year>", year_archive),
# 		等价于 path("articles/<str:year>", year_archive)
~~~



**Django内置提供了5个路径转换器**。最常用应该是 int

| 转换器 | 说明                                                         |
| ------ | ------------------------------------------------------------ |
| `str`  | 默认的转换器，匹配除了斜杠('/')之外的任何非空字符串。        |
| `int`  | 匹配零或正整数。                                             |
| `slug` | 匹配由 ASCII 字母、数字、连字符或下划线组成的任何字符串。    |
| `uuid` | 匹配格式为 UUID 的字符串，例如 `075194d3-6885-417e-a8a8-6c931e272f00`。 |
| `path` | 匹配任何非空字符串，包括斜杠('/')。可以用于捕获 URL 中的路径部分，包括斜杠。 |



**匹配 int 的例子**

~~~python
def year_archive(request, year):
    print(type(year))	# <class 'int'>
    return HttpResponse(f'{year} 所有的文章列表')


urlpatterns = [
    path("articles/2023", special_case_2023),
    path("articles/<int:year>", year_archive),	
    path("articles/<year>/<month>", month_archive),
]
~~~



**匹配 path 的例子**。在浏览器访问：`http://127.0.0.1:8000/download/a/b/c`，就可以看到：a/b/c

~~~python
from django.contrib import admin
from django.shortcuts import HttpResponse

from django.urls import path


def download_file(request, filepath):
    return HttpResponse(filepath)


urlpatterns = [
    path('download/<path:filepath>', download_file)
]
~~~



**总结**

- 路径转换器的格式是：`<名字>`，同时在视图函数多一个位置参数，且必须是同名的形参
- 一个路由上可以有多个路径转换器，依次作为位置参数传给视图函数。

- Django内置5中路径转换器，默认是str。同时Django也支持自定义路径转换器









## 路由函数re_path

**如果路由函数path和转换器都无法满足你的URL匹配设计，那你还可以使用 re_path**。 

我们知道 path 的原则是你写的URL是什么就匹配什么，而 re_path则是按照正则表达式的方式来匹配，更加通用且灵活，但缺点可能是不直观，不好理解。



**使用 re_path 的案例**

- 正则表达式中需要使用 `()` 将待匹配的参数包起来，这称之为分组
- 分组内，直接写正则表达式的称为 **无名分组**。此时视图函数的形参名可以随意定义。
- 分组内，可以使用 `?P<>` 的方式包裹一个变量名，这称为**有名分组**。此时视图函数的形参名必须保持一致。

~~~python
from django.contrib import admin
from django.shortcuts import HttpResponse, redirect

from django.urls import path, re_path


def year_archive(request, yyyy):
    # 对应的路由规则使用了无名分组，此时形参名yyyy是自定义的
    return HttpResponse(f'{yyyy} 所有的文章列表')


def month_archive(request, year, month):
    # 对应的路由规则使用了有名分组，定义了两个名字，year和month，此时形参名必须是这两个名字
    return HttpResponse(f'{year}年{month}月所有的文章列表')


def special_case_2023(request):
    return HttpResponse('this is a special case 2023, welcome!!!')


urlpatterns = [
    path("articles/2023", special_case_2023),
    # 无名分组
    re_path(r"^articles/([0-9]{4})$", year_archive),
    # 有名分组
    re_path(r"^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$", month_archive),
]
~~~



**补充**：

- Django早期版本时只有正则匹配，使用 url()，但是现在的Django版本只能使用re_path，已经没有了url()
- re_path 和 path整体使用方式是相同的，只是第一个参数 route变为正则表达式形式的字符串了。





## 代码结构调整(临时方案)

不知道大家发现没，我们现在的代码全部写在 urls.py中，包含所有的视图函数和所有的URL匹配规则。

对于简单的项目，这样做肯定是没问题的，但是对于正规的项目肯定不能这样做。这样做的缺点是，代码混乱，逻辑不清，不易维护。

正确的做法是，把不同功能的代码拆分在不同的文件中：

- urls.py中只定义URL的匹配规则
- 新建一个views.py，在这个文件中编写各个视图函数



**urls.py**

~~~python
from django.contrib import admin
from django.urls import path, re_path

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
	
    # hello 相关的
    path('hello/abc', views.ttt),
    path('hello/<a>', views.hello, kwargs={'a': 10, 'b': 20}),
    path('hello123', views.hello123),
    
    # articles相关的
    path("articles/2023", views.special_case_2023),
    path("articles/<year>", views.year_archive),
    re_path(r"^articles/([0-9]{4})$", views.year_archive),
    re_path(r"^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$", views.month_archive),
]
~~~



**views.py** 

~~~python
from django.shortcuts import HttpResponse, redirect


def hello(request, a, b):
    print(a)  # 形参a和b的名字需要path里面kwargs中的key保持一致
    print(b)  # 因此，形参a和b的位置关系不会影响a和b的值
    return HttpResponse('hello world')


def hello123(request):
    return redirect('http://www.baidu.com')


def ttt(request):
    return HttpResponse('ttt')


def year_archive(request, year=2056):
    return HttpResponse(f'{year} 所有的文章列表')


def month_archive(request, year, month=12):
    return HttpResponse(f'{year}年{month}月所有的文章列表')


def special_case_2023(request):
    return HttpResponse('this is a special case 2023, welcome!!!')


def download_file(request, filepath):
    return HttpResponse(filepath)
~~~







## 创建一个app

上节课讲到的临时方案，其实已经可以让项目的结构清晰很多，但并不是最终的解决方案。针对这种问题，Django有它自己的解决方案。



**Django的原则是一个项目中有多个app，每个app处理一个类型的服务**。这样做的好处是职责分明，便于项目的维护和扩展。

具体做法：

**第一步：使用startapp 命令创建一个app**

~~~bash
python3 manage.py startapp hello
~~~

命令执行后，会在项目文件夹中新产生一个名字为 hello 的文件夹（也是一个包）

~~~
hello/
    __init__.py				# 空文件，标识hello是一个包
    admin.py				# admin后台相关的文件
    apps.py					# hello作为一个app可以配置的文件
    migrations/				# 记录数据库变更记录
        __init__.py
    models.py				# 使用数据库的模型文件
    tests.py				# 单元测试的文件
    views.py				# 视图文件, 定义处理请求的视图函数
~~~



**第二步：在hello/views.py中编写视图函数**

- 在hello/views.py中编写视图函数，用来响应用户的请求：`http://127.0.0.1:8000/hello`

~~~python
from django.shortcuts import HttpResponse, redirect


def hello(request, a, b):
    print(a)  # 形参a和b的名字需要path里面kwargs中的key保持一致
    print(b)  # 因此，形参a和b的位置关系不会影响a和b的值
    return HttpResponse('hello world')


def ttt(request):
    return HttpResponse('ttt')
~~~



**第三步：在mysite.urls.py中做URL分发配置**

- 在mysite.urls.py中，从hello中导入views.py，并配置path

~~~python
from django.urls import path

from hello import views as hello_views		# 导入hello下面的views文件


urlpatterns = [
    path('hello/abc', hello_views.ttt),
    path('hello/<a>', hello_views.hello, kwargs={'a': 10, 'b': 20}),
]
~~~



类似地，在创建一个app，名字可以是 articles

- articles/views.py

~~~python
from django.shortcuts import HttpResponse


def year_archive(request, year=2056):
    return HttpResponse(f'{year} 所有的文章列表')


def month_archive(request, year, month=12):
    return HttpResponse(f'{year}年{month}月所有的文章列表')


def special_case_2023(request):
    return HttpResponse('this is a special case 2023, welcome!!!')
~~~

- mysite.urls.py

~~~python
from django.contrib import admin

from django.urls import path, re_path

from articles import views as articles_views

from hello import views as hello_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('hello/abc', hello_views.ttt),
    path('hello/<a>', hello_views.hello, kwargs={'a': 10, 'b': 20}),

    path("articles/2023", articles_views.special_case_2023),
    path("articles/<year>", articles_views.year_archive),
    re_path(r"^articles/([0-9]{4})$", articles_views.year_archive),
    re_path(r"^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$", articles_views.month_archive),

]
~~~









## 路由分发

上个项目的所有路由规则（真实项目可能有成百上千条）都定义在 mysite.urls.py中肯定是不合适的，此时可以使用Django提供的路由分发解决这个问题。



**Django路由分发的方式**：

- 第1步：每个app内新建一个 urls.py 文件，在其中定义这个app专有的URL匹配规则

- 第2步：在项目文件夹下的 urls.py中使用 include 转发



**具体demo**

- 第1步：在hello中新建一个 urls.py 文件，里面定义该应用的所有路由规则（写法和项目的urls.py是一样的）

~~~python
from django.urls import path

from . import views


# app中的每个路由匹配规则，不需要定义重复的前缀，比如：这里就不需要写 hello/abc, 直接写 abc即可
# 因为会在项目的 urls.py中统一定义前缀 hello
urlpatterns = [
    path('abc', views.ttt),
    path('<a>', views.hello, kwargs={'a': 10, 'b': 20}),
]
~~~

- 第2步：在articles中也新建一个 urls.py 文件，定义自己的路由规则。如果有多个应用，依次类推。

~~~python
from django.urls import path, re_path

from . import views


urlpatterns = [
    path("2023", views.special_case_2023),
    path("<year>", views.year_archive),
    re_path(r"^([0-9]{4})$", views.year_archive),
    re_path(r"^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$", views.month_archive),

]
~~~



- 第3步：在项目文件夹， mysite.urls.py 中做路由分发

~~~python
from django.contrib import admin

from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('hello/', include('hello.urls')),			# 注意这里不需要漏了hello后面的 /
    path('articles/', include('articles.urls')),
]
~~~



**注意**：

- 在项目的urls.py中，依然按照需求使用 re_path或者path，区别是 第二个参数使用了 include()，里面是字符串形式的分发命令。

    ~~~
    # 比如：
    	path("app01/", include("app01.urls")), 
    
    # 表示：
    	以 "app01/"开头的URL分发给 app01.urls.py中的路由规则继续向下匹配。
    ~~~

- 向下匹配时，URL的前缀会去掉后，再交给下一级做URL匹配，因此下一层就不需要重复定义前缀了。

- 理论上可以无限套娃（实际项目常用的是2-3层）







## 路由层总结

- 两个路由匹配函数：path()、re_path()，区别是他们的第一个参数是否支持正则表达式

- path()，可以使用路径转换器，默认提供5个路径转换器，转换器中定义的参数名需要和视图函数中的位置参数名保持一致。

- re_path()，存在有名分组和无名分组，有名分组时参数名需要和视图函数总的位置参数名保持一致，分明分组时不需要。

- 路由冲突。解决办法。

- 在项目中创建多个app，一个app处理一个类型的任务。

    ~~~bash
    python3 manage.py startapp hello
    ~~~

- 路由分发使用 include()。如：path("hello/", include("hello.urls"))

- **非常重要：路由匹配时按照 urlpatterns 中定义的顺序从上往下，只要匹配到一个，就立即执行对应的视图函数，并把request对象作为第一个位置参数，如果有其他参数，依次传递给视图函数。**









## 扩展1：URL上关于/的疑问



**疑问1：如果想在浏览器上访问：`http:127.0.0.1:8000/`，django如何设计路由匹配规则**

- 这种情况下 path函数的第一个参数是空字符串即可（注意：不能是 '/'）

~~~python
from django.contrib import admin

from django.urls import path

from django.shortcuts import HttpResponse


def index(request):
    return HttpResponse('welcome')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
]

~~~



**疑问2：有的URL上尾部带上 `/` 可以访问，为啥有的就不行**（通过两个例子说明）

**例子1：**尾部没有 `/` 。此时 你访问的URL只能是 `http://127.0.0.1:8000/blog`。因为你写的是什么，URL匹配时就认什么。

~~~python
from django.contrib import admin
from django.urls import path
from django.shortcuts import HttpResponse


def blog(request):
    return HttpResponse('blog list')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog', blog),					# 尾部无 /
]
~~~

**例子2：**尾部有 `/` ，

- 如果你访问的URL是 `http://127.0.0.1:8000/blog/`,没问题。
- 如果访问 `http://127.0.0.1:8000/blog` 也没问题。这是因为django内部默认做了重定向，让浏览器重新访问了一次 ` http://127.0.0.1:8000/blog/`
- 可以在django的settings.py中配置不允许重定向。比如 `APPEND_SLASH = False`

~~~python
from django.contrib import admin
from django.urls import path
from django.shortcuts import HttpResponse


def blog(request):
    return HttpResponse('blog list')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', blog),				# 尾部多了一个 /
]
~~~









## 扩展2：自定义路径转换器

有时，内置的路径转换器无法满足我们的需求，此时我们可以定义自己的路径转换器。

自定义路径转换器非常简单，三步走即可。



**第1步：定义**

比如，我们自定义一个解析4位数字的转换器。定义一个类，具备一个类属性 regex，两个方法：to_python, to_url

~~~python
class FourDigitConverter:
    regex = "[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%04d" % value
~~~



**第2步：注册**

使用register_converter方法注册，第一个参数是我们自定义类，第二个参数是自定义的标识符

~~~python
from django.urls import path, register_converter

register_converter(FourDigitYearConverter, "yyyy")		# 我们自己取的名字 yyyy
~~~



**第3步：使用**

在固定的格式中，使用自定义的标识符

~~~python
urlpatterns = [
    path("articles/2003/", views.special_case_2003),
    path("articles/<yyyy:year>/", views.common_year),	# 使用：<yyyy:year>
]
~~~



**完成代码**

~~~python
# urls.py

# 第一步：定义
class FourDigitConverter:
    regex = "[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return "%04d" % value
    
    

# 第2步：注册
from django.urls import path, register_converter

register_converter(FourDigitYearConverter, "yyyy")		# 我们自己取的名字 yyyy


# 第3步：使用
urlpatterns = [
    path("articles/2023", views.special_case_2023),
    path("articles/<yyyy:year>", views.year_archive),	# 使用：<yyyy:year>
]
~~~





