/**
 * Created by yuxiang on 2017/6/30.
 */
    $(function(){
        $("button.item_status").click(function(){
            var itemId = $(this).closest("tr").find("input[name='status_item_id']").val();
            var _this=$(this);
            $.ajax({
                type: 'post',
                url: "{% url 'index_common_update_status' %}",
                data: {
                    item_id: itemId,
                    item_class: '{{ item_class }}'
                },
                success: function(data){
                    if(data.code == 200){
                        alert (data.msg);

                        if(data.result.status == 0){
                            _this.html('关闭');
                            _this.closest("tr").find("td.status").html("开启");
                        } else {
                            _this.html('开启');
                            _this.closest("tr").find("td.status").html("关闭");
                        }
                    }
                }
            });
        });
    });