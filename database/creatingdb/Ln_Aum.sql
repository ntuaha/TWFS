drop table Ln_Aum;
create table Ln_Aum(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
LN_Aum numeric,
PRIMARY KEY (bank_code, Data_Dt)
);


