<?php
 $_GET["bank"]="玉山商業銀行";
 $_GET["year"]=2013;
 $_GET["month"]=10;
 //$_GET["column"]="[\"m1b\",\"cpi\",\"wpi\"]";
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
if(isset($_GET["bank"])){

    $ans = array();
	$dbconn = pg_connect("host=localhost port=5432 dbname=data user=aha password=dataaha305");
	$date = date("Y-m-d",mktime(0,0,0,$_GET["month"],1,$_GET["year"]));
	$check = array();

	
	$check["中小企業放款"] = "LN_SME";
	$check["中小企業放款佔整體存款比例"] = "LN_SME_RATE";
	$show["中小企業放款"]=0;
	$show["中小企業放款佔整體存款比例"]=1;
	foreach($check as $key=>$value){
		$sql = sprintf("SELECT bank_nm,%s FROM LSME where data_dt='%s' and bank_nm not in ('總計','小計') order by %s desc",$value,$date,$value);	
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
		echo sprintf("<div>%s, %s 在 %s 排名%d 餘額為%s,%s目前是%s在前面,而%s目前是%s在後面 </div>",$date,$bank,$key,$rank,show($show[$key],$v),$prev_bank,show($show[$key],$prev_v),$next_bank,show($show[$key],$next_v));
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
