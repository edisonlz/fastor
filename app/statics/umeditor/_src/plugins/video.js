///import core
///import plugins/inserthtml.js
///commands 视频
///commandsName InsertVideo
///commandsTitle  插入视频
///commandsDialog  dialogs\video
UM.plugins['video'] = function (){
    var me =this,
        div;

    function getYoukuVideoInfo(video_url, default_img_url){
        res = {}
        if(!video_url){
            return {};
        }
        var img_url = default_img_url || '';
        $.ajax({
            url: '/default/video/base_info',  //请求的URL
            timeout: 5000, //超时时间设置，单位毫秒
            type: 'get',  //请求方式，get或post
            async: false,
            data: {"url": video_url},
            dataType: 'json',//返回的数据格式
            //beforeSend: function (XMLHttpRequest) {},
            success: function (data) { //请求成功的回调函数
                res['img_url'] = data.h_image;
                res['vid'] = data.video_id;
                res['vid_int'] = data.vid_int;
                if (data.video_type == 'show') {
                  res['img_url'] = data.v_image;
                }
            }
        });
        return res;
    }
    /**
     * 创建插入视频字符窜
     * @param url 视频地址
     * @param width 视频宽度
     * @param height 视频高度
     * @param align 视频对齐
     * @param toEmbed 是否以flash代替显示
     * @param addParagraph  是否需要添加P 标签
     */
    function creatInsertStr(url,width,height,id,align,toEmbed,original_url){
        default_img_src = me.options.UMEDITOR_HOME_URL+'themes/default/images/spacer.gif';
        video_info = getYoukuVideoInfo(original_url, default_img_src);
        img_src = video_info['img_url'] || '';
        //return  !toEmbed ?
        //
        //        '<img ' + (id ? 'id="' + id+'"' : '') + ' width="'+ width +'" height="' + height + '" _url="'+url+'" class="edui-faked-video"'  +
        //        ' original_url="' + original_url + '"' +
        //        ' vid="' + video_info['vid'] + '"' +
        //        ' vid_int="' + video_info['vid_int'] + '"' +
        //        ' src="' + img_src +'" style="background:url('+ me.options.UMEDITOR_HOME_URL+'themes/default/images/videologo.gif) no-repeat center center; border:1px solid gray;'+(align ? 'float:' + align + ';': '')+'" />'
        //
        //        :
        return  '<embed type="application/x-shockwave-flash" class="edui-faked-video" pluginspage="http://www.macromedia.com/go/getflashplayer"' +
                ' original_url="' + original_url + '"' +
                ' vid="' + video_info['vid'] + '"' +
                ' vid_int="' + video_info['vid_int'] + '"' +
                ' src="' + url + '" width="' + width  + '" height="' + height  + '"'  + (align ? ' style="float:' + align + '"': '') +
                ' wmode="transparent" play="true" loop="false" menu="false" allowscriptaccess="never" allowfullscreen="true" >';
    }

    function switchImgAndEmbed(root,img2embed){
        utils.each(root.getNodesByTagName(img2embed ? 'img' : 'embed'),function(node){
            if(node.getAttr('class') == 'edui-faked-video'){

                var html = creatInsertStr( img2embed ? node.getAttr('_url') : node.getAttr('src'),node.getAttr('width'),node.getAttr('height'),null,node.getStyle('float') || '',img2embed, node.getAttr('original_url'));
                node.parentNode.replaceChild(UM.uNode.createElement(html),node)
            }
        })
    }

    me.addOutputRule(function(root){
        switchImgAndEmbed(root,true)
    });
    me.addInputRule(function(root){
        switchImgAndEmbed(root)
    });

    me.commands["insertvideo"] = {
        execCommand: function (cmd, videoObjs){
            videoObjs = utils.isArray(videoObjs)?videoObjs:[videoObjs];
            var html = [],id = 'tmpVedio';
            for(var i=0,vi,len = videoObjs.length;i<len;i++){
                 vi = videoObjs[i];
                 var format_url = vi.url.replace(/\?.*$/, '');
                 //html.push(creatInsertStr( format_url, vi.width || 420,  vi.height || 280, id + i,vi.align,false,vi.original_url));
                 html.push(creatInsertStr( format_url, vi.width || 553,  vi.height || 369, id + i,vi.align,false,vi.original_url));
            }
            me.execCommand("inserthtml",html.join(""),true);

        },
        queryCommandState : function(){
            var img = me.selection.getRange().getClosedNode(),
                flag = img && (img.className == "edui-faked-video");
            return flag ? 1 : 0;
        }
    };
};