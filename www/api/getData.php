<?php
// $_GET["date"]="[\"2013-06-01\",\"2013-05-01\",\"2012-06-01\"]";
// $_GET["item"]="[\"m1b\",\"cpi\",\"wpi\"]";
if(isset($_GET["date"])){

        $dates = json_decode($_GET["date"],true);
        $items = json_decode($_GET["column"],true);     
        $ans = array();
	$dbconn = pg_connect("host=localhost port=5432 dbname=data user=aha password=dataaha305");
        
        foreach($dates as $date){
                $sql = sprintf("SELECT %s FROM PFEI WHERE data_ym = '%s'",implode(",",$items),$date);
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
if(isset($_GET["ValidFromDt"])&&isset($_GET["ValidToDt"])&&isset($_GET["item"])){
        //取得時間區間
        //strtotime
  
        $ValidFromDt = date_format(date_create($_GET["ValidFromDt"]), 'Y-m-d');
        $ValidToDt = date_format(date_create($_GET["ValidToDt"]), 'Y-m-d');
        //取得item所有資訊
        $items = json_decode($_GET["item"],true);
        foreach($item as $items){

        }
        

}

?>
