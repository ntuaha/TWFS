create  temporary table A00 as select to_char(Data_dt,'YYYY-MM-DD') as Data_dt, cc_txn_bal/Cc_Open_Card_Cnt as val from cc where bank_code = '808' and Data_dt >= '2010-04-01' order by data_dt;
create  temporary table A01 as select to_char(Data_dt,'YYYY-MM-DD') as Data_dt, cc_txn_bal/Cc_Open_Card_Cnt as val from cc where bank_code = '812' and Data_dt >= '2010-04-01' order by data_dt;
create  temporary table A02 as select to_char(Data_dt,'YYYY-MM-DD') as Data_dt, cc_txn_bal/Cc_Open_Card_Cnt as val from cc where bank_code = '822' and Data_dt >= '2010-04-01' order by data_dt;
create  temporary table A03 as select to_char(Data_dt,'YYYY-MM-DD') as Data_dt, cc_txn_bal/Cc_Open_Card_Cnt as val from cc where bank_code = '013' and Data_dt >= '2010-04-01' order by data_dt;
create  temporary table A04 as select to_char(Data_dt,'YYYY-MM-DD') as Data_dt, cc_txn_bal/Cc_Open_Card_Cnt as val from cc where bank_code = '021' and Data_dt >= '2010-04-01' order by data_dt;
create  temporary table A05 as select to_char(Data_dt,'YYYY-MM-DD') as Data_dt, cc_txn_bal/Cc_Open_Card_Cnt as val from cc where bank_code = '012' and Data_dt >= '2010-04-01' order by data_dt;
create temporary table G as select A00.Data_dt,A00.val as A00,A01.val as A01,A02.val as A02,A03.val as A03,A04.val as A04,A05.val as A05
from A00
left join A01 on (A00.data_dt = A01.data_dt)
left join A02 on (A00.data_dt = A02.data_dt)
left join A03 on (A00.data_dt = A03.data_dt)
left join A04 on (A00.data_dt = A04.data_dt)
left join A05 on (A00.data_dt = A05.data_dt)
order by data_dt;
\copy (select * from G) to '/home/aha/Data/TWFS/data/avg_cc_txn_bal.csv_2' With CSV HEADER