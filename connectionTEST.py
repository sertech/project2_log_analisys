import psycopg2
DBNAME = "news"
try:
    db = psycopg2.connect(database=DBNAME)
    print ("connection ok")
    # print "connection succesful "
except:
    print ("error connecting to the db")


# selections
'''
news=> select * from authors where id=2;

name | Rudolf von Treppenwitz
bio  | Rudolf von Treppenwitz is a nonprofitable disorganizer specializing in procrastinatory operations.
id   | 2

news=> select * from articles where author=2;

author | 2
title  | Candidate is jerk, alleges rival
slug   | candidate-is-jerk
lead   | That political candidate is a real jerk, according to a rival.
body   | The rival alleged egotism, arrogance, and an almost fanatical devotion to media grandstanding. The candidate's campaign denied everything, and retaliated that the rival is a doo-doo head.
time   | 2016-08-15 18:55:10.814316+00
id     | 26

news=> select * from log where path like '%candidate-is-jerk' limit 1;

path   | /article/candidate-is-jerk
ip     | 198.51.100.195
method | GET
status | 200 OK
time   | 2016-07-01 07:00:47+00
id     | 1678924


'''

# ONE

'''
news=> select articles.slug, count(log.status) as views from articles,log where log.path like ('%'||articles.slug) group by articles.slug;
           slug            | views
---------------------------+--------
 so-many-bears             |  84504
 balloon-goons-doomed      |  84557
 goats-eat-googles         |  84906
 bears-love-berries        | 253801
 candidate-is-jerk         | 338647
 trouble-for-troubled      |  84810
 media-obsessed-with-bears |  84383
 bad-things-gone           | 170098
(8 rows)

news=> select path,count(status) as error from log where status like '%200 OK' and path like '%so-many-bears' group by
path;
          path          | error
------------------------+-------
 /article/so-many-bears | 84504
(1 row)

news=> select path,count(status) as error from log where status not like '%200 OK' and path like '%so-many-bears' group
 by path;
 path | error
------+-------
(0 rows)

'''

# TWO

'''
news=> select authors.name, authors.id, articles.author, articles.title from authors, articles where authors.id = artic
les.author order by authors.id;
          name          | id | author |               title
------------------------+----+--------+------------------------------------
 Ursula La Multa        |  1 |      1 | There are a lot of bears
 Ursula La Multa        |  1 |      1 | Bears love berries, alleges bear
 Ursula La Multa        |  1 |      1 | Goats eat Google's lawn
 Ursula La Multa        |  1 |      1 | Media obsessed with bears
 Rudolf von Treppenwitz |  2 |      2 | Trouble for troubled troublemakers
 Rudolf von Treppenwitz |  2 |      2 | Candidate is jerk, alleges rival
 Anonymous Contributor  |  3 |      3 | Bad things gone, say good people
 Markoff Chaney         |  4 |      4 | Balloon goons doomed
(8 rows)

news=> select authors.name, count(authors.id) as N_articles from authors, articles where authors.id = articles.author g
roup by authors.name order by N_articles desc;
          name          | n_articles
------------------------+------------
 Ursula La Multa        |          4
 Rudolf von Treppenwitz |          2
 Anonymous Contributor  |          1
 Markoff Chaney         |          1
(4 rows)

news=> select authors.name, count(log.status) as views from authors,log,articles where authors.id = articles.author and log.path like ('%'||articles.slug) group by authors.name order by views desc;
          name          | views
------------------------+--------
 Ursula La Multa        | 507594
 Rudolf von Treppenwitz | 423457
 Anonymous Contributor  | 170098
 Markoff Chaney         |  84557
(4 rows)

news=> select authors.name, count(log.status) as views from authors,log,articles where authors.id = articles.author and log.path like ('%'||articles.slug) and log.status like '%200 OK' group by authors.name order by views desc;
          name          | views
------------------------+--------
 Ursula La Multa        | 507594
 Rudolf von Treppenwitz | 423457
 Anonymous Contributor  | 170098
 Markoff Chaney         |  84557
(4 rows)

news=> select status from log group by status;
    status
---------------
 404 NOT FOUND
 200 OK
(2 rows)

'''


