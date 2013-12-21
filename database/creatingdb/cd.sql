drop table cd;
create table cd(
ETL_Dt timestamp not null default now(),
bank_code char(10),
Data_Dt timestamp ,
Bank_Nm TEXT,
C_Cd_Cnt integer,
C_Cd_Bal numeric,
P_Cd_Cnt integer,
P_Cd_Bal numeric,
O_Cd_Cnt integer,
O_Cd_Bal numeric,
PRIMARY KEY (bank_code, Data_Dt)
);