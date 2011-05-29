var pageeditstate = "display"

$(document).ready(function() {
	
	 $('#movieposter, #moviebackdrop').bind('dblclick', function(event) {
		var identifier = '';
	 	if (IMDbID == '' && $('#IMDB').val() != ''){
	 		IMDbID = $('#IMDB').val()
	 	}
	 	if (TMDbID == '' && $('#TMDbId').val() != '') {
	 		TMDbID = $('#TMDbId').val()
	 	} 
	 	
	 	if (TMDbID == '' && IMDbId == ''){
	 		alert("You must have a TMDb or IMDb ID to fetch a poster")
	 		return;
	 	}
	 	
	 	var imgtype = '';
	 	if (event.target.id == "movieposter"){
	 		imgtype = 'poster'
	 	} else if (event.target.id = "moviebackdrop"){
	 		imgtype = 'backdrop'
	 	}
	 	
       	 $('#imagepicker').dialog({
			width:500,
			modal: true,
			open: function() {
				$('#imagepickerlist').html('Loading')

				$.ajax({
				   url: "/fetchimagelist/" + movieid,
				   contentType: "application/x-www-form-urlencoded",
				   dataType: 'json',
				   data: 'imagetype=' + imgtype + '&IMDB=' + IMDbID + '&TMDbId=' + TMDbID,
				   success: function (data) {
				       	//$('#imagepickerlist').html('')
				       	$('.imagecarousel').html('')
				       	$('.imagecarousel').append('<ul id="imagepickerlist"></ul>')
				       	
				       	$(data).each(function(i){
			           		//$('#imagepickerlist').append(i+1, "<input type='button'>I am item" + i + "</input>")
			           		$('#imagepickerlist').append('<li id="'+ this.imageid +'">' + this.resolution + '<br ><img src="/fetchedpicthumbs/' + movieid + '/' + this.imageid +'?imgtype=' + imgtype +'" alt="" /></li>');
			          	});	
				       	
				       	$('#imagepickerlist').jcarousel({
							buttonNextHTML: '<button style="float:right" class="next">&gt;&gt;</button>',
							buttonPrevHTML: '<button style="float:left" class="prev">&lt;&lt;</button>',
						})
						
						$('#imagepickerlist').selectable({
							stop: function(e, ui) {
								$(".ui-selected:first", this).each( function() {
									$(this).siblings().removeClass("ui-selected");
								});
							}
						})

				  	}
				})
            			
			  },
			close: function() {
				
			},
			buttons: {
					"Select Image": function() {
						$.ajax({
			               url: "/savemovieimage/" + movieid + "/" + $('#imagepickerlist li.ui-selected:first').attr("id"),
			               contentType: "application/x-www-form-urlencoded",
			               data: 'imgtype=' + imgtype,
			               success: function (data) {
			               		$( '#imagepicker' ).dialog( "close" );
			               		document.getElementById(event.target.id).src = document.getElementById(event.target.id).src + "#"		
			               }  
			            });
				            
							
						},
						Cancel: function() {
							$( this ).dialog( "close" );
						}
				}
		});
               	
  	 });
	 });
//})

//    for (var i = carousel.first; i <= carousel.last; i++) {
        // Check if the item already exists
//        if (!carousel.has(i)) {
            // Add the item
//            carousel.add(i, "I'm item #" + i);
//        }
//    }
//};

function fetchsearch()
{
	//var movieid = window.location.pathname.split( '/' )[2];
	$.ajax({
               url: "/fetchmediasearch/" + movieid,
               type: "POST",
               contentType: "application/x-www-form-urlencoded",
               dataType: 'json',
               data: 'identifier=' + escape($('#fetchsearchterm').val()),
               success: function (data) {
               		$('#fetchsearchresults').html("")
               		$(data).each(function(i){
               			$('#fetchsearchresults').append('<li id="' + this.id + '"><b>' + this.name + '</b><br>' + this.desc + '</li>')
               			
               		})
               		
               		$('#fetchsearchresults').selectable({
               			stop: function(e, ui) {
               			  $(".ui-selected:first", this).each(function() {
		                     $(this).siblings().removeClass("ui-selected");
              			  });
               			}
               			
               		});
               		
               }
            }); 
}

