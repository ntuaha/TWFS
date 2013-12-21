drop table lppe;
create table lppe(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
LN_G numeric,
LN_P numeric,
PRIMARY KEY (bank_code, Data_Dt)
);