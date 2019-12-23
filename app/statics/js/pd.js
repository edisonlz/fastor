var TVHelper = function() {
    if (null != window.navigator.userAgent.match(/Yunos\/Tvhelper/i)) try {
        window.RemotePlayer.sendRemotePlayer('{"action":"play","info":{"vid":"' + window.videoIdEn + '","title":"' + window.videoTitle + '"}}')
    } catch(a) {}
};
window.onbeforeunload = function() {
    null != window.navigator.userAgent.match(/Yunos\/Tvhelper/i) && opCookie("_from_x_", window.videoIdEn, {
        domain: "youku.com",
        path: "/"
    })
};


var marginRecorder="";

function is_weixin(){
    var ua = navigator.userAgent.toLowerCase();
    if(ua.match(/MicroMessenger/i)=="micromessenger") {
        return true;
    } else {
        return false;
    }
}

var opCookie = function(a, b, c) {
    if ("undefined" != typeof b) {
        c = c || {};
        if (null === b) b = "",
        c = $.extend({},
        c),
        c.expires = -1;
        var d = "";
        if (c.expires && ("number" == typeof c.expires || c.expires.toUTCString))"number" == typeof c.expires ? (d = new Date, d.setTime(d.getTime() + 864E5 * c.expires)) : d = c.expires,
        d = "; expires=" + d.toUTCString();
        var e = c.path ? "; path=" + c.path: "",
        f = c.domain ? "; domain=" + c.domain: "",
        c = c.secure ? "; secure": "";
        document.cookie = [a, "=", encodeURIComponent(b), d, e, f, c].join("")
    } else {
        b = null;
        if (document.cookie && "" != document.cookie) {
            c = document.cookie.split(";");
            for (d = 0; d < c.length; d++) if (e = jQuery.trim(c[d]), e.substring(0, a.length + 1) == a + "=") {
                try {
                    b = decodeURIComponent(e.substring(a.length + 1))
                } catch(h) {
                    b = ""
                }
                break
            }
        }
        return b
    }
};
function QueryString() {
    var a, b, c;
    b = location.href.split("?");
    c = b[0];
    1 < b.length && (a = b[1]);
    if (c) {
        b = c.lastIndexOf("/");
        c = c.substr(b + 1);
        c = c.split(".")[0];
        b = c.split("_");
        for (c = 0; c < b.length; c += 2) b[c] && b[c + 1] && (this[b[c]] = b[c + 1]),
        b[c] && !b[c + 1] && (this[b[c]] = !0)
    }
    if (a) {
        var d = a.split("&");
        for (c = 0; c < d.length; c++) num = d[c].indexOf("="),
        0 < num ? (a = d[c].substring(0, num), b = d[c].substr(num + 1), this[a] = b) : this[d[c]] = !0
    }
}
var xparamsString = new QueryString,
numberFormat = function(a) {
    num = a.toString();
    a = Math.abs(num).toString();
    if (4 > a.length) return num;
    var b = ""; - 1 != num.indexOf(".") && (b = "." + num.split(".")[1]);
    var c = a.length,
    d = c % 3,
    e = [],
    d = 0 == d ? 3 : d;
    e[0] = a.slice(0, d);
    for (var f = 1; d + 3 <= c;) e[f++] = a.slice(d, d + 3),
    d += 3;
    e = e.join(",");
    0 === num.indexOf("-") && (e = "-" + e);
    return e + b
};
function setOldCookie() {
    opCookie("_from_x_", 1, {
        expires: 1,
        domain: "youku.com",
        path: "/"
    });
    opCookie("_top_banner_", 1, {
        expires: -1,
        domain: "youku.com",
        path: "/"
    })
}
var openApp = function() {
    var a = xparamsString.sharefrom;
    if (a) {
        var b = "",
        c = videoIdEn,
        d = "";
        if ("pkios" == a || "pkandroid" == a) null != window.navigator.userAgent.match(/android/i) && (b = "paike://vid/" + c),
        null != window.navigator.userAgent.match(/iphone|ipad/i) && (b = "paike://type=vid&value=" + c),
        d = "banner=pk";
        if ("android" == a || "ipad" == a || "iphone" == a) {
            var e = getCookie("__ysuid") || "";
            null != window.navigator.userAgent.match(/iphone/i) && (b = "youku://play?vid=" + c + "&source=mplaypage&cookieid=" + e);
            null != window.navigator.userAgent.match(/android/i) && (b = "youku://play?vid=" + c + "&source=mplaypage&cookieid=" + e);
            null != window.navigator.userAgent.match(/ipad/i) && (b = "youkuhd://play?vid=" + c + "&source=mplaypage&cookieid=" + e)
        }
        c = "";
        "pkios" == a ? c = "tp=1&cp=4009031&cpp=1000752": "pkandroid" == a ? c = "tp=1&cp=4009030&cpp=1000752": "android" == a ? c = "tp=1&cp=4009027&cpp=1000752": "ipad" == a ? c = "tp=1&cp=4009028&cpp=1000752": "iphone" == a && (c = "tp=1&cp=4009029&cpp=1000752");
        Log.log(1, c);
        if (b) {
            a = document.createElement("iframe");
            a.id = "openApp";
            a.width = 0;
            a.height = 0;
            a.src = b;
            $("body").append(a);
            if ("" != d) window.playPageUrl = -1 !== window.playPageUrl.indexOf("?") ? window.playPageUrl + ("&x&" + d) : window.playPageUrl + ("?x&" + d);
            setTimeout("window.location.href = window.playPageUrl;", 1E3)
        }
    }
},
checkSubscribe = function() {
    if (islogin()) {
        var a = login.getUserInfo().userid,
        b = window.videoOwnerID || 0;
        0 !== b && 0 !== a && $.ajax({
            url: "http://yws.youku.com/users/js_show.jsonp?login_uid=" + encodeUid(a) + "&uid=" + encodeUid(b) + "&callback=checkFollowStatusCallback&t=" + Math.random(),
            dataType: "jsonp",
            success: function(a) {
                if (a.data.friendship && !0 == a.data.friendship.following) if (null != window.navigator.userAgent.match(/MicroMessenger/i)) $("#fn-subscribe").html('<i class="subscribe act"></i><br><span class="subscribe-text">\u5df2\u8ba2\u9605</span>');
                else {
                    a = document.getElementById("subscribe");
                    if (null != a) a.innerHTML = '<span class="followed">\u5df2\u8ba2\u9605&nbsp;|&nbsp;\u53bb\u770b<a href="http://i.youku.com/u/home?ut=3" target="_blank">\u8ba2\u9605\u66f4\u65b0</a></span>';
                    a = $(".subscription .btn-maj");
                    null != a && a.removeClass("btn-maj").addClass("btn-sub").html("\u5df2\u8ba2\u9605")
                }
            }
        })
    }
},
subscribe = function(a) {
    if (!islogin()) return login(function() {
        $(".fn-favorite").trigger("click")
    }),
    !1;
    void 0 == a || null == a || 0 == a || (a = "http://i.youku.com/u/friends/follow_" + a + "?type=user&uccb=followUserCallback&deviceid=3&addtion=" + addtionSort(), xcomments.init(a))
},
followUserCallback = function(a) {
    if ((void 0 == a.error || 0 > a.error || void 0 == a.friend) && void 0 != a.en && "ERR_FRIENDSHIPS_EXIST" != a.en && void 0 != a.zh) {
        if ("ERR_PARAMS" == a.en) a.zh = "\u4e0d\u80fd\u8ba2\u9605\u81ea\u5df1";
        alert(a.zh)
    } else document.getElementById("subscribe").innerHTML = '<span class="followed">\u5df2\u8ba2\u9605&nbsp;|&nbsp;\u53bb\u770b<a href="http://i.youku.com/u/home?ut=3" target="_blank">\u8ba2\u9605\u66f4\u65b0</a></span>'
},
subscription = function(a) {
    if (!islogin()) return login(function() {
        $(".fn-favorite").trigger("click")
    }),
    !1;
    void 0 == a || null == a || 0 == a || (a = "http://i.youku.com/u/friends/follow_" + a + "?type=user&uccb=subscriptionCallback&deviceid=3&addtion=" + addtionSort(), xcomments.init(a), Log.log(1, "tp=1&cp=4008958&cpp=1000752"))
},
subscriptionCallback = function(a) {
    if ((void 0 == a.error || 0 > a.error || void 0 == a.friend) && void 0 != a.en && "ERR_FRIENDSHIPS_EXIST" != a.en && void 0 != a.zh) {
        if ("ERR_PARAMS" == a.en) a.zh = "\u4e0d\u80fd\u8ba2\u9605\u81ea\u5df1";
        alert(a.zh)
    } else $(".subscription .btn-maj").removeClass("btn-maj").addClass("btn-sub").html("\u5df2\u8ba2\u9605")
};
function addtionSort() {
    if (null != window.navigator.userAgent.match(/ipad/i)) return "1_1";
    if (null != window.navigator.userAgent.match(/iphone/i)) return "2_1";
    if (null != window.navigator.userAgent.match(/android/i)) return "3_1"
}
function videoLimit() {
    try {
        if (null != uckey) return ! 0;
        var a = navigator.userAgent,
        b = a.search(/ucbrowser/i);
        if ( - 1 != b && 9.8 <= parseFloat(a.substr(b + 10, 4))) return ! 0
    } catch(c) {
        if (a = navigator.userAgent, b = a.search(/ucbrowser/i), -1 != b && 9.8 <= parseFloat(a.substr(b + 10, 4))) return ! 0
    }
    try {
        return getUCSecret(window.videoIdEn),
        !0
    } catch(d) {} - 1 == window.navigator.userAgent.indexOf("MicroMessenger") && $("#app-download2").show();
    $("#wintipsAppLimit").find(".btn-maj").click(function() {
        $("#wintipsAppLimit").hide();
        $(".yk-mask").remove();
        Log.log(1, "tp=1&cp=4009283&cpp=1000752");
        var a = document.createElement("iframe");
        a.width = 0;
        a.height = 0;
        var b = navigator.userAgent,
        c = getCookie("__ysuid") || "";
        a.src = -1 != b.indexOf("iPad") ? "youkuhd://play?vid=" + window.videoIdEn + "&source=mplaypage&cookieid=" + c: "youku://play?vid=" + window.videoIdEn + "&source=mplaypage&cookieid=" + c;
        $("body").append(a);
        $("body").append("<div class='yk-mask' style='height:" + $(document).height() + "px;'></div>");
        $("#wintipsApp").show()
    });
    $("#wintipsAppLimit").find(".btn-sub").click(function() {
        $("#wintipsAppLimit").hide();
        $(".yk-mask").remove();
        Log.log(1, "tp=1&cp=4009284&cpp=1000752")
    })
}
var getCookie = function(a) {
    a = document.cookie.match(RegExp("(^| )" + a + "=([^;]*)(;|$)"));
    return null != a ? unescape(a[2]) : null
};
function browserOnly() {
    var a = navigator.userAgent.toLowerCase(),
    b = "safari" == a.match(/safari/i),
    c = "ucbrowser" == a.match(/ucbrowser/i),
    d = "crios" == a.match(/crios/i),
    e = "presto" == a.match(/presto/i),
    f = "qq" == a.match(/qq/i),
    h = "mercury" == a.match(/mercury/i),
    i = "flyflow" == a.match(/flyflow/i),
    a = "micromessenger" == a.match(/micromessenger/i);
    if (c) return "uc";
    if (d) return "chrome";
    if (e) return "opera";
    if (f) return "qq";
    if (h) return "mercury";
    if (i) return "baidu";
    if (a) return "weixin";
    if (b) return "safari"
}
function hideDeskTop() {
    for (var a = ["TPA"], b = 0; b < a.length; b++) if (xparamsString && xparamsString[a[b]] && "" != xparamsString[a[b]]) return ! 0;
    return ! 1
}
function encode64(a) {
    if (!a) return "";
    var a = a.toString(),
    b,
    c,
    d,
    e,
    f,
    h;
    d = a.length;
    c = 0;
    for (b = ""; c < d;) {
        e = a.charCodeAt(c++) & 255;
        if (c == d) {
            b += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(e >> 2);
            b += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((e & 3) << 4);
            b += "==";
            break
        }
        f = a.charCodeAt(c++);
        if (c == d) {
            b += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(e >> 2);
            b += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((e & 3) << 4 | (f & 240) >> 4);
            b += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((f & 15) << 2);
            b += "=";
            break
        }
        h = a.charCodeAt(c++);
        b += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(e >> 2);
        b += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((e & 3) << 4 | (f & 240) >> 4);
        b += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt((f & 15) << 2 | (h & 192) >> 6);
        b += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(h & 63)
    }
    return b
}
function encodeUid(a) {
    return ! a ? "": "U" + encode64(a << 2)
}
function hcbt(a) {
    var b = "";
    return b = genH(a)
}
function genH(a) {
    for (var b = !1,
    c = ""; ! b;) c = randomString(20),
    hstr = a + c,
    hashcash = S(hstr),
    "00" == hashcash.substring(0, 2) && (b = !0);
    return c
}
function randomString(a) {
    for (var b = "",
    c = 0; c < a; c++) var d = Math.floor(61 * Math.random()),
    b = b + "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz".substring(d, d + 1);
    return b
}
function S(a) {
    function b(a, b) {
        return a << b | a >>> 32 - b
    }
    function c(a) {
        var b = "",
        c, d;
        for (c = 7; 0 <= c; c--) d = a >>> 4 * c & 15,
        b += d.toString(16);
        return b
    }
    var d, e, f = Array(80),
    h = 1732584193,
    i = 4023233417,
    k = 2562383102,
    j = 271733878,
    n = 3285377520,
    g,
    l,
    m,
    o,
    p,
    a = function(a) {
        for (var a = a.replace(/\r\n/g, "\n"), b = "", c = 0; c < a.length; c++) {
            var d = a.charCodeAt(c);
            128 > d ? b += String.fromCharCode(d) : (127 < d && 2048 > d ? b += String.fromCharCode(d >> 6 | 192) : (b += String.fromCharCode(d >> 12 | 224), b += String.fromCharCode(d >> 6 & 63 | 128)), b += String.fromCharCode(d & 63 | 128))
        }
        return b
    } (a);
    g = a.length;
    var q = [];
    for (d = 0; d < g - 3; d += 4) e = a.charCodeAt(d) << 24 | a.charCodeAt(d + 1) << 16 | a.charCodeAt(d + 2) << 8 | a.charCodeAt(d + 3),
    q.push(e);
    switch (g % 4) {
    case 0:
        d = 2147483648;
        break;
    case 1:
        d = a.charCodeAt(g - 1) << 24 | 8388608;
        break;
    case 2:
        d = a.charCodeAt(g - 2) << 24 | a.charCodeAt(g - 1) << 16 | 32768;
        break;
    case 3:
        d = a.charCodeAt(g - 3) << 24 | a.charCodeAt(g - 2) << 16 | a.charCodeAt(g - 1) << 8 | 128
    }
    for (q.push(d); 14 != q.length % 16;) q.push(0);
    q.push(g >>> 29);
    q.push(g << 3 & 4294967295);
    for (a = 0; a < q.length; a += 16) {
        for (d = 0; 16 > d; d++) f[d] = q[a + d];
        for (d = 16; 79 >= d; d++) f[d] = b(f[d - 3] ^ f[d - 8] ^ f[d - 14] ^ f[d - 16], 1);
        e = h;
        g = i;
        l = k;
        m = j;
        o = n;
        for (d = 0; 19 >= d; d++) p = b(e, 5) + (g & l | ~g & m) + o + f[d] + 1518500249 & 4294967295,
        o = m,
        m = l,
        l = b(g, 30),
        g = e,
        e = p;
        for (d = 20; 39 >= d; d++) p = b(e, 5) + (g ^ l ^ m) + o + f[d] + 1859775393 & 4294967295,
        o = m,
        m = l,
        l = b(g, 30),
        g = e,
        e = p;
        for (d = 40; 59 >= d; d++) p = b(e, 5) + (g & l | g & m | l & m) + o + f[d] + 2400959708 & 4294967295,
        o = m,
        m = l,
        l = b(g, 30),
        g = e,
        e = p;
        for (d = 60; 79 >= d; d++) p = b(e, 5) + (g ^ l ^ m) + o + f[d] + 3395469782 & 4294967295,
        o = m,
        m = l,
        l = b(g, 30),
        g = e,
        e = p;
        h = h + e & 4294967295;
        i = i + g & 4294967295;
        k = k + l & 4294967295;
        j = j + m & 4294967295;
        n = n + o & 4294967295
    }
    p = c(h) + c(i) + c(k) + c(j) + c(n);
    return p.toLowerCase()
}
var bodyContent = function() {
    var a = $(window).height(),
    b = $(window).width();
    $("body").css({
        height: a + "px",
        overflow: "hidden"
    });
    90 === window.orientation || -90 === window.orientation ? ($(".yk-vmain").css({
        width: b - 257 + "px"
    }), $(".yk-vside").css({
        height: a - 40 + "px"
    }), $(".yk-vside").show(), setTimeout(function() {
        window.sidescroll = new iScroll($(".yk-vside")[0], {
            hScroll: !1,
            hScrollbar: !1,
            vScrollbar: !1
        })
    },
    2E3)) : $(".yk-vmain").css({
        width: "auto",
        overflow: "hidden"
    });
    playerWidth();
    $(window).on("orientationchange resize",
    function() {
        playerWidth();
        // if (0 == window.orientation || 180 == window.orientation) {
        //     var a = $(window).width(),
        //     b = $(window).height();
        //     $(".yk-vside").hide();
        //     $("body").css({
        //         height: b + "px"
        //     });
        //     //alert("here! width auto");
        //     // $(".yk-vmain").css({
        //     //     width: "auto"
        //     // })
        // } else if (!0 != window.isFullscreen) a = $(window).width(),
        // b = $(window).height(),
        // $(".yk-vmain").css({
        //     width: a - 257 + "px"
        // }),
        // $(".yk-vside").css({
        //     height: b - 40 + "px"
        // }),
        // $("body").css({
        //     height: b + "px"
        // }),
        // $(".yk-vside").show(),
        // window.sidescroll ? window.sidescroll.refresh() : window.sidescroll = new iScroll($(".yk-vside")[0], {
        //     hScroll: !1,
        //     hScrollbar: !1,
        //     vScrollbar: !1
        // }),
        // setTimeout("window.sidescroll.refresh()", 1E3);
    })
},
videoContent = {
    init: function() {
        var a = this;
        this.currentTabs = ["showlist", "folderlist", "mvlist", "relations", "demandlist"];
        this.setCurTab = "comments";
        this.current = "";
        this.tabs = $(".yk-vcontent .tab-box ul.tabs li");
        this.sideTabs = [];
        for (var b = 0; b < this.tabs.length; b++)"side" == this.tabs[b].getAttribute("_type") && this.sideTabs.push(this.tabs[b]);
        this.tabs.removeClass("currentt"); - 90 == window.orientation || 90 == window.orientation ? ($("#" + this.setCurTab + "_tab").addClass("current"), $("#ab_v_1427883541").insertAfter("#comments_content"), $.each(this.sideTabs,
        function() {
            this.style.display = "none";
            try {
                eval("(" + this.getAttribute("_to") + "Fun)").apply()
            } catch(a) {}
            $("#" + this.getAttribute("_to") + "_side").show();
            $("#" + this.getAttribute("_to")).hide()
        })) : $.each(this.sideTabs,
        function() {
            if ( - 1 !== $.inArray(this.getAttribute("_to"), a.currentTabs)) this.className = "current",
            $("#" + this.getAttribute("_to")).show();
            this.style.display = "block"
        });
        $(window).on("orientationchange",
        function() {
            a.tabs.removeClass("current"); - 90 == window.orientation || 90 == window.orientation ? ($.each(a.sideTabs,
            function() {
                this.style.display = "none";
                $("#" + this.getAttribute("_to") + "_side").show();
                $("#" + this.getAttribute("_to")).hide()
            }), "" == a.current || -1 !== $.inArray(a.current, a.currentTabs) || "payinfo" == a.current ? $("#" + a.setCurTab + "_tab").addClass("current") : $("#" + a.current + "_tab").addClass("current"), $("#ab_v_1427883541").insertAfter("#comments_content")) : $.each(a.sideTabs,
            function() {
                this.style.display = "block";
                if ("" == a.current) {
                    if ( - 1 !== $.inArray(this.getAttribute("_to"), a.currentTabs)) this.className = "current",
                    $("#" + this.getAttribute("_to")).show()
                } else $("#" + a.current + "_tab").addClass("current");
                "relations" == this.getAttribute("_to") ? $("#ab_v_1427883541").insertAfter("#related-list") : "showlist" == this.getAttribute("_to") ? $("#ab_v_1427883541").insertBefore("#showlist .yk-body .yk-footer") : "folderlist" == this.getAttribute("_to") ? $("#ab_v_1427883541").insertAfter("#showdrama-list-folder") : "mvlist" == this.getAttribute("_to") ? $("#ab_v_1427883541").insertAfter("#showdrama-list-mv") : "demandlist" == this.getAttribute("_to") && $("#ab_v_1427883541").insertAfter("#demand-list")
            });
            a.initCurrent()
        });
        this.initCurrent();
        this.bind()
    },
    initCurrent: function() {
        var a = this;
        this.tabs.each(function(b) {
            b = a.tabs.eq(b).attr("_to");
            0 < $("#" + b).length && $("#" + b).hide()
        });
        this.tabsCurrent = $(".yk-vcontent .tab-box ul.tabs li.current");
        if (0 >= this.tabs.length) return ! 1;
        if (0 < this.tabsCurrent.length) {
            var b = this.tabsCurrent.attr("_to");
            if (0 < $("#" + b).length) {
                $("#" + b).show();
                try {
                    eval("(" + b + "Fun)").apply()
                } catch(c) {}
                setTimeout(function() {
                    a.fixedContent($("#" + b)[0])
                },
                500)
            }
        }
    },
    bind: function() {
        var a = this;
        this.tabs.bind("click",
        function() {
            a.tabs.removeClass("current");
            a.tabs.each(function(b) {
                b = a.tabs.eq(b).attr("_to");
                0 < $("#" + b).length && $("#" + b).hide()
            });
            a.tabsCurrent = $(this);
            this.className += " current";
            var b = this.getAttribute("_to");
            a.current = b;
            if (0 < $("#" + b).length) {
                "videoinfo" == b && 0 < $(".vr").length && $.ajax({
                    url: "http://index.youku.com/dataapi/getData?num=100006&sid=" + window.showid_en,
                    type: "get",
                    dataType: "jsonp",
                    jsonp: "jsoncallback",
                    success: function(a) {
                        0 < a.result.index ? $(".vr .num").html(numberFormat(a.result.index)) : $(".vr .num").html("\u6682\u65e0")
                    }
                });
                $("#" + b).show();
                try {
                    eval("(" + b + "Fun)").apply()
                } catch(c) {}
                a.fixedContent($("#" + b)[0])
            }
        });
        $(window).on("orientationchange",
        function() {
            if (0 < a.tabsCurrent.length) {
                var b = a.tabsCurrent.attr("_to");
                0 < $("#" + b).length && ($("#" + b).show(), setTimeout(function() {
                    a.fixedContent($("#" + b)[0])
                },
                500))
            }
        })
    },
    fixedContent: function(a) {
        if (!0 == window.isFullscreen || !a) return ! 1;
        var b = $(window).height(),
        c = $(".yk-player").outerHeight(),
        b = b - c - 80 - 40;
        if ("none" != $(".app-download").css("display") || "none" != $(".m-backtrack").css("display")) b -= 40;
        if ( - 90 == window.orientation || 90 == window.orientation) b += 2 * $(".yk-player").outerHeight() / 3;
        a.style.height = b + "px";
        this.scroll && this.scroll.destroy();
        this.scroll = new iScroll(a.getAttribute("id"), {
            hScroll: !1,
            hScrollbar: !1,
            vScrollbar: !1,
            onScrollMove: function() {
                $("body").stop();
                if (0 < this.y) return $("body").animate({
                    scrollTop: 0
                },
                600),
                !1;
                if (0 > this.y) return $("body").animate({
                    scrollTop: 2 * $(".yk-player").outerHeight() / 3
                },
                600),
                !1
            }
        })
    },
    refreshContent: function() {
        if (0 == window.orientation || 180 == window.orientation) return ! 1;
        var a = this;
        if (this.scroll) this.scroll.refresh();
        else {
            var b = function() {
                a.scroll ? a.scroll.refresh() : setTimeout(b, 100)
            };
            setTimeout(b, 100)
        }
    },
    refreshHeight: function() {
        var a = this;
        if (0 < a.tabsCurrent.length) {
            var b = a.tabsCurrent.attr("_to");
            0 < $("#" + b).length && ($("#" + b).show(), setTimeout(function() {
                a.fixedContent($("#" + b)[0])
            },
            500), (90 == window.orientation || -90 == window.orientation) && $("#" + b).css("height", "100%"))
        }
    },
    showTabById: function(a) {
        var b = this;
        b.tabs.removeClass("current");
        b.tabs.each(function(c) {
            var d = b.tabs.eq(c).attr("_to");
            d != a && 0 < $("#" + d).length && $("#" + d).hide();
            d == a && (b.tabs.eq(c).addClass("current"), $("#" + d).show())
        })
    }
},
commentsFun = function() {
    1 == $("#comments_content").children().length && xcomments.init("http://" + cmts_domain + "/comments/xcomments?id=" + videoIdEn + "&callback=xcomments.disp&ver=v2", "pad");
    $("#comments").show()
},
folderlistFun = function() {
    0 >= $(".showdrama-list").children().length && loadDatas("folderlist", 50,
    function(a) {
        if (!a) return ! 1;
        a = eval("(" + a + ")");
        a.folderlist && List && List.init(a.folderlist, "folderlist")
    })
},
showlistFun = function() {
    var a = "showlist";
    "undefined" != typeof window.stage && "85" != window.cateId && 8 == window.stage.length && (a = "showlistbydate");
    var b = 50;
    "97" == window.cateId && (b = 100);
    var c = $(".showdrama-list").children().length;
    if ("85" == window.cateId) c = $(".showlists").children().length;
    0 >= $(".showDrama .drama-linkpanel .list").children().length && 0 >= c && loadDatas(a, b,
    function(b) {
        if (!b) return ! 1;
        b = eval("(" + b + ")");
        b[a] && List && List.init(b[a], a);
        $(".panel .handle-more").click(function() {
            var a = $(this).attr("vid");
            $(".rel-aspect[vid=" + a + "] li").css("display", "block");
            $(this).css("display", "none")
        });
        $(".program .handle").click(function() {
            var a = $(this).attr("vid");
            $(".item[vid=" + a + "]").hasClass("item-open") ? ($(".item[vid=" + a + "]").removeClass("item-open").addClass("item-close"), $(".rel-aspect[vid=" + a + "] li").css("display", "none")) : ($(".item[vid=" + a + "]").removeClass("item-close").addClass("item-open"), $(".rel-aspect[vid=" + a + "] li").css("display", "block"))
        });
        videoContent.refreshHeight()
    })
},
mvlistFun = function() {
    0 >= $(".showdrama-list").children().length && loadDatas("mvlist", 50,
    function(a) {
        if (!a) return ! 1;
        a = eval("(" + a + ")");
        a.mvlist && List && List.init(a.mvlist, "mvlist")
    })
},
relationsFun = function() {
    0 >= $("#relations_side .related-list").children().length && 0 >= $("#relations .related-list").children().length && RelationVideoPhone.videoPhone()
},
demandlistFun = function() {
    0 >= $("#demandlist_side .related-list").children().length && 0 >= $("#demandlist .related-list").children().length && loadDatas("demandlist", 100,
    function(a) {
        if (!a) return ! 1;
        a = eval("(" + a + ")");
        a.demandlist && 0 < $("#demandlist").length && ($("#demandlist_side .related-list").html(a.demandlist), $("#demandlist .related-list").html(a.demandlist));
        videoContent.refreshContent();
        $("#demandlist .yk-pageloading").hide();
        $("#demandlist_side .yk-pageloading").hide()
    });
    videoContent.refreshContent()
},
loadDatas = function(a, b, c) {
    var d = window.videoId || 0,
    e = window.showId || 0,
    f = window.parentVideoId || 0;
    0 < f && (e = window.patentShowId || 0);
    $.get("/x_getAjaxData", {
        md: a,
        pl: b || 20,
        vid: d,
        showid: e,
        v: f,
        singerid: window.singerId,
        o: window.o || 1,
        fid: window.folderId || 0,
        cateid: window.cateId || 0,
        playmode: window.playmode || 0,
        ver: "v2",
        type: window.type || 0
    },
    c)
},
List = {
    total: 0,
    pn: 0,
    pl: 0,
    pages: 0,
    firstMon: 0,
    lastMon: 0,
    startDate: 0,
    endDate: 0,
    init: function(a, b) {
        if (!a || !a.items) return ! 1;
        this.listObj = $(".showDrama .drama-linkpanel .list");
        if (0 >= this.listObj.length) this.listObj = "85" == window.cateId || "85" == a.cateid ? $(".showlists") : $(".showdrama-list");
        this.listPager1 = $(".drama-tab .list");
        this.listPager2 = $(".drama-select");
        this.initConfig(a);
        this.dataType = b;
        this.initList();
        this.genPageBar()
    },
    initConfig: function(a) {
        if (a.items) this.itemContent = a.items;
        if (a.total) this.total = parseInt(a.total);
        if (a.pn) this.pn = parseInt(a.pn);
        if (a.pl) this.pl = parseInt(a.pl);
        if (a.year) this.year = parseInt(a.year);
        if (a.firstMon) this.firstMon = parseInt(a.firstMon);
        if (a.lastMon) this.lastMon = parseInt(a.lastMon)
    },
    initList: function() {
        if (!this.itemContent) return ! 1;
        _this = this;
        this.listObj.parents(".yk-body").find(".yk-pageloading").hide();
        this.listObj.children().hide();
        for (var a = 0; a < this.listObj.length; a++) this.listObj[a].innerHTML = this.itemContent + this.listObj[a].innerHTML;
        videoContent.refreshContent();
        window.sidescroll && window.sidescroll.refresh()
    },
    addNewList: function(a, b, c) {
        if (!a && !b && !c) return ! 1;
        a || (a = 0);
        var d = this,
        e = window.videoId || 0,
        f = window.showId || 0,
        h = window.parentVideoId || 0;
        0 < h && (f = window.patentShowId || 0);
        var i = window.singerId || 0,
        k = window.o || 0,
        j = window.folderId || 0;
        this.listObj.parents(".yk-body").find(".yk-pageloading").show();
        $.get("/x_getAjaxData", {
            md: this.dataType,
            vid: e,
            showid: f,
            v: h,
            singerid: i,
            o: k,
            fid: j,
            pl: this.pl,
            pn: a,
            startdate: b,
            enddate: c,
            ver: "v2"
        },
        function(a) {
            if (!a) return ! 1;
            a = eval("(" + a + ")");
            a = a[d.dataType];
            if (!a || !a.items || "null" == a.items) return ! 1;
            d.initConfig(a);
            d.initList()
        })
    },
    genPageBar: function() {
        var a = "showlistbydate" == this.dataType ? this.genBarDate() : this.genBarNum();
        if ("" == a || "<ul></ul>" == a) return this.listPager1.parent().hide(),
        this.listPager2.hide(),
        !1;
        this.listPager1.html(function() {
            this.innerHTML = a
        });
        this.listPager2.find(".panel").html(function() {
            this.innerHTML = a
        });
        this.listPager1.parent().show();
        this.listPager2.show();
        this.bindClickToPage()
    },
    genBarNum: function() {
        if (0 == this.pl || 0 == this.total || this.total <= this.pl) return "";
        for (var a = this.pn,
        b = this.pl,
        c = this.total,
        d = Math.ceil(c / b), e = "<ul>", f = 1; f <= d; f++) {
            var h = "",
            i = (f - 1) * b + 1,
            k = f * b;
            k > c && (k = c);
            h += "<li ";
            h += ' i="' + f + '" ';
            a == f && (h += 'class="current"');
            h += "><a>" + i + " - " + k + "</a></li>";
            a == f && this.listPager2.find(".handle").html(function() {
                this.innerHTML = i + "-" + k
            });
            e += h
        }
        this.pages = d;
        return e + "</ul>"
    },
    genBarDate: function() {
        if (0 == this.lastMon) return "";
        var a = parseInt(this.firstMon),
        b = parseInt(this.lastMon),
        c = parseInt(this.year),
        d = parseInt(this.pn),
        e = "<ul>",
        f = b - a,
        h = parseInt(f / 3) + 1;
        if (0 == f) return "";
        for (f = 1; f <= h; f++) {
            var i = "",
            k = a + 3 * (f - 1),
            j = k + 2;
            j > b && (j = b);
            var n = k,
            g = j;
            10 > k && (k = "0" + k);
            10 > j && (j = "0" + j);
            i += "<li ";
            i += ' i="' + f + '" start="' + c + k + '" end="' + c + j + '" ';
            d == f && (i += 'class="current"');
            i += "><a>" + n + " - " + g + "\u6708</a></li>";
            d == f && this.listPager2.find(".handle").html(function() {
                this.innerHTML = n + "-" + g + "\u6708"
            });
            e += i
        }
        this.pages = h;
        return e + "</ul>"
    },
    loadImgs: function() {},
    bindClickToPage: function() {
        var a = this;
        this.listPager2.find(".handle").click(function(b) {
            b.preventDefault();
            b = a.listPager2.find(".panel");
            "none" == b.css("display") ? (b.show(), videoContent.refreshContent()) : b.hide()
        });
        var b = this.listPager1.find("li"),
        c = this.listPager2.find("li");
        if (1 >= b.length && 1 >= c.length) return ! 1;
        b.click(function() {
            if ("current" == this.className) return ! 1;
            var b = this.getAttribute("i") || 0;
            a.listPager1.find("li").removeClass("current");
            a.listPager2.find(".panel li:nth(" + (b - 1) + ")").addClass("current");
            this.className = "current";
            for (var c = 0; c < a.listPager2.find(".handle").length; c++) a.listPager2.find(".handle")[c].innerHTML = this.innerHTML;
            if (0 < $(".list_" + b).length) return a.changeCurrentList(b),
            !1;
            var c = this.getAttribute("start") || 0,
            f = this.getAttribute("end") || 0;
            a.addNewList(b, c, f)
        });
        c.click(function(b) {
            b.preventDefault();
            if ("current" == this.className) return ! 1;
            b = this.getAttribute("i") || 0;
            a.listPager2.find("li").removeClass("current");
            a.listPager1.find("li:nth(" + (b - 1) + ")").addClass("current");
            this.className = "current";
            for (var c = 0; c < a.listPager2.find(".handle").length; c++) a.listPager2.find(".handle")[c].innerHTML = this.innerHTML;
            a.listPager2.find(".panel").hide();
            if (0 < $(".list_" + b).length) return a.changeCurrentList(b),
            !1;
            var c = this.getAttribute("start") || 0,
            f = this.getAttribute("end") || 0;
            a.addNewList(b, c, f)
        })
    },
    changeCurrentList: function(a) {
        this.listObj.children().hide();
        $(".list_" + a).show();
        this.pn = parseInt(a);
        videoContent.refreshContent();
        window.sidescroll && window.sidescroll.refresh()
    }
},
Interact = {
    init: function() {
        this.downloadInit();
        this.updownInit();
        this.shareInit();
        this.favInit()
    },
    updownInit: function() {
        var a = this,
        b = $(".fn-up");
        if (0 >= b.length || "fn-up fn-up-return" == b[0].className) return ! 1;
        var c = opCookie("up-down" + window.videoId);
        if ("up" == c || "down" == c) return this.disableUpdown(c),
        !1;
        b.click(function() {
            a.updown("up")
        })
    },
    updown: function(a) {
        var b = $(".fn-up");
        if (0 >= b.length || "fn-up fn-up-return" == b[0].className) return ! 1;
        b = opCookie("up-down" + window.videoId);
        if ("up" == b || "down" == b) return this.disableUpdown(b),
        !1;
        var b = "",
        b = window.videoId,
        c = window.tcode,
        d = hcbt(c),
        b = '{"videoId":' + b + ',"type":"' + a + '","t":"' + c + '","s":"' + d + '","deviceid":3,"addtion":"1_1"}'; (new Image).src = "http://v.youku.com/QVideo/~ajax/updown?__ap=" + b;
        opCookie("up-down" + window.videoId, a, {
            expires: 1,
            domain: "youku.com",
            path: "/"
        });
        this.disableUpdown(a)
    },
    disableUpdown: function(a) {
        var b, c = parseInt(window.uptimes);
        "up" == a && (b = numberFormat(c + 1));
        $(".updown-stat").html(b);
        a = $(".fn-up");
        if (0 >= a.length) return ! 1;
        a.toggleClass("fn-up-return");
        a.unbind("click")
    },
    downloadInit: function() {
        var a = navigator.userAgent,
        b = $(".fn-download");
        if (0 >= b.length) return ! 1;
        var c = b.attr("class");
        if ( - 1 !== c.indexOf("fn-download-disabled")) return ! 1;
        if ( - 1 != a.indexOf("iPad")) {
            b = $(".fn-download");
            0 >= b.length && (b = $(".fn-download-disabled"));
            if (0 >= b.length) return ! 1;
            c = b.attr("class");
            b.show();
            Log.log(1, "tp=1&cp=4008915&cpp=1000752");
            var d = !1;
            window.onblur = function() {
                d = !1
            };
            $("#fn-download-div").click(function() {
                if (!0 === b.hasClass("fn-download-expand")) b.removeClass("fn-download-expand"),
                Log.log(1, "tp=1&cp=4009038&cpp=1000752");
                else {
                    d = !0;
                    var a = document.createElement("iframe");
                    a.width = 0;
                    a.height = 0;
                    var c = getCookie("__ysuid") || "";
                    a.src = "youkuhd://download?vid=" + window.videoIdEn + "&title=" + encodeURIComponent(window.videoTitle) + "&source=mplaypage&cookieid=" + c;
                    $("body").append(a);
                    $(".fn-more").removeClass("fn-more-expand");
                    $(".fn-more .panelBox").hide();
                    setTimeout(function() {
                        d ? Log.log(1, "tp=1&cp=4009056&cpp=1000752") : Log.log(1, "tp=1&cp=4009055&cpp=1000752");
                        b.addClass("fn-download-expand")
                    },
                    1E3);
                    Log.log(1, "tp=1&cp=4008885&cpp=1000752");
                    Log.log(1, "tp=1&cp=4009035&cpp=1000752")
                }
                return ! 1
            });
            $("#fn-download-install").click(function() {
                window.open("http://m.youku.com/webapp/dl?app=youku&source=webqr", "target=_blank");
                Log.log(1, "tp=1&cp=4009036&cpp=1000752")
            });
            $("#fn-download-close").click(function() {
                b.removeClass("fn-download-expand");
                Log.log(1, "tp=1&cp=4009038&cpp=1000752")
            })
        } else - 1 == a.indexOf("iPhone") && -1 != a.indexOf("Android") && window.downloadUrl && -1 !== window.downloadUrl.indexOf("http://") && (b.show(), Log.log(1, "tp=1&cp=4008915&cpp=1000752"), b.click(function() {
            window.open(window.downloadUrl, "target=_blank");
            Log.log(1, "tp=1&cp=4008885&cpp=1000752");
            return ! 1
        }))
    },
    shareInit: function() {
        var a = $(".fn-share a");
        if (!a) return ! 1;
        a.click(function() {
            $("#player").css("visibility", "hidden");
            $(".yk-winshare").show()
        });
        $(".yk-sharebox .btn-close").click(function() {
            "hidden" == $("#player").css("visibility") && $("#player").css("visibility", "visible");
            $(".yk-winshare").hide()
        });
        this.shareLaiwang()
    },
    favInit: function() {
        $(".fn-favorite").click(function() {
            if (!islogin()) return login(function() {
                $(".fn-favorite").trigger("click")
            }),
            !1;
            var a = '{"videoId":' + videoId + ',"deviceid":3,"addtion":"1_1"}'; (new Image).src = "http://v.youku.com/QVideo/~ajax/addFav?__ap=" + a;
            $(".fn-favorite").addClass("fn-favorite-return")
        })
    },
    shareLaiwang: function() {
        null != window.navigator.userAgent.match(/AliApp/i) && null != window.navigator.userAgent.match(/LW/i) && $("#share-laiwang").show().click(function() {
            $("#shareSend").show(0,
            function() {
                $("#shareSendTxt").html('<span style="font-size:18px;">\u5206\u4eab\u5230\u6765\u5f80\uff0c\u8bf7\u70b9\u51fb\u53f3\u4e0a\u89d2</span><br /><span>\u518d\u9009\u62e9\u3010\u5206\u4eab\u7ed9\u597d\u53cb\u3011</span><br /><span>\u6216\u3010\u5206\u4eab\u5230\u52a8\u6001\u3011</span>')
            }).click(function() {
                $("#shareSend").hide()
            })
        })
    }
},
topRecommend = function() {
    var a = xparamsString.adapter || "",
    b = xparamsString.backurl || "youku://";
    if ("" != a && "android" != a) return $(".m-backtrack").show(),
    videoContent.refreshHeight(),
    $(".m-backtrack a")[0].href = b,
    $(".m-backtrack a").click(function() {
        Log.log(1, "tp=1&cp=4008724&cpp=1000752")
    }),
    !1;
    var c = $("#app-download");
    c.show();
    var d = getCookie("__ysuid") || "";
    $("#app-download .btn-close").click(function() {
        c.hide();
        videoContent.refreshHeight();
        Log.log(1, "tp=1&cp=4008067&cpp=1000687")
    });
    $("#app-download .btn-download , #app-download .btn-maj").click(function() {
        $("body").append("<div class='yk-mask' style='height:" + $(document).height() + "px;'></div>");
        $("#wintipsApp").show();
        videoContent.refreshHeight();
        var a = document.createElement("iframe");
        a.width = 0;
        a.height = 0;
        a.src = "youkuhd://play?vid=" + videoIdEn + "&source=mplaypage&cookieid=" + d;
        $("#app-download").append(a);
        Log.log(1, "tp=1&cp=4008914&cpp=1000687")
    });
    if (0 < $("#btnWintipsApp").length) window.onblur = function() {},
    Log.log(1, "tp=1&cp=4009217&cpp=1000752");
    $("#btnWintipsApp").click(function() {
        $("body").append("<div class='yk-mask' style='height:" + $(document).height() + "px;'></div>");
        $("#wintipsApp").show();
        Log.log(1, "tp=1&cp=4009218&cpp=1000752");
        var a = document.createElement("iframe");
        a.width = 0;
        a.height = 0;
        a.src = "youkuhd://play?vid=" + window.videoIdEn + "&source=mplaypage&cookieid=" + d;
        $("body").append(a);
        setTimeout(function() {},
        1E3)
    });
    $("#wintipsApp").find(".btn-maj").click(function() {
        $("#wintipsApp").hide();
        $(".yk-mask").remove();
        Log.log(1, "tp=1&cp=4009220&cpp=1000752");
        window.open("http://m.youku.com/webapp/dl?app=youku&source=webqr", "target=_blank");
        Log.log(1, "tp=1&cp=4009036&cpp=1000752")
    });
    $("#wintipsApp").find(".btn-sub").click(function() {
        $("#wintipsApp").hide();
        $(".yk-mask").remove();
        Log.log(1, "tp=1&cp=4009221&cpp=1000752")
    });
    $("#app-download2 .btn-close").click(function() {
        $("#app-download2").hide();
        Log.log(1, "tp=1&cp=4009219&cpp=1000752")
    })
},
addDesktop = function() {
    if (hideDeskTop()) return ! 1;
    var a = opCookie("addDesktop"),
    b = browserOnly(); - 1 != window.navigator.userAgent.indexOf("OS 7") && $(".ico_adddesktop_ios").attr("class", "ico_adddesktop_ios7");
    1 != a && "safari" == b && ($(".addDesktop_ipad").show(), Log.log(1, "tp=1&cp=4009104&cpp=1000752"));
    $(".addDesktop_ipad .btnClose").click(function() {
        opCookie("addDesktop", 1, {
            expires: 7,
            domain: "youku.com",
            path: "/"
        });
        Log.log(1, "tp=1&cp=4009105&cpp=1000752")
    })
},
ykPlayerH5,
loadPlayerH5 = function() {
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
    //alert(is_weixin());
    if (xparamsString && xparamsString.firsttime) a.firsttime = xparamsString.firsttime;
    if (opCookie("xreferrer")) a.vvlogconfig.rurl = opCookie("xreferrer"),
    window.canRemoveXrefer && opCookie("xreferrer", "", {
        expires: -1,
        path: "/",
        domain: "youku.com"
    }),
    window.canRemoveXrefer = !0;
    if (2 == window.playmode) a.playlistconfig = {
        Type: "Folder",
        Fid: window.folderId,
        Ob: window.o
    };
    if (void 0 != xparamsString.adext && "" != xparamsString.adext) a.adconfig = {
        adext: xparamsString.adext
    };
    ykPlayerH5 = new YKU.Player("player", a)
};
function onPlayerReadyH5() {}
function onMediaSrcOK(a, b) {
    if ("3gphd" != a || "" == b) return ! 1;
    window.downloadUrl = b;
    Interact.downloadInit()
}
var autoFullscreen = function() {
    if (90 == window.orientation || -90 == window.orientation) {
        if (!1 == window.isFullscreen || !window.isFullscreen) try {
            ykPlayerH5 && ykPlayerH5.switchFullScreen()
        } catch(a) {
            onSwitchFullScreen()
        }
    } else if (!0 == window.isFullscreen) try {
        ykPlayerH5 && ykPlayerH5.switchFullScreen()
    } catch(b) {
        onSwitchFullScreen()
    }
},

