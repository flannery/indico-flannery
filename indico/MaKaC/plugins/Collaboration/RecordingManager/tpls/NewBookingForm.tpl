<% declareTemplate(newTemplateStyle=True) %>

<div><span>
<a id="scroll_down" name="top"></a>
<br />
</span></div>

<table cellspacing="0px" cellpadding="0px" width="1000px" border="0">
  <tr>
    <td cellspacing="0px" cellpadding="0px" width="550px" valign="top">
        <strong>1. <%= _("Select a talk:") %></strong>
        <br /> <!-- line breaks to make the pretty boxes below to line up -->
        <br />
        <br />
        <div class="nicebox">
        <div class="RMMatchPane">
            <% for talk in Talks: %>
                <% IndicoID = talk["IndicoID"] %>

                  <span>
                    <table cellspacing="0px" cellpadding="0px" border="0">
                    <tr>
                    <td width="370px">
                        <div id="div<%= IndicoID %>" class="RMtalkDisplay" onclick="RMtalkSelect('<%= IndicoID %>');" onmouseover="RMtalkBoxOnHover('<%= IndicoID %>');" onmouseout="RMtalkBoxOffHover('<%= IndicoID %>');">
                            <table cellpadding="0px" cellspacing="0px" border="0">
                            <tr>
                            <td colspan="2" width="370px">
                            <tt><strong><%= {'conference':      "E&nbsp;",
                                     'session':         "S&nbsp;&nbsp;",
                                     'contribution':    "C&nbsp;&nbsp;&nbsp;",
                                     'subcontribution': "SC&nbsp;&nbsp;&nbsp;&nbsp;"}[talk["type"]] %></strong></tt>
                            <strong><%= talk["titleshort"] %></strong>&nbsp;
                            </td>
                            </tr>
                            <tr>
                            <td width="180px" colspan="1" align="left">
                            <tt><%= {'conference':      "&nbsp;&nbsp;",
                                     'session':         "&nbsp;&nbsp;&nbsp;",
                                     'contribution':    "&nbsp;&nbsp;&nbsp;&nbsp;",
                                     'subcontribution': "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"}[talk["type"]] %></tt>
                            <%= talk["date_nice"] %>
                            </td>
                            <td width="190px" colspan="1" align="left">
                            <em>
                            <% if talk["speakers"] != '': %>
                            <%=    talk["speakers"] %>
                            <% end %>
                            </em>
                            </td>
                            </tr>
                            </table>
                        </div>
                    </td>
                    <!--  This column shows whether the talk has a matching LOID associated with it (only makes sense for web lectures, not plain video). -->
                    <td width="50px" valign="top">
                        <% if talk["LOID"] != '': %>
                            <div class="RMcolumnStatusNone" style="background-image: url('<%= "../images/RecordingManagerMicalaCheck.png" %>');">
                            </div>
                        <% end %>
                        <% else: %>
                            <div class="RMcolumnStatusNone">
                            </div>
                        <% end %>
                    </td>
                    <!--  This column shows whether a CDS record for this talk exists, or if it is pending. -->
                    <td width="50px" valign="top">
                        <% if talk["CDSID"] != 'none' and talk["CDSID"] != 'pending': %>
                            <div class="RMcolumnStatusCDSDone" id="divCDS<%= talk["IndicoID"] %>" onclick="RMCDSDoneClick('<%= talk["CDSURL"] %>');" onmouseover="RMCDSDoneOnHover('<%= talk["IndicoID"] %>');" onmouseout="RMCDSDoneOffHover('<%= talk["IndicoID"] %>');">
                            </div>
                        <% end %>
                        <% elif talk["CDSID"] == 'pending': %>
                            <div class="RMcolumnStatusCDSPending">
                            </div>
                        <% end %>
                        <% else: %>
                            <div class="RMcolumnStatusNone">
                            </div>
                        <% end %>
                    </td>
                    <!--  This column shows whether a link has been created from Indico to the CDS record. -->
                    <td width="50px" valign="top">
                        <% if talk["IndicoLink"] == True: %>
                            <div class="RMcolumnStatusNone" style="background-image: url('<%= "../images/RecordingManagerIndicoCheck.png" %>');">
                            </div>
                        <% end %>
                        <% else: %>
                            <div class="RMcolumnStatusNone">
                            </div>
                        <% end %>
                    </td>
                    </tr>
                    </table>
                    </span>
            <% end %>
        </div>
        </div>
    </td>
    <td width="400px" valign="top">
        <strong>2. <%= _("Select content type: ") %></strong>
        <span id="RMbuttonPlainVideo" class="RMbuttonDisplay" onclick="RMbuttonModeSelect('plain_video')" ><%= _("plain video") %></span>
        &nbsp;<%= _(" or ") %>&nbsp;
        <span id="RMbuttonWebLecture" class="RMbuttonDisplay" onclick="RMbuttonModeSelect('web_lecture')" ><%= _("web lecture") %></span>
        <div id="RMrightPaneWebLecture" class="RMHolderPaneDefaultInvisible">
            <br />
            <strong>3. <%= _("Select an orphan lecture object: ") %></strong>
        <div class="nicebox">
        <div class="RMMatchPane">
            <% for orphan in Orphans: %>
                <% lectureDBid = orphan["idLecture"] %>
                <% LOID        = orphan["LOID"] %>
                <div id="lo<%= lectureDBid %>" class="RMLODisplay" onclick="RMLOSelect(<%= lectureDBid %>)" onmouseover="RMLOBoxOnHover(<%= lectureDBid %>);" onmouseout="RMLOBoxOffHover(<%= lectureDBid %>);">
                    <table>
                        <tr width="100%">
                            <td width="30%" valign="top">
                                time: <%= orphan["time"] %><br />
                                date: <%= orphan["date"] %><br />
                                box:  <%= orphan["box"]  %>
                            </td>
                            <td width="70%" align="right">&nbsp;
