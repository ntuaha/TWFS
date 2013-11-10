
$(function(){
	
	var showDate = new Date(2013,06,05);
	getTrend(['1900-01-01',showDate],['cpi','stock_index','f_ins_dp','f_ins_ln']);
	getLsme([showDate]);
	
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
			

function getTrend(d,c,t){
	$.ajax({
		dataType: "json",
		url: "./api/getTrend.php",
		data: {
			'table':JSON.stringify(t),
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




function getLsme(d){
	$.ajax({
		dataType: "json",
		url: "./api/getLsme.php",
		data: {
			'date':JSON.stringify(d)
		},
		success: function( data ) {

			plotBarChart("#LSME",data);
		}
	});
}
function plotBarChart(dom,data){
	var margin = {top: 50, right: 20, bottom: 30, left: 50},
    width = $(dom).width() - margin.left - margin.right,
    height = $(dom).width()*0.3- margin.top - margin.bottom;


var formatPercent = d3.format(".0%");

var x = d3.scale.ordinal().rangeRoundBands([0, width], .1);
var y = d3.scale.linear().range([height, 0]);


var xAxis = d3.svg.axis().scale(x).orient("bottom").tickFormat(function(d){var s = "";
 for (i in d){
 	s = s+'\r\n'+d[i];
 }
 return s;
}
);

var yAxis = d3.svg.axis().scale(y).orient("left").tickFormat( d3.format("s"));

var tip = d3.tip().attr('class', 'd3-tip').offset([-10, 0])
  .html(function(d) {
    return "<strong>Frequency:</strong> <span style='color:red'>" + d.bank_nm + "放款中有"+d3.format(".2%")(parseFloat(d.ln_sme_rate)/100.0)+"為中小企業</span>";
  })

var svg = d3.select(dom).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.call(tip);

/*
d3.tsv("data.tsv", type, function(error, data) {
  x.domain(data.map(function(d) { return d.letter; }));
  y.domain([0, d3.max(data, function(d) { return d.frequency; })]);
  */

  x.domain(data.map(function(d) { return d.bank_nm; }));
  var max = 0
  for (i in data){
  	if (max<parseFloat(data[i].ln_sme))
  		max = parseFloat(data[i].ln_sme);
  }

  y.domain([0,max]);
  var z = d3.scale.linear().domain([0.0,0.4]).range(["blue","green"]);
  var z2 = d3.scale.linear().domain([0.0,0.4]).range([d3.rgb("blue").brighter(2),d3.rgb("green").brighter(2)]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")      
      .attr("y", -15)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("貸款金額");

  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("dy", "3em")
      .attr("x", function(d) { return x(d.bank_nm); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.ln_sme); })
      .attr("height", function(d) { return height - y(d.ln_sme); })
      .attr("fill",function(d){ return z(parseFloat(d.ln_sme_rate)/100.0); })
      .on()
      .on('mouseover',function(d,event,d){
      	d3.select(this)
			.transition()
			.duration(500)
			.attr("fill",function(d){ return z2(parseFloat(d.ln_sme_rate)/100.0); })
      	tip.show(this.__data__);
      })
      .on('mouseout', function(d,event,d){
      		d3.select(this)
			.transition()
			.duration(500)
			.attr("fill",function(d){ return z(parseFloat(d.ln_sme_rate)/100.0); })
      		tip.hide(this.__data__);
      })

var label = svg.selectAll("text")
.data(data)
.enter().append("text")
// REOVE THIS: .attr("x", function(d) { return x(d)+x.rangeBand()/2; })
// AND THIS TOO: .attr("y", 6)
.attr("text-anchor", "middle")
.attr("dy", ".71em")
.attr("y", function(d) { return y(0); })
.attr("x", function(d) { return x(d.bank_nm); })
.text(function(d) {return d.bank_nm})
.attr("transform", function(d) {    // transform all the text elements
  return "rotate(-90)";            // THEN rotate them to give a nice slope
});


}
function type(d) {
  d.frequency = +d.frequency;
  return d;
}

