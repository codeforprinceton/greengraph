/* Place all the behaviors and hooks related to the matching controller here.
All this logic will automatically be available in application.js.*/

var gasdoughnut = function(comgas, resgas) {

  var datagas = [
      {
          label: "Commercial",
          value: comgas,
          color:"#CE8147",
          highlight: "#f59a55",
      },
      {
          label: "Residential",
          value: resgas,
          color: "#561D25",
          highlight: "#762833",
      },
  ]

  var optionsgas = {
      //Boolean - Whether we should show a stroke on each segment
      segmentShowStroke : true,

      //String - The colour of each segment stroke
      segmentStrokeColor : "#fff",

      //Number - The width of each segment stroke
      segmentStrokeWidth : 2,

      //Number - The percentage of the chart that we cut out of the middle
      percentageInnerCutout : 50, // This is 0 for Pie charts

      //Number - Amount of animation steps
      animationSteps : 100,

      //String - Animation easing effect
      animationEasing : "easeOutBounce",

      //Boolean - Whether we animate the rotation of the Doughnut
      animateRotate : true,

      //Boolean - Whether we animate scaling the Doughnut from the centre
      animateScale : false,

      legendTemplate : '<ul class=gas-legend>'
                        +  '<li><span style=\"background-color:#F7464A\"></span>Commercial</li>'
                        +  '<li><span style=\"background-color:#46BFBD\"></span>Residential</li>'
                        + '</ul>'
  };

  //ugly hack to clear old chart on refresh
  $('#allgaschart').remove();
  $('#allgaschartcontainer').append('<canvas id="allgaschart" auto-legend></canvas>');

  //draw the total gas usage bar chart
  var cty = document.getElementById("allgaschart").getContext("2d");
  cty.canvas.width  = $('#allgaschartcontainer').innerWidth() - 50;
  var allgaschart = new Chart(cty).Doughnut(datagas, optionsgas);
};
