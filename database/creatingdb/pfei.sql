drop table pfei;
create table pfei(
id serial primary key,
ETL_Dt timestamp not null default now(),
Data_Ym timestamp ,
M1B numeric,
F_Ins_Dp numeric,
F_Ins_Ln numeric,
C_Ins_Dp numeric,
C_INs_Ln numeric,
Country_SME numeric,
Country_C_CL numeric,
Country_CL numeric,
MF_Bal numeric,
Bund_Txn_Amt numeric,
Stock_Index numeric,
WPI numeric,
CPI numeric,
Exchange_Rate numeric,
Rediscount_Rate numeric,
B_Ins_Rate numeric,
GDP numeric,
Y_DP numeric,
CONSTRAINT pfei_data_ym_idx UNIQUE(Data_Ym)
);

