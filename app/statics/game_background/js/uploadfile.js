/**
 * Created with PyCharm.
 * User: yinxing
 * Date: 14-4-30
 * Time: 下午4:18
 * To change this template use File | Settings | File Templates.
 */

function uploadImage(input_fileid, form_id, image_id, image_size)
{
    var url = '/app/img/upload';
    var fileSelector = input_fileid+ ' '+ '.image_input';
    var imageDivSelector = input_fileid + ' ' + '.img_div';
    var progressBarSelector = input_fileid + ' ' + '.progress';
    var inputButtonSelector = input_fileid + ' ' + '.fileinput-button';
    var imageContainerSelector = input_fileid + ' ' + '.img-polaroid';

    $(fileSelector).fileupload({
        autoUpload: true,//是否自动上传
        url: url,//上传地址
        dataType: 'json',
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        maxFileSize: 1048576,

        add: function (e, data) {
            var uploadErrors = [];
            var acceptFileTypes = /^image\/(gif|jpe?g|png)$/i;
            if ('type' in data.originalFiles[0] && !acceptFileTypes.test(data.originalFiles[0]['type'])) {
                uploadErrors.push('上传图片格式错误!');
            }

            if ('size' in data.originalFiles[0] && data.originalFiles[0]['size'] > 1048576) {
                uploadErrors.push('上传图片需要小于1M!');
            }

            if (uploadErrors.length > 0) {
                alert('error');
                show_error_msg(uploadErrors.join("\n"));
            } else {
                data.submit();
            }
        },

        done: function (e, data) {//设置文件上传完毕事件的回调函数
            //console.log(inputButtonSelector);

            if ("e" in data.result && data.result["e"]["code"] < 0) {
               //console.log(inputButtonSelector);
               //console.log(progressBarSelector);
               $(inputButtonSelector).show();
               $(progressBarSelector).hide();
               show_error_msg("upload error:" + data.result["e"]["code"] + ':' + data.result["e"]["desc"]);
               return;
            }

            $.each(data.result.files, function (index, file) {//
                $(imageContainerSelector).attr("src", file.url);
                $(imageContainerSelector).show()

                //在此处向表单中添加 url
                var form = $(form_id)
                var img_input = $(image_id)

                img_input.attr('value', file.url)
                form.append(img_input)
            });

            $(progressBarSelector).hide();
            $(imageDivSelector).show();
        },

        progressall: function (e, data) {//设置上传进度事件的回调函数

            $(inputButtonSelector).hide();
            $(progressBarSelector).show();

            var progress = parseInt(data.loaded / data.total * 100, 10);
            $(progressBarSelector + ' .bar').css(
                    'width',
                    progress + '%'
            );
        },

        fail: function (e, data) {
            $(inputButtonSelector).show();
            $(progressBarSelector).hide();
            console.log(inputButtonSelector);
            console.log(progressBarSelector);
            show_error_msg("上传失败!");
        }

    }).prop('disabled', !$.support.fileInput)
            .parent().addClass($.support.fileInput ? undefined : 'disabled');
}

function uploadImage2v(input_file)
{
    var url = '/app/img/upload';
    var fileSelector = input_file.find('.image_input');
    var imageDivSelector = input_file.find('.img_div');
    var progressBarSelector = input_file.find('.progress');
    var inputButtonSelector = input_file.find('.fileinput-button');
    var imageContainerSelector = input_file.find('.img-polaroid');
    var imageInputSelector = input_file.find('.result-input');
    var closeBtnSelector = input_file.find('.alert button');

    $(closeBtnSelector).click(function () {
            var btn = $(this);
            $(btn).next().attr("src", "");
            var parent = $(btn).parent();
            //隐藏
            parent.hide();
            //设置hidden input的值
            if (parent.next().next()) parent.next().next().val("");
            //显示上传按钮
            $(parent.parent().children()[0]).show();

        });

    $(fileSelector).fileupload({
        autoUpload: true,//是否自动上传
        url: url,//上传地址
        dataType: 'json',
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        maxFileSize: 1048576,

        add: function (e, data) {
            var uploadErrors = [];
            var acceptFileTypes = /^image\/(gif|jpe?g|png)$/i;
            var _URL = window.URL || window.webkitURL;
            var img = new Image();
            img.src = _URL.createObjectURL(data.originalFiles[0]);
            if ('type' in data.originalFiles[0] && !acceptFileTypes.test(data.originalFiles[0]['type'])) {
                uploadErrors.push('上传图片格式错误!');
            }

            if ('size' in data.originalFiles[0] && data.originalFiles[0]['size'] > 1048576) {
                uploadErrors.push('上传图片需要小于1M!');
            }
            img.onload = function () {
                if (img.width != 324 || img.height != 182) {
                    uploadErrors.push('上传图片尺寸错误。');
                }
                if (uploadErrors.length > 0) {
                    show_error_msg(uploadErrors.join("\n"));
                } else {
                    data.submit();
                }
            }
        },

        done: function (e, data) {//设置文件上传完毕事件的回调函数
            //console.log(inputButtonSelector);

            if ("e" in data.result && data.result["e"]["code"] < 0) {
               //console.log(inputButtonSelector);
               //console.log(progressBarSelector);
               $(inputButtonSelector).show();
               $(progressBarSelector).hide();
               show_error_msg("upload error:" + data.result["e"]["code"] + ':' + data.result["e"]["desc"]);
               return;
            }

            $.each(data.result.files, function (index, file) {//
                $(imageContainerSelector).attr("src", file.url);
                $(imageContainerSelector).show();

                var img_input = $(imageInputSelector);
                img_input.attr('value', file.url);
            });

            $(progressBarSelector).hide();
            $(imageDivSelector).show();
        },

        progressall: function (e, data) {//设置上传进度事件的回调函数

            $(inputButtonSelector).hide();
            $(progressBarSelector).show();

            var progress = parseInt(data.loaded / data.total * 100, 10);
            $(progressBarSelector.find('.bar')).css(
                    'width',
                    progress + '%'
            );
        },

        fail: function (e, data) {
            $(inputButtonSelector).show();
            $(progressBarSelector).hide();
            console.log(inputButtonSelector);
            console.log(progressBarSelector);
            console.log(e);
            console.log(data);
            show_error_msg("上传失败!");
        }

    }).prop('disabled', !$.support.fileInput)
            .parent().addClass($.support.fileInput ? undefined : 'disabled');
}