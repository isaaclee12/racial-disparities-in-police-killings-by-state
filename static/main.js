/* Description of functionality:
 *
 * The map of the United States is represented as an SVG (scalable vector graphics) image,
 * which is a format that represents pictures in XML format. Our map SVG is sourced from
 * wikipedia. The states in the image are designated with <path> elements.
 *
 * JQuery is used to bind click events to each <path> (state). When a state is clicked,
 * we get the <path> id and request the server for relevant data using our RESTful API.
 *
 * The JSON data is reformatted into a simple list and written to <div id="stats">
 */

google.charts.load('current', {'packages':['corechart']});

$("path:not(#frames)").click(function(e) {
  let state = $(this).attr("id");
  // switch two lines for live instance (use the IP address of YOUR hosting server)
  //$.getJSON("http://134.209.76.43:5000/stats/state/" + state, function(data) {
  $.getJSON("http://localhost:5000/stats/state/" + state, function(data) {

    var chartdata1 = google.visualization.arrayToDataTable([
        ['Race', 'Percent of Population'],
        ['Black', parseInt(data.percentPopulationBlack)],
        ['Non-Black', parseInt(data.percentPopulationNotBlack)]
    ]);
    var chartdata2 = google.visualization.arrayToDataTable([
        ['Race', 'Percent of Killings'],
        ['Black', parseFloat(data.percentKillingsBlack)],
        ['Non-Black', parseFloat(data.percentKillingsNotBlack)]
    ]);

    var chartoptions1 = {'title': 'Demographics of '+ data.stateName, 'width': 350, 'height': 350, chartArea:{top:50, left:20, bottom: 50, width:"100%", height:"100%"}, legend:{position: 'bottom'}};
    var chartoptions2 = {'title': 'Police Killings in ' + data.stateName, 'width': 350, 'height': 350, chartArea:{top:50, left: 20, bottom: 50, width:"100%", height:"100%"}, legend:{position: 'bottom'}};

    var chart1 = new google.visualization.PieChart(document.getElementById('chartContainer1'));
    chart1.draw(chartdata1, chartoptions1);
    var chart2 = new google.visualization.PieChart(document.getElementById('chartContainer2'));
    chart2.draw(chartdata2, chartoptions2);

    let stats = []
    //$.each(data, function(key,val) {
    //  stats.push("<li id'" + key + "'>" + key + ": " + val + "</li>");
    //});
    stats.push(data.totalPoliceKillings)
    $('#stats').html(stats.join(""));

  });
});
