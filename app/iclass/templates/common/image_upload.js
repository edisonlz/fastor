$("button[class='close']").click(function () {
    $(this).next('img').attr('src', '')
        .parent('div').hide().prev('span').show()
        .parent().children('input').attr('value', '');
});

var url = '/default/img/upload';

//generate the related tag ids into a array
function generate_upload_dict(common_prefix) {
    var key_arr = ['upload', 'button', 'progress', 'content', 'input', 'success'];
    var upload_dict = {};
    for (var i = 0; i < key_arr.length; i++) {
        upload_dict[key_arr[i]] = '#' + common_prefix + '-' + key_arr[i];
    }
    return upload_dict;
}

//add upload function to the element, initialization, mainly set upload params and callback
function add_upload_handler(upload_dict) {
    var pdf = upload_dict['pdf'];

    $(upload_dict['upload']).fileupload({
        autoUpload: true,//是否自动上传
        url: url,//上传地址
        dataType: 'json',
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        maxFileSize: 1048576 * 10,
        add: function (e, data) {
            var uploadErrors = [];
            var acceptFileTypes = /(\.|\/)(gif|jpe?g|png)$/i;
            if ('type' in data.originalFiles[0] && !acceptFileTypes.test(data.originalFiles[0]['type'])) {
                uploadErrors.push('上传图片格式错误!');
            }
            if ('size' in data.originalFiles[0] && data.originalFiles[0]['size'] > (1048576 * 10)) {
                uploadErrors.push('上传图片需要小于10M!');
            }
            if (uploadErrors.length > 0) {
                alert(uploadErrors.join("\n"));
            } else {
                data.submit();
            }
        },
        done: function (e, data) {//设置文件上传完毕事件的回调函数
            if ("e" in data.result && data.result["e"]["code"] < 0) {
                $(upload_dict['button']).show();
                $(upload_dict['progress']).hide();
                console.log(data.result["e"]);

                alert("upload error:" + data.result["e"]["code"]+ data.result["e"]["desc"]);
                return;
            }
            $.each(data.result.files, function (index, file) {//
                $(upload_dict['content']).attr("src", file.url).show();
                $(upload_dict['input']).attr('value', file.url);
            });
            $(upload_dict['button']).show();
            $(upload_dict['progress']).hide();
            $(upload_dict['success']).show();
        },
        progressall: function (e, data) {//设置上传进度事件的回调函数
            $(upload_dict['button']).hide();
            $(upload_dict['progress']).show();
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('div.bar').css('width', progress + '%');
        }
    })
}


function add_upload_pdf_handler(upload_dict) {

    $(upload_dict['upload']).fileupload({
        autoUpload: true,//是否自动上传
        url: url,//上传地址
        dataType: 'json',
        acceptFileTypes: /(\.|\/)(pdf)$/i,
        maxFileSize: 1048576 * 100,
        add: function (e, data) {
            var uploadErrors = [];
            var acceptFileTypes = /(\.|\/)(pdf)$/i;
            
            if ('type' in data.originalFiles[0] && !acceptFileTypes.test(data.originalFiles[0]['type'])) {
                uploadErrors.push('上传PDF格式错误!');
            }
            if ('size' in data.originalFiles[0] && data.originalFiles[0]['size'] > (1048576 * 100)) {
                uploadErrors.push('上传PDF需要小于100M!');
            }
            if (uploadErrors.length > 0) {
                alert(uploadErrors.join("\n"));
            } else {
                data.submit();
            }
        },
        done: function (e, data) {//设置文件上传完毕事件的回调函数
            if ("e" in data.result && data.result["e"]["code"] < 0) {
                $(upload_dict['button']).show();
                $(upload_dict['progress']).hide();
                console.log(data.result["e"]);

                alert("upload error:" + data.result["e"]["code"]+ data.result["e"]["desc"]);
                return;
            }
            $.each(data.result.files, function (index, file) {//
                $(upload_dict['content']).attr("src", file.url).show();
                $(upload_dict['input']).attr('value', file.url);
            });
            $(upload_dict['button']).show();
            $(upload_dict['progress']).hide();
            $(upload_dict['success']).show();
        },
        progressall: function (e, data) {//设置上传进度事件的回调函数
            $(upload_dict['button']).hide();
            $(upload_dict['progress']).show();
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('div.bar').css('width', progress + '%');
        }
    })
}


function add_upload_xlsx_handler(upload_dict) {

    $(upload_dict['upload']).fileupload({
        autoUpload: true,//是否自动上传
        url: url,//上传地址
        dataType: 'json',
        acceptFileTypes: /(\.|\/)(xlsx?)$/i,
        maxFileSize: 1048576 * 100,
        add: function (e, data) {
            var uploadErrors = [];
            var acceptFileTypes = /(\.|\/)(xlsx?)$/i;
            // if (!acceptFileTypes.test(data.originalFiles[0]['type'])) {
            //     uploadErrors.push('上传格式错误!');
            // }
            if ('size' in data.originalFiles[0] && data.originalFiles[0]['size'] > (1048576 * 100)) {
                uploadErrors.push('上传需要小于100M!');
            }
            if (uploadErrors.length > 0) {
                alert(uploadErrors.join("\n"));
            } else {
                data.submit();
            }
        },
        done: function (e, data) {//设置文件上传完毕事件的回调函数
            if ("e" in data.result && data.result["e"]["code"] < 0) {
                $(upload_dict['button']).show();
                $(upload_dict['progress']).hide();
                console.log(data.result["e"]);

                alert("upload error:" + data.result["e"]["code"]+ data.result["e"]["desc"]);
                return;
            }
            $.each(data.result.files, function (index, file) {
                $(upload_dict['content']).attr("src", file.url).show();
                $(upload_dict['input']).attr('value', file.url);
            });
            $(upload_dict['button']).show();
            $(upload_dict['progress']).hide();
            $(upload_dict['success']).show();
        },
        progressall: function (e, data) {//设置上传进度事件的回调函数
            $(upload_dict['button']).hide();
            $(upload_dict['progress']).show();
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('div.bar').css('width', progress + '%');
        }
    })
}


function show_error_msg(msg) {
    alert(msg);
}

