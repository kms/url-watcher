<?xml version="1.0" encoding="ISO-8859-1"?>

<!-- (c) Karl-Martin Skontorp <kms@skontorp.net> -->

    <xsl:stylesheet version="1.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:dc="http://purl.org/dc/elements/1.1/">

	<xsl:output method="xml"
	    encoding="ISO-8859-1" />

	<xsl:template match="/url-watcher">
	    <rss version="2.0">
		<channel>
		    <title>LA-Hams</title>
		    <link>http://la9pma.org/la-hams/</link>
		    <description>
		        A list of Norwegian ham web pages and other pages of
			interest to the radio amateur. List is sorted with 
			the latest updated pages on the top. All times in UTC.
		    </description>
		    <dc:creator>kms@skontorp.net</dc:creator>

		    <xsl:apply-templates select="pages" />

		</channel>
	    </rss>
	</xsl:template>

	<xsl:template match="/url-watcher/pages/page">
	    <item>
		<title>
		    <xsl:text>'</xsl:text>
		    <xsl:value-of select="title" />
		    <xsl:text>' was last updated </xsl:text>
		    <xsl:value-of select="lastModified/iso-8601" />
		</title>
		<link>
		    <xsl:value-of select="linkURL" />
		</link>
		<description />
		<dc:date>
		    <xsl:value-of select="lastModified/iso-8601" />
		</dc:date>
	    </item>
	</xsl:template>

    </xsl:stylesheet>
