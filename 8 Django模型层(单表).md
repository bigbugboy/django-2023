django模型层功能：

- 与数据库打交道，使用ORM（对象关系映射）方便的实现数据的增删改查操作。







------

# ORM简介

ORM（Object Relational Mapping），对象关系映射；

- 目的：能够让一个不用 SQL 语句的小白也能够通过 Python 面向对象的代码，方便的实现数据的增删改查操作。
- 缺点：需要额外学习成本；封装程度太高，有时候 SQL 语句的效率偏低。

~~~
ORM			DB
类			表
属性		   字段
对象		   行数据
~~~



Python Web框架常见ORM

- Django orm，强大，但只能在django中使用
- sqlalchemy：https://www.sqlalchemy.org/，通用，非常流行
- peewee：http://docs.peewee-orm.com/en/latest/，通用，django风格的orm
- 等等









------

# ORM快速体验

>Django 自带的 sqlite3 数据库是轻量级的个人开发数据库，不适合实际实际项目使用。



我们以bms项目为例，在它的基础上把数据库的操作换成使用ORM的操作。



**基础配置**。让 Django 连上 MySQL（底层使用 pymysql 建立连接，）

- 在 settings.py中

~~~python
# 使用 pymysql
# Django 默认用的是 mysqldb 模块链接 MySQL，但是该模块的兼容性不好，需要手动改为用 pymysql 链接。

import pymysql
pymysql.install_as_MySQLdb()



# 使用MySQL的配置
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'book',		# 安装app【简写的方式】
]



DATABASES = {
    # 注释掉默认的sqlite配置
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    # 使用 MySQL
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'demo',	
        'USER': 'root',
        'PASSWORD': '12345',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'CHARSET': 'utf8'
     }
}
~~~



**创建模型类**

- 在book/models.py

~~~python
from django.db import models


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.FloatField()
    publish_date = models.DateField()
    publisher = models.CharField(max_length=100)
    authors = models.CharField(max_length=100)
	
    class Meta:
        # 在Meta下面使用db_table字段指定 表名
        db_table = 'book'	

~~~



**在视图函数中使用**

- 在 book/views.py

~~~python
from django.shortcuts import render, redirect

from . import models


def book_list(request):
    books = models.Book.objects.all()
    return render(request, 'list.html', {'books': books})


publishers = ['北京出版社', '南京出版社', '上海出版社']
authors = ['李白', '白居易', '杜甫', '欧阳修', '李时珍']


def book_create(request):
    if request.method == 'GET':
        return render(
        	request, 
            'create.html', 
            {'publishers': publishers, 'authors': authors}
        )

    # POST
    data = request.POST
    models.Book.objects.create(
        title=data.get('title'),
        price=data.get('price'),
        publish_date=data.get('publish_date'),
        publisher=data.get('publisher'),
        authors=','.join(data.getlist('authors'))
    )
    return redirect(to='book_list')


def book_delete(request, book_id):
    models.Book.objects.get(id=book_id).delete()
    return redirect(to='book_list')


def book_edit(request, book_id):
    if request.method == 'GET':
        book = models.Book.objects.get(id=book_id)
        return render(
            request, 
            'edit.html', 
            {'book': book, 'publishers': publishers, 'authors': authors}
        )

    # POST
    data = request.POST
    models.Book.objects.filter(id=book_id).update(
        title=data.get('title'),
        price=data.get('price'),
        publish_date=data.get('publish_date'),
        publisher=data.get('publisher'),
        authors=','.join(data.getlist('authors')),
    )
    return redirect(to='book_list')
~~~









------

# 创建模型类

创建模型类之前需要配置好使用哪个数据库。

**指定数据库**。使用ORM需要在配置文件中指定使用哪个库

~~~python

DATABASES = {
    # 注释掉默认的sqlite配置
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    # 使用 MySQL
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'app08',	# 在mysql中自己预先创建好数据库app08
        'USER': 'root',
        'PASSWORD': '12345',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'CHARSET': 'utf8'
     }
}
~~~



**创建模型类**

在 Django 中创建模型类非常简单（Django 内部做了很多工作，使用者只需要简单调用即可），使用的时候只需要继承模型基类，然后定义字段即可。这部分代码写在每个应用下面的 models.py 文件内。

~~~python
from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    birthday = models.DateField()
~~~

其中，

- 模型类都要继承 models.Model
- 类下面的每个字段都对应数据库中的表字段及其字段类型、约束条件等





**数据库迁移**

Django支持通过模型类生成数据库表，只需要执行如下两个命令即可

- 在终端执行如下两条命令

~~~bash
python3 manage.py makemigrations 		-- 将操作记录先保存起来(migrations文件夹)

