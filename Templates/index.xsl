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
        #searchbox{padding: 3px 25px 4px 10px; background:transparent url('/Images/searchbox.png') 0 -24px no-repeat; width: 280px;}
      </style>
      <body style="background-color: #4e4e4e; font-family: Arial;">
        <div style="width: 97%; margin-left: auto; margin-right: auto; background-color: #d5d5d5;  border-left: 1px solid black; border-right: 1px solid black;">
          <div id="header" style="height: 117px; background-image: url('/Images/headerimg.png');background-repeat: repeat-x; padding-left: 15px;">
            <div style="float: right; margin-right: 15px; margin-top: 15px; height: 20px; wdith: 193px;">
              <form action="/search" method="get">
                <span id="searchbox">
                  <input type="text" placeholder="Search" name="search" style="background: transparent; border: none;font-weight: bold; color: #555; width: 225px;"/>
                </span>
                <br />
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
                <a class="header" style="padding-right: 15px; padding-left: 15px;">Cats</a>
              </span>
              <span style="float: right;padding-right: 15px;">
                <a class="header" href="/settings" style="padding-right: 15px; padding-left: 15px;">Settings</a>
                <a class="header" href="/exit" style="padding-left: 15px;">Shutdown</a>
              </span>
            </div>
          </div>
          <div id="content" style="padding: 15px 20px 15px 20px;">
            <h2>Unprocessed Movies</h2>
            <div style="">
              <ul>
              <xsl:for-each select="movies/movie">
                <a>
                  <xsl:attribute name="href">
                    /movie/<xsl:value-of select="Link"/>
                  </xsl:attribute>
                <li style ="padding-bottom: 5px;">
                  <xsl:if test="XML='none'">
                    <xsl:attribute name="style">color: red; padding-bottom: 5px;</xsl:attribute>
                  </xsl:if>
                  <xsl:if test="XML='complete'">
                    <xsl:attribute name="style">color: green; padding-bottom: 5px;</xsl:attribute>
                  </xsl:if>
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