playerWidth = function() {
    //2 is margin


    var margin = parseInt($(".play_div").css("margin").replace("px",""));

    if(marginRecorder==""){
        marginRecorder = margin;
    }

    var a = window.innerWidth, b = window.innerHeight; 

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
                height: 9 * a / 16 + "px"
            });
        }
    }

    // ! 0 == window.isFullscreen ?  : ($(".yk-player .yk-player-inner").css({
    //     width: a + "px",
    //     height: 9 * a / 16 + "px"
    // }), 90 === window.orientation || -90 === window.orientation ? $(".yk-player .yk-player-inner").css({
    //     width: a - 257 + "px",
    //     height: 9 * (a - 257) / 16 + "px"
    // }) : $(".yk-player .yk-player-inner").css({
    //     width: a + "px",
    //     height: 9 * a / 16 + "px"
    // }));

};


function onSwitchFullScreen() {

    ! 0 == window.isFullscreen ? (clearInterval(window.timers), window.isFullscreen = !1, $("body").removeClass("fullscreen"), playerWidth(), setTimeout("videoContent.refreshHeight();", 800)) : ($("body").addClass("fullscreen"), window.isFullscreen = !0, window.timers = setInterval("window.scrollTo(0, 1);", 1));
    setTimeout("playerWidth();", 500)
}
function onPlayerCompleteH5(a) {
    if (!0 == window.isFullscreen) try {
        ykPlayerH5 && ykPlayerH5.switchFullScreen()
    } catch(b) {}
    if (!a || !a.vid) return ! 1;
    window.videoId = a.vid;
    window.videoIdEn = a.vidEncoded;
    var c = "?x";
    if (window.folderId) {
        var c = "?f=" + window.folderId,
        d = "";
        0 == window.o && (d = "&o=0");
        c += d + "&x"
    } else window.singerId && (c = "?s=" + window.singerId + "&x");
    window.location.href = "/v_show/id_" + a.vidEncoded + ".html" + c
}
var RelationVideoPhone = {
    videoPhone: function() {
        var a = 1;
        3 == window.playmode && (a = 3);
        var b = 12;
        null != window.navigator.userAgent.match(/android/i) ? b = 17 : null != window.navigator.userAgent.match(/iphone/i) ? b = 15 : null != window.navigator.userAgent.match(/ipad/i) && (b = 14);
        a = "http://ykrec.youku.com/video/packed/list.json?guid=" + opCookie("__ysuid") + "&vid=" + window.videoId + "&cate=" + window.cateId + "&apptype=" + b + "&pg=" + a + "&module=1&pl=20&needTags=1&atrEnable=true&callback=RelationVideoPhone.videoPhoneCallback";
        b = 0;
        "undefined" != typeof window.videoOwnerID && (b = window.videoOwnerID || 0);
        b && (a += "&uid=" + b);
        "undefined" != typeof window.showId && (a += "&sid=" + window.showId);
        var b = document.getElementsByTagName("head").item(0),
        c = document.createElement("script");
        c.src = a + "&rand=" + Date.parse(new Date);
        b.appendChild(c)
    },
    videoPhoneCallback: function(a) { (a = this.createPhoneHtml(a)) ? null == window.navigator.userAgent.match(/ipad/i) ? ($("#relations .showdrama-list").html(a), $("#relations .yk-pageloading").hide()) : ($("#relations_side .related-list").html(a), $("#relations .related-list").html(a), videoContent.refreshContent(), $("#relations .yk-pageloading").hide(), $("#relations_side .yk-pageloading").hide()) : null == window.navigator.userAgent.match(/ipad/i) ? ($("#relations .showdrama-list").html(""), $("#relations .yk-pageloading").hide()) : ($("#relations_side .related-list").html(""), $("#relations .related-list").html(""), videoContent.refreshContent(), $("#relations .yk-pageloading").hide(), $("#relations_side .yk-pageloading").hide());
        appEventListener()
    },
    charset: function(a, b) {
        var c = 12;
        null != window.navigator.userAgent.match(/android/i) ? c = 17 : null != window.navigator.userAgent.match(/iphone/i) ? c = 15 : null != window.navigator.userAgent.match(/ipad/i) && (c = 14);
        var d = a.data[b],
        e = "",
        e = 1 == d.type ? "dvid": "dsid";
        return e = 1 == window.playmode ? "vc-vid=" + window.videoId + "&sct=" + window.cateId + "&pg=1&" + e + "=" + d.id + "&pos=" + b + "&dma=" + d.dma + "&abver=" + a.ver + "&apt=" + c + "&md=1&ord=" + a.ord + "&dct=" + d.dct + "&rtlid=" + a.req_id + "&algInfo=" + d.algInfo: 3 == window.playmode ? "vc-sid=" + window.showId + "&vid=" + window.videoId + "&sct=" + window.cateId + "&pg=3&pos=" + b + "&" + e + "=" + d.id + "&dma=" + d.dma + "&abver=" + a.ver + "&apt=" + c + "&md=1&dct=" + d.dct + "&ord=" + a.ord + "&rtlid=" + a.req_id + "&algInfo=" + d.algInfo: "vc-vid=" + window.videoId + "&sct=" + window.cateId + "&pg=1&" + e + "=" + d.id + "&pos=" + b + "&dma=" + d.dma + "&abver=" + a.ver + "&apt=" + c + "&md=1&ord=" + a.ord + "&dct=" + d.dct + "&rtlid=" + a.req_id + "&algInfo=" + d.algInfo
    },
    datafrom: function(a, b, c) {
        var a = {},
        d = 12;
        null != window.navigator.userAgent.match(/android/i) ? d = 17 : null != window.navigator.userAgent.match(/iphone/i) ? d = 15 : null != window.navigator.userAgent.match(/ipad/i) && (d = 14);
        if (1 == window.playmode) {
            var e = "",
            e = d + "-1-1-" + b + "-" + c;
            a.img = "y7.2-1-" + window.cateId + ".3." + (b + 1) + "-1." + e;
            a.title = "y7.2-1-" + window.cateId + ".3." + (b + 1) + "-2." + e;
            a.user = "y7.2-1-" + window.cateId + ".3." + (b + 1) + "-3";
            a.tag = "y7.2-1-" + window.cateId + ".3." + (b + 1) + "-4"
        } else 3 == window.playmode ? (e = d + "-3-1-" + b + "-" + c, a.img = "y7.2-2-" + window.cateId + ".3." + (b + 1) + "-1." + e, a.title = "y7.2-2-" + window.cateId + ".3." + (b + 1) + "-2." + e) : (e = d + "-1-1-" + b + "-" + c, a.img = "y7.2-3-" + window.cateId + ".3." + (b + 1) + "-1." + e, a.title = "y7.2-3-" + window.cateId + ".3." + (b + 1) + "-2." + e, a.user = "y7.2-3-" + window.cateId + ".3." + (b + 1) + "-3", a.tag = "y7.2-3-" + window.cateId + ".3." + (b + 1) + "-4");
        return a
    },
    clickLog: function(a) {
        if ("" != a) {
            var b = document.getElementsByTagName("head").item(0),
            c = document.createElement("script");
            c.src = a + "&rand=" + Date.parse(new Date);
            b.appendChild(c)
        }
    },
    createPhoneHtml: function(a) {
        var b = a.data;
        if (b) {
            for (var c = '<div class="items">',
            d = 0,
            e = b.length; d < e; d++) { - 1 === b[d].playLink.indexOf("cps.youku.com") && (b[d].playLink += "?x");
                var f = this.charset(a, d),
                h = this.datafrom(a, d, b[d].mm || 0);
                if (0 == d) window.nextVidEn = b[d].codeId,
                window.nextVidCharset = f.replace("vc-", "");
                var i = "",
                k = "";
                if ("undefined" != typeof b[d].clickLogUrl && "" != b[d].clickLogUrl) 2 == b[d].clickRecordType ? k = "at-" + b[d].clickLogUrl.replace("http://r.l.youku.com/rec_at_click?", "") : i = b[d].clickLogUrl;
                var j = "",
                n = "",
                g = b[d].title;
                20 < g.length && (g = g.substring(0, 20) + "...");
                if (1 == b[d].mm && (8 == b[d].type && (j = "\u76f4\u64ad"), "undefined" != typeof b[d].pay_state && (1 == b[d].pay_state || 2 == b[d].pay_state))) j = "\u7cbe\u9009";
                j && (n = '<div class="v-pic-label-bg"></div>', n += '<div class="v-pic-label">' + j + "</div>");
                c += '<div class="item">';
                c += '<div class="v v-horiz">';
                c += '<div class="v-thumb">';
                c += '<div class="v-pic-default">';
                c += '<img src="/index/img/mobile/video_defaultpic2.png">';
                c += n;
                c += "</div>";
                c += '<div class="v-pic-real" style="background-image:url(\'' + b[d].picUrl + "');\"></div>";
                c += '<a class="v-link" href="' + b[d].playLink + '" clicklogurl="' + i + '"  atcharset="' + k + '"  _hzcharset="hz-4008952-1000752" charset="' + f + '" data-from="' + h.img + '" title="' + g + '"></a>';
                c += "</div>";
                if ("\u76f4\u64ad" == j) c += '<div class="v-metadata">',
                c += '<div class="v-title"><a href="' + b[d].playLink + '"  _hzcharset="hz-4008952-1000752"  clicklogurl="' + i + '"  atcharset="' + k + '"  charset="' + f + '" data-from="' + h.title + '" >' + g + "</a></div>",
                c += '<div class="v-desc">',
                "false" == b[d].liveHouse && (c += '<i class="ico-stat-play" title="\u64ad\u653e"></i><span class="v-num">' + b[d].onlineAmount + "\u4eba\u6b63\u5728\u89c2\u770b</span>"),
                c += "</div>";
                else if ("\u7cbe\u9009" == j) {
                    j = "";
                    if ("undefined" != typeof b[d].performer[0].name) j = b[d].performer[0].name;
                    "undefined" != typeof b[d].performer[1].name && (j = j + "," + b[d].performer[1].name);
                    c += '<div class="v-metadata">';
                    c += '<div class="v-title"><a href="' + b[d].playLink + '"  _hzcharset="hz-4008952-1000752"  clicklogurl="' + i + '"  atcharset="' + k + '"  charset="' + f + '" data-from="' + h.title + '" >' + g + "</a></div>";
                    c += '<div class="v-desc">' + b[d].subTitle + "</div>";
                    c += '<div class="v-desc">\u4e3b\u6f14: ' + j + "</div>"
                } else c += '<div class="v-metadata">',
                c += '<div class="v-title"><a href="' + b[d].playLink + '"  _hzcharset="hz-4008952-1000752"  clicklogurl="' + i + '"  atcharset="' + k + '"  charset="' + f + '" data-from="' + h.title + '" >' + g + "</a></div>",
                c += '<div class="v-desc">',
                c += '<i class="ico-stat-play" title="\u64ad\u653e"></i><span class="v-num">' + b[d].playAmount + "\u4eba\u89c2\u770b</span>",
                c += "</div>";
                c += "</div>";
                c += "</div>";
                if (null != window.navigator.userAgent.match(/iphone/i) && (95 == window.cateId || 86 == window.cateId)) if (3 == d || 4 == d) c += '<div class="app">',
                c += '<div class="app-options">',
                c += "<p>\u4e0b\u8f7dAPP\u624d\u53ef\u7ee7\u7eed\u89c2\u770b\u54df~</p>",
                c += '<a class="app-btn-down" href="javascript:void(0);">\u4e0b\u8f7d</a><a class="app-btn-cancel" href="javascript:void(0);">\u53d6\u6d88</a>',
                c += "</div>",
                c += "</div>",
                c += '<div class="app-only" codeid=' + b[d].codeId + ">",
                c += '<a class="app-btn-only" href="javascript:void(0);">APP\u72ec\u64ad</a>',
                c += "</div>";
                c += "</div>"
            }
            return c + "</div>"
        }
        return ""
    }
}; (function(a) {
    document.addEventListener("click",
    function(b) {
        if (!b) b = a.event;
        if ((b = b.target || b.srcElement) && "A" == b.tagName) if ((b = b.getAttribute("clicklogurl")) && "" != b) {
            var c = document.getElementsByTagName("head").item(0),
            d = document.createElement("script");
            d.src = b + "&rand=" + Date.parse(new Date);
            c.appendChild(d)
        }
    })
})(window);
document.domain = "youku.com";
var xcomments = {
    cmts: null,
    url: "",
    page: 1,
    append: 0,
    loading: null,
    cmtBox: null,
    hCbox: null,
    loginBox: null,
    userName: "",
    userPage: "",
    replyId: "",
    hasMoreCmts: !0,
    curCmtTarget: null,
    tempContent: "",
    terminalType: "",
    tagHideCmtBox: !1,
    tagHideLoginBox: !1,
    init: function(a, b) {
        this.cmts = $("#comments_content");
        if (!this.cmts || 0 >= this.cmts.length) return ! 1;
        this.url = a;
        this.terminalType = b || "";
        this.loading = this.cmts.children();
        this.load();
        this.bind()
    },
    load: function() {
        var a = util.genUrl(this.url, {
            page: this.page,
            append: this.append
        });
        util.novaCall(a);
        this.page += 1
    },
    disp: function(a) {
        this.loading && this.loading.remove();
        a.con && this.cmts.append(a.con);
        this.hasMoreCmts = a.hasMoreCmts; ! this.hasMoreCmts && $("#moreComments") && $("#moreComments").remove();
        "pad" == this.terminalType && videoContent.scroll.refresh()
    },
    bind: function() {
        var a = this;
        this.cmts.on("click", "#moreComments",
        function() {
            $("#moreComments").remove();
            a.append = !0;
            a.cmts.append(a.loading);
            a.load();
            return ! 1
        });
        this.cmts.on("click", ".showCmtBox",
        function(b) {
            a.curCmtTarget = $((b || window.event).target);
            login.islogin() ? (a._setUserInfo(), a._createCmtBox(a.curCmtTarget)) : a._cmtLogin();
            return ! 1
        });
        $(window).on("orientationchange",
        function() {
            "pad" == a.terminalType && a.hCbox && "block" == a.hCbox.cmtBox.css("display") && xcommentBox.enlargeMask();
            if ("phone" == a.terminalType) {
                if (90 == window.orientation || -90 == window.orientation) {
                    if (a.hCbox && "block" == a.hCbox.cmtBox.css("display")) a.hCbox.hideBox(),
                    a.tagHideCmtBox = !0;
                    if ($("#yk-winlogin").length && "block" == $("#yk-winlogin").css("display")) $("#yk-winlogin .input-users").blur(),
                    $("#yk-winlogin .input-pwd").blur(),
                    $("#yk-winlogin").hide(),
                    $("#yk-mask").hide(),
                    a.tagHideLoginBox = !0
                }
                if (0 == window.orientation || 180 == window.orientation) {
                    if (a.tagHideCmtBox) a.hCbox.showBox(),
                    a.tagHideCmtBox = !1;
                    if (a.tagHideLoginBox) $("#yk-winlogin").show(),
                    $("#yk-mask").show(),
                    a.tagHideLoginBox = !1
                }
            }
        })
    },
    _createCmtBox: function(a, b) {
        var c = a.attr("data-cmstype"),
        c = {
            type: c,
            userName: this.userName,
            userPage: this.userPage,
            replyId: a.attr("data-rid"),
            srcCmtId: a.attr("data-srcid"),
            callback: this._submitCallback,
            content: b || (c == xcommentBox.buttonType.reply ? this._genDefaultCmtContent(a) : "")
        };
        this.hCbox = xcommentBox.create(c)
    },
    _cmtLogin: function() {
        var a = this;
        $(document).one("userchange",
        function() {
            a._setUserInfo();
            a._createCmtBox(a.curCmtTarget, a.tempContent)
        });
        login()
    },
    _submitCallback: function(a) {
        if (0 > a) {
            if ( - 5 == a) xcomments.tempContent = xcomments.hCbox.hTextarea.val(),
            xcomments.hCbox.hideBox(),
            xcomments._cmtLogin();
            return ! 1
        }
        xcomments.hCbox.hideBox();
        $("#no-comments").length && $("#no-comments").hide();
        var b = xcomments._submitCallbackRewriteContent(a.content);
        "pad" == xcomments.terminalType ? (videoContent.scroll.scrollToElement("#cmtsubmitnotice"), setTimeout(function() {
            videoContent.scroll.refresh()
        },
        100)) : window.scrollTo(0, $("#comments_content").first().offset().top - 40);
        $(".comment-list").first().prepend(b);
        $("#cmtsubmitnotice").html(xcommentBox.showNoticeTip(2 == a.state ? 100 : 0));
        $("#cmtsubmitnotice").show()
    },
    _submitCallbackRewriteContent: function(a) {
        return '<li class="item"><div class="text"><div class="bar"><span class="name">\u6211</span></div><div class="con">' + a + '</div><div class="panel"><span class="time">0\u5206\u949f\u524d</span><span class="via">\u6765\u81ea\u4f18\u9177</span></div></div></li>'
    },
    _genDefaultCmtContent: function(a) {
        var b = a.parents(".text"),
        a = b.find(".name").children().html() || "no-name-xxxx",
        b = b.find(".con").html(),
        a = " //@" + $.trim(a) + ":" + $.trim(b),
        a = a.replace(/<img[^<]+?alt="(.+?)"[^<]+?>/img, "[$1]").replace(/<a[^<]+?>(.+?)<\/a>/img, "$1 ");
        return this._stripTags(a).replace(/[\n\t\r]+/ig, " ")
    },
    _stripTags: function(a) {
        return a.replace(/<\w+(\s+("[^"]*"|'[^']*'|[^>])+)?>|<\/\w+>/gi, "")
    },
    _setUserInfo: function() {
        this.userName = login.getUserInfo().username || "";
        this.userPage = "http://i.youku.com/u/home/"
    }
},
xcommentBox = {
    cmtBox: null,
    contentMaxLen: 300,
    buttonType: {
        reply: "reply",
        publish: "publish"
    },
    create: function(a) {
        this.cmtBox ? this._modifyCmtBox(a.type) : (this.cmtBox = $(this._createPopbox(a.userName, a.userPage)), $("body").append(this.cmtBox), this.init(a.callback));
        this._updateData(a);
        this.hTextarea.val(a.content);
        this.showBox($(document).scrollTop());
        return this
    },
    init: function(a) {
        var b = this;
        this.hTextarea = this.cmtBox.find(".textarea");
        this.hWordcount = this.cmtBox.find(".wordlimit");
        this.hVerifycode = this.cmtBox.find(".validate");
        this.hSubmit = this.cmtBox.find(".cmt-submit");
        this.hError = this.cmtBox.find(".rep-error");
        this.hClose = this.cmtBox.find(".btn-close");
        this.hTextarea.val("");
        this.fCallback = a;
        this._initTextara();
        this._initSubmit();
        this._initClose();
        xVerifyCode.init(this.hVerifycode,
        function() {
            b.hError.hide()
        })
    },
    showBox: function(a) {
        this.cmtBox_show_do();
        if (0 == $("#cmt-mask").length) $("body").append('<div class="yk-mask" id="cmt-mask"></div>'),
        this.hMask = $("#cmt-mask");
        this.hMask.show();
        this.enlargeMask();
        this.cmtBox.css({
            display: "block",
            top: a + "px"
        });
        this.hTextarea.focus();
        if (this._isRenewScroll()) {
            var b = this;
            setTimeout(function() {
                window.scrollTo(0, b.cmtBox[0].offsetTop)
            },
            500)
        }
    },
    hideBox: function() {
        this.hTextarea.blur();
        this.cmtBox_hide_do();
        this.cmtBox.hide();
        this.hMask.hide()
    },
    enlargeMask: function() {
        this.hMask.css("height", $(window).height() > $(document).height() ? $(window).height() : $(document).height())
    },
    countWord: function() {
        var a = 0,
        b = this.contentMaxLen;
        if (this.hWordcount) a = $.trim(this.hTextarea.val()).length,
        $(this.hWordcount.children()[0]).html(a),
        a > b ? $(this.hWordcount.children()[0]).addClass("worderror") : $(this.hWordcount.children()[0]).removeClass("worderror")
    },
    _initSubmit: function() {
        var a = this;
        this.hSubmit.on("click",
        function() {
            var b = a.hTextarea.val(),
            c = a._checkBeforeSubmit(b);
            if (0 > c) return a.showNoticeTip(c),
            !1;
            c = a._genMobileStatCode(a);
            b = {
                videoId: window.videoId,
                content: b,
                verify_code: a.hVerifycode.find(".vcode-input").val(),
                reply_cid: a.rid ? a.rid: "",
                soure_id: a.scid ? a.scid: "",
                sync_ucenter: "",
                sync_renren: "",
                sync_sina: "",
                sync_tencent: "",
                sync_messenger: "",
                sync_qzone: "",
                sync_kaixin: "",
                log_source_id: c
            };
            $.post("/QComments/xcommentsSubmit", b, a.submitCallback, "json")
        })
    },
    _genMobileStatCode: function(a) {
        var b = "2-1";
        a.scid && (b = "2-2");
        "pad" == xcomments.terminalType && (b = "1-1", a.scid && (b = "1-2")); - 1 < navigator.userAgent.indexOf("Android") && (b = "3-1", a.scid && (b = "3-2"));
        return b
    },
    submitCallback: function(a) {
        xVerifyCode.isRefreshSrc = !0;
        xVerifyCode.refresh();
        if (!xcommentBox._checkAfterSubmit(a)) return ! 1;
        "function" == typeof xcommentBox.fCallback && xcommentBox.fCallback(a)
    },
    _checkBeforeSubmit: function(a) {
        var b = 1;
        1 > a.replace(/(^\s*)|(\s*$)/g, "").length ? b = -8 : a.replace(/(^\s*)|(\s*$)/g, "").length > this.contentMaxLen && (b = -11);
        return b
    },
    _checkAfterSubmit: function(a) {
        if (0 > a) {
            if ( - 5 == a) return "function" == typeof xcommentBox.fCallback && xcommentBox.fCallback(a),
            !1; ( - 9 == a || -10 == a) && xcommentBox.cmtBox.find(".cmt-vcode").addClass("input-error");
            xcommentBox.showNoticeTip(a);
            return ! 1
        }
        return ! 0
    },
    _initTextara: function() {
        var a = this;
        this.hTextarea.on("focus",
        function() {
            var b = this.getAttribute("data-state");
            if (! (b && "true" == b)) this.setAttribute("data-state", "true"),
            xVerifyCode.isRefreshSrc = !1,
            xVerifyCode.isShow(),
            a.countWord(),
            a.hError.hide(),
            a._setRangePos(this)
        });
        this.hTextarea.on("blur",
        function() {
            if ("" == this.value) this.value = this.defaultValue;
            this.setAttribute("data-state", "false")
        });
        this.hTextarea.on("propertychange",
        function() {
            a.countWord()
        });
        this.hTextarea.on("input",
        function() {
            a.countWord()
        });
        this.hTextarea.on("keyup",
        function() {
            a.countWord()
        })
    },
    _initClose: function() {
        var a = this;
        a.hClose.on("click",
        function() {
            a.hideBox()
        })
    },
    _updateData: function(a) {
        this.type = a.type;
        this.rid = a.replyId || "";
        this.scid = a.srcCmtId || ""
    },
    _isRenewScroll: function() {
        return navigator.userAgent.indexOf("Android") && navigator.userAgent.indexOf("360browser")
    },
    cmtBox_show_do: function() {
        $("#mheader_box").length && $("#mheader_box").hide();
        $("#player_tabsbox").length && $("#player_tabsbox").hide();
        $("#player").length && $("#player").css("visibility", "hidden")
    },
    cmtBox_hide_do: function() {
        $("#mheader_box").length && $("#mheader_box").show();
        $("#player_tabsbox").length && $("#player_tabsbox").show();
        $("#player").length && $("#player").css("visibility", "visible")
    },
    _modifyCmtBox: function(a) {
        this.hSubmit.html(a == this.buttonType.reply ? "\u56de\u3000\u590d": "\u53d1\u8868\u8bc4\u8bba")
    },
    _createPopbox: function(a, b) {
        return '<div class="yk-wincomment" style="top: 0px; display: block;"><div class="btn-close"><i></i></div><div class="yk-wincomment-head"><div class="title">\u53d1\u8868\u8bc4\u8bba</div></div><div class="yk-wincomment-body"><div class="yk-wincomment-form"><div class="comcon"><div class="rep-error" style="display:none"></div><div class="username"><a target="_blank" href="' + b + '">' + a + '</a></div><div class="commentTextArea"><textarea class="textarea"></textarea><div class="wordlimit"><span class="wordenter worderror">0</span><span class="wordtotal"> / 300</span></div></div><div class="validate" style="display:none"><input type="text" class="input-maj vcode-input" placeholder="\u9a8c\u8bc1\u7801"><img class="img-code vcode-img"><a href="#" class="btn-change vcode-refresh"><i></i></a></div><div class="comaction"><button class="btn-maj cmt-submit">\u53d1\u8868\u8bc4\u8bba</button></div></div></div></div></div>'
    },
    showNoticeTip: function(a) {
        var b = "",
        b = "",
        c = 0;
        if (0 > a) c = "undefined" == typeof this._noticeInfos[a] ? "-1": a,
        b = this._noticeInfos[c],
        ( - 9 == c || -10 == c) && this.hVerifycode.children().first().addClass("input-error"),
        this.hError.html(b),
        this.hError.show();
        else return c = "undefined" == typeof this._noticeInfos[a] ? "0": a,
        b = '<i class="' + ("0" == c ? "ico-succ": "ico-notice") + '"></i>' + this._noticeInfos[c]
    },
    _setRangePos: function(a) {
        a.setSelectionRange ? (a.focus(), a.setSelectionRange(0, 0)) : a.createTextRange && (a.blur(), a = a.createTextRange(), a.collapse(!0), a.moveEnd("character", 0), a.moveStart("character", 0), a.select())
    },
    _noticeInfos: {
        "0": "\u53d1\u8868\u6210\u529f",
        100 : "\u8bc4\u8bba\u5df2\u63d0\u4ea4\uff0c\u8bf7\u7b49\u5f85\u5ba1\u6838\u901a\u8fc7",
        "-1": "\u8bc4\u8bba\u53d1\u8868\u5931\u8d25",
        "-2": "\u60a8\u5df2\u88ab\u9650\u5236\u53d1\u8868\u8bc4\u8bba\uff0c\u8bf7\u8054\u7cfb\u7f51\u7ad9\u5ba2\u670d",
        "-5": "\u8bf7\u91cd\u65b0\u767b\u5f55",
        "-7": "\u60a8\u7684\u8bc4\u8bba\u542b\u6709\u7f51\u7ad9\u7981\u6b62\u5185\u5bb9\uff0c\u8bf7\u4fee\u6539\uff0c\u8c22\u8c22\uff01",
        "-8": "\u8bc4\u8bba\u5185\u5bb9\u4e0d\u80fd\u4e3a\u7a7a\uff0c\u8bf7\u8f93\u5165\u5185\u5bb9\u3002",
        "-9": "\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801",
        "-10": "\u9a8c\u8bc1\u7801\u8f93\u5165\u9519\u8bef\uff0c\u8bf7\u91cd\u65b0\u8f93\u5165",
        "-11": "\u60a8\u4e0d\u80fd\u8f93\u5165\u592a\u591a\u8bc4\u8bba\u5185\u5bb9\uff0c\u8bf7\u51cf\u5c11\u5185\u5bb9",
        "-12": "\u60a8\u8fd8\u672a\u8d2d\u4e70\u672c\u8282\u76ee\uff0c\u8bf7\u8d2d\u4e70\u89c2\u770b\u540e\u518d\u53d1\u8868\u8bc4\u8bba",
        "-14": "\u5f53\u524d\u89c6\u9891\u88ab\u8bbe\u7f6e\u4e3a\u7981\u6b62\u8bc4\u8bba",
        "-400": "\u60a8\u5df2\u7ecf\u53d1\u8868\u4e86\u8be5\u8bc4\u8bba",
        "-450": "\u60a8\u7684\u8bc4\u8bba\u542b\u6709\u7f51\u7ad9\u7981\u6b62\u5185\u5bb9\uff0c\u8bf7\u4fee\u6539\uff0c\u8c22\u8c22\uff01"
    }
},
xVerifyCode = {
    src: "",
    isRefreshSrc: !1,
    init: function(a, b) {
        var c = this;
        this.hVcode = a;
        this.hVcode.find(".vcode-refresh").on("click",
        function() {
            c.isRefreshSrc = !0;
            c.refresh();
            return ! 1
        });
        this.hVcode.find(".vcode-input").on("click",
        function() {
            "function" == typeof b && b();
            $(event.target).removeClass("input-error")
        })
    },
    isShow: function() {
        var a = this;
        $.getJSON("/QComments/~ajax/isNeedVerify", {},
        function(b) {
            b ? (a.refresh(), a.hVcode.show()) : a.hVcode.hide()
        })
    },
    refresh: function() {
        if (this.isRefreshSrc || "" == this.src) this.src = "/verify/?" + ((new Date).getTime() + "-" + Math.random()),
        this.hVcode.find(".vcode-input").val("");
        var a = this.hVcode.find(".vcode-img"),
        b = a.attr("src") || "";
        "" != this.src && 0 > b.indexOf(this.src) && a.attr("src", this.src)
    }
},
util = {
    novaCall: function(a) {
        var b = document.createElement("script");
        $("head")[0].appendChild(b);
        b.src = a
    },
    genUrl: function(a, b) {
        var a = a + (0 > a.indexOf("?") ? "?": "&"),
        c;
        for (c in b) a += c + "=" + b[c] + "&";
        return a.substr(0, a.length - 1)
    }
};