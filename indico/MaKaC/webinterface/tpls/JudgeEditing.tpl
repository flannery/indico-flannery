<% from MaKaC.reviewing import ConferenceReview %>
<% import MaKaC.webinterface.urlHandlers as urlHandlers %>

<table width="90%%" align="center" border="0" style="border-left: 1px solid #777777">
    <tr>
        <td colspan="5" class="groupTitle">Give opinion on layout of a contribution</td>
    </tr>
    <tr>
        <td nowrap class="titleCellTD"><span class="titleCellFormat">Approved requirements</span></td>
        <td width="60%%" id="criteriaListDisplay">
        </td>
    </tr>
    <tr>
        <td nowrap class="titleCellTD"><span class="titleCellFormat">Judgement</span></td>
        <td>
            <div id="inPlaceEditJudgement"><%= Editing.getJudgement() %></div>
        </td>
    </tr>
    <tr>
        <td nowrap class="titleCellTD"><span class="titleCellFormat">Comments</span></td>
        <td>
            <div id="inPlaceEditComments"></div>
            These comments, along with your judgement, will be sent by e-mail to the author(s)
        </td>
    </tr>
    <tr>
        <td colspan="10">
            <span id="submitbutton"></span>
            <span id="submittedmessage"></span>
		</td>
    </tr>
</table>


<script type="text/javascript">

var showWidgets = function(firstLoad) {
                           
    new IndicoUI.Widgets.Generic.selectionField($E('inPlaceEditJudgement'),
                        'reviewing.contribution.changeJudgement',
                        {conference: '<%= Contribution.getConference().getId() %>',
                        contribution: '<%= Contribution.getId() %>',
                        current: 'editorJudgement'
                        }, <%= ConferenceReview.predefinedStates %>);
    
    new IndicoUI.Widgets.Generic.richTextField($E('inPlaceEditComments'),
                           'reviewing.contribution.changeComments',
                           {conference: '<%= Contribution.getConference().getId() %>',
                            contribution: '<%= Contribution.getId() %>',
                            current: 'editorJudgement'
                           },400,200);
    
    <% if len (ConfReview.getLayoutCriteria()) == 0 : %>
        $E('criteriaListDisplay').set("No form criteria proposed for this conference.");
    <% end %>
    <% else: %>
        $E("criteriaListDisplay").set('');
        
        <% for c in ConfReview.getLayoutCriteria(): %>
        
            var newDiv = Html.div({style:{borderLeft:'1px solid #777777', paddingLeft:'5px', marginLeft:'10px'}});
            newDiv.append(Html.span(null,"<%=c%>"));
            newDiv.append(Html.br());
            
            if (firstLoad) {
                var initialValue = "<%= Editing.getAnswer(c) %>";
            } else {
                var initialValue = false;
            }
    
            newDiv.append(new IndicoUI.Widgets.Generic.radioButtonField(
                                                    null,
                                                    'horizontal2',
                                                    <%= str(range(len(ConfReview.reviewingQuestionsAnswers))) %>,
                                                    <%= str(ConfReview.reviewingQuestionsLabels) %>,
                                                    initialValue,
                                                    'reviewing.contribution.changeCriteria', 
                                                    {
                                                        conference: '<%= Contribution.getConference().getId() %>',
                                                        contribution: '<%= Contribution.getId() %>',
                                                        criterion: '<%= c %>',
                                                        current: 'editorJudgement'
                                                    }));
                                                
            $E("criteriaListDisplay").append(newDiv);
            $E("criteriaListDisplay").append(Html.br());
            
        <% end %>
    <% end %>
}

var showValues = function() {
    indicoRequest('reviewing.contribution.changeComments',
            {
                conference: '<%= Contribution.getConference().getId() %>',
                contribution: '<%= Contribution.getId() %>',
                current: 'editorJudgement'
            },
            function(result, error){
                if (!error) {
                    $E('inPlaceEditComments').set(result);
                }
            }
        )
    indicoRequest('reviewing.contribution.changeJudgement',
            {
                conference: '<%= Contribution.getConference().getId() %>',
                contribution: '<%= Contribution.getId() %>',
                current: 'editorJudgement'
            },
            function(result, error){
                if (!error) {
                    $E('inPlaceEditJudgement').set(result);
                }
            }
        )
    
    indicoRequest('reviewing.contribution.getCriteria',
            {
                conference: '<%= Contribution.getConference().getId() %>',
                contribution: '<%= Contribution.getId() %>',
                current: 'editorJudgement'
            },
            function(result, error){
                if (!error) {
                    if (result.length == 0) {
                        $E('criteriaListDisplay').set('No form criteria proposed for this conference.');
                    } else {
                        $E('criteriaListDisplay').set('');
                        for (var i = 0; i<result.length; i++) {
                            $E('criteriaListDisplay').append(result[i]);
                            $E('criteriaListDisplay').append(Html.br());
                        }
                    }
                    
                }
            }
        )   
}



<% if Editing.isSubmitted():%> 
var submitted = true;
<% end %>
<% else: %>
var submitted = false;

<% end %>

var updatePage = function (firstLoad){
    if (submitted) {
        submitButton.set('Mark as NOT submitted');
        $E('submittedmessage').set('Judgement submitted');
        showValues();
    } else {
        submitButton.set('Mark as submitted');
        $E('submittedmessage').set('Judgement not submitted yet');
        showWidgets(firstLoad);
    }
}

var submitButton = new IndicoUI.Widgets.Generic.simpleButton($E('submitbutton'), 'reviewing.contribution.setSubmitted',
        {
            conference: '<%= Contribution.getConference().getId() %>',
            contribution: '<%= Contribution.getId() %>',
            current: 'editorJudgement',
            value: true
        },
        function(result, error){
            if (!error) {
                submitted = !submitted;
                updatePage(false)
            } else {
                alert (error)
            }
        },
        ''
);

updatePage(true);

</script>