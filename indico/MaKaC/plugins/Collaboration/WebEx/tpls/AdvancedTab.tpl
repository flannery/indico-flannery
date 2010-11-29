
<div class="collaborationAdvancedTabTitleLine">
    <div class="collaborationAdvancedTabTitle">Information displayed in event page</div>
</div>

<div class="collaborationAdvancedTabCheckboxDiv" style="margin-top:10px">
    <input type="checkbox" id="showAccessPassword" class="centeredCheckBox" name="showAccessPassword" value="yes" ></input>
    <label for="displayPin" class="normal"><%= _("Show access password on event display page?") %></label>
    <img id="showAccessPasswordHelp" src="<%= systemIcon('help')%>" style="margin-left:5px; vertical-align:middle;" />
</div>

<div class="collaborationAdvancedTabTitleLine">
    <div class="collaborationAdvancedTabTitle">Other options</div>
</div>
<div style="margin-top:10px">
<% includeTpl('ConfModifCollaborationDefaultAdvancedTab') %>
</div>
