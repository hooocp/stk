--data import 

DROP TABLE IF EXISTS analyst.temphu_raw;


CREATE TABLE analyst.temphu_raw (stock_stock_id varchar(12), path string, trd_date string, open_price float, high_price float, low_price float, close_price float, trd_vol bigint, trd_amt double) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;

 LOAD DATA LOCAL inpath 'day.csv' INTO TABLE analyst.temphu_raw;

 --

DROP TABLE IF EXISTS analyst.temphu_raw_5min;


CREATE TABLE analyst.temphu_raw_5min (stock_id varchar(12), path string,trd_date string,trd_time string, open_price float, high_price float, low_price float,close_price float, trd_vol bigint, trd_amt double) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;

 LOAD DATA LOCAL inpath '5.csv' INTO TABLE analyst.temphu_raw_5min;

 --

DROP TABLE IF EXISTS analyst.temphu_raw_1min;


CREATE TABLE analyst.temphu_raw_5min (stock_id varchar(12), path string,trd_date string,trd_time string, open_price float, high_price float, low_price float,close_price float, trd_vol bigint, trd_amt double) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;

 LOAD DATA LOCAL inpath '5.csv' INTO TABLE analyst.temphu_raw_1min;

 --

DROP TABLE IF EXISTS analyst.temphu_raw_1min;


CREATE TABLE analyst.temphu_raw_5min (stock_id varchar(12), path string,trd_date string,trd_time string, open_price float, high_price float, low_price float,close_price float, trd_vol bigint, trd_amt double) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;

 LOAD DATA LOCAL inpath '5.csv' INTO TABLE analyst.temphu_raw_1min;

 --

DROP TABLE IF EXISTS analyst.temphu_raw_tick;


CREATE TABLE analyst.temphu_raw_5min (stock_id varchar(12), path string,trd_date string,trd_time string, open_price float, high_price float, low_price float,close_price float, trd_vol bigint, trd_amt double) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;

 LOAD DATA LOCAL inpath '5.csv' INTO TABLE analyst.temphu_raw_tick;

 ALL,export,SH600000,export,2015/06/18,0945,15.06,15.13,15.05,15.06,8127100,145292416.00 --

DROP TABLE IF EXISTS analyst.stock_day ;


CREATE TABLE analyst.stock_day AS
SELECT a.*,
       CASE
           WHEN a.close_price > b.close_price THEN 'up'
           WHEN a.close_price < b.close_price THEN 'down'
           ELSE 'unknown'
       END flag,
       row_number() over(partition BY a.stock_id
                         ORDER BY a.trd_date) sorted_num
FROM
  (SELECT a.*,
          row_number() over(partition BY a.stock_id
                            ORDER BY a.trd_date) sorted_num
   FROM analyst.temphu_raw a) a
JOIN
  (SELECT a.*,
          row_number() over(partition BY a.stock_id
                            ORDER BY a.trd_date) sorted_num
   FROM analyst.temphu_raw a) b ON a.stock_id=b.stock_id
WHERE a.stock_id=b.stock_id
  AND a.sorted_num = b.sorted_num+1 ;

 ----

DROP TABLE IF EXISTS analyst.stock_5_min ;


CREATE TABLE analyst.stock_5_min AS
SELECT a.*,
       row_number() over(partition BY a.stock_id
                         ORDER BY a.trd_date) sorted_num,
       row_number() over(partition BY a.stock_id,a.trd_time
                         ORDER BY a.trd_date) sorted_num_day
FROM analyst.temphu_raw_5min a;


DROP TABLE IF EXISTS analyst.stock_5_min_etl ;


CREATE TABLE analyst.stock_5_min_etl AS
SELECT stock_id,
       trd_date,
       stddev() std_price,
       avg() avg_price,
       stddev() std_vol,
       avg() avg_vol,
       

       
FROM analyst.temphu_raw_5min ;

 ---计算翻转概率

DROP TABLE IF EXISTS analyst.hu_fanzhuan;


CREATE TABLE analyst.hu_fanzhuan AS
SELECT stock_id,
       flag,
       group_stock_id,
       count(group_stock_id) group_count
FROM
  (SELECT *,
          row_number() over(partition BY stock_id,flag
                            ORDER BY sorted_num) - sorted_num group_stock_id
   FROM analyst.temphu_raw_2) a
GROUP BY stock_id,
         flag,
         group_stock_id HAVING group_count>1 ;

 ----多少天内任意购买，涨幅概率，涨幅标准差

DROP TABLE IF EXISTS analyst.temphu_raw_3 ;


CREATE TABLE analyst.temphu_raw_3 AS
SELECT a.a_stock_id,
       a.a_trd_date,
       min(a.trd_vol)over(partition BY a.a_stock_id, a.a_trd_date) min_trd_vol,
                                                                   a.a_trd_vol
FROM
  (SELECT a.stock_id a_stock_id,
          a.trd_date a_trd_date,
          b.trd_date b_trd_date,
          b.trd_vol,
          a.close_price,
          a.trd_vol a_trd_vol
   FROM analyst.temphu_raw_1 a
   INNER JOIN analyst.temphu_raw_1 b ON a.stock_id=b.stock_id
   WHERE (a.sorted_num-b.sorted_num)<=4
     AND (a.sorted_num>=b.sorted_num)>=0) a ;

 ---翻转数据导出

SELECT group_count,
       count(group_count),
       flag
FROM analyst.hu_fanzhuan
GROUP BY group_count,
         flag ;

 -----连续下行的翻转的分布

SELECT a.stock_id ,
       a.trd_date ,
       min(a.sorted_num-b.sorted_num) delt_days ,
       min(a.sorted_num-b.sorted_num) over(partition BY)
FROM analyst.temphu_raw_1 a
INNER JOIN analyst.temphu_raw_1 b ON a.stock_id = b.stock_id
WHERE a.sorted_num=<250*3
  AND (a.sorted_num-b.sorted_num)>=0
  AND (a.jiesu-b.close_price)>=0 ;

 -----多少天翻转

DROP TABLE IF EXISTS analyst.hu_fanzhuan ;


CREATE TABLE analyst.hu_fanzhuan AS
SELECT stock_id,
       flag,
       group_stock_id,
       count(group_stock_id) group_count
FROM
  (SELECT *,
          row_number() over(partition BY stock_id,flag
                            ORDER BY sorted_num) - sorted_num group_stock_id
   FROM analyst.temphu_raw_2) a
GROUP BY stock_id,
         flag,
         group_stock_id HAVING group_count>1 ;


SELECT group_count,
       count(group_count),
       flag
FROM analyst.hu_fanzhuan
GROUP BY group_count,
         flag ;

 -----其他

DROP TABLE IF EXISTS analyst.temphu_raw_3 ;


CREATE TABLE analyst.temphu_raw_3 AS
SELECT *
FROM
  (SELECT a_stock_id,
          a_trd_date
   FROM analyst.temphu_raw_2
   WHERE min_trd_vol=a_trd_vol) a
INNER JOIN analyst.temphu_raw_1 b ON a.a_stock_id=b.stock_id
AND a.a_trd_date=b.trd_date ;

 ----一天当中最佳卖点

SELECT trd_date,
       stock_id,
       max() analyst.temphu_raw_3
GROUP BY ;

