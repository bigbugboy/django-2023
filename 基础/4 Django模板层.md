# 4 Django模板层

django模版层功能：

- 接收视图层传过来的数据，渲染到html模版文件，支持逻辑判断。
- 此外，还支持模版文件的继承和导入，减少模版文件代码的重复书写。



扩展：

- 互联网早期使用模板的方式实现网页效果的，传统的全栈开发。
- 现在，主流的方式为前后端分离，前端静态页面，后端服务，中间使用api交互数据。

- 后端开发一般都要会一点前端基础。反之也是的。





## 前端基础之HTML

HTML是超文本标记语言缩写，我们在浏览器看到的页面，内部其实都是HTML代码(所有的网站内部都是HTML代码)。

**HTML文档结构**

```html
<html>
<head></head>:head内的标签不是给用户看的 而是定义一些配置主要是给浏览器看的
<body></body>:body内的标签 写什么浏览器就渲染什么 用户就能看到什么
</html>
```

HTML代码是没有格式的，可以全部写在一行都没有问题，只不过我们习惯了缩进来表示代码



**html demo**

~~~html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>我的网页</title>
</head>
<body>
  <h1>这是一级标题</h1>
  <h2>这是二级标题</h2>
  <h3>这是三级标题</h3>
  <h4>这是四级标题</h4>
  <h5>这是五级标题</h5>
  <h6>这是六级标题</h6>
http://dev-trial4312.igx.biz/
  <p>这是一个段落。</p>

  <a href="https://www.51zxw.net">这是一个链接</a>

  <p>这是一段 <b>加粗</b> 文本。</p>
  <p>这是一段 <i>斜体</i> 文本。</p>
  <p>这是一段 <u>下划线</u> 文本。</p>
	
  <!--  可以使用本地图片-->
  <img src="https://images.pexels.com/photos/3659862/pexels-photo-3659862.jpeg" alt="图片">
    

  <ul>
    <li>列表项 1</li>
    <li>列表项 2</li>
    <li>列表项 3</li>
  </ul>

  <form action="/submit" method="post">
    <label for="name">姓名:</label>
    <input type="text" id="name" name="name" required><br>
    <label for="email">邮箱:</label>
    <input type="email" id="email" name="email" required><br>
    <input type="submit" value="提交">
  </form>

  <audio src="audio.mp3" controls></audio>

  <video src="video.mp4" controls></video>
</body>
</html>
~~~





**body内常用基本标签**

| 标签   | 描述                               | 使用示例                                                     |
| ------ | ---------------------------------- | ------------------------------------------------------------ |
| h1     | 一级标题                           | `<h1>这是一级标题</h1>`                                      |
| h2     | 二级标题                           | `<h2>这是二级标题</h2>`                                      |
| h3     | 三级标题                           | `<h3>这是三级标题</h3>`                                      |
| h4     | 四级标题                           | `<h4>这是四级标题</h4>`                                      |
| h5     | 五级标题                           | `<h5>这是五级标题</h5>`                                      |
| h6     | 六级标题                           | `<h6>这是六级标题</h6>`                                      |
| p      | 段落                               | `<p>这是一个段落。</p>`                                      |
| a      | 链接                               | `<a href="https://www.example.com">这是一个链接</a>`         |
| b      | 加粗文本                           | `<p>这是一段 <b>加粗</b> 文本。</p>`                         |
| i      | 斜体文本                           | `<p>这是一段 <i>斜体</i> 文本。</p>`                         |
| u      | 下划线文本                         | `<p>这是一段 <u>下划线</u> 文本。</p>`                       |
| img    | 图像                               | `<img src="image.jpg" alt="图片">`                           |
| ul     | 无序列表                           | `<ul> <li>列表项 1</li> <li>列表项 2</li> <li>列表项 3</li> </ul>` |
| li     | 列表项                             | `<li>列表项</li>`                                            |
| form   | 表单                               | `<form action="/submit" method="post"> ... </form>`          |
| audio  | 音频                               | `<audio src="audio.mp3" controls></audio>`                   |
| video  | 视频                               | `<video src="video.mp4" controls></video>`                   |
| br     | 换行                               | `<p>这是第一行<br>这是第二行</p>`                            |
| strong | 强调文本（加粗，语义更强）         | `<p>这是一段 <strong>强调</strong> 文本。</p>`               |
| em     | 强调文本（斜体，语义更强）         | `<p>这是一段 <em>强调</em> 文本。</p>`                       |
| code   | 行内代码                           | `<p>这是一段包含 <code>行内代码</code> 的文本。</p>`         |
| pre    | 保留文本格式（通常用于显示代码块） | `<pre> ... </pre>`                                           |
| table  | 表格                               | `<table> ... </table>`                                       |
| tr     | 表格行                             | `<tr>...</tr>`                                               |
| td     | 表格单元格                         | `<td>单元格内容</td>`                                        |
| th     | 表格表头                           | `<th>表头</th>`                                              |
| div    | 块级容器，用于组织和布局内容       | `<div>...</div>`                                             |





