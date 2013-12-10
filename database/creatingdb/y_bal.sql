drop table y_bal;
create table y_bal(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
MY_TOT numeric,
FY_TOT numeric,
MY_Country numeric,
FY_Country numeric,
MY_OS numeric,
FY_Os numeric,
PRIMARY KEY (bank_code, Data_Dt)
);
