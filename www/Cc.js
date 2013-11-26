
$(function(){
drawGraphsForMonthlyData();
	
});
function show(date,banks,cities){

var margin = {top: 20, right: 100, bottom: 30, left: 100},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y-%m-%d").parse;

var x = d3.time.scale().range([0, width]);
var y = d3.scale.linear().range([height, 0]);
var color = d3.scale.category10();
var xAxis = d3.svg.axis().scale(x).orient("bottom");
var yAxis = d3.svg.axis().scale(y).orient("left");


var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
color.domain(banks);
/*
data.forEach(function(d) {
    d.date = parseDate(d.date);
});
*/
/*
d3.tsv("data.tsv", function(error, data) {
  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));

  data.forEach(function(d) {
    d.date = parseDate(d.date);
  });

  var cities = color.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(d) {
        return {date: d.date, temperature: +d[name]};
      })
    };
  });
*/
  x.domain(d3.extent(date, function(d) { return d; }));

  y.domain([
    //d3.min(cities, function(c) { return d3.min(c.values, function(v) { return v.temperature; }); }),
    0,
    d3.max(cities, function(c) { return d3.max(c.values, function(v) { return v.temperature; }); })
  ]);
var line = d3.svg.line()
    .interpolate("basis")
    .x(function(d) { 
      return x(parseDate(d.date)); 
    })
    .y(function(d) { 
      return y(d.temperature);
     });

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
      .style("text-anchor", "end")
      .text("流通卡數()");

  var city = svg.selectAll(".city")
      .data(cities)
    .enter().append("g")
      .attr("class", "city");

  city.append("path")
      .attr("class", "line")
      .attr("d", function(d) { 
        return line(d.values); 
      }).style("stroke", function(d) { return color(d.name); });

  city.append("text")
      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.date2) + "," + y(d.value.temperature) + ")"; })
      .attr("x", 3)
      .attr("dy", ".35em")
      .text(function(d) { return d.name; });



}
var names = [];
function drawGraphsForMonthlyData() {
    // Get some random data
    //var data = getDataForMonth();
    $.ajax({
    dataType: "json",
    url: "./api/getCC.php",
    data: {
      'date':JSON.stringify(['2013-06-01'])
    },
    success: function( ajaxdata ) {
//AJAX START
      var parseDate = d3.time.format("%Y-%m-%d").parse;
      for (i in ajaxdata){
        for(k in ajaxdata[i]["values"]){
          ajaxdata[i]["values"][k]["date2"]=parseDate(ajaxdata[i]["values"][k]["date"]);
          ajaxdata[i]["values"][k]["temperature"] = parseFloat(ajaxdata[i]["values"][k]["temperature"]);
        }
      }
     
      var banks=["中國信託商業銀行","國泰世華商業銀行","台新國際商業銀行","花旗(台灣)商業銀行","玉山商業銀行","遠東國際商業銀行"];
      var date =["2012-08-01","2012-09-01","2012-10-01","2012-11-01","2012-12-01","2013-01-01",
      "2013-02-01","2013-03-01","2013-04-01","2013-05-01","2013-06-01"];
      for (var i in date){
        date[i] = parseDate(date[i]);
      }
      var d = [];
      for (i in ajaxdata){
        for (j in banks){
          if (ajaxdata[i]["name"]==banks[j]){
            
            d.push(ajaxdata[i]); 
           
          } 
        }
        
      }
     
      if (d.length!=0){
        show(date,banks,d);
      }
    }});
}
  