**HTML就是编写网页的一套标准。**

```python
# HTML的注释
<!--单行注释-->

<!--
多行注释1
多行注释2
多行注释3
-->

# 由于HTML代码非常的杂乱无章并且很多，所以我们习惯性的用注释来划定区域方便后续的查找
# 参考51自学网首页源码：view-source:https://www.51zxw.net/
<!--导航条开始-->
导航条所有的html代码
<!--导航条结束-->
<!--左侧菜单栏开始-->
左侧菜单栏的HTMl代码
<!--左侧菜单栏结束-->
```









## 前端基础之CSS(上)

CSS：层叠样式表，就是给 HTML 标签添加样式，让其更加美观。



**使用CSS的三种方式**

- **行内式。**直接在 HTML 标签内使用style属性为标签设置样式。每个样式属性都被写在双引号中，使用分号进行分隔。

~~~html
<html>
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
  <h1 style="color: blue; font-size: 24px;">这是一个标题</h1>
  <p style="color: red; font-size: 16px;">这是一个段落。</p>
  <img style="width: 400px;" src="https://images.pexels.com/photos/3659862/pexels-photo-3659862.jpeg" alt="图片">
</body>
</html>
~~~

>请注意，行内式样式对于单个元素的样式定义非常方便，但在实际开发中，使用外部样式表（external style sheet）或内部样式表（internal style sheet）更加灵活和可维护，特别是对于多个页面具有相同样式的情况。



- **内部样式表。**在 HTML 文件内使用style标签来设置样式。style标签可以在文档的任何地方，但一般在 HTML 文档的 `<head>` 标签中定义样式，以便应用于整个文档或特定的元素

~~~html
<html>
<head>
  <meta charset="UTF-8">
  <title>Document</title>
  <style>
    h1 {
      color: blue;
      font-size: 24px;
    }
    p {
      color: red;
      font-size: 16px;
    }
    img {
      width: 400px;
    }
  </style>
</head>
<body>
  <h1>这是一个标题</h1>
  <p>这是一个段落。</p>
  <img src="https://images.pexels.com/photos/3659862/pexels-photo-3659862.jpeg" alt="图片">
</body>
</html>
~~~

>通过内部样式表，我们可以在一个地方集中定义多个元素的样式，并且可以使用选择器来选择不同的元素类型、类名或其他属性，以精确地应用样式。
>
>然而，与外部样式表相比，内部样式表仍然是与 HTML 文档耦合的，对于具有大量样式需求的网站或应用程序，使用外部样式表更加推荐。



- **外部样式表。**可以将样式定义放在一个独立的 CSS 文件中，并通过 HTML 文档中的链接引用该文件

~~~html
<html>
<head>
  <meta charset="UTF-8">
  <title>Document</title>
  <link rel="stylesheet" type="text/css" href="./styles.css">
</head>
<body>
  <h1>这是一个标题</h1>
  <p>这是一个段落。</p>
  <img src="https://images.pexels.com/photos/3659862/pexels-photo-3659862.jpeg" alt="图片">
</body>
</html>
~~~

styles.css

~~~css
h1 {
    color: blue;
    font-size: 24px;
}

p {
    color: red;
    font-size: 16px;
}

img {
    width: 400px;
}
~~~

>通过这种方式，我们可以在单独的 CSS 文件中管理和组织样式定义，并在多个页面中重复使用该样式表。这种分离的方式提高了代码的可维护性和可重用性，并使样式与内容分离，提升了开发效率。





**CSS的注释**

```css
/*单行注释*/

/*
多行注释1
多行注释2
多行注释3
*/

/*
通常我们在写css样式的时候也会用注释来划定样式区域
*/
```









## 前端基础之CSS(下)

学习 CSS 很多时候在学习选择器和属性的使用。

- 选择器用于选择要应用样式的 HTML 元素，也就是确定标签位置的方法
- 属性则用于指定元素的样式



**CSS语法结构**

```css
选择器 {
  属性1:值1;
  属性2:值2;
  属性3:值3;
  属性4:值4;
}
```



常用属性展示

| 属性               | 描述               | 示例                        |
| ------------------ | ------------------ | --------------------------- |
| `color`            | 指定文字颜色       | `color: red;`               |
| `font-size`        | 指定文字大小       | `font-size: 16px;`          |
| `background-color` | 指定背景颜色       | `background-color: yellow;` |
| `width`            | 指定元素的宽度     | `width: 200px;`             |
| `height`           | 指定元素的高度     | `height: 200px;`            |
| `margin`           | 指定元素的外边距   | `margin: 10px;`             |
| `padding`          | 指定元素的内边距   | `padding: 10px;`            |
| `border`           | 指定元素的边框样式 | `border: 1px solid black;`  |





**基本选择器**

- **id选择器**，根据id值确定一个标签

    ```css
    #id_name{
        color:red;
    }
    ```

- **class选择器**，根据class值确定一类标签

    ```css
    .class_name{
        color:red;
    }
    ```

