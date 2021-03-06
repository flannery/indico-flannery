  <tr>
    <td nowrap class="titleCellTD">
      <span class="titleCellFormat">%(personName)s</span>
    </td>
    <td>
      <table>
      <tr>
      	<td valign="top">
          <table>
          <tr>
            <td align="right">
              <select name="%(personChosen)s">
              %(personOptions)s
              </select>
            </td>
            <input type="hidden" name="performedAction" value="" disabled>
            <td><input type="submit" id="chooseButton" class="btn" value="<%= _("Choose")%>" %(disabledAdd)s onClick="setAction(this.form,'Add as %(personType)s');"><td>
            <td><input type="submit" class="btn" value="<%= _("Search")%>" onClick="setAction(this.form,'Search %(personType)s');"></td>
            <td><input type="submit" class="btn" value="<%= _("New")%>" onClick="setAction(this.form,'New %(personType)s');"></td>            
          </tr>
          %(submissionButtons)s
          </table>
        </td>
      </tr>
      <tr>
        <td align="left" valign="top">
          <ul class="UIPeopleList" style="width:300px">
          	<% counter = 0 %>
 
 		  <% if personDefined != None: %>
	            <% for person in personDefined: %>
    	             <li class="UIPerson">
        	             <input type="hidden" id="removeParams" />
            	         <span class="nameLink">						
			   <%= person[0].getFullName() %>
			   <% if person[1]: %>
			      <em><%= _("(submitter)")%>
			   <% end %>
			 </span>
			 <a href="#" class="UIRowButton" onclick="javascript:removeItem('<%= personType %>',<%= counter %>);return false;" ><img src="<%= systemIcon('remove') %>" title="Remove this <%= personType %> from your list" /></a>
                     </li>
		     <% counter += 1 %>
		   <% end %>
		 <% end %>
          </ul>
        </td>        
      </tr>
      </table>
    </td>
  </tr>

<script>
		
function setAction(form,text) {
  for (var i=0;i<form.length;i=i+1) {
    if (form.elements[i].type=="hidden" && form.elements[i].name == 'performedAction') {
      form.elements[i].value=text;
      form.elements[i].disabled=0;
      return;
    }
  }
}

function removeItem(type, index) {	
	setAction($E('removeParams').dom.form,'Remove '+type+'s');
	$E('removeParams').dom.name=type+"s";
	$E('removeParams').dom.value=index;
	$E('removeParams').dom.form.submit();
}

</script>
