<?xml version="1.0" encoding="ISO-8859-1"?>

<!-- (c) Karl-Martin Skontorp <kms@skontorp.net> -->

    <xsl:stylesheet version="1.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<xsl:output method="text"
	    encoding="ISO-8859-1"
	    omit-xml-declaration="yes" />

	<xsl:param name="now" />

	<xsl:template match="/url-watcher">
	    <xsl:text>LA-Hams: updates last 24 hours</xsl:text>
	    <xsl:text>&#x0A;</xsl:text>

	    <xsl:value-of select="substring(generated, 1, 16)" />
	    <xsl:text>&#x0A;</xsl:text>
	    <xsl:text>------------------------------</xsl:text>
	    <xsl:text>&#x0A;</xsl:text>
	    <xsl:text>&#x0A;</xsl:text>

	    <xsl:apply-templates select="pages/page[lastModified/unix >= ($now - 86400)]">
		<xsl:sort select="lastModified/iso-8601" order="descending" />
	    </xsl:apply-templates>
	</xsl:template>

	<xsl:template match="/url-watcher/pages/page">

	    <xsl:value-of select="title" />
	    <xsl:text> [</xsl:text>
	    <xsl:value-of select="lastModified/iso-8601" />
	    <xsl:text>]</xsl:text>
	    <xsl:text>&#x0A;</xsl:text>
	    <xsl:value-of select="linkURL" />
	    <xsl:text>&#x0A;</xsl:text>
	    <xsl:text>&#x0A;</xsl:text>
	</xsl:template>

    </xsl:stylesheet>