- **元素/标签选择器**，根据标签名确定一堆标签

    ```css
    span{
        color:red;
    }
    ```

- **通用选择器**，选择所有标签

    ```css
    *{
        color:red;
    }
    ```



**分组选择器**：多个选择器可以同时设置样式，选择器之间用逗号隔开。

```css
div, p, span{
    color:red;
}

#name, .animal, span{
    color:red;
}
```





**层级选择器**

- **后代选择器，空格隔开**，选择div 里面的所有span

    ```css
    div span{
        color:red;
    }
    ```

- **儿子选择器，>连接**，选择内部第一层的所有span

    ```css
    div>span{
        color:red;
    }
    ```

- **毗邻选择器，+连接**，选择div同级别的紧挨着的下面一个span，隔着一个都不行

    ```css
    div+span{
        color:red;
    }
    ```

- **弟弟选择器，~连接**，选择同级别下面所有的span

    ```css
    div~span{
        color:red;
    }
    ```



**属性选择器**：属性选择器，以`[]`作为标志。

- 含有某个属性的标签

    ```css
    [username]{  /*选择属性名含有username的标签*/
        color:red;
    }
    ```

- 含有某个属性且有某个值的标签，选择属性名为

    ```css
    [username='xliu']{	/*选择属性名含有username且名字为'xliu'的标签*/
        color:red;
    }
    ```

- 含有某个属性且有某个值的某个标签

    ```css
    input[username='xliu']{	/*选择属性名含有username且名字为'xliu'的input标签*/
        color:red;
    }
    ```



**伪类选择器**

```css
a:link{			/*a标签访问前的颜色*/
    color:red;
}
a:hover			/*鼠标悬浮在a标签上，显示的颜色*/
a:active		/*鼠标点击不松开时a标签的颜色，激活态*/
a:visited		/*访问之后a标签的颜色*/  
input:focus		/*input框获取焦点(鼠标点了input框)时的颜色
```



**伪元素选择器**

注意：before和after通常用来清除浮动带来的影响：**父标签塌陷问题**

```css
/*设置段落首字符样式*/
p:first-letter {
            font-size: 48px;
            color: orange;
        }

/*在文本开头 同css添加内容*/
p:before { 
            content: '你说的对';
            color: blue;
        }

/*在文本结尾 同css添加内容*/
p:after{
    ...
} 	
```









## 前端基础之JavaScript

JavaScript（简称 JS）在 HTML 中扮演着重要的角色，它为网页提供了交互性和动态性。以下是 JS 在 HTML 中的一些主要作用：

1. **交互性：** JavaScript 可以通过处理用户的输入和事件来实现与用户的交互，例如表单验证、响应按钮点击、处理鼠标移动等。它可以使用户与网页进行实时交互并提供动态反馈。
2. **动态内容：** JavaScript 可以通过 DOM（文档对象模型）操作 HTML 元素，实现动态更新和修改网页内容。它可以通过添加、删除或修改元素、文本和样式来实现动态内容的生成和更新。
3. **数据处理和验证：** JavaScript 可以对用户输入的数据进行处理和验证，确保数据的完整性和准确性。它可以执行表单验证、数据格式转换、计算等操作，以增强用户体验和数据的有效性。
4. **浏览器控制：** JavaScript 可以与浏览器进行交互，通过操作浏览器的对象和方法来实现对浏览器的控制。例如，打开新窗口、重定向页面、修改浏览器历史记录等。
5. **动画和效果：** JavaScript 可以使用动画库或通过直接操作元素的样式属性来创建动画效果。它可以实现平滑的过渡、淡入淡出、滚动效果等，为网页增添生动和吸引力。
6. **AJAX 和数据交互：** JavaScript 可以通过使用 AJAX（异步 JavaScript 和 XML）技术与服务器进行数据交互，实现无需刷新整个页面的数据更新。它可以通过异步请求和响应来获取、发送和处理数据，实现动态加载内容和实时更新。



补充：

- JavaScript 是一门编程语言，是脚本语言，它也可以写后端代码（node.js）。
- JavaScript 和 Java 没有关系，仅仅是当时的 JavaScript 为了蹭 Java 的热度。



**JavaScript基础语法知识**

~~~js
// 变量
var name = 'xliu'
let new_name = 'liuxu'

/*
基础数据类型：
数值类型：number
字符串类型：string
布尔型：bollean
空：null & undefined
条件、循环、函数
对象：object
*/
~~~

- 浏览器自带的控制台可以执行 JavaScript 代码



**js的注释**

```javascript
"""
// 单行注释

/*
多行注释1
多行注释2
多行注释3
*/
"""
```





**html引入js代码的两种方式**

- HTML文件内使用 <script> 标签用于嵌入 JavaScript 代码。一般会将它放在文档的最后。

~~~html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>JavaScript Demo</title>
</head>
<body>
    <h1>点击欢迎Demo</h1>
    <button onclick="greet()">点击这里</button>
    <p id="greeting"></p>


    <script>
        function greet() {
          var name = prompt("请输入您的名字：");
          var message = "欢迎，" + name + "！";
          document.getElementById("greeting").textContent = message;
        }
    </script>
