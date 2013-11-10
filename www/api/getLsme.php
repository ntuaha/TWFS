<?php
 $_GET["date"]="[\"2010-01-01\",\"2013-01-01\"]";
 //$_GET["column"]="[\"m1b\",\"cpi\",\"wpi\"]";
if(isset($_GET["date"])){

        $dates = json_decode($_GET["date"],true);
        $is = array();
        $ans = array();
	$dbconn = pg_connect("host=localhost port=5432 dbname=data user=aha password=dataaha305");

        
        //$d = date_create($date);
        $firstDayofYear = date("Y-m-d",mktime(0,0,0,1,1,intval(substr($date,0,4))));
        
        $sql = sprintf("SELECT * FROM Lsme WHERE data_dt='%s' ORDER BY ln_sme desc;",$dates[0]);
        $r = pg_query($dbconn,$sql);
        while($c = pg_fetch_array($r)){
                if(trim($c["bank_code"])=='0')
                        continue;
                $dd = explode(" ",$c['data_dt']);
                $dd = $dd[0];
                $ans[] = array("date"=>$dd,
                        "bank_code"=>trim($c["bank_code"]),
                        "bank_nm"=>trim($c["bank_nm"]),
                        "ln_sme"=>$c["ln_sme"],
                        "ln_sme_rate"=>$c["ln_sme_rate"],
                        "market_rate"=>$c["market_rate"]
                        );   

        }

        
	echo json_encode($ans);
	pg_close($dbconn);
}


?>
