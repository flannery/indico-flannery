<table width="100%%" border="0" cellspacing="1" cellpadding="0" 
        align="center" class="conf">
    <tr>
        <td class="confLogoBox">
            <!--LOGO-->
            %(logo)s
        </td>
        <td class="confTitleBox" width="100%%">
            <!--Conference main data-->
			<table width="100%%" border="0" cellspacing="0" cellpadding="0" align="center">
				<tr>
					<td colspan="2" class="confTitle" align="left" width="100%%" style="background:%(bgColorCode)s"><b><span class="conferencetitlelink" style="color:%(textColorCode)s">%(confTitle)s</span></b></td>
				</tr>
                <tr>
				   <td class="confDate" nowrap>%(confDateInterval)s</td>
				   <td class="confPlace">%(confLocation)s</td>
				</tr>
            </table>
        </td>
    </tr>
    <tr>
		%(menu)s
        %(body)s
    </tr>
</table>