python3 manage.py migrate  				-- 真正的操作数据库，新建表结构
~~~

- 执行了上述两条命令，就可以在数据库中看到多了一张表。Django默认帮我们创建的表的表名格式为："app名字_模型类名小写"。

~~~mysql
mysql> desc app08_user;
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| id       | int          | NO   | PRI | NULL    | auto_increment |
| username | varchar(100) | NO   |     | NULL    |                |
| password | varchar(100) | NO   |     | NULL    |                |
| age      | int          | NO   |     | NULL    |                |
| birthday | date         | NO   |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
5 rows in set (0.00 sec)
~~~

- 自定义表名。

~~~python
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    birthday = models.DateField()
    
    class META:
        db_table = 'user'		# 使用 db_table的值是什么，新建的表明就是什么
~~~



- **变更表结构**。只要表结构发生了变化，都可以通过上面的两条命令再次同步更新到数据库。

~~~bash
python3 manage.py makemigrations	# 操作一次就会在migrations中多一个迁移记录
python3 manage.py migrate  	
~~~



**三种情况**

- 1 如果数据库中没有表，想要使用 ORM 操作这张表，就需要定义模型类，然后使用迁移命令在数据库中创建表，然后再使用。
- 2 如果数据库中有这张表，想要使用 ORM 操作这张表，需要定义模型类，无需使用迁移命令创建表（因为数据库中已经有了）。
- 3 如果数据库中有表，不想使用 ORM 操作这张表，那无需定义模型类、无需使用迁移命令。











------

# 常用字段

**AutoField**

- int自增列，必须填入参数 `primary_key=True`。
- 当model中如果没有自增列，则自动会创建一个列名为id的列。



**BigAutoField**

- BigAutoField 继承自 AutoField

- bigint自增列，必须填入参数 `primary_key=True`



**IntegerField**

- 一个整数类型,范围在 -2147483648 to 2147483647



**BigIntegerField**

- 长整型(有符号的) -9223372036854775808 ～ 9223372036854775807



**SmallIntegerField**

- 小整数 -32768 ～ 32767



**PositiveSmallIntegerField**

- 正小整数 0 ～ 32767



**BooleanField**

- 布尔值类型



**FloatField**

- 浮点型



**DecimalField**

- 10进制小数
- 参数： `max_digits` 小数总长度，`decimal_places` 小数位长度





**CharField**

- 字符类型，必须提供 `max_length` 参数， 表示字符最大长度。



**TextField**

- 文本类型



**BinaryField**

- 二进制类型



**DateTimeField**

- 日期时间字段，格式 YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]，相当于Python中的datetime.datetime()实例
- 配置 `auto_now_add=True`，创建数据记录的时候会把当前时间添加到数据库。
- 配置上 `auto_now=True`，每次更新数据记录的时候会更新该字段。



**DateField**

- 日期字段，日期格式 YYYY-MM-DD，相当于Python中的datetime.date()实例。



**TimeField**

- 时间格式      HH:MM[:ss[.uuuuuu]]



EmailField(CharField)：

   - 字符串类型，Django Admin以及ModelForm中提供验证机制



IPAddressField(Field)

- 字符串类型，Django Admin以及ModelForm中提供验证 IPV4 机制



URLField(CharField)

- 字符串类型，Django Admin以及ModelForm中提供验证 URL



UUIDField(Field)

- 字符串类型，Django Admin以及ModelForm中提供对UUID格式的验证



> 当然了，Django ORM 也支持自定义字段，初学者暂时用不到。



**对应关系（部分）**

```
'AutoField': 'integer AUTO_INCREMENT',
'BigAutoField': 'bigint AUTO_INCREMENT',
'BinaryField': 'longblob',
'BooleanField': 'bool',
'CharField': 'varchar(%(max_length)s)',
'CommaSeparatedIntegerField': 'varchar(%(max_length)s)',
'DateField': 'date',
'DateTimeField': 'datetime',
'DecimalField': 'numeric(%(max_digits)s, %(decimal_places)s)',
'DurationField': 'bigint',
'FileField': 'varchar(%(max_length)s)',
'FilePathField': 'varchar(%(max_length)s)',
'FloatField': 'double precision',
'IntegerField': 'integer',
'BigIntegerField': 'bigint',
'IPAddressField': 'char(15)',
'GenericIPAddressField': 'char(39)',
'NullBooleanField': 'bool',
'OneToOneField': 'integer',
'PositiveIntegerField': 'integer UNSIGNED',
'PositiveSmallIntegerField': 'smallint UNSIGNED',
'SlugField': 'varchar(%(max_length)s)',
'SmallIntegerField': 'smallint',
'TextField': 'longtext',
'TimeField': 'time',
'UUIDField': 'char(32)',
```



