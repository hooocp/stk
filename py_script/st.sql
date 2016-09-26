SELECT trd_date,
       st_id,
       avg(op) avg_op,
       std(op) std_op,
       avg(hp) avg_hp,
       std(hp) std_hp,
       avg(lp) avg_lp,
       std(lp) std_lp,
       avg(cp) avg_cp,
       std(cp) std_cp,
       avg(cnt) avg_cnt,
       std(cnt) std_cnt,
       avg(amt) avg_amt,
       std(amt) std_amt,
       corr(cp,cnt) cp_cnt_corr,
       corr(amt,cnt) amt_cnt_corr 
FROM st.min_1
GROUP BY trd_date,
         st_id;

