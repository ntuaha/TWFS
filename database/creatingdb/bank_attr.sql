drop table bank_attr;
create table bank_attr(
ETL_Dt timestamp not null default now(),
bank_code char(4),
Bank_Nm TEXT,
Data_Dt timestamp ,
Start_Ym timestamp,
Bank_En_Nm TEXT,
SWIFT_BIC TEXT,
Bank_Area_Cd char(14) not null default 0,
Bank_Type_Cd int not null default -1,
Bank_Status_Cd char(1) not null default '',
Current_Bank_Cd char(4),
Tw_Area_Cd int,
comment text,
PRIMARY KEY (Data_Dt,bank_nm)
);



CREATE INDEX Bank_Cd_idx ON bank_attr(bank_code);


DROP FUNCTION insertBank() CASCADE;
CREATE FUNCTION insertBank() RETURNS TRIGGER AS $insertBank$
DECLARE
	count_user INTEGER;
BEGIN
    SELECT COUNT(*) INTO count_user FROM bank_attr WHERE bank_nm= NEW.bank_nm and data_dt = NEW.data_dt;
        IF count_user =0 THEN
            RETURN NEW;
        END IF;
    RETURN NULL;
END;    
$insertBank$ LANGUAGE plpgsql;

CREATE TRIGGER insertBank
BEFORE INSERT ON bank_attr
FOR EACH ROW
EXECUTE PROCEDURE insertBank();
