<% includeTpl('FilterCriterionOptions') %>

<% if form.getType() == "2priorities": %>
   <tr style="border-top: 1px solid #999;">
     <td>
       <% checked="" %>
       <% if critFormName == "sessionfirstpriority": %>
         <% checked=" checked" %>
       <% end %>
       <input type="checkbox" name="firstChoice" value="firstChoice"<%= checked %>>
     </td>
     <td>
       <em> <%= _("Only by first choice") %></em>
     </td>
    </tr>
<% end %>

