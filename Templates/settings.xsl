<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <head>
        <meta http-equiv="X-UA-Compatible" content="IE=8" />
        <title>Movie &lt;meta&gt;</title>
      </head>

      <style type="text/css">
        a.header{color: #DDD; font-weight: bold; }
        a.movieXMLcomplete{color: green; padding-bottom: 5px;}
        a.movieXMLnone{color: red; padding-bottom: 5px;}
        a.movieXMLincomplete{color: #4f61c5; padding-bottom: 5px;}
        #searchbox{padding: 3px 25px 4px 10px; background:transparent url('/Images/searchbox.png') 0 -24px no-repeat; width: 280px;}
        #mdir{margin-left: 40px; width: 180px;}
        #invaliddir{margin-left: 40px; width: 180px; background: pink;}
        #searchsuggestions{visibility: hidden; box-shadow: 0px 0px 8px #000; border-bottom-left-radius: 5px; border-bottom-right-radius: 5px; border: 1px solid #4e4e4e; padding-left: 5px; padding-right: 5px; padding-bottom: 5px; position: absolute; margin-left: 10px; background-color: #d5d5d5; min-width: 220px;}
      </style>

      <script type="text/javascript">
        var dirid=<xsl:value-of select="Settings/moviedircount"/>;
        function addDirInput()
        {
        var container = document.getElementById("moviedirectories");
        var div = document.createElement("DIV");
        div.id = "dir" + dirid;
        var inpt = document.createElement("INPUT");
        inpt.type="text";
        inpt.name ="invaliddir";
        inpt.id ="invaliddir";
        inpt.onblur = new Function("validateFSDir(this)");

        var delbtn = document.createElement("INPUT");
        delbtn.type = "button";
        delbtn.value = "x";
        delbtn.onclick = new Function("rmDirInput('" + div.id + "')");

        div.appendChild(inpt);
        div.appendChild(delbtn);

        container.appendChild(div);

        dirid++;
        }

        function rmDirInput(child)
        {
        var container = document.getElementById("moviedirectories");
        var div =  document.getElementById(child);
        container.removeChild(div);
        }

        function validateFSDir(input)
        {
        dir = input.value;
        req = new XMLHttpRequest();
        req.open("POST","/validatedirectory",true);
        req.setRequestHeader("Content-type","application/x-www-form-urlencoded ");
        req.send("dir=" + dir);

        req.onreadystatechange=function() {
        if (req.readyState==4) {
        if (req.status==404)
        {
        input.name = "invaliddir";
        input.id = "invaliddir";
        }
        if (req.status==200)
        {
        input.name = "mdirectory";
        input.id = "mdir"
        }
        }
        }


        }
      </script>

      <script type="text/javascript">
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

      <script type="text/javascript" src="Scripts/jquery-1.6.js"></script>
      <script type="text/javascript" src="Scripts/jquery.form.js"></script>

      <script type="text/javascript">
        $(document).ready(function() {
        var options = {
        //target:        '#output2',   // target element(s) to be updated with server response
        //beforeSubmit:  showRequest,  // pre-submit callback
        //success:       showResponse  // post-submit callback

        // other available options:
        //url:       url         // override for form's 'action' attribute
        //type:      type        // 'get' or 'post', override for form's 'method' attribute
        //dataType:  null        // 'xml', 'script', or 'json' (expected server response type)
        //clearForm: true        // clear all form fields after successful submit
        //resetForm: true        // reset the form after successful submit

        // $.ajax options can be used here too, for example:
        //timeout:   3000
        };

        // bind to the form's submit event
        $('#mmsettings').submit(function() {
        // inside event callbacks 'this' is the DOM element so we first
        // wrap it in a jQuery object and then invoke ajaxSubmit
        $(this).ajaxSubmit(options);

        // !!! Important !!!
        // always return false to prevent standard browser submit and page navigation
        return false;
        });
        });
      </script>

      <body style="background-color: #4e4e4e; font-family: Arial; height: 100%;">
        <div style="width: 97%; padding-bottom: 25px; margin-left: auto; margin-right: auto; background-color: #d5d5d5; border-left: 1px solid black; border-right: 1px solid black; overflow: auto;">
          <div id="header" style="height: 117px; background-image: url('/Images/headerimg.png');background-repeat: repeat-x; padding-left: 15px;">
            <div style="float: right; margin-right: 15px; margin-top: 15px; height: 20px; ">
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
                <a class="header" href="/" style="padding-right: 15px; padding-left: 15px;">
                  Unprocessed Movies (<xsl:value-of select="Settings/unprocessed"/>)
                </a>
                <a class="header" style="padding-right: 15px; padding-left: 15px;">Cats</a>
              </span>
              <span style="float: right;padding-right: 15px;">
                <a class="header" style="padding-right: 15px; padding-left: 15px;">Settings</a>
                <a class="header" href="/exit" style="padding-left: 15px;">Shutdown</a>
              </span>
            </div>
          </div>
          <div id="content" style="padding: 15px 20px 15px 20px;">

            <form enctype="multipart/form-data" id="mmsettings" method="post" action="savesettings">
              <div id="moviedirectories" >
                Directories: <input type="button" value="Add" onclick="addDirInput();"/>
                <xsl:for-each select="Settings/MovieDir">
                  <div>
                    <xsl:attribute name="id">
                      <xsl:value-of select="DirID"/>
                    </xsl:attribute>
                    <input type="text" name="mdirectory" id="mdir" Title="Example: D:\Movies" onblur="validateFSDir(this)">
                      <xsl:attribute name="value">
                        <xsl:value-of select="Dir"/>
                      </xsl:attribute>
                    </input>
                    <input type="button" value="x" onclick="rmDirInput('{DirID}');" />

                  </div>
                </xsl:for-each>
              </div>
              
              Movie file Extensions: <input type="text" id="fileExts" name="fileExts" value="{Settings/fileExtensions}" Title="Example: avi, mkv, mp4, ts" style="margin-top: 10px;" />
              <br />
              <input type="submit" value="Save" style="margin-top: 10px;"/>
            </form>
          </div>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>