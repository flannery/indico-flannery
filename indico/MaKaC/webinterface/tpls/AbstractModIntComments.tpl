
<table width="98%%" cellspacing="1" style="border-left:1px solid #777777" align="center">
    <tr>
		<form action=%(newCommentURL)s method="POST">
        <td style="border-top:2px solid #777777; background:#F6F6F6">
			<input type="submit" class="btn" value="<%= _("new comment")%>">
        </td>
		</form>
    </tr>
    %(comments)s
    <tr>
		<form action=%(newCommentURL)s method="POST">
        <td style="border-bottom:2px solid #777777; background:#F6F6F6">
			<input type="submit" class="btn" value="<%= _("new comment")%>">
        </td>
		</form>
    </tr>
</table>
