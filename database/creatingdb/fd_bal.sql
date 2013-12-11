drop table fd_bal;
create table fd_bal(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
FD_Bal numeric,
Trans_FD_Bal numeric,
PRIMARY KEY (bank_code, Data_Dt)
);
