<?php
 $_GET["bank"]="玉山商業銀行";
 $_GET["year"]=2013;
 $_GET["month"]=10;
 //$_GET["column"]="[\"m1b\",\"cpi\",\"wpi\"]";
if(isset($_GET["bank"])){

    $ans = array();
	$dbconn = pg_connect("host=localhost port=5432 dbname=data user=aha password=dataaha305");
	$date = date("Y-m-d",mktime(0,0,0,$_GET["month"],1,$_GET["year"]));
	$check = array();
	$check["信用卡流通卡數"] = "Cc_F_Card_Cnt";
	$check["信用卡有效卡數"] = "Cc_Open_Card_Cnt";
	$check["信用卡本月發卡數"] = "Cc_Issue_Card_Cnt";
	$check["本月簽帳金額"] = "Cyc_Bal";
	$check["循環信用餘額"] = "Cc_Txn_Bal";
	$check["本月預借現金金額"] = "Cc_Ln_Bal";
	$check["循環信用利息收入"] = "Cyc_Income";
	$check["簽帳手續費收入"] = "Txn_Fee";
	$check["預借現金手續費"] = "Cc_Ln_Fee";
	foreach($check as $key=>$value){
		$sql = sprintf("SELECT bank_nm,%s FROM CC where data_dt='%s' and bank_nm not in ('總計','小計') order by %s desc",$value,$date,$value);	
		//echo $sql."<br>";
		$r = pg_query($dbconn,$sql);
		$rank = 1;
		$prev_bank = "";
		$prev_bank = 0;
		$next_bank = "";
		$next_v = 0;
		$bank = "";
		$v = 0;
		$quit = 0;
		while($c = pg_fetch_array($r)){
			//echo sprintf("%d,%s,%s,%.0f<br>",$rank,$c["bank_nm"],$value,$c[strtolower($value)]);
			if($quit==1){
				$next_bank = $c["bank_nm"];
				$next_v = $c[strtolower($value)];
				break;
			}
			$prev_bank = $bank;
			$prev_v = $v;
			if($c["bank_nm"]==$_GET["bank"]){
				$quit= 1;
			}
			$bank = $c["bank_nm"];
			$v = $c[strtolower($value)];
			$rank+=1;
			//echo sprintf("%s,%s,%s,%s<br>",$prev_bank,$prev_v,$bank,$v);
		}
		$rank -=1;
		echo sprintf("<div>%s, %s 在 %s 排名%d 餘額為%d,%s在前面，目前是%d,而%s在後面,目前是%d </div>",$date,$bank,$key,$rank,$v,$prev_bank,$prev_v,$next_bank,$next_v);
	}
	

        
        // $sql = sprintf("SELECT %s,date_trunc('month',data_ym) as data_ym FROM PFEI WHERE data_ym between '%s' and '%s'",implode(",",$items),$dates[0],$dates[1]);
        // $r = pg_query($dbconn,$sql);
        // while($c = pg_fetch_array($r)){
        //         $dd = explode(" ",$c['data_ym']);
        //         $dd = $dd[0];
        //         foreach($items as $item){
        //                 if(!is_array($ans[$item])){
        //                         $ans[$item] = array();
        //                 }

        //                 $ans[$item][] = array("date"=>$dd,"value"=>$c[$item]);   
        //         }


        // }

        
	echo json_encode($ans);
	pg_close($dbconn);
}


?>
