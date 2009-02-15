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

        <xsl:template match="/url-watcher">
            <html>
                <head>
                    <title>
                        <xsl:text>LA-Hams List</xsl:text>
                    </title>
                    <link rel="stylesheet" href="../main.css" type="text/css" />
                    <link rel="icon" href="../la-hams-icon.png" type="image/png" />
                    <meta http-equiv="refresh" content="3600" />
                </head>

                <body>
                    <div class="bigHeader">
                        <img src="../la-hams.jpg" alt="LA-Hams" />
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

                    <div class="topLinks">
                        <a href="../">Back</a>
                    </div>

                    <div class="list">
                        <xsl:apply-templates select="pages" />
                    </div>
                </body>
            </html>
        </xsl:template>

        <xsl:key name="pages-by-category" match="/url-watcher/pages/page"
            use="category" />

        <xsl:template match="/url-watcher/pages">
            <xsl:for-each select="page[count(. | key('pages-by-category',
                category)[1]) = 1]">

                <xsl:sort select="category"
                    order="ascending" />

                <div class="date-category">
                    <xsl:apply-templates select="category" />
                </div>

                <xsl:for-each select="key('pages-by-category', category)">

                    <xsl:sort select="title" order="ascending" />

                    <div class="listLine">
                        <span class="link">
                            <a>
                                <xsl:attribute name="href">
                                    <xsl:value-of select="linkURL" />
                                </xsl:attribute>
                                <xsl:value-of select="title" />
                            </a>
                        </span>
                        <span class="timestamp">
                            <xsl:text> (</xsl:text>
                            <xsl:value-of select="substring(lastModified/iso-8601, 1, 10)" />
                            <xsl:text> </xsl:text>
                            <xsl:value-of select="lastModified/time" />
                            <xsl:text>)</xsl:text>
                        </span>
                    </div>
                </xsl:for-each>
            </xsl:for-each>
        </xsl:template>

        <xsl:template match="/url-watcher/pages/page/category">
            <xsl:choose>
                <xsl:when test=". = 'Personal'">
                    <img src="../p.png" alt="P" />
                    Personal
                </xsl:when>
                <xsl:when test=". = 'Group'">
                    <img src="../g.png" alt="G" />
                    Group
                </xsl:when>
                <xsl:when test=". = 'DX/Contest'">
                    <img src="../dx-c.png" alt="DX/C" />
                    DX/Contest
                </xsl:when>
                <xsl:when test=". = 'News'">
                    <img src="../n.png" alt="N" />
                    News
                </xsl:when>
                <xsl:when test=". = 'Commercial'">
                    <img src="../c.png" alt="C" />
                    Commercial
                </xsl:when>
                <xsl:when test=". = 'Misc'">
                    <img src="../m.png" alt="M" />
                    Misc
                </xsl:when>
            </xsl:choose>
        </xsl:template>

    </xsl:stylesheet>
