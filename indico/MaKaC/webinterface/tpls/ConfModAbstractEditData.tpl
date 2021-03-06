<form action=%(postURL)s method="POST">
<tr><td>
    <table align="center" width="100%%" border="0">
        <tr>
            <td nowrap class="titleCellTD"><span class="titleCellFormat"> <%= _("Title")%></span></td>
            <td><input type="text" name="title" size="90" value=%(title)s></td>
        </tr> 
        %(additionalFields)s
        <tr>
            <td nowrap class="titleCellTD"><span class="titleCellFormat"> <%= _("Primary authors")%></span></td>
            <td>
                <table cellspacing="0" cellpadding="0" width="50%%" align="left" valign="middle" border="0">
                    %(primaryAuthors)s
					<tr>
						<td colspan="3">
							<input type="submit" class="btn" name="remPrimAuthors" value="<%= _("remove selected primary authors")%>">
							<input type="submit" class="btn" name="addPrimAuthor" value="<%= _("new primary author")%>">
						</td>
					</tr>
				</table>
            </td>
        </tr>
        <tr>
            <td nowrap class="titleCellTD"><span class="titleCellFormat"> <%= _("Co-authors")%></span></td>
            <td>
                <table cellspacing="0" cellpadding="0" width="50%%" align="left" valign="middle" border="0">
                    %(coAuthors)s
					<tr>
						<td colspan="3">
							<input type="submit" class="btn" name="remCoAuthors" value="<%= _("remove selected co-authors")%>">
							<input type="submit" class="btn" name="addCoAuthor" value="<%= _("new co-author")%>">
						</td>
					</tr>
				</table>
            </td>
        </tr>
        <tr>
            <td nowrap class="titleCellTD"><span class="titleCellFormat"> <%= _("Contribution type")%></span></td>
            <td><select name="contribType">%(contribTypeItems)s</select></td>
        </tr>
        <tr><td colspan="2">&nbsp;</td></tr>
        <tr align="center">
            <td colspan="2" style="border-top:1px solid #777777;" valign="bottom" align="center">
                <input type="submit" class="btn" name="OK" value="<%= _("submit")%>">
                <input type="submit" class="btn" name="CANCEL" value="<%= _("cancel")%>">
            </td>
        </tr>
    </table>
</td></tr>
</form>

