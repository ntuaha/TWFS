drop table cc;
create table cc(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
Cc_F_Card_Cnt integer,
Cc_Open_Card_Cnt integer,
Cc_Issue_Card_Cnt integer,
Cc_Stop_Card_Cnt integer,
Cyc_Bal numeric,
Cc_Txn_Bal numeric,
Cc_Ln_Bal numeric,
Cc_Payment_Rate numeric,
Cc_BadDebit_Rate numeric,
Cc_BadDebit_Bal numeric,
Cyc_Income numeric,
Txn_Fee numeric,
Cc_Ln_Fee numeric,
Auth_Store_Cnt integer,
PRIMARY KEY (bank_code, Data_Dt)
);