function fetchdialog()
{
	//var movieid = window.location.pathname.split( '/' )[2];
	$('#fetchdialog').dialog({
			width:500,
			modal: true,
			buttons: {
				"Select Movie": function() {
					var checked = ($('#replacemissing:checked').val()  != undefined)
					$.ajax({
		               url: "/fetchmetadata/" + movieid,
		               contentType: "application/x-www-form-urlencoded",
		               dataType: 'xml',
		               data: 'replaceonlymissing=' + checked + '&' + $('#fetchsearchresults li.ui-selected:first').attr("id"),
		               success: function (data) {
		               		loadEditsFromXML(data)
		               		$( '#fetchdialog' ).dialog( "close" );
		               }
		            });
					
				},
				Cancel: function() {
					$( this ).dialog( "close" );
				}
			}
	});
	fetchsearch()
}



function rmListItem(child)
{
	child.parentNode.parentNode.removeChild(child.parentNode);
}

function addListItem(itemchild)
{
	var list = $(itemchild.parentNode).draggable( "option", "connectToSortable" );
	var node = $(itemchild.parentNode).clone();
	node.children("a").html("x").attr('onclick', 'rmListItem(this)');
	$(list).append(node);
	$(itemchild.parentNode).children("input").val('')
}

function saveMovieInfo()
{
	//var movieid = window.location.pathname.split( '/' )[2];
	
	var Genres = new Array();
	$('#GenreList').children('li').each(function (i) {
		Genres[i] = $(this).children('input').val()
	})
	
	var Persons = new Array();
	var personindex = 0;
	$('#CrewList').children('li').each(function (i) {
		Persons[i] = {
			'Name' : $(this).children('#crewname').val(),
			'Type' : $(this).children('#crewjob').val(),
			'Role' : ""
		}
		personindex++;
	})
	$('#ActorList').children('li').each(function (i) {
		Persons[personindex + i] = {
			'Name' : $(this).children('#castname').val(),
			'Type' : "Actor",
			'Role' : $(this).children('#castrole').val()
		}
	})
	
	
	var Studios = new Array();
	$('#StudioList').children('li').each(function (i) {
		Studios[i] = $(this).children('input').val()
	})
	

	
	var movieJSON = {
		'LocalTitle' : $('#LocalTitle').val(),
		'OriginalTitle' : $('#OriginalTitle').val(),
		'SortTitle' : $('#SortTitle').val(),
		'SortTitle' : $('#SortTitle').val(),
		'Added' : $('#Added').val(),
		'ProductionYear' : $('#ProductionYear').val(),
		'RunningTime' : $('#RunningTime').val(),
		'IMDBrating' : $('#IMDBrating').text(),
		'MPAARating' : $('#MPAARating').val(),
		'IMDBrating' : $('#IMDBrating').text(),
		'MPAARating' : $('#MPAARating').val(),
		'Description' : $('#Description').val(),
		'Type' : $('#Type').val(),
		'AspectRatio' : $('#AspectRatio').val(),
		'IMDB' : $('#IMDB').val(),
		'TMDbId' : $('#TMDbId').val(),
		'Genres' : Genres,
		'Persons' : Persons,
		'Studios' : Studios
		
	}
	
	var jsdata = JSON.stringify(movieJSON)
	
	$.ajax({
               url: "/saveMovieXML/" + movieid,
               type: "POST",
               contentType: "application/json",
               processData: false,
               data: jsdata,
               error: function(jqXHR, textStatus, errorThrown){alert("You are not authorized to edit the metadata")},
               success: function (data) {
               		pageeditstate = "display"
               		location.reload(true);
               }
            }); 
}

function editMovieInfo()
{
	
	
	//var movieid = window.location.pathname.split( '/' )[2];
	$.ajax({
		url: '/getMovieXML',
		data: "movieID=" + movieid,
		dataType: 'xml',
		error: function(jqXHR, textStatus, errorThrown){alert("You are not authorized to edit the metadata")},
		success: function(data, textStatus){
			loadEditsFromXML(data);
			pageeditstate = "editing"
		}
	});
}

