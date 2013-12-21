drop table atm;
create table atm(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
Issue_Card_Cnt integer,
F_Card_Cnt integer,
ATM_Cnt integer,
Txn_Cnt integer,
Txn_Bal numeric,
PRIMARY KEY (bank_code, Data_Dt)
);