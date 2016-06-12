

/* Place all the behaviors and hooks related to the matching controller here.
All this logic will automatically be available in application.js.*/

var gasbar = function(comgas, resgas) {

var datagasbar = {
    labels: ["Gas in THM"],
    datasets: [
        {
            label: "Commercial",
            backgroundColor: "rgba(255,99,132,0.2)",
            borderColor: "rgba(255,99,132,1)",
            borderWidth: 1,
            hoverBackgroundColor: "rgba(255,99,132,0.4)",
            hoverBorderColor: "rgba(255,99,132,1)",
            data: [comgas],
        },
        {
            label: "Resedential",
            backgroundColor: "rgba(155,99,132,0.2)",
            borderColor: "rgba(155,99,132,1)",
            borderWidth: 1,
            hoverBackgroundColor: "rgba(155,99,132,0.4)",
            hoverBorderColor: "rgba(155,99,132,1)",
            data: [resgas],
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


/* Place all the behaviors and hooks related to the matching controller here.
All this logic will automatically be available in application.js.*/

var electricbar = function(comelectric, reselectric) {

var dataelectricbar = {
    labels: ["Electricity in KWH"],
    datasets: [
        {
            label: "Commercial",
            backgroundColor: "rgba(255,99,132,0.2)",
            borderColor: "rgba(255,99,132,1)",
            borderWidth: 1,
            hoverBackgroundColor: "rgba(255,99,132,0.4)",
            hoverBorderColor: "rgba(255,99,132,1)",
            data: [comelectric],
        },
        {
            label: "Resedential",
            backgroundColor: "rgba(155,99,132,0.2)",
            borderColor: "rgba(155,99,132,1)",
            borderWidth: 1,
            hoverBackgroundColor: "rgba(155,99,132,0.4)",
            hoverBorderColor: "rgba(155,99,132,1)",
            data: [reselectric],
        }
    ]
};


  var optionselectricbar = {
  };

  //ugly hack to clear old chart on refresh
  $('#allelectricbarchart').remove();
  $('#allelectricbarchartcontainer').append('<canvas id="allelectricbarchart"></canvas>');

   //draw the total electric usage bar chart
  var cty = document.getElementById("allelectricbarchart").getContext("2d");
  cty.canvas.width  = $('#allelectricbarchartcontainer').innerWidth() - 50;
  var gasbarchart = new Chart(cty, {
    type: 'horizontalBar',
    data: dataelectricbar,
    options: optionselectricbar
    });
};
