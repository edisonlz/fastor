$(document).ready(function () {

    var sort_table = $("#sortable");

    function collect_channel_ids_with_order() {
        var children = sort_table.children();
        var ret = '';
        for (var i = 0; i < children.length; i++) {
            var child = children[i];
            ret += $(child).attr('value') + ',';
        }
        return ret.substring(0, ret.length - 1);
    }

    sort_table.sortable({
        axis: "y",
        items: ".sort-item",
        cursor: "crosshair",
        start: function (event, ui) {
            ui.item.startPos = ui.item.index();
            ui.item.addClass("active-item-shadow");
            ui.placeholder.css('height', ui.item.height());
        },
        stop: function (event, ui) {
            console.log("Start position: " + ui.item.startPos);
            console.log("New position: " + ui.item.index());
            ui.item.removeClass("active-item-shadow");
            ui.item.children('td').effect('highlight', {color: "#dddddd"}, 400);
            if (ui.item.startPos != ui.item.index()) {
                $("#save_position_btn").removeClass("disabled");
            }
        },
        helper: function (e, ui) {
            ui.children().each(function () {
                $(this).width($(this).width());
            });
            return ui;
        }
//            cancel: '.img-polaroid, .out_pick' #这行有神奇作用，加上会让表格里的input左键无法选中
    });
    if (typeof(save_position_btn_func) === 'undefined') {
        var save_position_btn = function () {
            var item_ids = $('#item_ids').val();
            $.ajax({
                type: 'POST',
                dataType: 'json',
                url: "{{ reorder_url }}",
                data: {
                    item_ids: item_ids
                },
                success: function (data) {
                    if (data.status === 'success') {
                        $().toastmessage({
                            position: 'middle-center'
                        });
                        $().toastmessage('showSuccessToast', '操作成功');
                        setTimeout(function () {
                            location.reload()
                        }, 1000);
                    } else {
                        $().toastmessage('showErrorToast', "操作失败")
                    }
                }
            });
        };
    }

    $("#save_position_btn").click(function () {
        var item_ids = collect_channel_ids_with_order();
        if (item_ids == '') {
            alert('没有要排序的内容');
            return false;
        }

        $("#item_ids").val(item_ids);
        if (typeof(save_position_btn_func) === 'undefined') {
            save_position_btn();
        } else {
            save_position_btn_func();
        }
    });

//    $(".del").click(function () {
//        var status = confirm("确认删除吗?");
//           if (!status) {
//               return false;
//           }
//    });


//    $.fn.editable.defaults.mode = 'popup';
//    $.fn.editable.defaults.success = function (data) {
//        $().toastmessage({
//            position: 'middle-center'
//        });
//        if (data.status == "success") {
//            $().toastmessage('showSuccessToast', '操作成功');
//        } else {
//            $().toastmessage('showErrorToast', data.msg);
//            setTimeout(function () {
//                    location.reload()
//                }, 1000);
//        }
//    };

//    $('.select_pick').editable({
//        showbuttons: false,
//        source: [
//            {value: 1, text: '开启'},
//            {value: 0, text: '关闭'}
//        ]
//    });

});
