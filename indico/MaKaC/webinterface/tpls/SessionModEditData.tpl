<form id="SessionDataModificationForm" method="POST" action=%(postURL)s>
  <table width="60%%" align="center" border="0" style="border-left: 1px solid #777777;padding-left:2px">
    <tr>
      <td colspan="2" class="groupTitle">%(pageTitle)s</td>
    </tr>
    %(errors)s
    %(code)s
    <tr> 
      <td class="titleCellTD"><span class="titleCellFormat"><%= _("Title")%></span></td>
      <td>
	<input type="text" name="title" size="80" value=%(title)s>
      </td>
    </tr>
    <tr>
      <td class="titleCellTD"><span class="titleCellFormat"><%= _("Description")%></span></td>
      <td>
	<textarea name="description" cols="80" rows="8" wrap="soft">%(description)s</textarea>
      </td>
    </tr>
    

    <% includeTpl('EventLocationInfo', event=self._rh._target, modifying=True, parentRoomInfo=roomInfo(self._rh._target, level='inherited'), showParent=True) %>

    <tr>
      <td class="titleCellTD"><span class="titleCellFormat"><%= _("Start date")%></span></td>
      <td valign="top" bgcolor="white" width="100%%">&nbsp;
      <span id="sDatePlace"></span>
                <input type="hidden" value="<%= sDay %>" name="sDay" id="sDay"/>                                       
                <input type="hidden" value="<%= sMonth %>" name="sMonth" id="sMonth"/>
                <input type="hidden" value="<%= sYear %>" name="sYear" id="sYear"/>   
                <input type="hidden" value="<%= sHour %>" name="sHour" id="sHour" />
                <input type="hidden" value="<%= sMinute %>" name="sMinute" id="sMinute" />
      %(autoUpdate)s
      </td>
    </tr>
    <tr>
      <td class="titleCellTD"><span class="titleCellFormat"><%= _("End date")%></span></td>
      <td valign="top" bgcolor="white" width="100%%">&nbsp;
      <span id="eDatePlace"></span>
                <input type="hidden" value="<%= eDay %>" name="eDay" id="eDay"/>                                       
                <input type="hidden" value="<%= eMonth %>" name="eMonth" id="eMonth"/>
                <input type="hidden" value="<%= eYear %>" name="eYear" id="eYear"/> 
                <input type="hidden" value="<%= eHour %>" name="eHour" id="eHour" />
                <input type="hidden" value="<%= eMinute %>" name="eMinute" id="eMinute" />
      %(adjustSlots)s
      </td>
    </tr>
    <tr>
      <td class="titleCellTD"><span class="titleCellFormat"><%= _("Contribution duration")%></span></td>
      <td bgcolor="white" width="100%%">&nbsp;
      <input type="text" size="2" name="durHour" value=%(durHour)s />:
      <input type="text" size="2" name="durMin" value=%(durMin)s />
      </td>
    </tr>
    %(Type)s
    %(Colors)s
    %(convener)s        
    <tr align="center">
      <td colspan="2" class="buttonBar" valign="bottom" align="center">
	<input type="submit" class="btn" value="<%= _("ok")%>" name="OK" onClick="this.form.eDay.disabled=0;this.form.eMonth.disabled=0;this.form.eYear.disabled=0;" />
	<input type="submit" class="btn" value="<%= _("cancel")%>" name="CANCEL" />
      </td>
    </tr>
  </table>
</form>

<script type="text/javascript">
IndicoUI.executeOnLoad(function()
    {       
        
        var startDate = IndicoUI.Widgets.Generic.dateField(true,null,['sDay', 'sMonth', 'sYear','sHour', 'sMinute']);
        $E('sDatePlace').set(startDate);
            
        var endDate = IndicoUI.Widgets.Generic.dateField(true,null,['eDay', 'eMonth', 'eYear', 'eHour', 'eMinute']); 
        $E('eDatePlace').set(endDate);
        
        <% if sDay != '': %>
            startDate.set('<%= sDay %>/<%= sMonth %>/<%= sYear %><%= " " %><%if len (sHour) == 1:%>0<%= sHour %><%end%><%else:%><%= sHour %><%end%>:<% if len (sMinute) == 1:%>0<%= sMinute %><%end%><%else:%><%= sMinute %><%end%>');
        <% end %>
        
        <% if eDay != '': %>
            endDate.set('<%= eDay %>/<%= eMonth %>/<%= eYear %><%= " " %><%if len (eHour) == 1:%>0<%= eHour %><%end%><%else:%><%= eHour %><%end%>:<% if len (eMinute) == 1:%>0<%= eMinute %><%end%><%else:%><%= eMinute %><%end%>');
        <% end %> 
     });   
injectValuesInForm($E('SessionDataModificationForm'));

</script>
