
type("DateTimeSelector", ["RealtimeTextBox"],
     {
         get: function(direct) {

             // let the programmer choose if for some reason
             // conversion should be bypassed
             var value = RealtimeTextBox.prototype.get.call(this);

             if (value && !direct) {
                 // convert formats, server <-> client
                 var dateTime = Util.parseDateTime(value, this.displayFormat);

                 if (dateTime) {
                     return Util.formatDateTime(dateTime, IndicoDateTimeFormats.Server);
                 } else {
                     return null;
                 }
             } else {
                 return value;
             }
         },

         draw: function() {
             this.enableEvent();
             return this.IWidget.prototype.draw.call(this, this.tab);
         },

         set: function(value, direct) {
             // let the programmer choose if for some reason
             // conversion should be bypassed
             if (!direct) {
                 // convert formats, server <-> client
                 var dateTime = Util.parseDateTime(value, IndicoDateTimeFormats.Server);
                 RealtimeTextBox.prototype.set.call(
                     this,
                     Util.formatDateTime(dateTime, this.displayFormat));
             } else {
                 RealtimeTextBox.prototype.set.call(this, value);
             }
         },


         _setElementErrorState: function(element, text) {
             // use "passive" mode, so that fields can be verified live
             this._stopErrorList = IndicoUtil.markInvalidField(element, text, true)[1];
         },

         _checkErrorState: function() {

             var value = this.get();

             if (!value) {
                 return $T('Date is invalid');
             } else {
                 return null;
             }
         }
     },
     function(args, format) {
         this.displayFormat = format || IndicoDateTimeFormats.Default;
         this.RealtimeTextBox(args);

         this.input;
         this.trigger = Html.img({src: imageSrc("calendarWidget")});
         this.tab = Html.div("dateField", this.input, this.trigger);
         var self = this;

         this.observe(function() {
             self.askForErrorCheck();
             return true;
         });
         // set up the calendar widget to appear on click
         var cal = Calendar.setup({
             inputField: this.input.dom,
             button: this.trigger.dom,
             displayArea: this.input,
             eventName: "click",
             ifFormat: this.displayFormat,
             showsTime: true,
             align: "",
             // notify the selector each time a new date/time is set
             // (since onkeydown/onkeyup won't be called)
             onUpdate: function() { self.notifyChange(); }
         });

     });



type("StartEndDateWidget", ["InlineEditWidget"],
     {
         /* builds the basic structure for both display and
            edit modes */
         __buildStructure: function(start, end) {
             // keep everything in separate lines
             return Html.table({},
                     Html.tbody({},
                             Html.tr("startEndDate",
                                     Html.td("startEndDateEntry", "Starts :"),
                                     Html.td({}, start)),
                             Html.tr("startEndDate",
                                     Html.td("startEndDateEntry", "Ends :"),
                                     Html.td({}, end))));
         },

         __verifyDates: function() {

             var valid = true;

             this.startDate.askForErrorCheck();
             this.endDate.askForErrorCheck();

             if (this.startDate.inError() || this.endDate.inError()) {
                 valid = false;
             } else {

                 var sDateTime = Util.parseJSDateTime(this.startDate.get(), IndicoDateTimeFormats.Server);
                 var eDateTime = Util.parseJSDateTime(this.endDate.get(), IndicoDateTimeFormats.Server);

                 if (sDateTime >= eDateTime) {
                     valid = false;
                     this.startDate.setError($T('Start date should be before end date'));
                     this.endDate.setError($T('End date should be after start date'));
                 } else {
                     valid = true;
                     this.startDate.setError(null);
                     this.endDate.setError(null);
                 }
             }

             this._setSave(valid);
         },

         _handleEditMode: function(value) {

             this.shiftTimes = Html.checkbox({});

             // create datefields
             this.startDate = new DateTimeSelector();
             this.endDate = new DateTimeSelector();

             // set them to the values that are passed
             this.startDate.set(Util.formatDateTime(value.startDate, IndicoDateTimeFormats.Server));
             this.endDate.set(Util.formatDateTime(value.endDate, IndicoDateTimeFormats.Server));

             var self = this;

             this.startDate.observe(function() {
                 self.__verifyDates();
                 return true;
             });
             this.endDate.observe(function() {
                 self.__verifyDates();
                 return true;
             });

             // call buildStructure with modification widgets
             return Html.div({},
                             this.__buildStructure(this.startDate.draw(), this.endDate.draw()),
                             Html.div("widgetCheckboxOption",
                                      this.shiftTimes,
                                      Html.span({},
                                      $T("Move session/contribution times in the timetable accordingly"))));
         },

         _handleDisplayMode: function(value) {
             // call buildStructure with spans
             return this.__buildStructure(
                 Util.formatDateTime(value.startDate),
                 Util.formatDateTime(value.endDate));
         },

         _getNewValue: function() {
             return {startDate: Util.parseDateTime(this.startDate.get(),
                                                   IndicoDateTimeFormats.Server),
                     endDate: Util.parseDateTime(this.endDate.get(),
                                                 IndicoDateTimeFormats.Server),
                     shiftTimes: this.shiftTimes
                     };
         },

         _verifyInput: function() {
             if (!Util.parseDateTime(this.startDate.get())) {
                 return false;
             } else if (!Util.parseDateTime(this.endDate.get())){
                 return false;
             }
             return true;
         }
     },
     function(method, attributes, initValue) {
         this.InlineEditWidget(method, attributes, initValue);
     });


/*
 * A widget that contains a DateTimeSelector and a duration field
 */
type("DateTimeDurationWidget", ["IWidget"],
     {
         draw: function() {
             this.dateTimeField = new DateTimeSelector({});

             $B(this.dateTimeField, this.data.accessor('dateTime'));

             return Html.div(
                 {},
                 Html.label("fieldLabel", this.dateTimeLabel),
                 this.dateTimeField.draw(),
                 Html.span({style:{marginLeft: pixels(10)}},""),
                 Html.label("fieldLabel", this.durationLabel),
                 $B(IndicoUI.Widgets.Generic.durationField(),
                    this.data.accessor('duration')));
         },
         set: function(property, value) {
             this.data.set(property, value);
         },
         accessor: function(property) {
             return this.data.accessor(property);
         }
     },

     /*
      * There are 2 optional labels:
      * - One before the date/time field.
      * - One before the duration field.
      * All 4 element (the 2 fields and the 2 labels) appear in a line.
      * @param {String} defaultDateTime Date formatted like %d/%m/%Y %H:%M (python format)
      * @param {String} defaultDur a duration (for ex: 20)
      * @param {String} dateTimeLabel
      * @param {String} durationLabel
      */
     function(defaultDateTime, defaultDur, dateTimeLabel, durationLabel) {
         this.dateTimeLabel = dateTimeLabel || $T("Date/Time:");
         this.durationLabel = durationLabel || $T("Duration(min):");

         this.data = new WatchObject();
         this.data.set('dateTime', defaultDateTime);
         this.data.set('duration', defaultDur);
     });
