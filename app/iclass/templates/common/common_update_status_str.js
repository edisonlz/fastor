/**
 * Created by yuxiang on 2017/6/30.
 */
    $(function(){
        $("button.item_status").click(function(){

            var status_str = $(".item_status").html();

            status_str = status_str.replace(/\ +/g, "");  //去掉空格
            status_str = status_str.replace(/[\r\n]/g, "");  //去掉回车换行

            var msg_str = "你确定" + status_str + "嘛！";

            var result = confirm(msg_str);
            if (!result) {
                return false;
            }

            var itemId = $(this).closest("tr").find("input[name='status_item_id']").val();
            var _this=$(this);
            $.ajax({
                type: 'post',
                url: "{% url 'common_update_status_str' %}",
                data: {
                    item_id: itemId,
                    item_class: '{{ item_class }}'
                },
                success: function(data){
                    if(data.code == 200){
                        alert(data.msg);

                        if(data.result.status=="0"){
                            _this.html('关闭');
                            _this.closest("tr").find("td.status").html("开启");
                        } else {
                            _this.html('开启');
                            _this.closest("tr").find("td.status").html("关闭");
                        }
                    };
                }
            });
        });
    });