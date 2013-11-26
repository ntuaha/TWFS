<?php
 //$_GET["date"]="[\"2013-01-01\"]";
 //$_GET["column"]="[\"Mortgage_Bal\",\"Decorator_Hse_Bal\",\"Ln_Workder_Bal\",\"Other_CL_Bal\"]";
if(isset($_GET["date"])){

    $dates = json_decode($_GET["date"],true);
    //$items = json_decode($_GET["column"],true); 
    $is = array();
    $ans = array();
	$dbconn = pg_connect("host=localhost port=5432 dbname=data user=aha password=dataaha305");

    //$firstDayofYear = date("Y-m-d",mktime(0,0,0,1,1,intval(substr($date,0,4))));
        
    $sql = sprintf("SELECT *,date_trunc('month',Cc.data_dt) as data_dt_show FROM Cc left join Bank_attr as B on (Cc.Bank_nm=b.bank_nm) WHERE Cc.data_dt between '2012-07-01' and '2013-06-01' and B.Bank_Type_Cd=1 order by Cc.data_dt asc,Cc.bank_code asc;",$dates[0]);
    //echo $sql;
    $r = pg_query($dbconn,$sql);
    while($c = pg_fetch_array($r)){
        $add = false;
        foreach($ans as $key => $v){
            if ($ans[$key]["name"] == $c[3]){
                if(!is_array($ans[$key]["values"])){
                    $ans[$key]["values"] = array();                    
                }
                $ans[$key]["values"][]=array("date"=>explode(" ",$c["data_dt_show"])[0],"temperature"=>$c["cc_open_card_cnt"]);
                $add = true;
                break;
            }
        }
        if($add==false){
            $ans[] = array("name"=>$c[3],"values"=>array());
            $ans[$c[3]]["values"][]=array("date"=>explode(" ",$c["data_dt_show"])[0],"temperature"=>$c["cc_open_card_cnt"]);
        }

        /*
        $dd = explode(" ",$c['data_dt'])[0]; 
        if(is_array($ans[$dd])){
            if(!is_array($ans[$c["bank_nm"]])){
                $ans[$c["bank_nm"]] = array();
            }
            foreach($c as $ck => $cs){
                if ($ck=="data_dt_show"){
                    $ans[$c["bank_nm"]][$ck] = explode(" ",$cs)[0];        
                }else{
                    $ans[$c["bank_nm"]][$ck] = $cs;        
                }
            }

        }
        */
            
    }

        
	echo json_encode($ans);
	pg_close($dbconn);
}


?>
