drop table cl_info;
create table cl_info(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
Mortgage_Cnt numeric,
Mortgage_Bal numeric,
Decorator_Hse_Cnt numeric,
Decorator_Hse_Bal numeric,
Ln_Car_Cnt numeric,
Ln_Car_Bal numeric,
Ln_Worker_Cnt numeric,
Ln_Worker_Bal numeric,
Other_CL_Cnt numeric,
Other_CL_Bal numeric,
PRIMARY KEY (bank_code, Data_Dt)
);







