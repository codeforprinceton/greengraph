/* Place all the behaviors and hooks related to the matching controller here.
All this logic will automatically be available in application.js.*/

var electricdoughnut = function(comelectric, reselectric) {
    var dataelectric = {
    labels: [
        "Commercial",
        "Residential"
    ],
    datasets: [
        {
            data: [comelectric, reselectric],
            backgroundColor: [
                "#70E4EF",
                "#4D6CFA"
            ],
            hoverBackgroundColor: [
                "#48efff",
                "#617eff"
            ]
        }]
};

var optionselectric = {
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
  $('#allelectricchart').remove();
  $('#allelectricchartcontainer').append('<canvas id="allelectricchart"></canvas>');

   //draw the total gas usage bar chart
   var cty = document.getElementById("allelectricchart").getContext("2d");
   cty.canvas.width  = $('#allelectricchartcontainer').innerWidth() - 50;
   var allelectricchart = new Chart(cty,{
        type: 'pie',
        data: dataelectric,
        options: optionselectric
    });
};
