
var marginRecorder="";

function is_weixin(){
    var ua = navigator.userAgent.toLowerCase();
    if(ua.match(/MicroMessenger/i)=="micromessenger") {
        return true;
    } else {
        return true;
    }
}

var ykPlayerH5, player,danmu;

var is_playing = false;
var is_opendanmu = false;

var bodyContent = function() {
    playerWidth();


    $(window).on("orientationchange resize",
        function() {
            playerWidth();
    })
},

loadPlayerH5 = function(opendanmu,default_open_daumu) {
    var a = {
        id: "youku-player",
        vid: window.videoId,
        prefer: "h5",
        expand: 0,
        canWide: 0,
        paid: window.paid,
        client_id: "youkumobileplaypage",
        wintype: "interior",
        events: {
            onPlayStart: function() {if(default_open_daumu)is_playing = true; onplaying()},
            onPlayerReady: onPlayerReadyH5,
            onPlayEnd: onPlayerCompleteH5,
            onSwitchFullScreen: onSwitchFullScreen,
            onMediaSrcOK: onMediaSrcOK
        },
        weixin : is_weixin(),
        playlistconfig: {},
        vvlogconfig: {
            rurl: window.document.referrer
        },
        adconfig: {}
    };

    if (2 == window.playmode) a.playlistconfig = {
        Type: "Folder",
        Fid: window.folderId,
        Ob: window.o
    };

    ykPlayerH5 = new YKU.Player("player", a)
    player = ykPlayerH5.player()._player;
    player.addEventListener("playing",onplaying,false);
    player.addEventListener("pause",onpause,false);
    player.addEventListener("seeked",onseeked,false);
    player.addEventListener("ended",onstop,false);
    player.addEventListener("waiting",onpause,false);


    is_opendanmu=opendanmu;
    if(!opendanmu) return;
    //弹幕层设置,使用了定制的jquery.danmu.js

    $("#player").append('<div class="danmu-div" id="danmu-uuid" ></div>');


    /* player controller danmu button */


    var danmu_on = 1;
    var daumu_text = '关弹';
    if(!default_open_daumu){
        danmu_on = 0; 
        daumu_text = '开弹';
    }

    var danmu_button = '<div class="x-danmu"  style="display: block;"><button id="danmuSwitch" data-on='+danmu_on+' class="x-danmu-btn" title="弹幕">'+daumu_text+'</button></div>';
    $(".x-playshow").before(danmu_button);

    $("#danmuSwitch").click(function(){
        var on = $(this).data("on");
        if(on==1){
            onpause();
            $(this).data("on",0);
            $(this).text("开弹");
        }else{
            is_playing = true;
            onplaying();
            $(this).data("on",1);
            $(this).text("关弹");
        }
    });
    /*  end player controller danmu button */


    var options = { left: 0,
                    top: 0 ,
                    height: "100%",
                    width: "100%",
                    zindex :100,
                    speed:20000,
                    sumTime:65535,
                    defaultColor:"#ffffff",
                    fontSizeSmall:12,
                    FontSizeBig:14,
                    opacity:1,
                    topBottonDanmuTime:6000,
                    urlToPostDanmu:"",
                    urlToGetDanmu:"/default/danmu"
                };


    $(".danmu-div").danmu({
        width: "100%",
        height: "100%",
        danmuLoop:false,
        speed: options.speed,
        opacity: options.opacity,
        fontSizeSmall: options.fontSizeSmall,
        FontSizeBig: options.FontSizeBig,
        SubtitleProtection:false,
        positionOptimize:false
    });

    danmu = $(".danmu-div");
    play_danmu(options);
};

var is_danmu = false;

function play_danmu(options){
    if(is_danmu) return;
    is_danmu = true;

    this.getDanmu=function(){
        $.getJSON(options.urlToGetDanmu, function(data, status) {
            
            for (var i = 0; i < data.length; i++) {
                 var d = data[i];
                $('.danmu-div').danmu("addDanmu", d);
            }
        });
    };

    var danmuData =[
       { text:"这是滚动弹幕" ,color:"white",size:1,position:0,time:0},
       { text:"这是滚动弹幕" ,color:"white",size:1,position:0,time:0},
       { text:"这是滚动弹幕" ,color:"white",size:1,position:0,time:0},
       { text:"这是滚动弹幕" ,color:"white",size:1,position:0,time:1},
       { text:"这是顶部弹幕" ,color:"yellow" ,size:1,position:1,time:2},
       { text:"这是底部弹幕" , color:"red",size:1,position:2,time:3}
    ];

    var color = ["#fff","#000","#ece","#200","#800","#500"];

    for(var i=4;i<65535;i++){
        danmuData.push({ text:"这是滚动弹幕"+i,color:color[i%6],size:0,position:0,time:i});
    }

    $(".danmu-div").danmu("addDanmu",danmuData);

    //主计时器
    var mainTimer=setInterval(function(){
        if(Math.abs($(".danmu-div").data("nowTime") - player.currentTime) > 0.5){
            $(".danmu-div").data("nowTime",parseInt(player.currentTime));
        }
    },1000);

    //onplaying();
}



function onplaying() {
    if(is_playing){
        $('.danmu-div').danmu('danmuStart');    
        $('.danmu-div').danmu('danmuResume');
    }
}

function onpause() {
    $('.danmu-div').danmu('danmuPause');
}

function onseeked(){
    $(".danmu-div").data("nowTime",parseInt(player.currentTime));
}

function onstop(){
    $('.danmu-div').danmu('danmuStop');
}


function onPlayerReadyH5() {}

function onMediaSrcOK(a, b) {
    if ("3gphd" != a || "" == b) return ! 1;
    window.downloadUrl = b;
}

var playerWidth = function() {
    //2 is margin
    var margin = parseInt($(".play_div").css("margin").replace("px",""));
    if(marginRecorder==""){
        marginRecorder = margin;
    }
    var a = $(window).width(), b = $(window).height();

    if(window.isFullscreen == ! 0) {
        $(".yk-player .yk-player-inner").css({
            width: a + "px",
            height: b + "px"
        });
        $(".play_div").css("margin","0px");

    } else{
        if( (90 === window.orientation || -90 === window.orientation) && a>b ) {
            $(".yk-player .yk-player-inner").css({
                width: a + "px",
                height: b + "px"
            });
            $(".play_div").css("margin","0px");
            
        }else{
            var a = window.innerWidth - marginRecorder*2, 
            b = window.innerHeight - marginRecorder*2;

            $(".play_div").css("margin",marginRecorder+"px");
            $(".yk-player .yk-player-inner").css({
                width: a + "px",
                height: a * 9/ 16 + "px"
            });
        }
    }
};


function onSwitchFullScreen() { 
    if(! 0 == window.isFullscreen) {
        clearInterval(window.timers);
         window.isFullscreen = !1; 
         $("body").removeClass("fullscreen");
         setTimeout("videoContent.refreshHeight();", 800);
    } else {
         $("body").addClass("fullscreen");
         window.isFullscreen = !0;
         window.timers = setInterval("window.scrollTo(0, 1);", 1);
    }

    if(is_opendanmu && $("#danmuSwitch").data("on")==1){
        onpause();
    }
    
    setTimeout(function() {
                            playerWidth();
                            if(is_opendanmu && $("#danmuSwitch").data("on")==1) onplaying();
                          }, 200);
}

function onPlayerCompleteH5(a) {
}
