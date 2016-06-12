/* Place all the behaviors and hooks related to the matching controller here.
All this logic will automatically be available in application.js.*/

var gasdoughnut = function(comgas, resgas) {
  var datagas = {
    labels: [
        "Commercial",
        "Residential"
    ],
    datasets: [
        {
            data: [comgas, resgas],
            backgroundColor: [
                "rgba(70,187,97,0.7)",
                "rgba(130,220,170,0.7)"
            ],
            hoverBackgroundColor: [
                "rgba(70,187,97,1)",
                "rgba(130,220,170,1)"
            ]
        }]
};


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
  };

  //ugly hack to clear old chart on refresh
  $('#allgaschart').remove();
  $('#allgaschartcontainer').append('<canvas id="allgaschart" auto-legend></canvas>');

  //draw the total gas usage bar chart
  var cty = document.getElementById("allgaschart").getContext("2d");
  cty.canvas.width  = $('#allgaschartcontainer').innerWidth() - 50;
  var allgaschart = new Chart(cty,{
        type: 'pie',
        data: datagas,
        options: optionsgas
    });
};
