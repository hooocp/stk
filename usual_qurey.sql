-- 常用查询类sql

SELECT DISTINCT a_id,
                a_trd_date,
                min_trd_vol,
                a_trd_vol
FROM analyst.temphu_raw_2
ORDER BY a_trd_date DESC;

----
SELECT count(*)
FROM analyst.temphu_raw_1 a
INNER JOIN analyst.temphu_raw_1 b ON a.id=b.id



