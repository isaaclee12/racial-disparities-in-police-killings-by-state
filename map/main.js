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

$("path").click(function(e) {
  let state = $(this).attr("id");
  $.getJSON("http://localhost:5000/stats/state/" + state, function(data) {
    let stats = []
    $.each(data, function(key,val) {
      stats.push("<li id'" + key + "'>" + key + ": " + val + "</li>");
    });
    $('#stats').html(stats.join(""));
  });
});
