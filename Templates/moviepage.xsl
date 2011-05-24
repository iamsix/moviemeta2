<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" doctype-public="" />
  <xsl:template match="/">
    <html >

      <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>Movie &lt;meta&gt;</title>
        <style type="text/css">
	      	body {background: #232323 url('/Images/bg-gradient.png') repeat-x; font-family: Arial}
	        a.header{color: #DDD; font-weight: bold; font-size: 10pt;}
	        a{color: #4e5785;}
	        a.movieXMLcomplete{color: green;}
	        a.movieXMLnone{color: red;}
	        a.movieXMLincomplete{color: #4f61c5;}
	        #cast {font-family: Arial; font-size: 10pt; cellspacing: 0; cellpadding: 0; border: 0} 
	        #searchbox{padding: 3px 25px 4px 10px; background:transparent url('/Images/searchbox.png') 0 -24px no-repeat; width: 280px;}
	        td.castpic{padding: 2px 5px 2px 5px}
	        td.person{padding: 5px 60px 0px 30px}
	        #searchsuggestions{visibility: hidden; box-shadow: 0px 0px 8px #000; border-bottom-left-radius: 5px; border-bottom-right-radius: 5px; border: 1px solid #4e4e4e; padding-bottom: 5px; position: absolute; margin-left: 10px; background-color: #d5d5d5; min-width: 220px;}
	        
	        #ui-datepicker-div { font-size: 12px; }
	        .ui-autocomplete, .ui-menu ui-widget, .ui-widget-content, .ui-corner-all{ font-size: 12px; }
	        
	        .sortablelist { list-style-type: none; margin: 0; padding: 5px; background: #eee; }
			.sortablelist li { margin: 0 3px 3px 3px; padding: 0.1em; padding-left: 1.5em; font-size: 1.4em; height: 18px; }
			.sortablelist li span { position: absolute; margin-left: -1.3em; margin-top: 0.3em; }
			
			span.editcontrolR{margin-left: 20px; float: right; background: #000; padding: 5px 15px 5px 15px; box-shadow: -2px 2px 5px rgba(0, 0, 0, 0.5); text-align: right; cursor: pointer; border: 1px #555 solid;}
			
			#fetchdialog {display: none}
			#fetchsearchresults .ui-selecting { background: #FECA40; }
			#fetchsearchresults .ui-selected { background: #F39814; color: white; }
			#fetchsearchresults { list-style-type: none; margin: 0; padding: 0;}
			#fetchsearchresults li { margin: 3px; padding: 0.4em; background: #ccc;}
	
	      </style>     
	      <style type="text/css">
			@import "/Templates/jquery-ui-1.8.13.custom.css";
		  </style>
		  
	  	  <script type="text/javascript" src="/Scripts/searchsuggestions.js"> </script>
	      <script type="text/javascript" src="/Scripts/jquery-1.6.js"> </script>
	      <script type="text/javascript" src="/Scripts/jquery-ui-1.8.13.custom.min.js"> </script>
	      <script type="text/javascript" src="/Scripts/jquery-ui-timepicker-addon.js"> </script> 
	      <script type="text/javascript" src="/Scripts/editmovie.js"> </script>
      </head>     
      <body>
        <div style="width: 97%; padding-bottom: 25px; margin-left: auto; margin-right: auto; background-color: #d5d5d5; border-left: 1px solid black; border-right: 1px solid black; overflow: auto;">
          <div id="header" style="height: 117px; background-image: url('/Images/headerimg.png');background-repeat: repeat-x; padding-left: 15px;">
            <div style="float: right; margin-right: 15px; margin-top: 15px; height: 20px; ">
              <form action="/search" method="get">
                <span id="searchbox">
                  <input type="text" autocomplete="off" onblur='hideSuggestions()' onkeydown="return keypress(event.keyCode)" onkeyup="searchsuggestion(this, event.keyCode)" placeholder="Search" name="search" style="background: transparent; border: none;font-weight: bold; color: #555; width: 225px;"/>
                </span>
                <br />
                <div id="searchsuggestions"></div>
                <span style="float: right; font-size: 9pt; text-align: right; font-weight: bold;">
                  <a class="header">Advanced</a>
                </span>
              </form>
            </div>
            <img src="/Images/logo.png" alt="Movie Meta Logo" style="margin-top: 10px; " />
            <div id ="menu" style="margin-top: 14px; color: #DDD; font-size: 10pt; ">
              <span>
                <a class="header" href="/list" style="padding-right: 15px; ">Movie List</a>
                <a class="header" href="/" style="padding-right: 15px; padding-left: 15px;">Unprocessed Movies (<xsl:value-of select="Title/unprocessed"/>)</a>
                <a class="header" style="padding-right: 15px; padding-left: 15px;">Cats</a>
              </span>
              <xsl:if test="$EditControls='True'">
	              <span style="float: right;padding-right: 15px;">
	                <a class="header" href="/settings" style="padding-right: 15px; padding-left: 15px;">Settings</a>
	                <a class="header" href="/exit" style="padding-left: 15px;">Shutdown</a>
	              </span>
              </xsl:if>
            </div>
          </div>

          <div id="content" style="padding: 15px 20px 15px 20px;">
            <div id="lefcol" style="width: 210px; float:left;overflow: auto; font-size: 10pt; padding-bottom: 15px; padding-right: 20px;">
             
              <b>Poster</b><br />
              <img src="/movie/{Title/movieID}/folder.jpg" alt="Movie Poster" style="margin-top: 10px; width: 180px"/>
              <br /><br />
	          <span style="font-size: 12pt; font-weight: bold;">Movie Info </span><br/>
	          <div id="movieinfo">
	              <b>Content Rating: </b> <span id="spMPAARating"><xsl:value-of select="Title/MPAARating"/></span><br/>
	              <b>Runtime: </b> <span id="spRunningTime"><xsl:value-of select="Title/RunningTime"/></span><br/>
	              <b>Aspect Ratio: </b> <span id="spAspectRatio"><xsl:value-of select="Title/AspectRatio"/></span><br/>
	              <b>Type: </b> <span id="spType"><xsl:value-of select="Title/Type"/></span><br/>
	              <b>Added: </b> <span id="spAdded"><xsl:value-of select="Title/Added"/></span><br/>
	              <br/>
	              <b>IMDB: </b> <span id="spIMDB"><a href="http://www.imdb.com/title/{Title/IMDB}/">Link</a></span><br/>
	              <b>TMDb: </b> <span id="spTMDbId"><a href="http://www.themoviedb.org/movie/{Title/TMDbId}">Link</a></span><br/>
	          </div>
	          <br />
              <b>Genres</b><br />
              <span id="spGenres">
              <xsl:for-each select="Title/Genres/Genre">
                <a href="/Genre/{.}">
                  <xsl:value-of select="."/>
                </a>
                <br />
              </xsl:for-each>
              </span>
              <br /><b>Studios</b><br />
              <span id="spStudios">
              <xsl:for-each select="Title/Studios/Studio">
                <xsl:value-of select="."/>
                <br/>
              </xsl:for-each>
              </span>
              
              
            </div>
            <div id="rightcol" style="font-size: 10pt; overflow: auto; padding-right: 10px;">
              <img src="/movie/{Title/movieID}/backdrop.jpg" alt="Movie frame" style="Height: 250px; padding-top: 10px; padding-left: 10px; float: right;"/>
              <span id="titles">
	              <span id="movietitle" style="font-weight: bold; font-size: 20pt;">
	                <xsl:value-of select="Title/LocalTitle"/>
	              </span>
	              <span id="movieyear" style="font-weight: bold; font-size: 16pt; color: grey;">
	                (<xsl:value-of select="Title/ProductionYear"/>)
	              </span>
	              <br/>
	              <xsl:if test="not(Title/OriginalTitle=Title/LocalTitle)">
	                <span id="originaltitle" style="font-size: 10pt; color: grey; font-style: italic;">
	                  <xsl:value-of select="Title/OriginalTitle"/>
	                  <br/>
	                </span>
	              </xsl:if>
              </span>
              <div id="movierating">
	              <div style="background: url('/Images/stars.png') 0 -16px repeat-x; width: 180px; height: 15px; float: left;">
	                <div style="background: url('/Images/stars.png') 0 0 repeat-x; height: 15px; width: {Title/IMDBrating * 10}%; float: left; color: transparent;">
	                  <pre style="font-size: 15px;"></pre>
	                </div>
	              </div>
              
	              <span style="padding-left: 5px; color: #7d6432; font-weight: bold; font-size: 12pt;">
	                <xsl:value-of select="Title/IMDBrating"/>
	              </span> / 10
              </div>
              <br/><br/>
              <div style="">
                <b>Overview</b>
                <hr/>                
                <span id="moviedescription"><xsl:value-of select="Title/Description"/></span>
                <br/>
                <br/>
                <b>Crew</b>
                <hr/>
                <span id="moviecrew">
	                <xsl:for-each select="Title/Persons/Person">
	                  <xsl:if test="not(Type='Actor')">
	
	                    <b><xsl:value-of select="Type"/>: </b>
	                    <a href="/Person/{Name}">
	                      <xsl:value-of select="Name"/>
	                    </a>
	                    <br/>
	
	                  </xsl:if>
	                </xsl:for-each>
                </span>
                <br/>
                <b>Cast</b>
                <hr/>
                <div id="moviecast">
	                <table id="cast">
	                  <tbody>
	                  <xsl:for-each select="Title/Persons/Person">
	                    <xsl:if test="Type='Actor'">
	                      <tr>
	                        <td class="castpic">
	                          <img src="/ImagesByName/{Name}/folder.jpg" alt="Picture of {Name}" style="width: 35px;"/>
	                        </td>
	                        <td class="person">
	                          <a href="/Person/{Name}">
	                            <xsl:value-of select="Name"/>
	                          </a>
	                        </td>
	                        <td class="character">
	                          as <xsl:value-of select="Role"/>
	                        </td>
	                      </tr>
	                    </xsl:if>
	                  </xsl:for-each>
	                  </tbody>
	                </table>
				</div>              
              </div>
            </div>
          </div>
        </div>
		<xsl:if test="$EditControls='True'">
	        <div id="editcontrols" style="width: 97%; margin-left: auto; margin-right: auto;" >
	        	<span onclick="editMovieInfo()" class="editcontrolR" id="editbutton" >
	          		<a class="header">Edit</a>
	          	</span>
	          	<span onclick="saveMovieInfo()" class="editcontrolR" id="savebutton" style="display: none;" >
	          		<a class="header">Save</a>
	          	</span>
	          	<span onclick="location.reload(true)" class="editcontrolR" id="canceledit" style="display: none;" >
	          		<a class="header">Cancel</a>
	          	</span>
	          	<span onclick="fetchdialog()" class="editcontrolR" id="fetchbutton" >
	          		<a class="header">Fetch Movie Data</a><br />
	          	</span>
	        </div>
	        <div id="fetchdialog" style="background: #333;" title="Movie Search">
		    	<input type="text" id="fetchsearchterm" value="{Title/LocalTitle} {Title/ProductionYear}" /><input type="button" value="Search" onclick="fetchsearch()" />
		    	<ul id="fetchsearchresults">
		    		No results found
		    	</ul>
        	</div>
        </xsl:if>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>