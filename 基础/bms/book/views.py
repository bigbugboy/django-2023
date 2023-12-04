from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
import pymysql

from . import models


def get_db_conn():
    return pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='12345',
        db='demo',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )


def book_list(request):

    # with get_db_conn() as conn:
    #     with conn.cursor() as cursor:
    #         sql = 'SELECT * FROM book'
    #         cursor.execute(sql)
    #         books = cursor.fetchall()
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 1))

    all_books = models.Book.objects.all()
    paginator = Paginator(all_books, size)
    books = paginator.get_page(page)
    return render(request, 'list.html', {'books': books})


def book_create(request):
    if request.method == 'GET':
        publishers = ['北京出版社', '南京出版社', '上海出版社']
        authors = ['李白', '白居易', '杜甫', '欧阳修', '李时珍']
        return render(request, 'create.html', {'publishers': publishers, 'authors': authors})

    # post
    data = request.POST

    # with get_db_conn() as conn:
    #     with conn.cursor() as cursor:
    #         sql = 'INSERT INTO book(title, price, publish_date, publisher, authors) VALUES(%s, %s, %s, %s, %s)'
    #         book_data = (
    #             data.get('title'),
    #             data.get('price'),
    #             data.get('publish_date'),
    #             data.get('publisher'),
    #             ','.join(data.getlist('authors'))
    #         )
    #         cursor.execute(sql, book_data)
    #         conn.commit()

    models.Book.objects.create(
        title=data.get('title'),
        price=data.get('price'),
        publish_date=data.get('publish_date'),
        publisher=data.get('publisher'),
        authors=','.join(data.getlist('authors'))
    )

    return redirect(to='book_list')


def book_delete(request, book_id):
    # with get_db_conn() as conn:
    #     with conn.cursor() as cursor:
    #         sql = 'DELETE FROM book WHERE id=%s'
    #         cursor.execute(sql, book_id)
    #         conn.commit()
    models.Book.objects.filter(id=book_id).delete()
    return redirect(to='book_list')


def book_edit(request, book_id):
    publishers = ['北京出版社', '南京出版社', '上海出版社']
    authors = ['李白', '白居易', '杜甫', '欧阳修', '李时珍']
    if request.method == 'GET':
        # with get_db_conn() as conn:
        #     with conn.cursor() as cursor:
        #         sql = 'SELECT * FROM book WHERE id=%s'
        #         cursor.execute(sql, book_id)
        #         book = cursor.fetchone()
        #         book['authors'] = book['authors'].split(',')
        book = models.Book.objects.get(id=book_id)
        return render(request, 'edit.html', {'book': book, 'publishers': publishers, 'authors': authors})

    # post
    # with get_db_conn() as conn:
    #     with conn.cursor() as cursor:
    #         sql = """
    #             UPDATE book
    #             SET title=%s, price=%s, publish_date=%s, publisher=%s, authors=%s
    #             WHERE id=%s
    #         """
    #         data = request.POST
    #         book_data = (
    #             data.get('title'),
    #             data.get('price'),
    #             data.get('publish_date'),
    #             data.get('publisher'),
    #             ','.join(data.getlist('authors')),
    #             book_id
    #         )
    #         print(book_data)
    #         cursor.execute(sql, book_data)
    #         conn.commit()
    data = request.POST
    models.Book.objects.filter(id=book_id).update(
        title=data.get('title'),
        price=data.get('price'),
        publish_date=data.get('publish_date'),
        publisher=data.get('publisher'),
        authors=','.join(data.getlist('authors')),
    )
    return redirect(to='book_list')
