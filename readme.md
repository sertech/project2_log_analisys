this program contains three functions question_ONE, question_TWO and question_THREE. Each function answers the three tasks required, the database is called news with the following description:
List of relations
Schema |   Name   | Type  |  Owner
--------+----------+-------+---------
public | articles | table | vagrant
public | authors  | table | vagrant
public | log      | table | vagrant
(3 rows)

there is no installation, the file called reports.py should be in the same folder where the virtual machine is. with the following command

vagrant@vagrant:/vagrant/Project 2 logs analysis project$ python reports.py


1. What are the most popular three articles of all time?
the solution to this question is contained in the first function called question_ONE within the the query:

[select articles.title, count(log.status) as views from articles,log where log.path like ('%'||articles.slug) and log.status like '%200 OK' group by articles.title order by views DESC limit 3;]

The main idea is to count the successful views, and the column status from the table log has that information, so in this case a successful view is registered in the database as a 200 OK http response and the tables articles and logs are related by the columns slug and path respectively

######################################################################
What are the most popular three articles of all time?
    Candidate is jerk, alleges rival - 338647 views
    Bears love berries, alleges bear - 253801 views
    Bad things gone, say good people - 170098 views
######################################################################

2. Who are the most popular article authors of all time?
the solution to this question is contained in the first function called question_TWO within the following query:

select authors.name, count(log.status) as views from authors,log,articles where authors.id = articles.author and log.path like ('%'||articles.slug) and log.status like '%200 OK' group by authors.name order by views desc;

######################################################################
Who are the most popular article authors of all time?
    Ursula La Multa - 507594 views
    Rudolf von Treppenwitz - 423457 views
    Anonymous Contributor - 170098 views
    Markoff Chaney - 84557 views
######################################################################

This also follows the same logic counting successful views marked as 200 OK http responses but this time is grouping the results by authors, counting which authors have the most views across all their articles.

3. On which days did more than 1% of requests lead to errors?
the solution to this question is contained in the first function called question_THREE within the following query:

select day as dayz,errors as errorsz from (select time::DATE as day, sum(case when status like '404 NOT FOUND' then 1 else 0 end)*100.0/count(status) as errors from log group by time::DATE order by errors desc) as derivedtable where errors between 1 and 100;

######################################################################
On which days did more than 1% of requests lead to errors?
    2016-07-17 -       2.26% errors
######################################################################

This query uses a nested select, the purpose is first to sum all the errors registered each day by the value '404 NOT FOUND' in the column status in the table log and calculate its percentage in relation to all the visits to the website and finally desplay which day had more than 1% errors