**其他ORM字段参数（部分）**

```
null                数据库中字段是否可以为空
db_column           数据库中字段的列名
default             数据库中字段的默认值
primary_key         数据库中字段是否为主键
db_index            数据库中字段是否可以建立索引
unique              数据库中字段是否可以建立唯一索引
unique_for_date     数据库中字段【日期】部分是否可以建立唯一索引
unique_for_month    数据库中字段【月】部分是否可以建立唯一索引
unique_for_year     数据库中字段【年】部分是否可以建立唯一索引

verbose_name        Admin中显示的字段名称
blank               Admin中是否允许用户输入为空
editable            Admin中是否可以编辑
help_text           Admin中该字段的提示信息
```









------

# ORM查询数据

**查询所有数据** 

~~~python
from . import models

def user_list(request):
    # 返回的是 QuerySet对象
    users = models.User.objects.all()	
    print(users)
    return Httpresponse('ok')
~~~



**查询满足条件的数据**

~~~python
from . import models

def user_list(request):
    # 返回的是 QuerySet对象
    users = models.User.objects.filter(age=18)
    print(users)
    return Httpresponse('ok')
~~~



**查询满足条件的第一条数据**

~~~python
from . import models

def user_list(request):
    # 则链式调用first()
    users = models.User.objects.filter(age=18).first()
    print(users)
    return Httpresponse('ok')
~~~



**查询满足条件的只有一条数据**

- **查询满足条件的唯一一条数据，结果不存在或有多个结果，都会报错**。

~~~python

from . import models

def user_list(request):
    u = models.User.objects.get(id=3)
    print(u)
    return Httpresponse('ok')
~~~



**扩展：让打印的User对象或者 QuerySet 对象可读**

- 增加魔法方法 `__str__`。这样再打印User对象或者 QuerySet 对象时就比较可读了。

~~~python
from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    birthday = models.DateField()
    
    def __str__(self):
        return f'id: {self.id}, username: {self.username}, age: {self.age}'

~~~







------

# ORM增加数据

**使用 create()** 在数据库中插入一行数据，并返回一个模型类的实例对象

~~~python
from . import models

def create_user(request):
    u = models.User.objects.create(
        username='xliu',
        password='12345',
        age=18,
        birthday='2023-11-20'
    )
    print(u)
    return Httpresponse('OK')
~~~



**使用 save()** 先实例化一个对象，然后调用对象的save方法把数据保存在数据库中

~~~python
from . import models

def save_user(request):
    user_obj = models.User(
        username='liuxu', 
        password='12345',
        birthday = '2023-11-20'
    )
    user_obj.age = 20
    user_obj.save()
    
    return Httpresponse('OK')
~~~

- 对于日期/时间字段也可以使用Python中的 datetime 模块

~~~python
from datetime import datetime
from . import models

def save_user(request):
    user_obj = models.User(
        username='liuxu', 
        password='12345',
        birthday = datetime.now()
    )
    user_obj.age = 20
    user_obj.save()
    
    return Httpresponse('OK')
~~~



**使用 bulk_create() 批量增加** 

- 先生成一堆对象，存在列表中，再将列表中的对象一次性插入到数据库中，避免多次与数据库打交道，减少数据库的时间操作。

~~~python
from datetime import datetime
from . import models

def bulk_create_user(request):
    users = []
    for i in range(100):
        obj = models.User(
            username=f'liuxu{i}', 
            password='12345',
            age=20,
            birthday='2002-11-20'
        )
        users.append(obj)
    
	models.User.objects.bulk_create(users)	# bulk_create一次性插入
    return Httpresponse('OK')
~~~









------

# ORM删除数据

**删除满足条件的数据**。==切记：先查找再删除==

- delete 默认是批量删除（只要满足条件的记录都会被删除）

~~~python
from . import models

def delete_user(request):
    res = models.User.objects.filter(age=18).delete()
    print(res)	# res是该删除操作影响的条数信息
    return Httpresponse('ok')
~~~



**使用对象的delete**

~~~python
from . import models

def delete_user(request, user_id):
    obj = models.User.objects.filter(age=18).first()
    obj.delete()
    
    # obj = models.User.objects.filter(id=2)
    # obj.delete()
    return Httpresponse('ok')
~~~



**全部删除**（慎用）

~~~python
from . import models

def delete_user(request):
    models.User.objects.delete()	# 全部删除！！！
    return Httpresponse('ok')
~~~











------

# ORM修改数据

**使用 update()** 更新数据。原则：先查找再更新

- update默认是批量更新，只要是满足filter条件的数据都会被更新。

~~~python
from . import models

def update_user(request):
    models.User.objects.filter(pk=2).update(username='LLLLL')
    return Httpresponse('ok')
~~~