<!--
                                <img src="<%= PreviewURL %><%= LOID %>/video0001.jpg">
                                <img src="<%= PreviewURL %><%= LOID %>/video0002.jpg"><br />
 -->
                            </td>
                        </tr>
                        <tr width="100%">
                            <td width="100%" colspan="2">&nbsp;
<!--
                            <img src="<%= PreviewURL %><%= LOID %>/content0001.jpg">
                            <img src="<%= PreviewURL %><%= LOID %>/content0002.jpg">
                            <img src="<%= PreviewURL %><%= LOID %>/content0003.jpg">
                            <img src="<%= PreviewURL %><%= LOID %>/content0004.jpg">
 -->
                             </td>
                        </tr>
                    </table>
                </div>
            <% end %>
        </div>
        </div>
        </div>
        <div id="RMrightPanePlainVideo" class="RMHolderPaneDefaultInvisible">
            <br />
            <strong>3. <%= _("Select options: ") %></strong>
            <div class="RMMatchPane" style="height: 200px;">
                Select video aspect ratio:
                <input type="radio" name="talks" value="standard" id="RMvideoFormat4to3" onclick="RMchooseVideoFormat('standard')" checked>
                <label for="RMvideoFormat4to3">standard (4/3)</label>
                &nbsp;&nbsp;&nbsp;
                <input type="radio" name="talks" value="wide" id="RMvideoFormat16to9" onclick="RMchooseVideoFormat('wide')">
                <label for="RMvideoFormat16to9">wide (16/9)</label>
            </div>
        </div>
    </td>
  </tr>
</table>