</body>
</html>
~~~





- HTML文件内使用 <script> 标签引入外部 JavaScript文件（使用src属性引入）。

~~~html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>JavaScript Demo</title>

</head>
<body>
    <h1>JavaScript Demo</h1>
    <button onclick="greet()">点击这里</button>
    <p id="greeting"></p>

    <script charset="utf-8" type="text/javascript" src="./script.js"></script>
</body>
</html>
~~~

script.js

~~~js
function greet() {
    var name = prompt("请输入您的名字：");
    var message = "欢迎，" + name + "！";
    document.getElementById("greeting").textContent = message;
}
~~~

确保 HTML 文档和 `script.js` 文件在同一个目录下，浏览器中打开 HTML 文件时，页面将以外部引入的方式加载 JavaScript 文件并运行相应的代码。

这种方式使得 JavaScript 代码与 HTML 文件分离，使得代码更易于维护和管理，并提供了更好的可扩展性和重用性。







## 使用模板的场景

- 服务器直接返回 HTML 页面的开发模式。
- 多个页面的结构相同，仅数据不一样。此时没必要写多个 HTML 页面。



公司A介绍页 company_a.html

~~~html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>公司介绍</title>
</head>
<body>
  <h1>公司介绍页</h1>
  
  <div>
    <h2>公司A</h2>
    <p>公司A是一家全球领先的科技公司，专注于开发创新的软件解决方案。</p>
    <p>地址：公司A地址</p>
    <p>电话：公司A电话</p>
  </div>
</body>
</html>
~~~

公司B介绍页 company_b.html

~~~html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>公司介绍</title>
</head>
<body>
  <h1>公司介绍页</h1>
  
  <div>
    <h2>公司B</h2>
    <p>公司B是一家全球知名的制造业公司，致力于生产高品质的产品。</p>
    <p>地址：公司B地址</p>
    <p>电话：公司B电话</p>
  </div>
</body>
</html>
~~~



想让服务器提提供服务，把这两个网页展示在浏览器上。如果不使用模板的方式，以目前我们掌握的技术大概率能写出来如下解决方案。

- 设计一个路由匹配规则，动态的匹配公司名字
- 在视图函数中，按照公司名字找到对应公司的 HTML文件。读文件内容然后 HttpResponse 响应给浏览器

路由匹配 urls.py

~~~python
from django.urls import path

from . import views


urlpatterns = [
    path('company/<name>', views.test9),
]

~~~

视图函数 views.py

~~~python
 import os

from django.conf import settings
from django.shortcuts import HttpResponse


def test9(request, name):
    # 此处需要使用django项目的配置文件，从根路径找到需要的 HTML 文件
    filepath = os.path.join(settings.BASE_DIR, 'app01', f'company_{name}.html')
    with open(filepath, 'r') as f:
        return HttpResponse(f.read())
~~~







## 首次使用模板

**Demo：使用模板的解决方案**

- 项目根路径下新建文件夹 templates,（也就是和manage.py文件同级的地址） 文件夹内新建模板文件 company.html

~~~html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>公司介绍</title>
</head>
<body>
  <h1>公司介绍页</h1>

  <div>
    <h2>{{ name }}</h2>
    <p>{{ description }}</p>
    <p>地址：{{ address }}</p>
    <p>电话：{{ phone }}</p>
  </div>
</body>
</html>
~~~

- Django 配置文件 settings.py 做如下修改。`'DIRS': ['templates']`，请注意 `DIRS`中的配置的文件夹名字和上一步中新建的文件夹名字相同即可，具体叫什么名字无所谓。比如：上一步新建的文件夹名字是 'xxx'，则在配置文件中配置 'xxx' 即可。但一般我们都会使用 'templates' 这个名字。

~~~python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],	# 表示在项目哪个文件夹下查找模板文件
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
~~~

- 路由匹配 urls.py

~~~python
from django.urls import path

from . import views


urlpatterns = [
    path('company/<name>', views.test10),
]

~~~

- 视图函数 views.py

~~~python
from django.shortcuts import render


def test10(request, name):
    companys = {
        'a': {
            'name': '公司A',
            'description': '公司A是一家全球领先的科技公司，专注于开发创新的软件解决方案。',
            'address': '公司A地址',
            'phone': '公司A电话'
        },
        'b': {
            'name': '公司B',
            'description': '公司B是一家全球知名的制造业公司，致力于生产高品质的产品。',
            'address': '公司B地址',
            'phone': '公司B电话'
        }
    }
    company = companys[name]
    return render(request, 'company.html', company)
~~~







## 配置App自己的模板文件夹

在项目根路径下的 templates文件夹下统一保存所有的模板文件看起来挺好的，但是实际项目中一般多有很多个app，每个app可能都会有很多很多个模板文件，并且可能出现多个app需要使用同名的模板文件，此时templates文件夹可能就不方便使用了。