**使用save() 更新数据**

~~~python
from . import models

def update_user(request):
    obj = models.User.objects.get(pk=2)
    obj.username = 'XUUUUU'		# 此处是修改属性，再保存
    obj.save()
    return Httpresponse('ok')
~~~











------

# objects自动补全的配置方法

在pycharm编辑器中，使用ORM时，模型类对象下面没有自动补全 objects及其下面可以使用的方法（很难受）。这是因为 Django 模型基类中特殊语法定义导致的。不过没关系，我可能可以通过类型提示的知识来解决这个问题。



**使用类型提示**

~~~python
from django.db import models


class User(models.Model):
    objects: models.query.QuerySet	# 有了这行代码，我们在视图函数中就可以开心的自动补全了

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    birthday = models.DateField()

    def __str__(self):
        return f'id: {self.id}, username: {self.username}, age: {self.age}'

~~~

> 提示：这样做的好处只是在编写代码时有自动补全，不会有其他额外功能。





扩展：为什么模型类可以使用 objects。这要看源码

~~~python
# 打印看看 objects 到底是什么类型
print(type(models.User.objects))		
# <class 'django.db.models.manager.Manager'>


# 查看源码 Manager
class Manager(BaseManager.from_queryset(QuerySet)):
    pass


# 其中 QuerySet 是一个类，它下面有我们使用的方法
# from_queryset是一个特殊的方法，它会返回一个通过type定义的类
class BaseManager
    @classmethod
    def from_queryset(cls, queryset_class, class_name=None):
        if class_name is None:
            class_name = "%sFrom%s" % (cls.__name__, queryset_class.__name__)
            return type(
                class_name,
                (cls,),
                {
                    "_queryset_class": queryset_class,
                    **cls._get_queryset_methods(queryset_class),
                },
            )
~~~











------

# QuerySet对象

QuerySet是一种类似列表一样的，可循环遍历、可索引切片；

一个QuerySet对象可以包含一个或多个元素，通常每个元素都是一个Model 类实例对象，也有特殊的QuerySet（列表包含字典、列表包含元组）。

```python
queryset = models.User.objects.all() 	# 返回值是一个QuerySet对象
print(queryset) # <QuerySet [<User: id: 1, username: xliu, age: 18>, <User: id: 2, username: liuxu, age: 20>, <User: id: 3, username: liuxu2, age: 20>]>

# 打印出来这个效果是因为在 User下面定义了魔法方法 __str__


res = models.User.objects.values('username', 'age')
# res = <QuerySet [{'username': 'xliu', 'age': 18}, {'username': 'liuxu', 'age': 20}, {'username': 'liuxu2', 'age': 20}]>


res2 = models.User.objects.values_list('username', 'age')
# res2 = <QuerySet [('xliu', 18), ('liuxu', 20), ('liuxu2', 20)]>
```

- **QuerySet特性之可切片和索引**

~~~python
res3 = models.User.objects.all()[:2]	# 前两个
# res3 = <QuerySet [<User: id: 1, username: xliu, age: 18>, <User: id: 2, username: liuxu, age: 20>]>

res3 = models.User.objects.all()[2]	# 第两个
# res3=<User: id: 3, username: liuxu2, age: 20>
~~~

>提示：切片使用的值不支持负数



- **QuerySet特性之可迭代**

~~~python
res4 = models.User.objects.all()
for u in res4:
    print(u)
    

# 打印结果
id: 1, username: xliu, age: 18
id: 2, username: liuxu, age: 20
id: 3, username: liuxu2, age: 20
~~~



- **QuerySet支持链式操作**

~~~python
res5 = models.User.objects.all().filter(age=18).filter(username='liuxu')
print(res)	# <QuerySet []>
~~~



**QuerySet对象可以使用13个API**

- 下一小节详细讲解













------

# 13条基本方法(上)

**all()**：获取所有数据，返回QuerySet对象

```python
res = models.User.objects.all()
```

**filter()**：获取满足条件的数据，返回QuerySet对象

```python
res1 = models.User.objects.filter(age=18)

# 可以同时使用多个条件, and 的关系
res2 = models.User.objects.filter(age=18, username='liuxu')

# 也可以filter再filter
res2 = models.User.objects.filter(age=18).filter(username='liuxu')
```

**get()**：获取具体数据对象，数据不存在报错，存在多个结果也报错

```python
res = models.User.objects.get(pk=1)
# res = User object
```

**first()**：获取QuerySet对象中的第一个数据

```python
res = models.User.objects.all().first()
# res = User object
```

**last()**：获取QuerySet对象中的最后一个数据

**values()**：获取指定字段，返回QuerySet对象

