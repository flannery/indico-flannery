<table width="90%%" align="center" border="0" style="border-left: 1px solid #777777;" cellpadding="0" cellspacing="0">
    <tr>
       <td width="90%%">
            <table align="center" width="100%%" cellpadding="0" cellspacing="0">
            <tr>
                    <td class="dataCaptionTD"><span class="dataCaptionFormat"> <%= _("Start date")%></span></td>
                    <td bgcolor="white" class="blacktext">%(start_date)s</td>
                    <form action=%(editURL)s method="POST">
                    <td rowspan="2" valign="bottom" align="right" width="1%%">
                    	%(fitToInnerSlots)s
                    </td>
                    </form>
                </tr>
                <tr>
                    <td class="dataCaptionTD"><span class="dataCaptionFormat"> <%= _("End date")%></span></td>
                    <td bgcolor="white" class="blacktext">%(end_date)s</td>
                </tr>
            	<tr>
                    <td colspan="3" class="horizontalLine">&nbsp;</td>
                </tr>
                <tr>
                    <td style="border-bottom:2px solid #777777;padding-bottom:1px" 
                        valign="bottom" align="left" colspan="3">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="left" width="100%%">
                                    <b>%(day)s</b>
                                </td>
                                <form action=%(newSlotURL)s method="POST">
                                <td>
                                    %(newSlotBtn)s                    
                                </td>
                                </form>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td colspan="3">
                        %(slots)s
                    </td>
                </tr>
                <tr>
                    <td style="border-top:2px solid #777777;padding-bottom:1px" 
                            valign="bottom" align="left" colspan="3">
                        &nbsp;
                    </td>
                </tr>
            </table>
            <br>
       </td>
    </tr>
</table>