<div id="RMlowerPane" class="RMHolderPaneDefaultVisible" style="margin-left: 150px;">
    <span>
        <br />
        <strong>4. <%= _("Select language(s) in which the talk was given") %></strong>
        <br />
        <% if not FlagLanguageDataOK: %>
            <font color="red"><%= _("ERROR: Malformed language data. Please check Recording Manager plugin settings.") %>
            <ul>
                <% for msg in LanguageErrorMessages: %>
                <li><%= msg %></li>
                <% end %>
            </ul>
            </font>
        <% end %>
        <% else: %>
        <!-- http://www.loc.gov/marc/languages/ -->
        <input type="checkbox" value="<%= LanguageCodePrimary %>" id="RMLanguagePrimary" onclick="RMLanguageTogglePrimary('<%= LanguageCodePrimary %>')"><%= LanguageDictionary[LanguageCodePrimary] %></input>
        &nbsp;&nbsp;&nbsp;&nbsp;
        <input type="checkbox" value="<%= LanguageCodeSecondary %>" id="RMLanguageSecondary" onclick="RMLanguageToggleSecondary('<%= LanguageCodeSecondary %>')"><%= LanguageDictionary[LanguageCodeSecondary] %></input>
        &nbsp;&nbsp;&nbsp;&nbsp;
        <input type="checkbox" name="Other" value="other" id="RMLanguageOther" onclick="RMLanguageToggleOther()">Other</input>
        <select id="RMLanguageOtherSelect">
            <option value="chooseOne" onclick="RMLanguageSelectOther(0)">-- <%= _('Choose one') %> --</option>
            <% for languageCode in LanguageCodes: %>
                <% if languageCode != LanguageCodePrimary and languageCode != LanguageCodeSecondary: %>
                <option value="<%=languageCode%>" onclick="RMLanguageSelectOther('<%=languageCode%>')"><%=LanguageDictionary[languageCode]%></option>
                <% end %>
            <% end %>
        </select>
        <span id="RMSelectLanguage">
        <!--  Javascript button here -->
        </span>
        <% end %>
    </span>
    <span>
        <br />
        <strong>5. <%= _("Create CDS record (and update micala database)") %></strong>
        <br />
        <span id="RMbuttonCreateCDSRecord">
        <!--  Javascript button here -->
        </span>
        <span id="RMMatchSummaryMessage">
        </span>
    </span>
    <br />
    <br />
    <br />
    <span>
        <strong>6. <%= _("Create Indico link to CDS record") %></strong>
        <br />
        <div id="RMbuttonCreateIndicoLink">
        <!--  Javascript button here -->
        </div>
    </span>
</div>

<script type="text/javascript">
    var RMselectedTalkId    = '';
    var RMselectedLODBID    = '';
    var RMselectedTalkName  = '';
    var RMselectedLOName    = '';
    var RMviewMode          = '';
    var RMvideoFormat       = 'standard';
    var RMLanguageFlagPrimary   = true;
    var RMLanguageFlagSecondary = false;
    var RMLanguageFlagOther     = false;
    var RMLanguageValuePrimary   = '<%= LanguageCodePrimary %>';
    var RMLanguageValueSecondary = '<%= LanguageCodeSecondary %>';
    var RMLanguageValueOther    = 0;

    // convert Python list of dictionaries Talks into a Javascript dictionary of dictionaries RMTalkList
    // (even though it's called RMTalkList, which is confusing)
    var RMTalkList = {
    <% for talk in Talks: %>
    "<%= talk["IndicoID"] %>": <%= jsonEncode(talk) %>,
    <% end %>
    };

    // Pass the metadata we need for each lecture object
    // convert Python list of dictionaries Orphans into a Javascript dictionary of dictionaries RMLOList
    // (even though it's called RMLOList, which is confusing)
    var RMLOList = {
    <% for orphan in Orphans: %>
        "<%= orphan["idLecture"]   %>": <%= jsonEncode(orphan) %>,
    <% end %>
    };

    // Draw the two buttons, which start out as disabled until
    // the user has selected both talk and LO
    $E('RMbuttonCreateCDSRecord').set(ButtonCreateCDSRecord.draw());
    $E('RMbuttonCreateIndicoLink').set(ButtonCreateIndicoLink.draw());

</script>