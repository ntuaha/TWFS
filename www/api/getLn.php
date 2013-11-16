<?php
 //$_GET["date"]="[\"2013-01-01\"]";
 //$_GET["column"]="[\"Mortgage_Bal\",\"Decorator_Hse_Bal\",\"Ln_Workder_Bal\",\"Other_CL_Bal\"]";
if(isset($_GET["date"])){

        $dates = json_decode($_GET["date"],true);
        //$items = json_decode($_GET["column"],true); 
        $is = array();
        $ans = array();
	$dbconn = pg_connect("host=localhost port=5432 dbname=data user=aha password=dataaha305");

        
        //$d = date_create($date);
        $firstDayofYear = date("Y-m-d",mktime(0,0,0,1,1,intval(substr($date,0,4))));
        
        $sql = sprintf("SELECT *,date_trunc('month',data_dt) as data_dt_show FROM CL_INFO WHERE data_dt = '%s' order by bank_code",$dates[0]);
        //echo $sql;
        $r = pg_query($dbconn,$sql);
        while($c = pg_fetch_array($r)){
          //      print_r($c);
                  $dd = explode(" ",$c['data_dt']);
          //      $dd = $dd[0];
                if(!is_array($ans[$c["bank_nm"]])){
                        $ans[$c["bank_nm"]] = array();
                }
                foreach($c as $ck => $cs){
                        $ans[$c["bank_nm"]][$ck] = $cs;        
                }
                
        }

        
	echo json_encode($ans);
	pg_close($dbconn);
}


?>
