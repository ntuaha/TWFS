<?php
 //$_GET["date"]="[\"2013-06-01\",\"2012-06-01\"]";
 //$_GET["column"]="[\"m1b\",\"cpi\",\"wpi\"]";
if(isset($_GET["date"])){

        $dates = json_decode($_GET["date"],true);
        $items = json_decode($_GET["column"],true); 
        $is = array();
        foreach($items as $item){
                $is[] = sprintf("avg(%s) as %s",$item,$item);
        }    
        $ans = array();
	$dbconn = pg_connect("host=localhost port=5432 dbname=data user=aha password=dataaha305");

        foreach($dates as $date){
                //$d = date_create($date);
                $firstDayofYear = date("Y-m-d",mktime(0,0,0,1,1,intval(substr($date,0,4))));
                
                $sql = sprintf("SELECT %s FROM PFEI WHERE data_ym between '%s' and '%s'",implode(",",$is),$firstDayofYear,$date);
                $r = pg_query($dbconn,$sql);
                $c = pg_fetch_array($r);
                foreach($items as $item){
                        if(!is_array($ans[$item])){
                                $ans[$item] = array();
                        }
                        $ans[$item][$date] = $c[$item];                        
                }
        }
	echo json_encode($ans);
	pg_close($dbconn);
}


?>