这种情况下，我们可以为每个app单独创建 一个模板文件夹。也就是说，可以在每个app分别创建一个 templates 文件夹，里面只放app自己的模板文件。这样就会清爽很多。



想要这样做，我们需要分如下三个来实现。

第一步：在某个需要使用模板的app内新建一个templates文件夹，该文件夹内放app需要的模板文件

- **注意：此时文件夹的名字只能是 'templates'，并且和配置文件中的 'DIRS' 没有关系。**

第二步：在django的配置文件settings.py中做如下配置修改。

~~~python
# INSTALLED_APPS 中注册app
    # 简写：'app01',
    # 完整写法：'app01.apps.App01Config'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01',
]

# TEMPLATES中, 'APP_DIRS': True,	表示使用app自己的模板文件夹
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
~~~

第三步：在视图函数内直接使用模板文件 app01/views.py

~~~python
def test10(request, name):
    companys = {
        'a': {
            'name': '公司A',
            'description': '公司A是一家全球领先的科技公司，专注于开发创新的软件解决方案。',
            'address': '公司A地址',
            'phone': '公司A电话'
        },
        'b': {
            'name': '公司B',
            'description': '公司B是一家全球知名的制造业公司，致力于生产高品质的产品。',
            'address': '公司B地址',
            'phone': '公司B电话'
        }
    }
    company = companys[name]
    return render(request, 'company.html', company)

~~~





**扩展了解：apps.py**

每个app内默认都有 `apps.py` 文件， 在这个文件中定义了app的配置类。这个类继承自 `django.apps.AppConfig`，并定义了一些应用程序的元数据和配置选项。

- `default_auto_field`：该属性指定默认的自动主键字段类型。在 Django 3.2 及以上版本中，需要显式设置该属性，以避免警告信息。可以根据需要选择适合的自动主键字段类型。
- `name`：该属性指定应用程序的名称。它应该与包含 `apps.py` 文件的目录名称相同。
- `verbose_name`：该属性定义应用程序的可读名称，用于在 Django 管理后台等地方显示。

通过在 `apps.py` 文件中自定义应用程序配置类，您可以对应用程序进行更细粒度的配置和定制。例如，您可以在该文件中定义信号处理器、注册应用程序信号、设置应用程序的默认配置等。

**请注意，`apps.py` 文件是可选的，如果您不创建该文件，Django 会使用默认的应用程序配置**。但是，如果您需要对应用程序进行特定的配置或添加自定义逻辑，创建和使用 `apps.py` 文件是一种推荐的做法。

总而言之，`apps.py` 文件提供了一种在应用程序级别上进行配置和定制的方式，使您能够对应用程序进行更加精细的控制和管理。







## 模板语法之render

一般都是在视图函数中通过render函数来使用渲染模板，因此我们先来研究下render函数的使用。可以看到render函数需要的参数还挺多，不过我们经常使用的是前三个，其中前两个必须的。

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

- request 就是视图函数的request参数，把它传给render
- template_name 是模板文件的名字，以字符串的形传进来即可
- context是可选的参数。如果模板需要数据，就通过context把数据传进来。如果模板不需要数据，就不需要使用这个参数。



其中，`context` 参数是一个字典，用于将数据传递给模板并进行渲染。这个字典中的键将作为模板中的变量，对应的值将被替换为实际的数据。

```python
from django.shortcuts import render

def my_view(request):
    context = {
        'name': 'liuxu',
        'age': 18,
        'hobbys': ['吃饭', '睡觉', '打豆豆']
    }
    return render(request, 'my_template.html', context)
```

在上述示例中，`context` 字典包含了三个键值对，分别是 `'name'`、`'age'` 和 `'country'`。这些键和对应的值将被传递给模板进行渲染。

在模板中，您可以通过使用双花括号 `{{ }}` 来访问这些变量。my_template.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<p>Name: {{ name }}</p>
<p>Age: {{ age }}</p>
<p>Hobbys: {{ hobbys }}</p>

</body>
</html>
```

模板中的变量名与字典中的键相对应。当模板被渲染时，模板引擎会将变量名替换为对应的值。







## 模板语法之传值

模板文件中，一共会使用两个标识符：`{{ }}` 和 `{% %}`，在标识符内实现所有的模板语法

```python
# {{ }}	
变量相关; 用在：传值、过滤器、自定义过滤器filter

