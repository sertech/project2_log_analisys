#! /usr/bin/env python3

import psycopg2

myConnection = psycopg2.connect(database="news")


def question_ONE(a_connection):
    cursor = a_connection.cursor()
    query = "select articles.title, count(log.status) as views from \
            articles,log where log.path like ('%'||articles.slug)\
            and log.status like '%200 OK' group by articles.title \
            order by views DESC limit 3"
    cursor.execute(query)
    print("#"*70)
    print("What are the most popular three articles of all time?")
    for (title, views) in cursor.fetchall():
        print("    {} - {} views".format(title, views))
    print("#"*70)


def question_TWO(a_connection):
    cursor = a_connection.cursor()
    query = "select authors.name, count(log.status) as views from \
            authors,log,articles where authors.id = articles.author \
            and log.path like ('%'||articles.slug) and \
            log.status like '%200 OK' group by authors.name \
            order by views desc"
    cursor.execute(query)
    print("#"*70)
    print("Who are the most popular article authors of all time?")
    for (name, views) in cursor.fetchall():
        print("    {} - {} views".format(name, views))
    print("#"*70)


def question_THREE(a_connection):
    cursor = a_connection.cursor()
    query = "select day as dayz,errors as errorsz \
            from (select time::DATE as day, sum(case when status like \
            '404 NOT FOUND' then 1 else 0 end)*100.0/count(status) as errors \
            from log group by time::DATE order by errors desc) \
            as derivedtable where errors between 1 and 100"
    cursor.execute(query)
    print("#"*70)
    print("On which days did more than 1% of requests lead to errors?")
    for (day, errorsz) in cursor.fetchall():
        print("    {} - {:10.2f}% errors".format(day, errorsz))
    print("#"*70)


question_ONE(myConnection)
question_TWO(myConnection)
question_THREE(myConnection)
myConnection.close()