```python
res = models.User.objects.values('username', 'age')
# res = <QuerySet [{'username': 'xliu', 'age': 19}, {'username': 'liuxu', 'age': 20}]>

# 补充：作用类似SQL语句select name, age from user
```

**values_list()**：获取指定字段，返回QuerySet对象

```python
res = models.User.objects.values_list('username', 'age')
# res = <QuerySet [('xliu', 18), ('liuxu', 20), ('liuxu2', 20)]>

# 补充：列表套元祖的对象
```



**总结：**

- **返回值是QuerySet的方法：all、filter、values、values_list**
- **返回值是模型类对象的方法：get、first、last**









------

# 13条基本方法(下)

**distinct()**：去重（注意排除`pk`后再去重），返回QuerySet对象

```python
res = models.User.objects.values('age').distinct()
# res = <QuerySet [{'age': 18}, {'age': 20}]>
```

**order_by()**：排序（默认升序排序，降序在字段前加`-`），返回QuerySet对象

```python
res = models.User.objects.values_list('age').order_by('age')

# 降序
res = models.User.objects.values_list('age').order_by('-age')
```

**reverse()**：反转，前提是已经排序过，否则没有效果，返回QuerySet对象

```python
res = models.User.objects.values_list('age').order_by('age').reverse()
# res <QuerySet [(20,), (19,)]>

# 可以理解为，升序或降序的另一种方式
```

**count()**：统计个数，返回数字

```python
res = models.User.objects.count()
# res = 2
```

**exclude()**：排除不满足条件字段，返回QuerySet对象

```python
res = models.User.objects.values_list('username')
# res=<QuerySet [('xliu',), ('liuxu',), ('liuxu2',)]>

res = models.User.objects.values_list('username').exclude(username='xliu')
# res = <QuerySet [('liuxu',), ('liuxu2',)]>
```

>filter内是不是不能使用不等于的判断方式？遇到这种需求是使用exclude



**exists()**：判断是否有对象，返回布尔值

```python
res = res = models.User.objects.filter(pk=1212).exists()
# True
```



**总结：**

- **返回值是QuerySet的方法：distinct、order_by、reverse、exclude**
- **返回值是数字的方法：count**
- **返回值是布尔值的方法：exists**











# 双下划线查询方法

双下划线方法可以在 `filter()` 里面实现神奇的操作，灵活地实现数据的过滤查询操作。

**基本语法**

```python
filter(字段名__方法)
```

**常用双下划线方法**

```python
filter(age__gt=35)		# 过滤年龄 > 35的
filter(age__lt=35)		# 过滤年龄 < 35的

filter(age__gte=35)		# 过滤年龄 >= 35
filter(age__lte=35)		# 过滤年龄 <= 35

filter(age__in=[18,35,50])		# 年龄是这三个之中一个的
filter(age__range=[18, 50]		# 年龄在18-50之间的，包括首尾
       
filter(username__contains='s')		# 名字包含's'的，区分大小写
filter(username__icontains='s')		# 名字包含's'的，不区分大小写
       
filter(username__startswith='s')	# 名字以's'开头的
filter(username__endswith='s')		# 名字以's'结尾的
       
filter(username__isnull=False)		# name字段不能为空的

filter(birthday__year='2020')	# 出生日期是2020年的
filter(birthday__month='5')	    # 出生日期是5月的
filter(birthday__day='21')		# 出生日期是21日的
```











------

# F查询

>准备表结构
>
>~~~python
>class Apple(models.Model):
>    name = models.CharField(max_length=50, default='苹果')
>    cost_price = models.DecimalField(max_digits=10, decimal_places=2)	# 成本价
>    selling_price = models.DecimalField(max_digits=10, decimal_places=2)	# 售价
>~~~



F查询可以获得表中某个字段的数据值，尤其适合表中两个字段之间的比较运算。

~~~python
from django.db.models import F

# 1.查询售价低于成本价的苹果
res = models.Apple.objects.filter(cost_price__lt=F('selling_price'))

# 2. 查询售价高于等于10倍成本价的苹果
res = models.Apple.objects.filter(selling_price__gte=F('cost_price') * 10)
~~~



F方法也能实现将值在原来值的基础做修改

~~~python
# 将所有苹果的售价提高9.9
models.Apple.objects.update(selling_price=F('selling_price') + 9.9)
~~~



但在操作字符类型的数据时，F不能直接做字符串的拼接，需要借助`Concat、Value`

```python
from django.db.models.functions import Concat
from django.db.models import F, Value


# 3.将所有苹果名字后面加上爆款两个字
 models.Apple.objects.update(name=Concat(F('name'), Value('爆款')))
```









------

# Q查询

- 多个条件筛选过滤时，`filter()`采用逻辑与的操作；设置逻辑或或者逻辑非则要借助Q查询
- Q()将条件包起来，多个Q直接用逗号 `,` 隔开默认依然是逻辑与的关系。

