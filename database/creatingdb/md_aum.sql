drop table md_aum;
create table md_aum(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
Md_Aum numeric,
PRIMARY KEY (bank_code, Data_Dt)
);
