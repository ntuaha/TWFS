<?php
if(isset($_GET["date"])){
//$_GET["date"]="2013-06-01";
	$dbconn = pg_connect("host=localhost port=5432 dbname=data user=aha password=dataaha305");
	$sql = sprintf("SELECT * FROM PFEI WHERE data_ym = '%s'",$_GET["date"]);
	$r = pg_query($dbconn,$sql);
	$c = pg_fetch_array($r);
	$col1 = $c['cpi'];

        $sql = sprintf("SELECT cpi FROM PFEI WHERE data_ym = (timestamp '%s'-interval '1 month')",$_GET["date"]);
        $r = pg_query($dbconn,$sql);
        $c = pg_fetch_array($r);
        $col2_1 = $c['cpi'];
        $col2 = ($col1-$col2_1)/$col2_1;
        
        $sql = sprintf("SELECT cpi FROM PFEI WHERE data_ym = (timestamp '%s'-interval '1 year')",$_GET["date"]);
        $r = pg_query($dbconn,$sql);
        $c = pg_fetch_array($r);
        $col3_1 = $c['cpi'];
        $col3 = ($col1-$col3_1)/$col3_1;
      
	$sql = sprintf("SELECT data_Ym,cpi FROM PFEI WHERE data_ym between date_trunc('year',timestamp '%s') and timestamp '%s' order by data_Ym",$_GET["date"],$_GET["date"]);
        $r = pg_query($dbconn,$sql);
	$da = array();
	
        while($c = pg_fetch_array($r)){
        	$da[] = array("data_ym"=>$c[0],"cpi"=>$c[1]);
	}
 
        $c =array("col1"=>$col1,"col2"=>$col2,"col3"=>$col3,"col4"=>$da);
       
	echo json_encode($c);
	pg_close($dbconn);
}

?>
