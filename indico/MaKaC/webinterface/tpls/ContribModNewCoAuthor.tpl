<form action=%(postURL)s method="POST">
    <table width="60%%" align="center" border="0" 
                                    style="border-left: 1px solid #777777">
        <tr>
            <td class="groupTitle" colspan="2"><%= _("Defining a new co-author")%></td>
        </tr>
        <tr>
            <td nowrap class="titleCellTD"><span class="titleCellFormat"><%= _("Title")%></span>
            </td>
            <td bgcolor="white" width="100%%" valign="top" class="blacktext">
                <select name="title">%(titles)s</select>
            </td>
        </tr>
        <tr>
            <td nowrap class="titleCellTD">
                <span class="titleCellFormat"><%= _("Family name")%></span>
            </td>
            <td bgcolor="white" width="100%%" valign="top" class="blacktext">
                <input type="text" size="70" name="surName" value="">
            </td>
        </tr>
        <tr>
            <td nowrap class="titleCellTD">
                <span class="titleCellFormat"><%= _("First name")%></span>
            </td>
            <td bgcolor="white" width="100%%" valign="top" class="blacktext">
                <input type="text" size="70" name="name" value="">
            </td>
        </tr>
        <tr>
            <td nowrap class="titleCellTD">
                <span class="titleCellFormat"><%= _("Affiliation")%></span>
            </td>
            <td bgcolor="white" width="100%%" valign="top" class="blacktext">
                <input type="text" size="70" name="affiliation" value="">
            </td>
        </tr>
        <tr>
            <td nowrap class="titleCellTD">
                <span class="titleCellFormat"><%= _("Email")%></span>
            </td>
            <td bgcolor="white" width="100%%" valign="top" class="blacktext">
                <input type="text" size="70" name="email" value="">
            </td>
        </tr>
        <tr>
            <td nowrap class="titleCellTD">
                <span class="titleCellFormat"><%= _("Address")%></span>
            </td>
            <td bgcolor="white" width="100%%" valign="top" class="blacktext">
                <textarea name="address" rows="5" cols="50"></textarea>
            </td>
        </tr>
        <tr>
            <td nowrap class="titleCellTD">
                <span class="titleCellFormat"><%= _("Telephone")%></span>
            </td>
            <td bgcolor="white" width="100%%" valign="top" class="blacktext">
                <input type="text" size="25" name="phone" value="">
            </td>
        </tr>
        <tr>
            <td nowrap class="titleCellTD">
                <span class="titleCellFormat"><%= _("Fax")%></span>
            </td>
            <td bgcolor="white" width="100%%" valign="top" class="blacktext">
                <input type="text" size="25" name="fax" value="">
            </td>
        </tr>
        <tr>
            <td nowrap class="titleCellTD">
                <span class="titleCellFormat"><%= _("Submission control")%></span>
            </td>
            <td bgcolor="white" width="100%%" valign="top" class="blacktext">
                <input type="checkbox" name="submissionControl" checked="checked"><%= _("Give submission rights to the author.")%><br><br><i><font color="black"><b><%= _("Note")%>: </b></font><%= _("If this person does not already have an Indico account, he or she will be sent an email asking to register as a user. After the registration the user will automatically be given submission rights.")%></i>
            </td>
        </tr>
        <tr>
            <td colspan="2">&nbsp;</td>
        </tr>
        <tr>
            <td colspan="2">
                <input type="submit" class="btn" name="ok" value="<%= _("submit")%>">
                <input type="submit" class="btn" name="ok_and_new" value="<%= _("submit & new")%>">
                <input type="submit" class="btn" name="cancel" value="<%= _("cancel")%>">
            </td>
        </tr>
    </table>
</form>
