<?xml version="1.0"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml">

  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>

  <xsl:template match="/">
    <html>
      <head>
        <title>Question 2</title>
        <style>
          #resultTable {
            border-style: solid;
            border-color: black;
            border-width: 1px;
          }
         #resultTable td {
            border-style: dotted;
            border-color: grey;
            border-width: 1px;
            padding: 1px;
          }
          .column1 {
            color: grey;
            text-align: right;
          }
          .column2 {
            color: maroon;
            text-align: left;
          }
        </style>
      </head>
      <body>
        <h1>Exam Result</h1>

        <table id="resultTable">
          <tr>
            <td class="column1">Reference Number</td>
            <td class="column2"><xsl:value-of select="result/@ref"/></td>
          </tr>
          <tr>
            <td class="column1">Exam Number</td>
            <td class="column2"><xsl:value-of select="result/examId"/></td>
          </tr>
          <tr>
            <td class="column1">Contestant ID</td>
            <td class="column2"><xsl:value-of select="result/contestantId"/></td>
          </tr>
          <tr>
            <td class="column1">Digital Signature</td>
            <td class="column2"><xsl:value-of select="result/digitalSignature"/></td>
          </tr>
          <tr>
            <td class="column1">Score</td>
            <td class="column2"><xsl:value-of select="result/score"/></td>
          </tr>
          <tr>
            <td class="column1">Band</td>
            <td class="column2"><xsl:value-of select="result/band"/></td>
          </tr>
        </table>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
