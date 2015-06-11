/* Place all the behaviors and hooks related to the matching controller here.
All this logic will automatically be available in application.js.*/

var biggraph = function(bigchartlabels, bigchartdata) {

var biggraphdata = {
    labels: bigchartlabels,
    datasets: [
        {
            label: "Energy usage in kWh",
            fillColor: "rgba(219, 244, 173, .6)",
            strokeColor: "rgba(86, 130, 89, 1)",
            pointColor: "rgba(86, 130, 89, 1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(86, 130, 89, 1)",
            data: bigchartdata
          }
    ]
};


var biggraphoptions = {
    //Boolean - Whether grid lines are shown across the chart
    scaleShowGridLines : true,

    //String - Colour of the grid lines
    scaleGridLineColor : "rgba(0,0,0,.05)",

    //Number - Width of the grid lines
    scaleGridLineWidth : 1,

    //Boolean - Whether to show horizontal lines (except X axis)
    scaleShowHorizontalLines: true,

    //Boolean - Whether to show vertical lines (except Y axis)
    scaleShowVerticalLines: true,

    //Boolean - Whether the line is curved between points
    bezierCurve : true,

    //Number - Tension of the bezier curve between points
    bezierCurveTension : 0.4,

    //Boolean - Whether to show a dot for each point
    pointDot : true,

    //Number - Radius of each point dot in pixels
    pointDotRadius : 4,

    //Number - Pixel width of point dot stroke
    pointDotStrokeWidth : 1,

    //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
    pointHitDetectionRadius : 20,

    //Boolean - Whether to show a stroke for datasets
    datasetStroke : true,

    //Number - Pixel width of dataset stroke
    datasetStrokeWidth : 2,

    //Boolean - Whether to fill the dataset with a colour
    datasetFill : true,

};

//ugly hack to clear old chart on refresh
  $('#biggraph').remove();
  $('#biggraphcontainer').append('<canvas id="biggraph"></canvas>');
    //draw the total gas usage bar chart
    var cty = document.getElementById("biggraph").getContext("2d");
    cty.canvas.width  = $('#biggraphcontainer').innerWidth() - 50;
    cty.canvas.height = $('#biggraphcontainer').innerHeight() - 50;
    var biggraph = new Chart(cty).Line(biggraphdata, biggraphoptions);
};