~~~python
import django.db.models import Q

# 1.查询卖出数大于100或者价格小于600的书籍

res = models.Apple.objects.filter(Q(maichu__gt=100), Q(price__lt=600))  
~~~



- 管道符`|`分割是逻辑或的操作，波浪号`~`分割是逻辑非的操作。

```python
from django.db.models import Q

# 查询成本价小于10元，并且 销售价大于20元的苹果（逗号分割，还是and关系）
res = models.Apple.objects.filter(Q(cost_price__lt=10), Q(selling_price__gt=20))  


# | or关系
# 查询成本价小于10元，或者 销售价大于20元的苹果
res = models.Apple.objects.filter(Q(cost_price__lt=10)|Q(selling_price__gt=20))  


# ~ not关系
res = models.Apple.objects.filter(~Q(cost_price__lt=10)|Q(selling_price__gt=20))  
```





**Q的高级用法**：查询条件的左边也可以是字符串的形式（了解）

```python
q = Q()					# 实例化Q对象
q.connector = 'or'				# 修改连接关系
q.children.append(('cost_price__lt', 10))		# 字符串的查询条件
q.children.append(('selling_price__gt', 20))

res = models.Apple.objects.filter(q)  		# filter内支持传q对象
print(res)
```









------

# 打印ORM语句背后的原生SQL

**方式1 query 属性**

~~~python
res = models.User.objects.filter(pk=1)
print(res.query)
# SELECT `app01_user`.`id`, `app01_user`.`username`, `app01_user`.`password`, `app01_user`.`age`, `app01_user`.`birthday` FROM `app01_user` WHERE `app01_user`.`id` = 1

res = models.User.objects.values_list('username')
print(res.query)	
# SELECT `app01_user`.`username` FROM `app01_user`


res = models.Apple.objects.filter(Q(cost_price__lt=10)|Q(selling_price__gt=20))
print(res.query)
# SELECT `app01_apple`.`id`, `app01_apple`.`name`, `app01_apple`.`cost_price`, `app01_apple`.`selling_price` FROM `app01_apple` WHERE (`app01_apple`.`cost_price` < 10 OR `app01_apple`.`selling_price` > 20)
~~~



**方式2 配置文件中全局配置**

- 去配置文件settngs.py中配置一下即可，在终端会自动以日志的形式打印ORM背后执行的SQL

~~~python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}
~~~









# 查询优化之only & defer

**惰性查询**

orm查询是惰性查询，当需要数据时才真正的到数据库取数据。仅仅一个查询语句是不会去数据库的，用到这个数据时才去数据库，比如打印操作时再去数据库。

```python
res = models.User.objects.all()		# 此时不执行语句
print(res)				# 使用结果时才不得不去数据库查询数据
```

并且，拿到查询结果后，后续再使用这个结果时不会再访问数据库。

~~~python
res = models.User.objects.filter(pk=1).first()
print(res)
print(111111)
for u in res:
    print(u.usenrame)		# 此时不会再访问数据库
~~~



**only 优化**

`only()`方法则不同，`only()`方法内可以指定查询的字段，返回的结果中再使用`only`括号内的字段时不会再去数据库，使用其他的字段则再去数据库。

~~~python
res = models.User.objects.filter(pk=1).only('username').first()
print(res.username)		# 查询数据库
print(111111)
print(res.username)		# 不会查询数据库
print(111111)
print(res.age)			# 再次查询数据库
~~~

>**补充**：only 括号内可以传入多个字段，用逗号隔开。



**defer 优化**

`defer()`方法和`only()`方法用法一样，但是查询的方式却完全相反。返回的结果中再使用`defer`括号内的字段时需要再去数据库，而使用其他的字段则无需去数据库。

~~~python
res = models.User.objects.filter(pk=1).defer('birthday').first()
print(res.username)		# 查询数据库
print(111111)
print(res.username)		    # 不会查询数据库
print(res.age)		    	# 不会查询数据库
print(111111)
print(res.birthday)	 		# 再次查询数据库
~~~

>**补充**：defer 括号内可以传入多个字段，用逗号隔开。









# 执行原生SQL

Django ORM非常好用，但有时我们也希望能够执行原生的SQL语句，此时ORM也是支持的。



**raw() 完全执行原生SQL**

```python
sql = 'SELECT * FROM app01_user where id=%s'	# 注意是 app01_user
res = models.User.objects.raw(sql, [1])			# 此时也不会访问数据库

# 需要具体结果时才会访问数据库获取数据，并将结果封装为Django模型对象或字典对象。
for result in res:
    print(result)
```



**extra() 查询中添加额外的SQL语句片段**