# {% %}		
逻辑相关; 用在：标签(if判断 for循环)、自定义标签simple_tag、inclusion_tag、模版继承extend和导入include
```



**传值**：所谓传值，就是在渲染模板时，把模板需要的数据传进来，然后渲染出一个完整 HTML 页面。

- 支持传递的数据类型：python基本数据类型、函数、对象等



app01/views.py

~~~python
from django.shortcuts import render

def test11(request):
    def my_func():
        return '返回值是123'

    class Cat:
        def __init__(self, name, color):
            self.name = name
            self.color = color

        def __str__(self):
            return '我的名字是' + self.name

        def talk(self):
            return '喵喵喵'

    class Dog:
        def __str__(self):
            return '无名狗'


    context = {
        'name': 'liuxu',
        'age': 18,
        'hobbys': ['吃饭', '睡觉', '打豆豆'],
        'my_tuple': (1, 2, 3, 4, 5),
        'my_dict': {'a': 10, 'b': 'haha'},
        'my_set': {'a', 'b', 'c'},
        'my_bool': False,
        'my_func': my_func,
        'my_cat': Cat('mimi', '白色'),
        'my_dog': Dog
    }
    return render(request, 'my_template.html', context)
~~~



app01/templates/my_template.html

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h3 style="color:red;">基本数据类型</h3>
<p>Name: {{ name }}</p>
<p>Age: {{ age }}</p>
<p>Hobbys: {{ hobbys }}</p>
<p>my_tuple: {{ my_tuple }}</p>
<p>my_dict: {{ my_dict }}</p>
<p>my_set: {{ my_set }}</p>
<p>my_bool: {{ my_bool }}</p>


<h3 style="color:red;">函数、对象</h3>
<p>my_func: {{ my_func }}</p>
<p>my_cat: {{ my_cat }}</p>
<p>my_dog: {{ my_dog }}</p>

<h3 style="color:red;">对象取值</h3>
<p>my_cat_color: {{ my_cat.color }}</p>
<p>my_cat_talk: {{ my_cat.talk }}</p>

<h3 style="color:red;">列表取值</h3>
<p>Hobbys[0]: {{ hobbys.0 }}</p>
<p>my_tuple[0]: {{ my_tuple.0 }}</p>

<h3 style="color:red;">字典取值</h3>
<p>my_dict: {{ my_dict.items }}</p>

</body>
</html>
~~~



**总结**：

- 变量传值时，既支持python基本的数据类型，还支持函数、对象和类。
- 如果传递的是函数名，则渲染函数的返回值，且此时函数不能有参数(否则，不做任何处理)。
- 传递对象时，如果对象有`__str__`方法，则返回该方法的返回值。
- 【扩展】如果该对象有`__call__`方法，则优先执行`__call__`里面的返回值；如果没有该方法，则再直接打印该对象（打印就是调用`__str__`）。
- 如果传递的是类名，则会实例化一个对象（不能有`__init__`初始化对象哦，因为这就相当于函数有参数了），在HTML页面打印该对象（打印就是调用`__str__`）。
- django模版语法的取值，是固定的格式，只能采用“句点符” `.`

```python
<p>{{ d.username }}</p>			# 字典使用点key方式
<p>{{ l.0 }}</p>			# 列表使用点索引的方式
<p>{{ obj.get_class }}</p>		# 对象点属性或方法的方式
```

- **传值的非常简单，得到什么数据就展示出来，几乎没有逻辑判断**。







## 模板语法之过滤器

**过滤器**：就是模版语法内置的内置方法；可以把它理解为支持带参数的函数。**和传值相比，过滤器有了部分逻辑判断，可以按照需求对数据多处理。**

**基本语法**：`{{数据|过滤器:参数}}`，其中参数是可选的（因为有些过滤器不需要使用参数）。

**注意**：过滤器最多接收两个参数：管道符号前一个，管道符后面一个，如：`{{ current_time|date:'Y-m-d H:i:s' }}`



**常用过滤器**

- 如需查看django中的所有过滤器，请参考官网：https://docs.djangoproject.com/en/4.2/ref/templates/builtins/

| 过滤器           | 描述                             | 示例用法                             |
| ---------------- | -------------------------------- | ------------------------------------ |
| `length`         | 返回字符串或列表的长度           | `{{ text|length }}`                  |
| `title`          | 将字符串中的单词首字母转换为大写 | `{{ text|title }}`                   |
| `capfirst`       | 将字符串的首字母转换为大写       | `{{ text|capfirst }}`                |
| `wordcount`      | 计算字符串中的单词数量           | `{{ text|wordcount }}`               |
| `date`           | 格式化日期                       | `{{ date|date:"Y-m-d" }}`            |
| `time`           | 格式化时间                       | `{{ time\|time:"H:i" }}              |
| `default`        | 如果变量为空，则使用默认值       | `{{ var|default:"N/A" }}`            |
| `filesizeformat` | 格式化文件大小                   | `{{ size|filesizeformat }}`          |
| `floatformat`    | 格式化浮点数                     | `{{ num|floatformat:2 }}`            |
| `join`           | 将列表的元素连接为字符串         | `{{ list|join:", " }}`               |
| `lower`          | 将字符串转换为小写               | `{{ text|lower }}`                   |
| `pluralize`      | 根据数量选择单数或复数形式       | `{{ count|pluralize:"vote,votes" }}` |
| `random`         | 从列表中随机选择一个元素         | `{{ list|random }}`                  |
| `slice`          | 返回列表的切片                   | `{{ list|slice:":2" }}`              |
| `striptags`      | 去除字符串中的 HTML 标签         | `{{ html|striptags }}`               |
| `add`            | 将参数与变量相加                 | `{{ num1|add:num2 }}`                |
| `truncatechars`  | 截断字符串为指定长度             | `{{ text|truncatechars:20 }}`        |
| `truncatewords`  | 截断字符串为指定单词数量         | `{{ text|truncatewords:10 }}`        |
| `upper`          | 将字符串转换为大写               | `{{ text|upper }}`                   |
| `urlize`         | 将文本中的 URL 转换为链接        | `{{ text|urlize }}`                  |

 

