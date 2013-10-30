drop table bank_attr;
create table bank_attr(
ETL_Dt timestamp not null default now(),
bank_id serial,
Valid_From_Dttm timestamp ,
Valid_To_Dttm timestamp,
Bank_Nm TEXT,
Bank_En_Nm TEXT,
Bank_Function int,
Bank_Categories_1 int,
Bank_Categories_2 int,
Bank_Short_Nm char(8),
Bank_Area int,
PRIMARY KEY (bank_id, Valid_From_Dttm)
);

