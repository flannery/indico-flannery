<table width="80%%" align="center" border="0" style="border-left: 1px solid #777777">
        <tr>
            <td class="groupTitle" colspan="2"> <%= _("Re-allocating conferences")%></td>
    </tr>
    <tr>
        <td align="left" colspan="2" bgcolor="white" style="padding-bottom:10px">
             <%= _("Selected conferences to be moved")%>:
            <ul>%(selectedItems)s</ul>
             <%= _("Please, select the destination category where to move the conferences mentioned above (use the blue arrows to navigate in the category tree)")%>:<br>
                %(categTree)s
        </td>
    </tr>
    <tr>
		<form action="%(cancelURL)s" method="POST">
        <td style="border-top:1px solid #777777; padding-top:10px" align="center">
			<input type="submit" class="btn" name="cancel" value="<%= _("cancel")%>">
        </td>
		</form>
    </tr>
</table>

