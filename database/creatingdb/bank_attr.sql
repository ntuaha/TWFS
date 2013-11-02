drop table bank_attr;
create table bank_attr(
ETL_Dt timestamp not null default now(),
bank_code char(4),
Data_Dt timestamp ,
Bank_Nm TEXT,
Bank_En_Nm TEXT,
Bank_Function int,
Bank_Categories int,
Bank_BIC int,
Bank_Short_Nm char(8),
Bank_Area int,
PRIMARY KEY (bank_code, Data_Dt)
);
CREATE INDEX Bank_Nm_idx ON bank_attr(Bank_Nm);


DROP FUNCTION insertBank() CASCADE;
CREATE FUNCTION insertBank() RETURNS TRIGGER AS $insertBank$
DECLARE
	count_user INTEGER;
BEGIN
    SELECT COUNT(*) INTO count_user FROM bank_attr WHERE bank_code = NEW.bank_code and data_dt = NEW.data_dt;
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
