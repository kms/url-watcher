<?xml version="1.0" encoding="ISO-8859-1"?>

<!DOCTYPE xsl:stylesheet [ 
<!ENTITY nbsp "&#160;"> 
]> 

<!-- (c) Karl-Martin Skontorp <kms@skontorp.net> -->

    <xsl:stylesheet version="1.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<xsl:output method="xml"
	    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"
	    doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" 
	    encoding="ISO-8859-1"
	    omit-xml-declaration="yes" />

	<xsl:param name="now" />

	<xsl:template match="/url-watcher">
	    <html>
		<head>
		    <title>
			<xsl:text>LA-Hams</xsl:text>
		    </title>
		    <link rel="stylesheet" href="main.css" type="text/css" />
		    <link rel="icon" href="la-hams-icon.png" type="image/png" />
		    <meta http-equiv="refresh" content="3600" />
		</head>

		<body>
		    <div class="bigHeader">
			<img src="la-hams.jpg" alt="LA-Hams" />
		    </div>

		    <div class="updated">
			<xsl:choose>
			    <xsl:when test="generated/@no-cache = 'true'">
				Full update:
			    </xsl:when>
			    <xsl:when test="generated/@no-cache = 'false'">
				Update: 
			    </xsl:when>
			</xsl:choose>
			<xsl:value-of select="substring(generated, 1, 16)" />
			<xsl:text> (</xsl:text>
			<xsl:value-of select="generated/@runtime" />
			<xsl:text> s.)</xsl:text>
		    </div>

		    <div class="xml">
			<a href="rss20.xml">
			    <img src="xml.png" alt="XML" />
			</a> (RSS 2.0)
			&nbsp; &nbsp; &nbsp;
			<a href="la-hams.xml">
			    <img src="xml.png" alt="XML" />
			</a> (Raw)
		    </div>

		    <div class="about">
			A list of Norwegian ham web pages and other pages of
			interest to the radio amateur. List is sorted with 
			the latest updated pages on the top. All times in UTC.
			RSS 2.0 feed (for news aggregators) and raw XML data
			available above. The list is updated every 6 hours.
			Contact <a
			    href="mailto:LA9PMA@skontorp.net">LA9PMA@skontorp.net</a>
			with comments or additions to the list.
		    </div>
		    
		    <div class="topLinks">
			<a href="list/">List of pages, by category</a>
		    </div>

		    <div class="legend">
			<span class="legendElement">
			    <img src="p-small.png" alt="P" />
			    Personal
			</span>
			<span class="legendElement">
			    <img src="g-small.png" alt="G" />
			    Group
			</span>
			<span class="legendElement">
			    <img src="n-small.png" alt="N" />
			    News
			</span>
			<span class="legendElement">
			    <img src="dx-c-small.png" alt="DX/C" />
			    DX/Contest
			</span>
			<span class="legendElement">
			    <img src="c-small.png" alt="C" />
			    Commercial
			</span>
			<span class="legendElement">
			    <img src="m-small.png" alt="M" />
			    Misc.
			</span>
		    </div>

		    <div class="list">
			<xsl:apply-templates select="pages" />
		    </div>
		</body>
	    </html>
	</xsl:template>

	<xsl:key name="pages-by-date" match="/url-watcher/pages/page"
	    use="substring(lastModified/iso-8601, 1, 10)" />

	<xsl:template match="/url-watcher/pages">
	    <xsl:for-each select="page[count(. | key('pages-by-date',
		substring(lastModified/iso-8601, 1, 10))[1]) = 1]">

		<xsl:sort select="lastModified/iso-8601"
		    order="descending" />

		<div class="date-category">
		    <xsl:value-of select="lastModified/date" />
		</div>

		<xsl:for-each select="key('pages-by-date',
		    substring(lastModified/iso-8601, 1, 10))">

		    <xsl:sort select="lastModified/time" order="descending" />

		    <div class="listLine">
			<div class="time">
			    <xsl:value-of select="lastModified/time" />
			</div>
			<div class="categoryIcon">
			    <xsl:apply-templates select="category" />
			    &nbsp;
			</div>
			<div class="link">
			    <a>
				<xsl:attribute name="href">
				    <xsl:value-of select="linkURL" />
				</xsl:attribute>
				<xsl:value-of select="title" />
			    </a>
			</div>
			<div>&nbsp;</div>
		    </div>
		</xsl:for-each>
	    </xsl:for-each>
	</xsl:template>

	<xsl:template match="/url-watcher/pages/page/category">
	    <xsl:choose>
		<xsl:when test=". = 'Personal'">
		    <img src="p-small.png" alt="P" />
		</xsl:when>
		<xsl:when test=". = 'Group'">
		    <img src="g-small.png" alt="G" />
		</xsl:when>
		<xsl:when test=". = 'DX/Contest'">
		    <img src="dx-c-small.png" alt="DX/C" />
		</xsl:when>
		<xsl:when test=". = 'News'">
		    <img src="n-small.png" alt="N" />
		</xsl:when>
		<xsl:when test=". = 'Commercial'">
		    <img src="c-small.png" alt="C" />
		</xsl:when>
		<xsl:when test=". = 'Misc'">
		    <img src="m-small.png" alt="M" />
		</xsl:when>
	    </xsl:choose>
	</xsl:template>

    </xsl:stylesheet>