~~~python
# 查询年龄大于平均年龄的用户
res = models.User.objects.extra(where=['age > (SELECT AVG(age) FROM app01_user)'])
print(res)


# 在查询结果中添加额外的字段
res = models.User.objects.extra(select={'nickname': 'UPPER("username")'})
for u in res:
    print(u.username, u.nickname)
~~~











# 两个聪明的方法

**get_or_create**

>~~~python
>def get_or_create(self, defaults=None, **kwargs):
>    """
>    Look up an object with the given kwargs, creating one if necessary.
>    Return a tuple of (object, created), where created is a boolean
>    specifying whether an object was created.
>    """
>    pass
>~~~

- 在数据库中查找一个对象或创建新对象。
- 通过关键字参数`**kwargs`指定查询条件来查找现有对象。
- `defaults`参数，是一个字典，包含要创建的字段和对应的值

~~~python
u, created = models.User.objects.get_or_create(
    username='jack',
    defaults={
        'age': 18,
        'password': '123456789',
        'birthday': '2023-12-10'
    }		# defaults中的字段用于新建时的默认值
)
print(u, created)

"""

- 根据指定条件查找一个对象，如果找到多个则报错（底层是get方法）
- 如果找不到对象，则创建一个新对象，创建对象时需要的字段值来自defaults参数
- 返回值是一个2元组，元组的第二个参数是布尔值表示是否创建
    - 找到一个对象时，(对象, False)
    - 创建一个对象时，(对象, True)
"""
~~~

>思考：登录并注册是不是可以用这个方法？





**update_or_create**

>```python
>def update_or_create(self, defaults=None, **kwargs):
>    """
>    Look up an object with the given kwargs, updating one with defaults
>    if it exists, otherwise create a new one.
>    Return a tuple (object, created), where created is a boolean
>    specifying whether an object was created.
>    """
>    pass
>```

- 在数据库中更新现有对象或创建新对象。
- 通过关键字参数`**kwargs`指定查询条件来查找现有对象。
- `defaults`参数，是一个字典，包含要更新或创建的字段和对应的值

~~~python
u, created = models.User.objects.update_or_create(
    username='jack2',
    defaults={
        'age': 38,
        'password': '123456789',
        'birthday': '2023-12-10'
    }
)
print(u, created)		# 返回值也是2元组，同 get_or_create
~~~













# 两个404方法

Django提供了两个实用函数，用于从数据库中获取对象，如果对象不存在，则抛出404错误页面。

这两个方法不是 ORM 语句，但是底层使用的是 ORM

**get_object_or_404**

- `get_object_or_404()`函数接受两个参数：模型类和查询条件。它尝试从数据库中获取满足查询条件的对象。如果找到匹配的对象，则返回该对象；如果没有找到对象，则会抛出一个404错误页面。

~~~python
from django.shortcuts import HttpResponse, get_object_or_404


def shortcuts(request):
    obj = get_object_or_404(models.User, id=10)
    return HttpResponse(obj.username)
~~~



**get_list_or_404**

- `get_list_or_404()`函数，它接受一个模型类和查询条件作为参数。内部使用`filter()`方法从数据库中过滤对象列表，并检查列表是否为空。如果列表为空，则抛出404错误页面；如果列表不为空，则返回对象列表。

~~~python
from django.shortcuts import HttpResponse, get_list_or_404


def shortcuts(request):
    obj_list = get_list_or_404(models.User, id__gte=2)
    return HttpResponse(obj_list)
~~~









# ORM开启事务

在Django的ORM中，事务是用于执行数据库操作的一种机制，它可以确保一系列数据库操作要么全部成功执行，要么全部回滚到事务开始之前的状态，从而保持数据库的一致性。

Django的ORM默认情况下使用自动提交模式，即每个数据库操作都会立即提交到数据库。然而，有时候我们需要将多个操作放在一个事务中，以确保它们的原子性和一致性。**Django提供了两种方式来处理事务：基于函数装饰器和基于上下文管理器。**



**基于上下文**。如果在`with`块内发生任何异常，事务将会回滚，否则事务将会提交。

~~~python
from django.db import transaction
from django.shortcuts import HttpResponse


def trans(request):
    with transaction.atomic():
        models.User.objects.filter(pk=1).update(age=100)
        raise
        models.User.objects.filter(pk=2).update(age=200)

    return HttpResponse('ok')
~~~



**基于函数装饰器**。如果在函数执行期间发生任何数据库操作异常，事务将会回滚，否则事务将会提交

~~~python
from django.db import transaction
from django.shortcuts import HttpResponse


@transaction.atomic
def trans(request):
    models.User.objects.filter(pk=1).update(age=100)
    raise
    models.User.objects.filter(pk=2).update(age=200)
        
    return HttpResponse('ok')
