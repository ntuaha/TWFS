drop table cl;
create table cl(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
CL_Cnt numeric,
CL_Bal numeric,
PRIMARY KEY (bank_code, Data_Dt)
);


