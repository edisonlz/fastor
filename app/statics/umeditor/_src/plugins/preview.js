///import core
///commands 预览
///commandsName  Preview
///commandsTitle  预览
/**
 * 预览
 * @function
 * @name UM.execCommand
 * @param   {String}   cmdName     preview预览编辑器内容
 */
UM.commands['preview'] = {
    execCommand : function(){
        var w = window.open('', '_blank', ''),
            d = w.document,
            c = this.getContent(null,null,true),
            path = this.getOpt('UMEDITOR_HOME_URL'),
            use_mathquill = c.indexOf('mathquill-embedded-latex')!=-1,
            formula = c.indexOf('mathquill-embedded-latex')!=-1 ?
                '<link rel="stylesheet" href="' + path + 'third-party/mathquill/mathquill.css"/>' +
                '<script src="' + path + 'third-party/jquery.min.js"></script>' +
                '<script src="' + path + 'third-party/mathquill/mathquill.min.js"></script>':'';

        if(!use_mathquill) {
            formula += '<link rel="stylesheet" href="/static/bootstrap-3/css/bootstrap.css"/>' +
                    '<link rel="stylesheet" href="/static/bootstrap-3/css/bootstrap.css"/>' +
                    '<link href="/static/edit_demo/css/layout.css" type="text/css" rel="stylesheet">' +
                    '<script src="/static/js/jquery-1.11.3.min.js"></script>' +
                    '<script src="/static/js/jquery-ui.js"></script>';
            d.open();
            d.write('<html>' +
                '<head lang="en"><meta charset="UTF-8"><title>优酷视频微信管理系统-预览</title>' +
                '<meta content="width=device-width, initial-scale=1" name="viewport">' +
                formula + '</head><body><div class="container"><div class="row">' +
                '<div class="app-preview" style="float:none;margin:10px auto;">' +
                '<div class="app-header"></div><hr/>' +
                c + '</div></div></div>' +
                '<script>' +
                '$("embed.edui-faked-video, img").each(function(){' +
                    'height=$(this).height();' +
                    'width=$(this).width();' +
                    '$(this).height(height / 3.14);' +
                    '$(this).width(width / 3.14);' +
                '})' +
                '</script>' +
                '</body></html>');
            d.close();
        }else {
            d.open();
            d.write('<html><head>' + formula + '</head><body><div>' + c + '</div></body></html>');
            d.close();
        }
    },
    notNeedUndo : 1
};