# three
'''
news=> select status, count(status) from log group by status;
    status     |  count
---------------+---------
 404 NOT FOUND |   12908
 200 OK        | 1664827
(2 rows)

news=> select count(status) from log;
  count
---------
 1677735
(1 row)

news=> select time::DATE,count(status) as ERRORS from log where status like '404 NOT FOUND' group by time::DATE order b
y ERRORS DESC;
    time    | errors
------------+--------
 2016-07-17 |   1265
 2016-07-19 |    433
 2016-07-24 |    431
 2016-07-05 |    423
 2016-07-06 |    420
 2016-07-21 |    418
 2016-07-08 |    418
 2016-07-09 |    410
 2016-07-15 |    408
 2016-07-22 |    406
 2016-07-11 |    403
 2016-07-03 |    401
 2016-07-30 |    397
 2016-07-26 |    396
 2016-07-28 |    393
 2016-07-25 |    391
 2016-07-02 |    389
 2016-07-20 |    383
 2016-07-14 |    383
 2016-07-13 |    383
 2016-07-29 |    382
 2016-07-04 |    380
 2016-07-16 |    374
 2016-07-18 |    374
 2016-07-23 |    373
 2016-07-12 |    373
 2016-07-10 |    371
 2016-07-27 |    367
 2016-07-07 |    360
 2016-07-31 |    329
 2016-07-01 |    274
(31 rows)


news=> select time::DATE, count(status) as total, sum(case when status like '200 OK' then 1 else 0 end) as OKs, sum(case when status like '404 NOT FOUND' then 1 else 0 end) as ERRORs from log group by time::DATE;
    time    | total |  oks  | errors
------------+-------+-------+--------
 2016-07-01 | 38705 | 38431 |    274
 2016-07-02 | 55200 | 54811 |    389
 2016-07-03 | 54866 | 54465 |    401
 2016-07-04 | 54903 | 54523 |    380
 2016-07-05 | 54585 | 54162 |    423
 2016-07-06 | 54774 | 54354 |    420
 2016-07-07 | 54740 | 54380 |    360
 2016-07-08 | 55084 | 54666 |    418
 2016-07-09 | 55236 | 54826 |    410
 2016-07-10 | 54489 | 54118 |    371
 2016-07-11 | 54497 | 54094 |    403
 2016-07-12 | 54839 | 54466 |    373
 2016-07-13 | 55180 | 54797 |    383
 2016-07-14 | 55196 | 54813 |    383
 2016-07-15 | 54962 | 54554 |    408
 2016-07-16 | 54498 | 54124 |    374
 2016-07-17 | 55907 | 54642 |   1265
 2016-07-18 | 55589 | 55215 |    374
 2016-07-19 | 55341 | 54908 |    433
 2016-07-20 | 54557 | 54174 |    383
 2016-07-21 | 55241 | 54823 |    418
 2016-07-22 | 55206 | 54800 |    406
 2016-07-23 | 54894 | 54521 |    373
 2016-07-24 | 55100 | 54669 |    431
 2016-07-25 | 54613 | 54222 |    391
 2016-07-26 | 54378 | 53982 |    396
 2016-07-27 | 54489 | 54122 |    367
 2016-07-28 | 54797 | 54404 |    393
 2016-07-29 | 54951 | 54569 |    382
 2016-07-30 | 55073 | 54676 |    397
 2016-07-31 | 45845 | 45516 |    329
(31 rows)

news=> select time::DATE as DATA,count(status)*100.0/(select count(*)from log) as ERRORS from log where status like '404 NOT FOUND' group by time::DATE order by ERRORS DESC;
    data    |         errors
------------+------------------------
 2016-07-17 | 0.07539927342518335732
 2016-07-19 | 0.02580860505383746539
 2016-07-24 | 0.02568939671640634546
 2016-07-05 | 0.02521256336668186573
 2016-07-06 | 0.02503375086053518583
 2016-07-21 | 0.02491454252310406590
 2016-07-08 | 0.02491454252310406590
 2016-07-09 | 0.02443770917337958617
 2016-07-15 | 0.02431850083594846624
 2016-07-22 | 0.02419929249851734630
 2016-07-11 | 0.02402047999237066640
 2016-07-03 | 0.02390127165493954647
 2016-07-30 | 0.02366285498007730661
 2016-07-26 | 0.02360325081136174664
 2016-07-28 | 0.02342443830521506674
 2016-07-25 | 0.02330522996778394681
 2016-07-02 | 0.02318602163035282688
 2016-07-20 | 0.02282839661805946708
 2016-07-14 | 0.02282839661805946708
 2016-07-13 | 0.02282839661805946708
 2016-07-29 | 0.02276879244934390711
 2016-07-04 | 0.02264958411191278718
 2016-07-16 | 0.02229195909961942738
 2016-07-18 | 0.02229195909961942738
 2016-07-23 | 0.02223235493090386742
 2016-07-12 | 0.02223235493090386742
 2016-07-10 | 0.02211314659347274748
 2016-07-27 | 0.02187472991861050762
 2016-07-07 | 0.02145750073760158786
 2016-07-31 | 0.01960977150741922890
 2016-07-01 | 0.01633154222806343076
(31 rows)

news=> select time::DATE, sum(case when status like '404 NOT FOUND' then 1 else 0 end)*100.0/count(status) as ERRORs from log group by time::DATE order by errors desc;
    time    |         errors
------------+------------------------
 2016-07-17 |     2.2626862468027260
 2016-07-19 | 0.78242171265427079381
 2016-07-24 | 0.78221415607985480944
 2016-07-05 | 0.77493816982687551525
 2016-07-06 | 0.76678716179209113813
 2016-07-08 | 0.75884104277104059255
 2016-07-21 | 0.75668434677141977879
 2016-07-15 | 0.74233106509952330701
 2016-07-09 | 0.74226953436164820045
 2016-07-11 | 0.73949024716956896710
 2016-07-22 | 0.73542730862587399920
 2016-07-03 | 0.73087157802646447709
 2016-07-26 | 0.72823568354849387620
 2016-07-30 | 0.72086140213897917310
 2016-07-31 | 0.71763551096084633003
 2016-07-28 | 0.71719254703724656459
 2016-07-25 | 0.71594675260469119074
 2016-07-01 | 0.70791887353055160832
 2016-07-02 | 0.70471014492753623188
 2016-07-20 | 0.70201807284124860238
 2016-07-29 | 0.69516478317046095612
 2016-07-13 | 0.69409206234142805364
 2016-07-14 | 0.69389086165664178564
 2016-07-04 | 0.69212975611533067410
 2016-07-16 | 0.68626371609967338251
 2016-07-10 | 0.68087136853309842354
 2016-07-12 | 0.68017286967304290742
 2016-07-23 | 0.67949138339344919299
 2016-07-27 | 0.67353043733597606856
 2016-07-18 | 0.67279497742359099822
 2016-07-07 | 0.65765436609426379247
(31 rows)

news=> select day as dayz,errors as errorsz from (select time::DATE as day, sum(case when status like '404 NOT FOUND' then 1 else 0 end)*100.0/count(status) as errors from log group by time::DATE order by errors desc) as derivedtable where errors between 1 and 100;

    dayz    |      errorsz
------------+--------------------
 2016-07-17 | 2.2626862468027260
(1 row)
'''
