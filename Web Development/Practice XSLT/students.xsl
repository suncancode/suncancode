<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml">
    <xsl:template match="/">
        <html>
            <head>
                <title>Student Information</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 20px;
                    }
                    table {
                        border-collapse: collapse;
                        width: 100%;
                    }
                </style>
            </head>
            <body>
                <h2>Student Records</h2>
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Course</th>
                        <th>Grade</th>
                    </tr>
                    <xsl:for-each select="students/student">
                        <tr>
                            <td><xsl:value-of select="id"/></td>
                            <td><xsl:value-of select="name"/></td>
                            <td><xsl:value-of select="course"/></td>
                            <td><xsl:value-of select="grade"/></td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>