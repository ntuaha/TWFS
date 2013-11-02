drop table lsme;
create table lsme(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
LN_SME numeric,
LN_SME_RATE numeric,
MARKET_RATE numeric,
PRIMARY KEY (bank_code, Data_Dt)
);
