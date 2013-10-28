var monthFormat = d3.time.format("%Y-%m-%d");
var percentFormat = d3.format(".2f");
var insertValue = function(id,value,suffix){
	var v = parseFloat(value);
	if(v>0){
		$("#"+id).html("漲 "+value+suffix).addClass("label label-important");
	}else if(v<0){
		$("#"+id).html("跌 "+value+suffix).addClass("label label-success");
	}else{
		$("#"+id).html("無任何變化").addClass("label");
	}
}
var date_array = null;
$(function(){
	
	var showDate = new Date(2013,06,05);
	
	setDate(showDate);
	Month(date_array,["cpi","wpi"]);
	MeanValue([date_array[0],date_array[2]],["cpi","wpi"]);

	//補上月份
	$(".year").html(showDate.getYear()+1900);
	$(".month").html(showDate.getMonth());
});
function setDate(d){
	//歸到月初
	var date1 = new Date(d.getYear()+1900,d.getMonth()-1,1);
	//上一個月
	var date2 = new Date(date1);
	date2.setMonth(date2.getMonth() - 1);	
	//去年同一時間
	var date3 = new Date(date1);
	date3.setYear(date3.getYear()+1900 - 1);
	date_array= [monthFormat(date1),monthFormat(date2),monthFormat(date3)];
}

function MeanValue(d,c){
	$.ajax({
		dataType: "json",
		url: "./api/getMean.php",
		data: {
			'date':JSON.stringify(d),
			'column':JSON.stringify(c) 
		},
		success: function( data ) {
			
			var cpi_0 = parseFloat(data["cpi"][date_array[0]]);
			var cpi_1 = parseFloat(data["cpi"][date_array[2]]);
			//累積yoy
			var temp = percentFormat((cpi_0-cpi_1)/cpi_1*100);
			insertValue("col4",temp,"%");
		}
	});
}

function Month(d,c){
	$.ajax({
		dataType: "json",
		url: "./api/getData.php",
		data: {
			'date':JSON.stringify(d),
			'column':JSON.stringify(c) 
		},
		success: function( data ) {
			
			var cpi_0 = parseFloat(data["cpi"][date_array[0]]);
			var cpi_1 = parseFloat(data["cpi"][date_array[1]]);
			var cpi_2 = parseFloat(data["cpi"][date_array[2]]);
			//當月資料
			$("#col1").html(cpi_0);
			//mom
			insertValue("col2",percentFormat((cpi_0-cpi_1)/cpi_1*100),"%");
			//yoy
			insertValue("col3",percentFormat((cpi_0-cpi_2)/cpi_2*100),"%");
		}
	});
}
