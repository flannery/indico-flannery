<% import MaKaC.webinterface.urlHandlers as urlHandlers %>
<% from MaKaC.common.timezoneUtils import nowutc %>
<% from MaKaC.conference import ContribStatusNone %>

<% dueDateFormat = "%a %d %b %Y" %>

<% if ConfReview.isReferee(User): %>
<table class="Revtab" width="90%%" cellspacing="0" align="center" border="0" style="border-left: 1px solid #777777;padding-left:2px">
    <tr>
        <td nowrap class="groupTitle" colspan=4><%= _("Contributions to judge as Referee")%></td>
    </tr>
    <tr>
        <td nowrap class="titleCellFormat" style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;border-bottom: 1px solid #5294CC;">Id</td>
        <td nowrap class="titleCellFormat" style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;border-bottom: 1px solid #5294CC;"><%= _("Title")%></td>
        <td nowrap class="titleCellFormat" style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;border-bottom: 1px solid #5294CC;"><%= _("State")%></td>
        <td nowrap class="titleCellFormat" style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;border-bottom: 1px solid #5294CC;"><%= _("Due date")%></td>
    </tr>
   
    <% for c in ConfReview.getJudgedContributions(User): %>
        <% if not isinstance(c.getStatus(), ContribStatusNone): %>
	    <tr valign="top">
            <td style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;"><%= c.getId() %></td>
            <td style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;"><a href="<%= urlHandlers.UHContributionModifReviewing.getURL(c) %>"><%= c.getTitle() %></a></td>
            <td style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;">
            <% if c.getReviewManager().getLastReview().getRefereeJudgement().isSubmitted(): %>
                <span style="color:green;"><%= _("Judged:")%> <%= c.getReviewManager().getLastReview().getRefereeJudgement().getJudgement() %></span>
            <% end %>
            <% else: %>
                <span style="color:red;"><%= _("Not judged yet")%></span><br>
                <%= "<br>".join(c.getReviewManager().getLastReview().getReviewingStatus()) %>
            <% end %>
            </td>    
            <td style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;">
                <% date = c.getReviewManager().getLastReview().getAdjustedRefereeDueDate() %>
                <% if date is None: %>
                    <%= _("Due date not set.")%>
                <% end %>
                <% else: %>
                <% if date < nowutc() and not c.getReviewManager().getLastReview().getRefereeJudgement().isSubmitted(): %>
                    <span style="color:red;">
                    <% end %>
                    <% else: %>
                    <span style="color:green;">
                    <% end %>
                    <%= date.strftime(dueDateFormat) %>
                    </span>
                <% end %>
            </td>                    
        </tr>
        <% end %>
    <% end %>
</table>
<br>
<% end %>

<% if ConfReview.isEditor(User): %>
<table class="Revtab" width="90%%" cellspacing="0" align="center" border="0" style="border-left: 1px solid #777777;padding-left:2px">
    <tr>
        <td nowrap class="groupTitle" colspan=4><%= _("Judge editing of the contribution")%></td>
    </tr>
    <tr>
        <td nowrap class="titleCellFormat" style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;border-bottom: 1px solid #5294CC;"><%= _("Id")%></td>
        <td nowrap class="titleCellFormat" style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;border-bottom: 1px solid #5294CC;"><%= _("Title")%></td>
        <td nowrap class="titleCellFormat" style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;border-bottom: 1px solid #5294CC;"><%= _("State")%></td>
        <td nowrap class="titleCellFormat" style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;border-bottom: 1px solid #5294CC;"><%= _("Due date")%></td>
    </tr>
   
	<% for c in ConfReview.getEditedContributions(User): %>
        <% if not isinstance(c.getStatus(), ContribStatusNone): %>
        <tr valign="top">
            <td style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;"><%= c.getId() %></td>
            <td style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;"><a href="<%= urlHandlers.UHContributionModifReviewing.getURL(c) %>"><%= c.getTitle() %></a></td>
            <td style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;">
                <% if c.getReviewManager().getLastReview().getEditorJudgement().isSubmitted(): %>
                    <span style="color:green;"><%= _("Layout judgement given")%></span>
                <% end %>
                <% else: %>
                    <span style="color:red;"><%= _("Layout judgement not given yet")%></span>
                    <% if c.getReviewManager().getLastReview().getRefereeJudgement().isSubmitted(): %>
                    <span style="color:green;"><br><%= _("but Referee already judged contribution")%></span>
                    <% end %>
                <% end %>
            </td>   
            <td style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;">
            <% date = c.getReviewManager().getLastReview().getAdjustedEditorDueDate() %>
            <% if date is None: %>
                <%= _("Due date not set.")%>
            <% end %>
            <% else: %>
                <% if date < nowutc() and not c.getReviewManager().getLastReview().getEditorJudgement().isSubmitted(): %>
                <span style="color:red;">
                <% end %>
                <% else: %>
                <span style="color:green;">
                <% end %>
                <%= date.strftime(dueDateFormat) %>
                </span>
            <% end %>
            </td>                    
        </tr>
        <% end %>
    <% end %>
    
</table>
<br>
<% end %>

<% if ConfReview.isReviewer(User): %>
<table class="Revtab" width="90%%" cellspacing="0" align="center" border="0" style="border-left: 1px solid #777777;padding-left:2px">
    <tr>
        <td nowrap class="groupTitle" colspan=4><%= _("Give advice on content of the contribution")%></td>
    </tr>
    <tr>
        <td nowrap class="titleCellFormat" style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;border-bottom: 1px solid #5294CC;"><%= _("Id")%></td>
        <td nowrap class="titleCellFormat" style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;border-bottom: 1px solid #5294CC;"><%= _("Title")%></td>
        <td nowrap class="titleCellFormat" style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;border-bottom: 1px solid #5294CC;"><%= _("State")%></td>
        <td nowrap class="titleCellFormat" style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;border-bottom: 1px solid #5294CC;"><%= _("Due date")%></td>
    </tr>
   
	<% for c in ConfReview.getReviewedContributions(User): %>
        <% if not isinstance(c.getStatus(), ContribStatusNone): %>
        <tr valign="top">
            <td style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;"><%= c.getId() %></td>
            <td style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;"><a href="<%= urlHandlers.UHContributionModifReviewing.getURL(c) %>"><%= c.getTitle() %></a></td>
            <td style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;">
                <% if c.getReviewManager().getLastReview().hasGivenAdvice(User): %>
                    <span style="color:green;"><%= _("Advice given")%></span>
                <% end %>
                <% else: %>
                    <span style="color:red;"><%= _("Advice not given yet")%></span>
                    <% if c.getReviewManager().getLastReview().getRefereeJudgement().isSubmitted(): %>
                    <span style="color:green;"><br><%= _("but Referee already judged contribution")%></span>
                    <% end %>
                <% end %>
            </td>
            <td style="border-right:5px solid #FFFFFF;border-left:5px solid #FFFFFF;">
            <% date = c.getReviewManager().getLastReview().getAdjustedReviewerDueDate() %>
            <% if date is None: %>
                <%= _("Due date not set.")%>
            <% end %>
            <% else: %>
                <% if date < nowutc() and not c.getReviewManager().getLastReview().hasGivenAdvice(User): %>
                <span style="color:red;">
                <% end %>
                <% else: %>
                <span style="color:green;">
                <% end %>
                <%= date.strftime(dueDateFormat) %>
                </span>
            <% end %>
            </td>                    
        </tr>
        <% end %>
    <% end %>
    
</table>
<% end %>