其中，关于日期（date）和时间（time）的两个过滤器比较实用，如下是关于这两个过滤器使用的参数格式。不需要死记烂背，需要时直接查找使用即可。

| 格式字符 |                 描述                 | 输出示例                               |
| :------: | :----------------------------------: | -------------------------------------- |
|  **日**  |                                      |                                        |
|   `d`    |   某月的某日，2 位带前导零的数字。   | `'01'` 到 `'31'`                       |
|   `j`    |       某月的某日，前面没有零。       | `'1'` 到 `'31'`                        |
|   `D`    |     某周的某日，3 个字母的文本。     | `'Fri'`                                |
|   `l`    |         某周的某日，长文本。         | `'Friday'`                             |
|   `S`    |  某月英文序号后缀的某日，2 个字符。  | `'st'`、`'nd'`、`'rd'` 或 `'th'`       |
|   `w`    |    某周的某日，不含前导零的数字。    | `'0'` （星期天）到 `'6'` （星期六）    |
|   `z`    |              某年的某日              | `1` 到 `366`                           |
|  **周**  |                                      |                                        |
|   `W`    | 年的 ISO-8601 周数，周从星期一开始。 | `1`，`53`                              |
|  **月**  |                                      |                                        |
|   `m`    |       月份，2 位数，前面加 0。       | `'01'` 到 `'12'`                       |
|   `n`    |          没有前导零的月份。          | `'1'` 到 `'12'`                        |
|   `M`    |         月，3 个字母的文本。         | `'Jan'`                                |
|   `b`    |     月，小写的 3 个字母的文本。      | `'jan'`                                |
|   `F`    |             月，长文本。             | `'January'`                            |
|   `N`    |   美联社风格的月份缩写。专属扩展。   | `'Jan.'`、`'Feb.'`、`'March'`、`'May'` |
|   `t`    |           特定月份的天数。           | `28` 到 `31`                           |
|  **年**  |                                      |                                        |
|   `y`    |       年，2 位带前导零的数字。       | `'00'` 到 `'99'`                       |
|   `Y`    |       年，4 位带前导零的数字。       | `'0001'`, ..., `'1999'`, ..., `'9999'` |
|   `L`    |         是否为闰年的布尔值。         | `True` 或 `False`                      |
| **时间** |                                      |                                        |
|   `g`    |    小时，12 小时格式，无前导零。     | `'1'` 到 `'12'`                        |
|   `G`    |    小时，24 小时格式，无前导零。     | `'0'` 到 `'23'`                        |
|   `h`    |         小时，12 小时格式。          | `'01'` 到 `'12'`                       |
|   `H`    |         小时，24 小时格式。          | `'00'` 到 `'23'`                       |
|   `i`    |                分钟。                | `'00'` 到 `'59'`                       |
|   `s`    |       秒，2 位带前导零的数字。       | `'00'` 到 `'59'`                       |
|   `u`    |                微秒。                | `000000` 到 `999999`                   |
|   `A`    |          `'AM'` 或 `'PM'`。          | `'AM'`                                 |
|   `I`    |        夏令时，无论是否生效。        | `'1'` 或 `'0'`                         |
|   `O`    |        与格林威治时间的时差。        | `'+0200'`                              |







## 模板语法之if判断

上两节课 可以看到，过滤器虽然有了部分逻辑操作，但是本质上依然属于是传值的范畴，即展示数据的作用。并且你会发现传值、过滤器 都是在 `{{ }}` 内部使用。

如果想在模板中使用逻辑，那就需要引入标签（Tag）的概念了。django模板中有很多个标签可以使用，所有的标签都需要在  `{% %} ` 中使用。

我们这节课看看使用频率并列第一的 `if` 标签。和Python类似，这个标签是用来做条件判断的。

**if标签的基本语法**

- 几乎和 Python 中的 if 语句完全一致，但是在模板语法中需要使用 `endif` 结束判断

```python
{% if b == 'abc' %}
    <p>123</p>
{% elif b == 'def'%}
    <p>456</p>
{% else %}
    <p>789</p>
{% endif %}		
```



**布尔运算符**

- and, or, not,  `==`, `!=`, `<`, `>`, `<=`, `>=`, `in`, `not in`, `is`, and `is not`

~~~python
{% if athlete_list and coach_list %}
    Both athletes and coaches are available.
{% endif %}
~~~



**配合过滤器一块使用**

~~~python
{% if messages|length >= 100 %}
   You have lots of messages today!
{% endif %}
~~~









## 模板语法之for循环

另一个使用频率最高的就是 `for` 标签了，和Pythn中的for语言一样，它是用来循环的。

