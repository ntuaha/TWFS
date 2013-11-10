drop table ln;
create table ln(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
Ln_Do numeric,
Ln_St numeric,
Ln_Ml numeric,
Ln_Ao numeric,
PRIMARY KEY (bank_code, Data_Dt)
);


