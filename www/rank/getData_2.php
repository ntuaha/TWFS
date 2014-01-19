<?php
 
 function show($mode,$v){
 	if($mode==0){//數字
 		if($v>1e9)
 			return sprintf("%.0f億",$v/1e8);
 		else if($v>1e8)
 			return sprintf("%.2f億",$v/1e8);
 		else if($v>1e5)
 			return sprintf("%.0f萬",$v/1e4);
 		else if($v>1e4)
 			return sprintf("%.2f萬",$v/1e4);
 		else if($v>100)
 			return sprintf("%.0",$v);
 		else
 			return sprintf("%.2",$v);

 	}else if($mode==1){ //百分比
 		return sprintf("%.1f%%",$v);

 	}
 }
function t($v1,$v2){
	$r = (floatval($v2)-floatval($v1))/floatval($v1)*100.0;
	return $r;
}

function GG($table,$column,$title){

	$dbconn = pg_connect("host=localhost port=5432 dbname=data user=aha password=dataaha305");
	$date1 = date("Y-m-d",mktime(0,0,0,12,1,2012));
	$date2 = date("Y-m-d",mktime(0,0,0,11,1,2013));

	$sql = sprintf("SELECT A.bank_code,B.bank_nm,%s,B.stock_type FROM %s as A left join bank_attr as B on (A.bank_code = B.bank_code) where B.stock_type<>'A' and A.data_dt='%s' and A.bank_nm not in ('總計','小計') order by %s desc,length(B.bank_nm) desc",$column,$table,$date2,$column);
	//echo "123<br/>";
	//echo $sql."<br>";
	$r = pg_query($dbconn,$sql);
	$rank = 1;
	$bank_list = array();
	$prev='';
	while($c = pg_fetch_array($r)){
		if($prev!=$c["bank_code"]){
			$bank_list[$c["bank_code"]] = array("name"=>$c["bank_nm"],"type"=>$c["stock_type"],"rank"=>$rank,"v"=>$c[$column]);
			$prev = $c["bank_code"];
			$rank++;	
		}
	}
	$rank = 1;
	$prev='';
	$sql = sprintf("SELECT A.bank_code,B.bank_nm,%s,B.stock_type FROM %s as A left join bank_attr as B on (A.bank_code = B.bank_code) where B.stock_type<>'A' and A.data_dt='%s' and A.bank_nm not in ('總計','小計') order by %s desc,length(B.bank_nm) desc",$column,$table,$date1,$column);
	$r = pg_query($dbconn,$sql);
	while($c = pg_fetch_array($r)){
		if($prev!=$c["bank_code"]){
			$bank_list[$c["bank_code"]]["prev_rank"] = $rank;
			$bank_list[$c["bank_code"]]["prev_v"] = $c[$column];
			$prev = $c["bank_code"];
			$rank++;
		}
			
		
	}
	echo sprintf("<H2>%s</H2>",$title);
	echo "<table><tr>";
	$num=1;
	foreach($bank_list as $key => $value){
		if($value["name"]=="建華商業銀行"){
			$value["name"]="永豐商業銀行";
		}
		if($num%12==1 and $num!=1){
			echo "</tr><tr>";
		}
		if(trim($key)=="808"){
			if($value["prev_rank"]>$value["rank"]){
			echo sprintf("<td style='height:60px;width=200px'><div style='background:green;color:yellow'>%s</div><div style='background:red;color:white'>%s => %s (%+.2f%%)</div></td>",$key."<br/>".$value["name"],$value["prev_rank"],$value["rank"],t($value["prev_v"],$value["v"]));
			}elseif($value["prev_rank"]<$value["rank"]){	
				echo sprintf("<td style='height:60px;width=200px'><div style='background:green;color:yellow'>%s</div><div style='background:green;color:white'>%s => %s (%+.2f%%)</div></td>",$key."<br/>".$value["name"],$value["prev_rank"],$value["rank"],t($value["prev_v"],$value["v"]));

			}else{
				echo sprintf("<td style='height:60px;width=200px'><div style='background:green;color:yellow'>%s</div><div style='background:gray;color:white'>%s => %s (%+.2f%%)</div></td>",$key."<br/>".$value["name"],$value["prev_rank"],$value["rank"],t($value["prev_v"],$value["v"]));

			}
			
		}else{
			if($value["prev_rank"]>$value["rank"]){
			echo sprintf("<td style='height:60px;width=200px'><div>%s</div><div style='background:red;color:white'>%s => %s (%+.0f%%)</div></td>",$key."<br/>".$value["name"],$value["prev_rank"],$value["rank"],t($value["prev_v"],$value["v"]));
			}elseif($value["prev_rank"]<$value["rank"]){	
				echo sprintf("<td style='height:60px;width=200px'><div>%s</div><div style='background:green;color:white'>%s => %s (%+.0f%%)</div></td>",$key."<br/>".$value["name"],$value["prev_rank"],$value["rank"],t($value["prev_v"],$value["v"]));

			}else{
				echo sprintf("<td style='height:60px;width=200px'><div>%s</div><div style='background:gray;color:white'>%s => %s (%+.0f%%)</div></td>",$key."<br/>".$value["name"],$value["prev_rank"],$value["rank"],t($value["prev_v"],$value["v"]));

			}
		}
		
		$num++;
		if($num==24)
			break;
			

	}
	echo "</tr></table><hr>";



	
        
	//echo json_encode($bank_list);
	pg_close($dbconn);
}	
echo "<h1>2013民營銀行排名變化</h1>";
GG("MD_Aum","md_aum","活期存款平均餘額");
GG("ln_Aum","ln_aum","放款平均餘額");
GG("lsme","ln_sme","中小企業放款餘額");
GG("cc","cc_open_card_cnt","信用卡有效卡數");
GG("cl_info","mortgage_bal","房貸餘額");


?>
