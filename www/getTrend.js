
$(function(){
	
	var showDate = new Date(2013,06,05);
	getTrend(['1900-01-01',showDate],['cpi','stock_index','f_ins_dp','f_ins_ln']);
	
});
function plotSVG(dom,input){
	
var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = $(dom).width() - margin.left - margin.right,
    height = $(dom).width()*0.6- margin.top - margin.bottom;

var parseDate = d3.time.format("%Y-%m-%d").parse;
var xscale = d3.time.scale().range([0, width]);
var yscale = d3.scale.linear().range([height, 0]);
var xAxis = d3.svg.axis().scale(xscale).orient("bottom");
var yAxis = d3.svg.axis().scale(yscale).orient("left").tickFormat(function(d) { if(d<1.0){return d3.format("%")(d);}else if(d>1e6){ return (d3.format("s"))(d);}else{return d;} });
var line = d3.svg.line().x(function(d) { return xscale(d.d); }).y(function(d) { return yscale(d.v); });

//放置DOM的位置
var svg = d3.select(dom).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


for (i in input){
	input[i].d = parseDate(input[i].date);
	input[i].v = parseFloat(input[i].value);
}

  xscale.domain(d3.extent(input, function(d) { return d.d; }));
  yscale.domain(d3.extent(input, function(d) { return d.v; }));


  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end");
      //.text("CPI (2011=100)");

  svg.append("path")
      .datum(input)
      .attr("class", "line")
      .attr("d", line);

}

function getTrend(d,c){
	$.ajax({
		dataType: "json",
		url: "./api/getTrend.php",
		data: {
			'date':JSON.stringify(d),
			'column':JSON.stringify(c) 
		},
		success: function( data ) {

			plotSVG("#CPI",data['cpi']);
		      plotSVG("#STOCK",data['stock_index']);
		      plotSVG("#F_Ins_Dp",data['f_ins_dp']);
		      plotSVG("#F_Ins_Ln",data['f_ins_ln']);
		      var t = [];
		      for(i in data['f_ins_dp']){
		      	 var ratio = parseFloat(data['f_ins_ln'][i].value) / parseFloat(data['f_ins_dp'][i].value);
		      	 var date = data['f_ins_ln'][i].date;
		      	 t.push({'date':date,'value':ratio});
		      }
		      plotSVG("#F_DP_LN_RATIO",t);
		      

		}
	});
}
