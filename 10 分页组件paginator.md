# 10 分页组件paginator



分页的必要性：

- 网页上无法展示所有数据，只能展示部分数据
- 避免在网络请求中传输大量的数据，按需请求数据





## 手动实现分页

- offset和limit 此时需要执行原生SQL语句

~~~python
def book_list(request):
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))

    sql = 'select * from book limit %s offset %s'
    books = models.Book.objects.raw(sql, [size, (page - 1) * size])
    return render(request, 'list.html', {'books': books})
~~~

> 浏览器访问：http://127.0.0.1:8000/book/list?page=1&size=10，其中：
>
> - page 表示页数
> - size 表示每页展示数据的条数



- QuerySet的切片操作

~~~python
def book_list(request):
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))

    books = models.Book.objects.all()[(page - 1) * size: page * size]
    return render(request, 'list.html', {'books': books})
~~~



**注意**：

- 手动处理分页需要自己校验参数的合法性







## 使用paginator实现分页

- 参考官方文档：https://docs.djangoproject.com/zh-hans/4.2/topics/pagination/

**基本使用**

~~~python
from django.core.paginator import Paginator


def book_list(request):
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))

    all_books = models.Book.objects.all()
    paginator = Paginator(all_books, size)
    books = paginator.get_page(page)
    return render(request, 'list.html', {'books': books})
~~~



**HTML页面配置**（默认size=1）

~~~html
<div class="pagination">
    <span class="step-links">
        {% if books.has_previous %}
            <a href="?page=1">&laquo; first</a>
            <a href="?page={{ books.previous_page_number }}">previous</a>
        {% endif %}

        <span class="current">
            Page {{ books.number }} of {{ books.paginator.num_pages }}.
        </span>

        {% if books.has_next %}
            <a href="?page={{ books.next_page_number }}">next</a>
            <a href="?page={{ books.paginator.num_pages }}">last &raquo;</a>
        {% endif %}
    </span>
</div>
~~~









## 集成bootstrap的分页组件

- 参考官网：https://v3.bootcss.com/components/#pagination



视图函数

~~~python
from django.core.paginator import Paginator


def book_list(request):
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))

    all_books = models.Book.objects.all()
    paginator = Paginator(all_books, size)
    books = paginator.get_page(page)
    return render(request, 'list.html', {'books': books})
~~~

模板文件

~~~html
<!--集成bootstrap的分页样式-->
<nav aria-label="Page navigation">
    <ul class="pagination">
        {% if books.has_previous %}
        <li>
            <a href="?page={{ books.previous_page_number }}" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
            </a>
        </li>
        {% else %}
        <li class="disabled">
            <a href="#" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
            </a>
        </li>
        {% endif %}
        
        {% for p in books.paginator.page_range %}
        {% if p == books.number %}
        <li class="active"><a href="?page={{ p }}">{{ p }}</a></li>
        {% else %}
        <li><a href="?page={{ p }}">{{ p }}</a></li>
        {% endif %}
        {% endfor %}

        {% if books.has_next %}
        <li>
            <a href="?page={{ books.next_page_number }}" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
            </a>
        </li>
        {% else %}
        <li class="disabled">
            <a href="#" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
            </a>
        </li>
        {% endif %}

    </ul>
</nav>
~~~

