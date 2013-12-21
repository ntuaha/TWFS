drop table nc;
create table nc(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
NC_Bal numeric,
NC_M numeric,
NC_O numeric,
PRIMARY KEY (bank_code, Data_Dt)
);