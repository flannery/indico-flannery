<table>
    <tbody>
        % if Booking.getHasAccessPassword() and Booking.showAccessPassword(): 
        <tr>
            <td class="collaborationConfDisplayInfoLeftCol">
                <span>${ _('Meeting password')}:</span>
            </td>
            <td class="collaborationConfDisplayInfoRightCol">
                ${ Booking.getAccessPassword() }
            </td>
        </tr>
        % elif Booking.getHasAccessPassword(): 
        <tr>
            <td class="collaborationConfDisplayInfoLeftCol">
                <span>${ _('Meeting password')}:</span>
            </td>
            <td class="collaborationConfDisplayInfoRightCol">
                ${ _("This WebEx meeting password is hidden.") }
            </td>
        </tr>
        % endif
        <tr>
            <td class="collaborationConfDisplayInfoLeftCol">
                <span>${ _('Agenda')}:</span>
            </td>
            <td class="collaborationConfDisplayInfoRightCol">
                ${ Booking._bookingParams["meetingDescription"] }
            </td>
        </tr>
        <tr>
            <td class="collaborationConfDisplayInfoLeftCol">
                <span>${ _('Toll free call in number')}:</span>
            </td>
            <td class="collaborationConfDisplayInfoRightCol">
                ${ Booking.getPhoneNum() }
            </td>
        </tr>
        <tr>
            <td class="collaborationConfDisplayInfoLeftCol">
                <span>${ _('Toll call in number')}:</span>
            </td>
            <td class="collaborationConfDisplayInfoRightCol">
                ${ Booking.getPhoneNumToll() }
            </td>
        </tr>
        <tr>
            <td class="collaborationConfDisplayInfoLeftCol">
                <span>${ _('Call in access code')}:</span>
            </td>
            <td class="collaborationConfDisplayInfoRightCol">
                ${ Booking.getPhoneAccessCode() }
            </td>
        </tr>
        <tr>
            <td class="collaborationConfDisplayInfoLeftCol">
                <span>${ _('Join URL')}:</span>
            </td>
            <td class="collaborationConfDisplayInfoRightCol">
                <a href="${ Booking.getUrl() }" target="_blank" >${ Booking.getUrl() }</a>
            </td>
        </tr>
    </tbody>
</table>
