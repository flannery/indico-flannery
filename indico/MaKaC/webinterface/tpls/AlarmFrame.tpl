
<table align="center" width="90%%">
  <form action="%(addAlarmURL)s" method="POST">
  <tr>
    <td>
      <input type="submit" class="btn" value="<%= _("add new alarm")%>">
    </td>
  </tr>
  </form>
</table>

<table width="90%%" align="center" border="0" style="border-left: 1px solid #777777">
    <tr>
        <td colspan="4" nowrap class="groupTitle">
             <%= _("List of existing alarms")%>
        </td>
    </tr>
    <tr>
        <td bgcolor="white" width="90%%">
            <table width="100%%">
                <tr>
                    <td nowrap class="titleCellFormat"><%= _("Date")%> (%(timezone)s):</td>
                    <td nowrap class="titleCellFormat"><%= _("Subject")%>:</b></td>
                    <td nowrap class="titleCellFormat"><%= _("To")%>:</b></td>
                    <td nowrap class="titleCellFormat"><%= _("Action")%>:</td>
                </tr>
            <% if alarms == "":%>
                <tr><td colspan="4"><em><%= _("There are not alarms yet")%></em></td></tr>
            <% end %>
            <% else: %>
                %(alarms)s
            <% end %>
            </table>
        </td>
    </tr>
</table>
