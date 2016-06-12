

/* Place all the behaviors and hooks related to the matching controller here.
All this logic will automatically be available in application.js.*/

var gasbar = function(comgas, resgas) {

var datagasbar = {
    labels: ["Commercial", "Residential"],
    datasets: [
        {
            label: "All gas consumed in THM since 2009",
            backgroundColor: "rgba(255,99,132,0.2)",
            borderColor: "rgba(255,99,132,1)",
            borderWidth: 1,
            hoverBackgroundColor: "rgba(255,99,132,0.4)",
            hoverBorderColor: "rgba(255,99,132,1)",
            data: [comgas, resgas],
        }
    ]
};


  var optionsgasbar = {
  };

  //ugly hack to clear old chart on refresh
  $('#allgaschartbar').remove();
  $('#allgaschartbarcontainer').append('<canvas id="allgaschartbar" auto-legend></canvas>');

  //draw the total gas usage bar chart
  var cty = document.getElementById("allgaschartbar").getContext("2d");
  cty.canvas.width  = $('#allgaschartbarcontainer').innerWidth() - 50;
  var gasbarchart = new Chart(cty, {
    type: 'horizontalBar',
    data: datagasbar,
    options: optionsgasbar
    });
};