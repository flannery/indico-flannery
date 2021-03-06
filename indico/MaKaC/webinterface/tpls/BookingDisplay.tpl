<% from MaKaC.common.timezoneUtils import isToday, isTomorrow, isSameDay %>

<% id = Booking.getId() %>

<div class="collaborationDisplayBookingLine" style="padding-left: 20px">

    <div class="collaborationConfDisplayBookingLine">
    <span class="collaborationDisplayBookingType" style="font-style:italic">
        <%= Booking._getTypeDisplayName() %>
    </span>

    <% if Booking.getStartDate(): %>
        <% if Kind == 'scheduled' and isSameDay(Booking.getStartDate(), Booking.getEndDate(), Timezone): %>
            <span>
            <% if isToday(Booking.getStartDate(), Timezone) : %>
            today
            <% end %>
            <% elif isTomorrow(Booking.getStartDate(), Timezone) : %>
                tomorrow
            <% end %>
            <% else: %>
                <%= formatDate(Booking.getAdjustedStartDate(Timezone).date(), format = "%a %d/%m") %>
            <% end %>
            </span>
            from
            <%= formatTime(Booking.getAdjustedStartDate(Timezone).time()) %>
            to
            <%= formatTime(Booking.getAdjustedEndDate(Timezone).time()) %>
        <% end %>
        <% else: %>
            <% if Kind == 'scheduled' : %>
                from
                <% if isToday(Booking.getStartDate(), Timezone) : %>
                    today at
                <% end %>
                <% elif isTomorrow(Booking.getStartDate(), Timezone) : %>
                    tomorrow at
                <% end %>
                <% else: %>
                    <%= formatDate(Booking.getAdjustedStartDate(Timezone).date(), format = "%a %d/%m") %> at
                <% end %>

                <%= formatTime(Booking.getAdjustedStartDate(Timezone).time()) %>

                until

            <% end %>
            <% else: %>
                ongoing until
            <% end %>



            <% if isToday(Booking.getEndDate(), Timezone) : %>
                today at
            <% end %>
            <% elif isTomorrow(Booking.getEndDate(), Timezone) : %>
                tomorrow at
            <% end %>
            <% else: %>
                <%= formatDate(Booking.getAdjustedEndDate(Timezone).date(), format = "%a %d/%m") %> at
            <% end %>

            <%= formatTime(Booking.getAdjustedEndDate(Timezone).time()) %>
        <% end %>.
    <% end %>

    <% firstLineInfo = Booking._getFirstLineInfo(Timezone) %>
    <% if firstLineInfo: %>
        <%= firstLineInfo %>
    <% end %>

    <% displayInfo = Booking._getInformationDisplay(Timezone) %>
    <% launchInfo = Booking._getLaunchDisplayInfo() %>

    <% if displayInfo or launchInfo: %>
    <span style="margin-left:20px;"></span>
    <% end %>

    <% if displayInfo: %>
        <span class="collaborationDisplayMoreInfo" id="collaborationBookingMoreInfo<%=id%>"><%= _("More Info") %></span>
    <% end %>

    <% if displayInfo and Kind == 'ongoing' and launchInfo: %>
        <span style="margin-left: 5px; margin-right:5px;">|</span>
    <% end %>

    <% if Kind == 'ongoing' and launchInfo: %>
        <a href="<%= launchInfo['launchLink'] %>" id="bookingLink<%=id%>">
            <%= launchInfo['launchText'] %>
        </a>
        <script type="text/javascript">
            $E('bookingLink<%=id%>').dom.onmouseover = function (event) {
                IndicoUI.Widgets.Generic.tooltip($E('bookingLink<%=id%>').dom, event,
                        '<div class="collaborationLinkTooltipConference"><%= launchInfo["launchTooltip"] %><\/div>');
            }
        </script>
    <% end %>
    </div>

    <% if displayInfo: %>
        <div id="collaborationInfoLine<%=id%>" style="visibility: hidden; overflow: hidden;">
            <div class="collaborationDisplayInfoLine">
            <%= Booking._getInformationDisplay(Timezone) %>
            </div>
        </div>

        <script type="text/javascript">
            var bookingInfoState<%=id%> = false;
            var height<%=id%> = IndicoUI.Effect.prepareForSlide('collaborationInfoLine<%=id%>', true);
            $E('collaborationBookingMoreInfo<%=id%>').observeClick(function(){
                if (bookingInfoState<%= Booking.getId() %>) {
                    IndicoUI.Effect.slide('collaborationInfoLine<%=id%>', height<%=id%>);
                    $E('collaborationBookingMoreInfo<%=id%>').set($T('More info'));
                    $E('collaborationBookingMoreInfo<%=id%>').dom.className = 'collaborationDisplayMoreInfo';
                } else {
                    IndicoUI.Effect.slide('collaborationInfoLine<%=id%>', height<%=id%>);
                    $E('collaborationBookingMoreInfo<%=id%>').set($T('Hide info'));
                    $E('collaborationBookingMoreInfo<%=id%>').dom.className = 'collaborationDisplayHideInfo';
                }
                bookingInfoState<%=id%> = !bookingInfoState<%=id%>;
            });
            $E('collaborationBookingMoreInfo<%=id%>').dom.onmouseover = function (event) {
                IndicoUI.Widgets.Generic.tooltip($E('collaborationBookingMoreInfo<%=id%>').dom, event,
                        '<div class="collaborationLinkTooltipConference">Click here to show / hide detailed information.<\/div>');
            }
        </script>
    <% end %>
</div>