function loadEditsFromXML(data)
{
	
			$("#editbutton").hide();
			$("#savebutton").show();
			$("#canceledit").show()
			//xmldoc = data;
			var option = $(data).find('MPAARating').text();
			$('#spMPAARating').html('<br /><input id="MPAARating" value="' + option + '" />');
			var MPAARatings = ["G", "PG", "PG-13", "R", "NC-17", "NR"]
			$( "#MPAARating" ).autocomplete({
				source: MPAARatings,
				minLength: 0
			});
			$('#MPAARating').click(function() { $(this).autocomplete( "search", "" ); });

			option = $(data).find('RunningTime').text();
			$('#spRunningTime').html('<br /><input id="RunningTime" value="' + option + '" />');
			
			option = $(data).find('AspectRatio').text();
			$('#spAspectRatio').html('<br /><input id="AspectRatio" value="' + option + '" />');
			var AspectRatios = ["1.33:1", "1.78:1", "1.85:1", "2.35:1", "2.40:1"]
			$( "#AspectRatio" ).autocomplete({
				source: AspectRatios,
				minLength: 0
			});
			$('#AspectRatio').click(function() { $(this).autocomplete( "search", "" ); });
			
			option = $(data).children('Title').children('Type').text();
			$('#spType').html('<br /><input id="Type" value="' + option + '" />');
			var Types = ["XviD", "DivX", "x264", "DVD", "HD-DVD", "Blu-Ray"]
			$( "#Type" ).autocomplete({
				source: Types,
				minLength: 0
			});
			$('#Type').click(function() { $(this).autocomplete( "search", "" ); });
			
			option = $(data).find('Added').text();
			$('#spAdded').html('<br /><input id="Added" value="' + option + '" />');
			$( "#Added" ).datetimepicker({
				ampm: true,
				timeFormat: 'hh:mm:ss TT'
			});
			
			option = $(data).find('IMDB').text();
			$('#spIMDB').html('<br /><input id="IMDB" value="' + option + '" />');
			
			option = $(data).find('TMDbId').text();
			$('#spTMDbId').html('<br /><input id="TMDbId" value="' + option + '" />');
			
			var Genres = ["Action", "Adventure", "Animation", "Comedy", "Crime",
			"Disaster", "Documentary", "Drama", "Family", "Fantasy", "Horror", "Indie",
			"Martial Arts", "Music", "Mystery", "Romance", "Science Fiction", 
			"Sports Film", "Suspense","Thriller", "Western"]
			option = $(data).find('Genre');
			var genrelist = $('<ul class="sortablelist" id="GenreList"></ul>');
			for (i = 0; i <= option.length-1; i++) {
				genrelist.append('<li><span class="ui-icon ui-icon-arrowthick-2-n-s"></span><input class="genreAC" type="text" value="' + option.eq(i).text() + '" /><a onclick="rmListItem(this)">x</a></li>');
			}
			$('#spGenres').html('<ul class="sortablelist"><li id="newGenre"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span><input id="newGenrei" type="text" placeholder="New Genre" /><a onclick="addListItem(this)">+</a></li></ul>');
			genrelist.appendTo('#spGenres');
			
			$( ".genreAC" ).autocomplete({
				source: Genres,
				minLength: 0
			});	
			$( "#newGenrei" ).autocomplete({
				source: Genres,
				minLength: 0,
				select: function(event, ui) {$(this).val(ui.item.value); 
											addListItem(this);
											return false;}
			});	
			
			$('#newGenrei').click(function() { $(this).autocomplete( "search", "" ); });		
			$( "#GenreList" ).sortable({
				receive: function() { $(this).children("li").children("a").html("x").attr('onclick', 'rmListItem(this)');}	
			});
			
			$( "#newGenre" ).draggable({
				connectToSortable: "#GenreList",
				helper: "clone",
				revert: "invalid"
			});
			
			option = $(data).find('Studio');
			var studiolist = $('<ul class="sortablelist" id="StudioList"></ul>');
			for (i = 0; i <= option.length-1; i++) {
				studiolist.append('<li><span class="ui-icon ui-icon-arrowthick-2-n-s"></span><input type="text" value="' + option.eq(i).text() + '" /><a onclick="rmListItem(this)">x</a></li>');
			}			
			$('#spStudios').html('<ul class="sortablelist"><li id="newStudio"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span><input type="text" placeholder="New Studio" /><a onclick="addListItem(this)">+</a></li></ul>');
			studiolist.appendTo('#spStudios');	
				
			$( "#StudioList" ).sortable({
				receive: function() { $(this).children("li").children("a").html("x").attr('onclick', 'rmListItem(this)');}	
			});
			
			$( "#newStudio" ).draggable({
				connectToSortable: "#StudioList",
				helper: "clone",
				revert: "invalid"
			});
			
			
			var div = $('#titles');
			div.html('');
			option = $(data).find('LocalTitle').text();
			div.append('<b>Local Title:</b> <br /><input style="width: 250px;" id="LocalTitle" value="' + option + '" /><br />')
			option = $(data).find('OriginalTitle').text();
			div.append('<b>Original Title:</b> <br /><input style="width: 250px;" id="OriginalTitle" value="' + option + '" /><br />')
			option = $(data).find('SortTitle').text();
			div.append('<b>Sorting Title:</b> <br /><input style="width: 250px;" id="SortTitle" value="' + option + '" /><br />')
			option = $(data).find('ProductionYear').text();
			div.append('<b>Production Year:</b> <br /><input id="ProductionYear" value="' + option + '" /><br />')
			option = $(data).find('IMDBrating').text();
			$('#movierating').html('<b>Movie Rating:</b> <br /><span id="IMDBrating"></span><div style="width: 250px;" id="RatingSlider"><div>')
			$( "#RatingSlider" ).slider({
				value: option,
				min: 0,
				max: 10,
				step: 0.1,
				slide: function( event, ui ) {
					$( "#IMDBrating" ).text(ui.value);
				}
			});
			$( "#IMDBrating" ).text( $( "#RatingSlider" ).slider( "value" ) );
			
			option = $(data).find('Description').text();
			$('#moviedescription').html('<textarea id="Description" style="width: 100%;  height: 100px;">' + option  + '</textarea>')
			
			option = $(data).find('Person');
			var crewlist = $('<ul class="sortablelist" id="CrewList"></ul>');
			for (i = 0; i <= option.length-1; i++) {
				if (option.eq(i).children('Type').text() != "Actor")
				{
					crewlist.append('<li><span class="ui-icon ui-icon-arrowthick-2-n-s"></span><input id="crewname" type="text" value="' + option.eq(i).children('Name').text() + '" /> as: <input id="crewjob" type="text" value="' + option.eq(i).children('Type').text() +'" /><a onclick="rmListItem(this)">x</a></li>');					
				}
			}
			$('#moviecrew').html('<ul class="sortablelist"><li id="newCrew"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span><input id="crewname" type="text" placeholder="Crew Name" /> as: <input id="crewjob" type="text" placeholder="Job" /><a onclick="addListItem(this)">+</a></li></ul>')
			crewlist.appendTo('#moviecrew');
			$( "#newCrew" ).draggable({
				connectToSortable: "#CrewList",
				helper: "clone",
				revert: "invalid"
			});	
			
			$( "#CrewList" ).sortable({
				receive: function() { $(this).children("li").children("a").html("x").attr('onclick', 'rmListItem(this)');}	
			});
			
			
			var castlist = $('<ul class="sortablelist" id="ActorList"></ul>');
			for (i = 0; i <= option.length-1; i++) {
				if (option.eq(i).children('Type').text() == "Actor")
				{
					castlist.append('<li><span class="ui-icon ui-icon-arrowthick-2-n-s"></span><input id="castname" type="text" value="' + option.eq(i).children('Name').text() + '" /> as: <input id="castrole" type="text" value="' + option.eq(i).children('Role').text() +'" /><a onclick="rmListItem(this)">x</a></li>');					
				}
			}
			$('#moviecast').html('<ul class="sortablelist"><li id="newCast"><span class="ui-icon ui-icon-arrowthick-2-n-s"></span><input id="castname" type="text" placeholder="Actor Name" /> as: <input id="castrole" type="text" placeholder="Role" /><a onclick="addListItem(this)">+</a></li></ul>')
			castlist.appendTo('#moviecast');
			$( "#newCast" ).draggable({
				connectToSortable: "#ActorList",
				helper: "clone",
				revert: "invalid"
			});
			
			$( "#ActorList" ).sortable({
				receive: function() { $(this).children("li").children("a").html("x").attr('onclick', 'rmListItem(this)');}	
			});
			
			document.getElementById('movieposter').src = document.getElementById('movieposter').src + "#"
			document.getElementById('moviebackdrop').src = document.getElementById('moviebackdrop').src + "#"
		
		}