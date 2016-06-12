/* Place all the behaviors and hooks related to the matching controller here.
All this logic will automatically be available in application.js.*/

var biggraph = function(bigchartlabels, bigchartdata) {

var biggraphdata = {
    labels: bigchartlabels,
    datasets: [
        {
            label: "Energy usage in kWh",
            fill: true,
            lineTension: 0.1,
            backgroundColor: "rgba(48, 130, 89,0.4)",
            borderColor: "rgba(48, 130, 89,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(48, 130, 89,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(48, 130, 89,1)",
            pointHoverBorderColor: "rgba(48, 130, 89,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: bigchartdata,
        }
    ]
};


var biggraphoptions = {
  skipLabels : 3,
    //Boolean - Whether grid lines are shown across the chart
    scaleShowGridLines : true,

    //String - Colour of the grid lines
    scaleGridLineColor : "rgba(0,0,0,.15)",

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
    pointHitDetectionRadius : 3,

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
    var biggraph = new Chart(cty, {
        type: 'line',
        data: biggraphdata,
        options: biggraphoptions
    });
};