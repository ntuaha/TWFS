
$(function(){
drawGraphsForMonthlyData();
	
});
function show(data,legend_names,mmax,mmin){

  var radius = 77,
      minradius = 47,
      padding = 10;

var radius_scale = d3.scale.linear()
                    .domain([mmin, mmax])
                    .range([54, 84]);




  //var color = d3.scale.ordinal()
  //    .range(["#aaaaff", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);
  var color = d3.scale.category20();

  var arc = d3.svg.arc()
      .outerRadius(radius)
      .innerRadius(radius - 30);

  var pie = d3.layout.pie()
      .sort(null)
      .value(function(d) { return d.value; });
/*
  d3.csv("data.csv", function(error, data) {
    color.domain(d3.keys(data[0]).filter(function(key) { return key !== "State"; }));

    data.forEach(function(d) {
      d.ages = color.domain().map(function(name) {
        return {name: name, population: +d[name]};
      });
    });
*/
    color.domain(legend_names);

    var legend = d3.select("#chart").append("svg")
        .attr("class", "legend")
        .attr("width", radius * 2.5)
        .attr("height", radius * 2.5)
      .selectAll("g")
        .data(color.domain().slice().reverse())
      .enter().append("g")
        .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .text(function(d) { return d; });

    var svg = d3.select("#chart").selectAll(".pie")
        .data(data)
      .enter().append("svg")
        .attr("class", "pie")
        .attr("width", radius * 2.5)
        .attr("height", radius * 2.5)
      .append("g")
        .attr("transform", "translate(" + radius + "," + radius + ")");

    svg.selectAll(".arc")
        .data(function(d) { return pie(d.ln_info); })
      .enter().append("path")
        .attr("class", "arc")
        .attr("d", arc)
        .style("fill", function(d) { return color(d.data.name); })
        .attr("transform", function(d) {              

                d.innerRadius = minradius;
                d.outerRadius = radius_scale(d.sum);
   
        });

    svg.append("text")
        .attr("dy", ".35em")
        .style("text-anchor", "middle")
        .text(function(d) { return d.bank_name; });

}
var names = [];
function drawGraphsForMonthlyData() {
    // Get some random data
    //var data = getDataForMonth();
    $.ajax({
    dataType: "json",
    url: "./api/getLn.php",
    data: {
      'date':JSON.stringify(['2013-06-01'])
    },
    success: function( ajaxdata ) {
//AJAX START
      var data = [];
      var max = 0.0;
      var min = 1e18;
      var sum = 0.0;
      legend_names = ["房貸餘額","房屋整修餘額","汽車貸款餘額","員工福利貸款餘額","其他個人消費貸款餘額"];
      for (var i in ajaxdata){
        mortgage_bal = (parseFloat(ajaxdata[i].mortgage_bal))/1e6;
        decorator_hse_bal = parseFloat(ajaxdata[i].decorator_hse_bal)/1e6;
        ln_car_bal = parseFloat(ajaxdata[i].ln_car_bal)/1e6;
        ln_worker_bal = parseFloat(ajaxdata[i].ln_worker_bal)/1e6;
        other_cl_bal = parseFloat(ajaxdata[i].other_cl_bal)/1e6;

        sum = sum+mortgage_bal+decorator_hse_bal+ln_car_bal+ln_worker_bal+other_cl_bal;
        var row = {
          "bank_name":i,
          "sum":sum,
          "ln_info":[
          {name:"房貸餘額",value:mortgage_bal},
          {name:"房屋整修餘額",value:decorator_hse_bal},
          {name:"汽車貸款餘額",value:ln_car_bal},
          {name:"員工福利貸款餘額",value:ln_worker_bal},
          {name:"其他個人消費貸款餘額",value:other_cl_bal}
          ] 
        };

        if ((mortgage_bal+decorator_hse_bal+ln_car_bal+ln_worker_bal+other_cl_bal) >0.001 ){
          max = Math.max(max,mortgage_bal,decorator_hse_bal,ln_car_bal,ln_worker_bal,other_cl_bal);
          min = Math.min(min,mortgage_bal,decorator_hse_bal,ln_car_bal,ln_worker_bal,other_cl_bal);
          data.push(row);  
          //names.push([i,"#EFEFEF"]);
        }                
      }
      if (data.length!=0){
        show(data,legend_names,max,min);
      }
    }});
}
  

