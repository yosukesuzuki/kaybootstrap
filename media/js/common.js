//from http://stackoverflow.com/questions/3830418/is-there-a-jquery-plugin-to-convert-utc-datetimes-to-local-user-timezone
(function ($) {
$.fn.localTimeFromUTC = function (format) {
    return this.each(function () {

        // get provided date 
        var tagText = $(this).html();
        var givenDate = new Date(tagText);

        if(givenDate == 'NaN') return;

        // get time offset from browser 
        var offset = -(givenDate.getTimezoneOffset() / 60);

        // apply offset 
        var hours = givenDate.getHours();
        hours += offset;
        givenDate.setHours(hours);

        // format the date 
        var localDateString = $.format.date(givenDate, format);
        $(this).html(localDateString);
    });
};
})(jQuery);

$(document).ready(function() {
    $('.display_time_local').localTimeFromUTC('yyyy-MM-dd HH:mm');
});
