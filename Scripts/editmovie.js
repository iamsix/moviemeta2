

function editMovieInfo()
{
	//var div = document.getElementById("movieinfo");
	var movieid = window.location.pathname.split( '/' )[2];
	$.ajax({
		url: '/getMovieXML',
		data: "movieID=" + movieid,
		dataType: 'xml',
		success: function(data) {
			var option = $(data).find('MPAARating').text();
			$('#spMPAARating').html('<br /><input id="MPAARating" value="' + option + '" />');
			var MPAARatings = ["G", "PG", "PG-13", "R", "NC-17", "NR"]
			$( "#MPAARating" ).autocomplete({
				source: MPAARatings,
				minLength: 0
			});
			$('#MPAARating').click(function() { $('#MPAARating').autocomplete( "search", "" ); });

			option = $(data).find('RunningTime').text();
			$('#spRunningTime').html('<br /><input id="RunningTime" value="' + option + '" />');
			
			option = $(data).find('AspectRatio').text();
			$('#spAspectRatio').html('<br /><input id="AspectRatio" value="' + option + '" />');
			var AspectRatios = ["1.33:1", "1.78:1", "1.85:1", "2.35:1", "2.40:1"]
			$( "#AspectRatio" ).autocomplete({
				source: AspectRatios,
				minLength: 0
			});
			$('#AspectRatio').click(function() { $('#AspectRatio').autocomplete( "search", "" ); });
			
			option = $(data).find('Type').eq(0).text();
			$('#spType').html('<br /><input id="Type" value="' + option + '" />');
			var Types = ["XviD", "x264", "DVD", "HD-DVD", "Blu-Ray"]
			$( "#Type" ).autocomplete({
				source: Types,
				minLength: 0
			});
			$('#Type').click(function() { $('#Type').autocomplete( "search", "" ); });
			
			option = $(data).find('Added').text();
			$('#spAdded').html('<br /><input id="Added" value="' + option + '" />');
			$( "#Added" ).datetimepicker({
				ampm: true,
				timeFormat: 'hh:mm:ss'
			});
			
			option = $(data).find('IMDB').text();
			$('#spIMDB').html('<br /><input id="IMDB" value="' + option + '" />');
			
			option = $(data).find('TMDbId').text();
			$('#spTMDbId').html('<br /><input id="TMDbId" value="' + option + '" />');
		}
	});
}