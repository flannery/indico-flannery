<form action=%(postURL)s method="POST">
    <table width="80%%" align="center" border="0" style="border-left: 1px solid #777777">
        <tr>
            <td class="groupTitle" colspan="3">Configuration of worldpay</td>
        </tr>
        <tr>
            <td nowrap class="dataCaptionTD"><span class="titleCellFormat">Title</span></td>
            <td align="left" colspan="2"><input type="text" name="title" size="60" value="%(title)s"></td>
        </tr>
		<tr>
			<td class="dataCaptionTD"><span class="dataCaptionFormat">URL of worldpay</span></td>
			<td align="left" colspan="2"><input type="text" name="url" size="60" value="%(url)s"></td>
		</tr>
		<tr>
			<td class="dataCaptionTD"><span class="dataCaptionFormat">Description</span></td>
			<td align="left" colspan="2"><input type="text" name="description" size="60" value="%(description)s"></td>
		</tr>
		<tr>
			<td class="dataCaptionTD"><span class="dataCaptionFormat">InstID</span></td>
			<td align="left" colspan="2"><input type="text" name="instId" size="60" value="%(instId)s"></td>
		</tr>
		<tr>
			<td class="dataCaptionTD"><span class="dataCaptionFormat">Test mode</span></td>
			<td align="left" colspan="2"><input type="text" name="testMode" size="60" value="%(testMode)s"></td>
		</tr>
		<tr>
			<td class="dataCaptionTD"><span class="dataCaptionFormat">Accepted Payment response</span></td>
			<td align="left" valign="top"><textarea name="APResponse" rows="12" cols="60">%(APResponse)s</textarea></td>
			<td rowspan=2 nowrap>You can use the following tags to personalize the responses.<br>
						         <u>Warning</u>: the %% character is reserved. Use %%%% to use it.<br><br>
								<table><tr><td width="10"><td><pre>%(legend)s</pre></td></tr></table></td>
		</tr>
		<tr>
			<td class="dataCaptionTD"><span class="dataCaptionFormat">Cancelled Payment response</span></td>
			<td align="left" valign="top"><textarea name="CPResponse" rows="12" cols="60">%(CPResponse)s</textarea></td>
		</tr>
		<tr><td>&nbsp;</td></tr>
        <tr>
            <td colspan="3" align="left"><input type="submit" value="OK">&nbsp;<input type="submit" value="cancel" name="cancel"></td>
        </tr>
    </table>
</form>
