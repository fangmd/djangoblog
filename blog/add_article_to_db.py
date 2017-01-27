# !/usr/bin/env python3
# -*- coding:utf-8 -*-

import django
import sys
import os

from django.utils.timezone import utc

sys.path.append(os.path.abspath("/home/double/djangoblog/blog"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

import os
import re
import sqlite3
from blog.models import Article, Tag, Category
from django.utils import timezone
from django.utils.dateparse import parse_datetime


# class Article:
#     """
#     id, title, body, created_time, last_modified_time, status, abstract, views, likes, topped, category_id
#     """
#
#     def __init__(self, *args, **kwargs):
#         pass
#
#     def __str__(self):
#         return 'asd'
#
#
# class Category:
#     """
#     id, name, create_time, last_modified_time
#     """
#
#     def __init__(self):
#         pass
#
#     def __str__(self):
#         return 'category'


def get_sqlite3_conn(sqlite3_path):
    # print("connect db : ", str(sqlite3_path))
    return sqlite3.connect(sqlite3_path)


def print_sqlite3(conn, table_name):
    cursor = conn.execute("SELECT * from " + table_name)
    for row in cursor:
        a = Article
        a.id = row[0]
        a.title = row[1]
        print(a.id, a.title)


def insert_category_id(conn, category_id, created_time):
    insert_sql = r"INSERT INTO blog_category(name, create_time, last_modified_time)" \
                 " VALUES ( '" + category_id + "', '" + \
                 created_time + "', '" + created_time + "')"
    print(insert_sql)
    cursor = conn.execute(insert_sql)
    conn.commit()
    for row in cursor:
        print("create a category:", category_id, " id:" + row[0])
        return row[0]


def get_category_id(conn, category_id, created_time):
    """
    使用 分类名 获取分类在数据库中的 id
    :param conn:
    :param category_id: 分类 str
    :param created_time: 分类的创建时间
    :return: int 分类在数据库中的 id
    """
    query_sql = r"SELECT * from blog_category WHERE name='" + category_id + "'"
    # print(query_sql)
    cursor = conn.execute(query_sql)
    # print(type(cursor), cursor.rowcount, cursor.arraysize)
    for row in cursor:
        # print("get category id :", row[0])
        return row[0]

    return insert_category_id(conn, category_id, created_time)


def get_article(conn, title):
    """
    通过 title 查询文章
    :param title: 文章标题
    :return:
    """
    query_sql = r"SELECT * from blog_article WHERE title='" + title + "'"
    cursor = conn.execute(query_sql)
    for row in cursor:
        return "文章在数据中"
    return


def save_tags(tags):
    """
    Tags 数据库插入
    :param tags: list tags
    :return: null
    """
    if tags:
        for tag in tags:
            t = None
            try:
                t = Tag.objects.get(name=tag)
            except Exception:
                pass
            if not t:
                t = Tag(name=tag)
            t.save()


def insert_article_to_db(conn, article):
    """
    插入文章
    :param conn:
    :param article: 文章类
    :return:
    """
    if not get_article(conn, article.title):
        try:
            save_tags(article.tags)
            conn.execute("INSERT INTO blog_article "
                         "(title, body, created_time, last_modified_time, status, views, likes, topped, category_id) "
                         "VALUES "
                         "(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         [article.title, article.body, article.created_time,
                          article.last_modified_time, article.status, str(
                             article.views),
                          str(article.likes), str(article.topped),
                          str(get_category_id(conn, article.category_id, article.created_time))])
        except sqlite3.OperationalError:
            # print(add)
            print(article.title)
        conn.commit()


def save_category(category_id):
    category = None
    try:
        category = Category.objects.get(name=category_id)
    except Exception:
        pass
    if not category:
        category = Category(name=category_id)
        category.save()


def parse_md_to_article(file_path):
    """
    解析 md文件
    :param file_path: md文件路径
    :return: Article 文章对象
    """
    with open(file_path) as f:
        print(file_path)
        content = f.read()
        head = re.findall(r"---[.\\n\s\S]*---", content)
        # print(re.findall(r"---[.\\n\s\S]*---", content))

        title = re.findall(
            r"^title: .*$", content, re.M)[0].split(": ")[1]

        if not title:
            print(file_path, "-------")
        created_time = re.findall(
            r"^date: .*$", content, re.M)[0].split(": ")[1]

        tags = re.findall(
            r"^tags: .*$", content, re.M)[0].split(": ")[1]
        tags = list(filter(None, re.split(r"[\[ ,\]]", tags, re.M)))
        try:
            category_id = re.findall(
                r"^category: .*$", content, re.M)[0].split(": ")[1]
        except IndexError:
            category_id = re.findall(
                r"^categories: .*$", content, re.M)[0].split(": ")[1]

        body = content.split(head[0])[1].strip()

        abstract = body.split("<!--more-->")[0]

        last_modified_time = created_time
        status = 'p'
        views = 0
        likes = 0
        topped = 0

        article = None
        try:
            article = Article.objects.get(title=title)
        except Exception:
            pass

        if not article:
            article = Article()

        article.title = title
        if created_time:
            p = parse_datetime(created_time.strip()).replace(tzinfo=utc)
            naive = p
            article.created_time = naive
            article.last_modified_time = naive
        else:
            print("----------error create time is null:", title)

        article.body = body
        article.abstract = abstract
        article.status = status
        article.views = views
        article.likes = likes
        article.topped = topped
        article.save()

        save_tags(tags=tags)
        for tag in tags:
            article.tags.add(Tag.objects.get(name=tag))
        c = None

        save_category(category_id)
        try:
            c = Category.objects.get(name=category_id)
        except Exception:
            pass
        if not c:
            c = Category(name=category_id)

        article.category_id = c.id

        # print(article.title, article.created_time, article.tags, article.category_id)

    return article


def get_all_md_file(root_directory):
    """
    获取 root——directory 下的所有 *.md *.mkd 文件路径
    :param root_directory: 根路径
    :return: list 文件集合
    """
    file_paths = []

    for root, dirs, files in os.walk(root_directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            if file_path.endswith("md") or file_path.endswith("mkd") or file_path.endswith("mdown"):
                print(file_path)
                file_paths.append(file_path)
    return file_paths


def root():
    file_paths = get_all_md_file("/Users/double/Documents/blog2/source/_posts")
    conn = get_sqlite3_conn(
        '/Users/double/djangoblog/blog/db.sqlite3')
    for file_path in file_paths:
        article = parse_md_to_article(file_path)
        insert_article_to_db(conn=conn, article=article)
    conn.close()


# TODO: root
if __name__ == '__main__':
    root()

# TODO: test
# conn = get_sqlite3_conn('/Users/double/djangoblog/blog/db.sqlite3')
# table_name = "blog_article"
# print_sqlite3(conn, table_name)

# a = parse_md_to_article(
#     "/Users/double/Documents/blog2/source/_posts/uml/uml用户指南读书笔记.md")

# print(a)
# test insert article
# insert_article_to_db(conn, a)

# test insert category
# get_category_id(conn, "Andraaaasdoid", "2016-11-22 13:12:42.314055")


# get_all_md_file("/Users/double/Documents/blog2/source/_posts")
# a = parse_md_to_article("/Users/double/Documents/blog2/source/_posts/Android/Handler机制总结.md")
# insert_article_to_db(conn, a)

# test save tags
# save_tags(conn, ['tag5', 'tag6', 'tag7'])
