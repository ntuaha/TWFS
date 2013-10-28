<?php
 //$_GET["date"]="[\"1990-01-01\",\"2013-01-01\"]";
 //$_GET["column"]="[\"m1b\",\"cpi\",\"wpi\"]";
if(isset($_GET["date"])){

        $dates = json_decode($_GET["date"],true);
        $items = json_decode($_GET["column"],true); 
        $is = array();
        $ans = array();
	$dbconn = pg_connect("host=localhost port=5432 dbname=data user=aha password=dataaha305");

        
        //$d = date_create($date);
        $firstDayofYear = date("Y-m-d",mktime(0,0,0,1,1,intval(substr($date,0,4))));
        
        $sql = sprintf("SELECT %s,date_trunc('month',data_ym) as data_ym FROM PFEI WHERE data_ym between '%s' and '%s'",implode(",",$items),$dates[0],$dates[1]);
        $r = pg_query($dbconn,$sql);
        while($c = pg_fetch_array($r)){
                $dd = explode(" ",$c['data_ym']);
                $dd = $dd[0];
                foreach($items as $item){
                        if(!is_array($ans[$item])){
                                $ans[$item] = array();
                        }

                        $ans[$item][] = array("date"=>$dd,"value"=>$c[$item]);   
                }


        }

        
	echo json_encode($ans);
	pg_close($dbconn);
}


?>
