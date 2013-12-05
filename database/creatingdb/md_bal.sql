drop table md_bal;
create table md_bal(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
MD numeric,
FD numeric,
DP_Y numeric,	
DP_Other numeric,	
PRIMARY KEY (bank_code, Data_Dt)
);