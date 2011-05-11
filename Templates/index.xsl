<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <head>
        <meta http-equiv="X-UA-Compatible" content="IE=8" />
        <title>Movie &lt;meta&gt;</title>
      </head>
      <style type="text/css">
        a{color: #4f61c5;}
        a.header{color: #DDD; font-weight: bold; }
        a.movieXMLcomplete{color: green; padding-bottom: 5px;}
        a.movieXMLnone{color: red; padding-bottom: 5px;}
        a.movieXMLincomplete{color: #4f61c5; padding-bottom: 5px;}
        #searchbox{padding: 3px 25px 4px 10px; background:transparent url('/Images/searchbox.png') 0 -24px no-repeat; width: 280px;}
        #invaliddir{margin-left: 40px; width: 180px; background: pink;}
        #searchsuggestions{visibility: hidden; box-shadow: 0px 0px 8px #000; border-bottom-left-radius: 5px; border-bottom-right-radius: 5px; border: 1px solid #4e4e4e; padding-left: 5px; padding-right: 5px; padding-bottom: 5px; position: absolute; margin-left: 10px; background-color: #d5d5d5; min-width: 220px;}
      </style>

      <script type="text/javascript">
        function refreshlist()
        {
        req = new XMLHttpRequest();
        req.open("GET","/refresh_movielist",true);
        req.setRequestHeader("Content-type","text/plain");
        req.send();

        req.onreadystatechange=function() {
        if (req.readyState==4) {
        location.reload(true);
        };
        };
        }

        function searchsuggestion(input)
        {
        div = document.getElementById("searchsuggestions");
        searchstring = input.value;
        req = new XMLHttpRequest();
        req.open("POST","/searchsuggestions",true);
        req.setRequestHeader("Content-type","application/x-www-form-urlencoded ");
        req.send("search=" + searchstring);

        req.onreadystatechange=function()
        {
        if (req.readyState==4)
        {
        if (req.status==200)
        {
        div.innerHTML = req.responseText;
        div.style.visibility = "visible";
        }
        }

        }
        }

        function hideSuggestions()
        {
        setTimeout('document.getElementById("searchsuggestions").style.visibility = "hidden"', 250)
        }

      </script>

        <body style="background-color: #4e4e4e; font-family: Arial;">
        <div style="width: 97%; margin-left: auto; margin-right: auto; background-color: #d5d5d5;  border-left: 1px solid black; border-right: 1px solid black;">
          <div id="header" style="height: 117px; background-image: url('/Images/headerimg.png');background-repeat: repeat-x; padding-left: 15px;">
            <div style="float: right; margin-right: 15px; margin-top: 15px; height: 20px;">
              <form action="/search" method="get">
                <span id="searchbox">
                  <input type="text" onblur='hideSuggestions()' onkeyup="searchsuggestion(this)" placeholder="Search" name="search" style="background: transparent; border: none;font-weight: bold; color: #555; width: 225px;"/>
                </span>
                <br />
                <div id="searchsuggestions"></div>
                <span style="float: right; font-size: 9pt; text-align: right; font-weight: bold;">
                  <a class="header">Advanced</a>
                </span>
              </form>
            </div>
            <img src="/Images/logo.png" style="margin-top: 10px; " />
            <div id ="menu" style="margin-top: 14px; color: #DDD; font-size: 10pt; ">
              <span>
                <a class="header" href="/list" style="padding-right: 15px; ">Movie List</a>
                <a class="header" href="/" style="padding-right: 15px; padding-left: 15px;">Unprocessed Movies (<xsl:value-of select="movies/unprocessed"/>)</a>
                <a class="header" href ="#" onclick="refreshlist()" style="padding-right: 15px; padding-left: 15px;">Cats</a>
              </span>
              <span style="float: right;padding-right: 15px;">
                <a class="header" href="/settings" style="padding-right: 15px; padding-left: 15px;">Settings</a>
                <a class="header" href="/exit" style="padding-left: 15px;">Shutdown</a>
              </span>
            </div>
          </div>
          <div id="content" style="padding: 15px 20px 15px 20px;">
            <h2>
              <xsl:copy-of select="movies/listname" />
            </h2>
            <div style="">
              <ul>
              <xsl:for-each select="movies/movie">
                <a>
                  <xsl:attribute name="href">
                    /movie/<xsl:value-of select="Link"/>
                  </xsl:attribute>
                  <xsl:attribute name="title">
                    <xsl:value-of select="Path"/>
                  </xsl:attribute>
                  <xsl:attribute name="class">
                    movieXML<xsl:value-of select="XML"/>
                  </xsl:attribute>
                <li style ="padding-bottom: 5px;">
                  <xsl:value-of select="LocalTitle"/> (<xsl:value-of select="ProductionYear"/>)
                </li>
                </a>
              </xsl:for-each>
              </ul>
            </div>
          </div>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>