**for标签的基本语法**

- 同样需要使用 `endfor` 结束循环。

```python
# 循环打印每次循环的索引和元素值
{% for item in li %}
    <p>{{ forloop.counter }}, {{item}}</p>		
{% endfor %}
    
    
# 补充：forloop
parentloop
counter0			# 循环的索引，从0开始
counter				# 循环的索引，从1开始
revcounter			# 倒序索引
revcounter0
first				# 是否是第一次循环，True/False
last				# 是否是最后一次循环，True/False


# if 和 for 一块使用
{% for item in books %}
    {% if forloop.first %}
        <p style="color: red">{{ item }}</p>
    {% else %}
         <p>{{ item }}</p>
    {% endif %}
{% endfor %}
```



- 反向循环

~~~python
{% for obj in list reversed %}
~~~

- 处理为空的情况

~~~python
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% empty %}
    <li>Sorry, no athletes in this list.</li>
{% endfor %}
</ul>
~~~







## 模板语法之with

with也是一个常用的标签，一般有两种情况下会使用这个标签。

- 在模板中需要多次使用非常繁琐的方式拿到一个值，**起别名**
- 多次访问一个来自数据库中的值（多次消耗资源），**缓存数据**



**案例**

- 被赋值的变量只能在 `{% with %}` 和 `{% endwith %}` 之间使用

~~~python
{% with nb=d.hobby.3.info %}
    <p>{{ nb }}</p>
    <p>{{ nb }}</p>
{% endwith %}



{% with total=business.employees.count %}
    {{ total }} employee{{ total|pluralize }}
{% endwith %}

~~~

- 可以同时赋值多个变量

```python
{% with alpha=1 beta=2 %}
    ...
{% endwith %}
```



上述demo是最新的语法，非常简洁。同时django也兼容以前版本的语法

~~~python
{% with business.employees.count as total  %}
    <p>{{ total }}</p>
{% endwith %}
~~~









## 模板语法之csrf_token

还记得，前面课程中提交POST请求会报错，当时把配置文件中的一行代码注释就解决了这个问题。

login.html

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



settings.py

~~~python
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



但是，这个报错的原因到底是什么呢？报错原因是Django帮我们做了 CSRF 保护，非法的请求都会出现这个报错。

CSRF（Cross-Site Request Forgery，跨站请求伪造）是一种常见的网络安全漏洞，攻击者利用用户在已认证的网站上的身份执行非意愿的操作。Django 提供了内置的 CSRF 保护机制，以帮助防止 CSRF 攻击。



**钓鱼网站**

假设有一个在线银行应用程序，用户在该应用程序中可以执行转账操作。该应用程序存在一个CSRF攻击漏洞，攻击者可以利用该漏洞执行非授权的转账操作。

攻击步骤如下：

1. 用户在浏览器，登录了银行应用程序。

2. 在同一浏览器中，攻击者诱使用户访问了一个恶意网站。该网站中包含一个自动提交的表单，用于执行转账操作。

    html

3. ```
    <form action="http://bankapp.com/transfer" method="post">
        <input type="hidden" name="to_account" value="attacker_account">
        <input type="hidden" name="amount" value="10000">
        <input type="submit" value="点击这里获取免费礼品">
    </form>
    
    
    注意，攻击者在表单中设置了隐藏字段，将转账金额设置为10000，并将目标账户设置为攻击者自己的账户。
    ```

4. 用户点击了恶意网站中的提交按钮，触发了表单的自动提交。

5. 浏览器发送了一个POST请求到银行应用程序的转账页面，请求中包含了用户的有效会话cookie。

6. 银行应用程序接收到请求后，由于没有进行CSRF令牌验证，误认为这是用户在合法的操作，并执行了转账操作，将10000转到了攻击者的账户。

这就是一个使用CSRF攻击漏洞的示例。攻击者利用了用户当前已经登录的会话，构造了一个伪造的POST请求，绕过了CSRF保护机制。由于银行应用程序没有对请求进行CSRF令牌的验证，攻击者成功地执行了非授权的转账操作。

要防止这种攻击，银行应用程序应该正确实施CSRF保护机制，包括为每个表单生成和验证CSRF令牌。这样，即使攻击者构造了伪造的POST请求，没有合法的CSRF令牌，银行应用程序将拒绝该请求并保护用户的资金安全。



Django的CSRF保护机制：

- 给每个需要保护的网页生成一个csrf token
- 在中间件中，校验该网页是否具备有效的 csrf token



在表单中添加一个标签就好了

~~~html
<form action="/app01/login" method="post">
  <p>用户名：<input type="text" name="username"></p>
  <p>密码：<input type="password" name="password"></p>
  <input type="submit" value="登录"> {% csrf_token %}
</form>
~~~





django模板中还有很多知识点，但是我们就不一一介绍了。因为我觉的这些都不是重点，感兴趣的同学可以自己参考官方文档，了解如下知识点：

- 模版导入

- 模版继承

- 自定义过滤器和标签
- 标签 url 



