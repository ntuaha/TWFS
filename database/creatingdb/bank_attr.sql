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
Bank_Status_Cd char(1) not null default '%',
Current_Bank_Cd char(4),
Tw_Area_Cd int,
comment text,
Stock_Type char(1),
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

#
# ALTER TABLE bank_attr ADD Stock_Type char(1)
#
# UPDATE bank_attr SET Stock_Type='A%' where bank_code in ('001','004','005','006','007','008','009','050','016');
# https://www.twnch.org.tw/banklist/service/%E6%9C%AC%E5%9C%8B%E6%B0%91%E7%87%9F%E9%8A%80%E8%A1%8C%E7%B6%B2%E7%AB%99.asp
# 民營銀行
# http://www.banking.gov.tw/ch/ap/bankno_excel.jsp
# SELECT bank_Code,bank_nm from bank_attr where bank_nm like '%%華僑%%' or
bank_nm like '%上海%' or
bank_nm like '%世華%' or
bank_nm like '%中國國際%' or
bank_nm like '%中國信託%' or
bank_nm like '%玉山%' or
bank_nm like '%大眾%' or
bank_nm like '%日盛%' or
bank_nm like '%泛亞%' or
bank_nm like '%聯信%' or
bank_nm like '%台北銀行%' or
bank_nm like '%高雄銀行%' or
bank_nm like '%中華開發工業%' or
bank_nm like '%富邦%' or
bank_nm like '%台中商業銀行%' or
bank_nm like '%新竹國際商業銀行%' or
bank_nm like '%華南%' or
bank_nm like '%遠東%' or
bank_nm like '%萬泰%' or
bank_nm like '%中興%' or
bank_nm like '%聯邦%' or
bank_nm like '%慶豐%' or
bank_nm like '%誠泰%' or
bank_nm like '%陽信%' or
bank_nm like '%第七商業銀行%' or
bank_nm like '%板信%' or
bank_nm like '%台北國際%' or
bank_nm like '%中國農民%' or
bank_nm like '%中華開發%' or
bank_nm like '%華泰%' or
bank_nm like '%三信商業銀行%' or
bank_nm like '%第一商業銀行%' or
bank_nm like '%彰化商業銀行%' or
bank_nm like '%台灣中小企業%' or
bank_nm like '%臺南區中小企業銀行%' or
bank_nm like '%高雄區中小企業銀行%' or
bank_nm like '%花蓮區中小企業銀行%' or
bank_nm like '%臺東區中小企業銀行';


# UPDATE bank_attr SET stock_Type='B' where bank_code in 
(SELECT bank_Code from bank_attr where bank_nm like '%%華僑%%' or
bank_nm like '%上海%' or
bank_nm like '%世華%' or
bank_nm like '%中國國際%' or
bank_nm like '%中國信託%' or
bank_nm like '%玉山%' or
bank_nm like '%大眾%' or
bank_nm like '%日盛%' or
bank_nm like '%泛亞%' or
bank_nm like '%聯信%' or
bank_nm like '%台北銀行%' or
bank_nm like '%高雄銀行%' or
bank_nm like '%中華開發工業%' or
bank_nm like '%富邦%' or
bank_nm like '%台中商業銀行%' or
bank_nm like '%新竹國際商業銀行%' or
bank_nm like '%華南%' or
bank_nm like '%遠東%' or
bank_nm like '%萬泰%' or
bank_nm like '%中興%' or
bank_nm like '%聯邦%' or
bank_nm like '%慶豐%' or
bank_nm like '%誠泰%' or
bank_nm like '%陽信%' or
bank_nm like '%第七商業銀行%' or
bank_nm like '%板信%' or
bank_nm like '%台北國際%' or
bank_nm like '%中國農民%' or
bank_nm like '%中華開發%' or
bank_nm like '%華泰%' or
bank_nm like '%三信商業銀行%' or
bank_nm like '%第一商業銀行%' or
bank_nm like '%彰化商業銀行%' or
bank_nm like '%台灣中小企業%' or
bank_nm like '%臺南區中小企業銀行%' or
bank_nm like '%高雄區中小企業銀行%' or
bank_nm like '%花蓮區中小企業銀行%' or
bank_nm like '%臺東區中小企業銀行');

#外資銀行
update bank_attr set stock_type ='C' where bank_code in ('810','021','052','081');
update bank_attr set bank_code ='324' where bank_nm='美商花旗銀行' ;
select * from bank_attr where bank_code in ('810','021','052','081');
select bank_code,bank_nm from bank_attr where bank_nm like '%花旗%';
select bank_code,bank_nm,stock_type from bank_attr where bank_nm like '%花旗%';
#修正花旗
#insert into bank_attr (bank_code,bank_nm,stock_type,data_dt) values('021','花旗','C',NOW());
select bank_code,bank_nm from md_aum where bank_nm like '%花旗%';
update md_aum set bank_code='021' where bank_nm like '%花旗%';

select bank_code,bank_nm from md_aum where bank_nm like '%星展%';	
select bank_code,bank_nm from bank_attr where bank_nm like '%星展%';	