~~~











# 补充choice

如果某个字段值的可能性是可以完全列举出来的，那么一般情况下都会采用`choices`参数。比如用户表中的：性别、学历、工作经验、是否婚配等。

使用它的目的有两点：数据库保存数据方便；数据标识性强，便于展示。

~~~python
class User(models.Model):
    objects: models.query.QuerySet

    SEX = [
        ('0', '男'),
        ('1', '女'),
        ('2', '其他'),
    ]

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    birthday = models.DateField(auto_now_add=True)			# 保存时的当前日期
    sex = models.SmallIntegerField(default=0, choices=SEX)	# choices

    def __str__(self):
        return f'id: {self.id}, username: {self.username}, age: {self.age}'
~~~

**使用`choices`参数需要注意点：**

- 由二元组组成的一个可迭代对象（例如，列表或元组），用来给字段提供选择项。



**存取demo**

~~~python
from app01 import models

# 存
models.User.objects.create(username='刘旭', age=18, sex=0)
models.User.objects.create(username='女老师', age=18, sex=1)
models.User.objects.create(username='另一个老师', age=18, sex=4)

# 取
user_obj = models.User.objects.filter(username='刘旭').first()
print(user_obj.sex)		# 0
print(user_obj.get_sex_display())	# 男

user_obj = models.User.objects.filter(username='另一个老师').first()
print(user_obj.get_sex_display())  # 4
~~~

- 存数据按照字段的数据类型，可以存列举之外的值（只要值的类型满足即可）。
- 取数据时，如果当初存的数据在元祖第一个元素列举的范围内，则很容易取出第二个描述信息；如果当时存的不在那个范围内，则直接取出数据库中存的数据。
- 取数据的方式的固定写法：`get_字段名_display()`



扩展了解：Django3.1以后版本出现 IntegerChoices

~~~python
class User(models.Model):
    objects: models.query.QuerySet

    class SexChoices(models.IntegerChoices):	# 定义
        MALE = 0, '男'
        FEMALE = 1, '女'
        OTHER = 2, '其他'

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    birthday = models.DateField(auto_now_add=True)
    sex = models.SmallIntegerField(default=0, choices=SexChoices.choices)	# 配置

    def __str__(self):
        return f'id: {self.id}, username: {self.username}, age: {self.age}'
    
    
  

# views.py
# 存 可以更加清爽
models.User.objects.create(
	username='刘旭2', age=18, sex=models.User.SexChoices.MALE.value
)

# 取 和传统的方式一致
user_obj = models.User.objects.filter(username='刘旭').first()
print(user_obj.sex)		# 0
print(user_obj.get_sex_display())	# 男
~~~







# Django shell命令

Django提供了一个命令行工具称为"Django shell"，它允许你在交互式环境中与你的Django应用程序进行交互。通过Django shell，你可以执行数据库查询、操作模型对象以及运行其他与Django相关的任务。

要打开Django shell，可以在终端中进入你的Django项目的根目录，并运行以下命令：

```
python manage.py shell
```

这将启动Django shell，并显示一个Python交互式解释器，你可以在其中输入Python代码并与你的Django应用程序进行交互。

**查询数据库对象**

```python
>>> from app01 import models
>>> res = models.User.objects.all()
>>> res
<QuerySet [<User: id: 1, username: xliu, age: 100>, <User: id: 2, username: liuxu, age: 20>, <User: id: 3, username: liuxu2, age: 20>, <User: id: 4, username: xliu, age: 18>, <User: id: 6, username: jack, age: 18>, <User: id: 7, username: jack2, age: 38>, <User: id: 8, username: mack, age: 19>, <User: id: 9, username: mack, age: 19>, <User: id: 10, username: mack, age: 19>, <User: id: 14, username: 刘旭, age: 18>, <User: id: 15, userne: 女老师, age: 18>, <User: id: 16, username: 另一个老师, age: 18>, <User: id: 17, username: 刘旭2, age: 18>]>
>>> 

```

**创建和保存对象**

```python
>>> u = models.User(username='haha', password='11111', age=28)
>>> u.save()
>>> u = models.User.objects.get(username='haha')
>>> u
<User: id: 18, username: haha, age: 28>
>>> 
```

**更新对象**

```python
>>> u.age = 35
>>> u.save()
>>> 
```

**删除对象**

```python
>>> models.User.objects.filter(pk=10).delete()
(1, {'app01.User': 1})
>>> 
```



这只是一些Django shell的常见用法示例，你可以在Django shell中执行任意的Python代码和Django ORM操作。

在交互式环境中使用Django shell可以方便地测试和调试你的代码，以及执行各种与数据库和模型相关的任务。





