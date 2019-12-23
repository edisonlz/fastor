/* Simplified Chinese translation for the jQuery Timepicker Addon /
/ Written by Will Lu */
//(function($) {
//	$.timepicker.regional['zh-CN'] = {
//		timeOnlyTitle: '选择时间',
//		timeText: '时间',
//		hourText: '小时',
//		minuteText: '分钟',
//		secondText: '秒钟',
//		millisecText: '毫秒',
//		microsecText: '微秒',
//		timezoneText: '时区',
//		currentText: '现在时间',
//		closeText: '关闭',
//		timeFormat: 'yy:mm:dd',
//		timeSuffix: '',
//		amNames: ['AM', 'A'],
//		pmNames: ['PM', 'P'],
//		isRTL: false
//	};
//	$.timepicker.setDefaults($.timepicker.regional['zh-CN']);
//})(jQuery);

jQuery(function($){
        $.datepicker.regional['zh-CN'] = {
                    closeText: '关闭',
        prevText: '&#x3C;上月',
        nextText: '下月&#x3E;',
        currentText: '今天',
        monthNames: ['一月','二月','三月','四月','五月','六月',
        '七月','八月','九月','十月','十一月','十二月'],
        monthNamesShort: ['一月','二月','三月','四月','五月','六月',
        '七月','八月','九月','十月','十一月','十二月'],
        dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],
        dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],
        dayNamesMin: ['日','一','二','三','四','五','六'],
        weekHeader: '周',
        dateFormat: 'yy-mm-dd',
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: true,
        yearSuffix: '年'};
    $.datepicker.setDefaults($.datepicker.regional['zh-CN']);
});