(function() {
    var W, K;
    function F(a) {
        var b = (new Date).getTime() + "-1772732-" + ++da;
        return a ? a + "-" + b: b
    }
    function G(a) {
        var b = {
            undefined: "undefined",
            number: "number",
            "boolean": "boolean",
            string: "string",
            "[object Function]": "function",
            "[object RegExp]": "regexp",
            "[object Array]": "array",
            "[object Date]": "date",
            "[object Error]": "error"
        };
        return b[typeof a] || b[Object.prototype.toString.call(a)] || (a ? "object": "null")
    }
    function L(a) {
        return "number" === typeof a && isFinite(a)
    }
    function M(a, b, c, d) {
        var e, f, g;
        if (!a || !b) return a || {};
        if (d) for (e = 0, g = d.length; e < g; ++e) f = d[e],
        Object.prototype.hasOwnProperty.call(b, f) && (c || !(f in a)) && (a[f] = b[f]);
        else {
            for (f in b) Object.prototype.hasOwnProperty.call(b, f) && (c || !(f in a)) && (a[f] = b[f]); ({
                valueOf: 0
            }).propertyIsEnumerable("valueOf") || M(a, b, c, "hasOwnProperty,isPrototypeOf,propertyIsEnumerable,toString,toLocaleString,valueOf".split(","))
        }
        return a
    }
    function h(a, b) {
        var c = 2 < arguments.length ? X(arguments, 2) : null;
        return function() {
            var d = "string" === typeof a ? b[a] : a,
            e = c ? X(arguments, 0, !0).concat(c) : arguments;
            return d.apply(b || d, e)
        }
    }
    function X(a, b) {
        var c, d;
        b || (b = 0);
        try {
            return Array.prototype.slice.call(a, b)
        } catch(e) {
            d = [];
            for (c = a.length; b < c; ++b) d.push(a[b]);
            return d
        }
    }
    function B(a) {
        var b = document.createElement("div");
        b.innerHTML = a;
        a = b.childNodes;
        return a[0].parentNode.removeChild(a[0])
    }
    function s(a) {
        return a.toString().replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, "")
    }
    function N(a) {
        return a.length
    }
    function H(a, b) {
        for (var c = a.split(""), d = 0, e = "", f = 0; f < c.length; f++) {
            d += /[^\x00-\xff]/g.test(c[f]) ? 2 : 1;
            if (d > b) break;
            e += c[f]
        }
        return e
    }
    function w(a) {
        return (a + "").replace(/[&<>"'\/`]/g,
        function(a) {
            return ea[a]
        })
    }
    function p(a, b, c, d) {
        for (var e, f, g, m, j, h = [], z, Y = a.length;;) {
            e = a.lastIndexOf(O, Y);
            if (0 > e) break;
            f = a.indexOf(P, e);
            if (e + 1 >= f) break;
            m = z = a.substring(e + 1, f);
            j = null;
            g = m.indexOf(ga); - 1 < g && (j = m.substring(g + 1), m = m.substring(0, g));
            g = b[m];
            c && (g = c(m, g, j));
            "undefined" === typeof g && (g = "~-" + h.length + "-~", h.push(z));
            a = a.substring(0, e) + g + a.substring(f + 1);
            d || (Y = e - 1)
        }
        return a.replace(ha,
        function(a, b, c) {
            return O + h[parseInt(c, 10)] + P
        }).replace(ia, O).replace(ja, P)
    }
    function u(a) {
        if (a) url = "http://hz.youku.com/red/click.php?tp=1&cp=" + a + "&cpp=1000658&" + (new Date).getTime(),
        a = new Image(1, 1),
        a.src = url,
        a.onload = function() {}
    }
    function I(a, b, c) {
        var d = [],
        e = "&",
        f = function(a, c) {
            var e = b ? /\[\]$/.test(b) ? b: b + "[" + c + "]": c;
            "undefined" != e && "undefined" != c && d.push("object" === typeof a ? I(a, e, !0) : "[object Function]" === Object.prototype.toString.call(a) ? encodeURIComponent(e) + "=" + encodeURIComponent(a()) : encodeURIComponent(e) + "=" + encodeURIComponent(a))
        };
        if (!c && b) e = /\?/.test(b) ? /\?$/.test(b) ? "": "&": "?",
        d.push(b),
        d.push(I(a));
        else if ("[object Array]" === Object.prototype.toString.call(a) && "undefined" != typeof a) for (var g = 0,
        c = a.length; g < c; ++g) f(a[g], g);
        else if ("undefined" != typeof a && null !== a && "object" === typeof a) for (g in a) f(a[g], g);
        else d.push(encodeURIComponent(b) + "=" + encodeURIComponent(a));
        return d.join(e).replace(/^&/, "").replace(/%20/g, "+")
    }
    function o(a, b) {
        C(a, b) || (a.className += " " + b)
    }
    function C(a, b) {
        return RegExp("(^| )" + b + "( |$)").test(a.className)
    }
    function r(a, b) {
        a.className = a.className.replace(RegExp("(^| )" + b + "( |$)"), " ").replace(/^\s+|\s+$/g, "")
    }
    function y(a, b) {
        if (!s(b) || !a) return [];
        if (a.querySelectorAll) return a.querySelectorAll("." + b);
        for (var c = [], d = a.getElementsByTagName("*"), e = d.length, f = 0; f < e; f++) C(d[f], b) && c.push(d[f]);
        return c
    }
    function i(a, b, c) {
        a.addEventListener ? a.addEventListener(b, c, !1) : a.attachEvent ? a.attachEvent("on" + b, c) : a["on" + b] = c
    }
    function R(a, b, c) {
        a.removeEventListener ? a.removeEventListener(b, c, !1) : a.detachEvent ? a.detachEvent("on" + b, c) : a["on" + b] = null
    }
    function $() {
        M(this.constructor.prototype, {
            publish: function(a) {
                this._evts[a] || (this._evts[a] = null)
            },
            on: function(a, b, c) {
                var d = this._evts;
                d[a] = {};
                d[a].type = a;
                this.name && (d[a].type = this.name + ":" + a);
                d[a].fn = function() {
                    b.apply(c, arguments)
                }
            },
            after: function(a, b, c) {
                this.on(a, b, c)
            },
            fire: function(a) {
                var b = this._evts[a];
                if (b) {
                    var c = {
                        target: this,
                        type: b.type
                    },
                    d = Array.prototype.slice.call(arguments, 1),
                    e = d[0],
                    f = typeof e;
                    if (e && ("object" === f || "function" === f || "function" === G(e))) for (var g in c) d[0][g] ? d[0]["_" + g] = c[g] : d[0][g] = c[g];
                    else d[0] = c;
                    "function" === G(b.fn) && b.fn.apply(this, d)
                }
            },
            detach: function(a) {
                delete this._evts[a]
            }
        },
        !1);
        this._evts = {}
    }
    function v(a) {
        $.call(this);
        this._isApplySuperClass || M(this.constructor.prototype, v.prototype, !1);
        if (a) for (var b in a) this.set(b, a[b]);
        "function" === G(this.initializer) && this.initializer.apply(this, arguments)
    }
    function k(a, b, c) {
        $.call(this);
        var d = this._id = F("uploader-swf"),
        c = c || {},
        e = ((c.version || ka) + "").split("."),
        e = k.isFlashVersionAtLeast(parseInt(e[0], 10), parseInt(e[1], 10), parseInt(e[2], 10)),
        f = k.isFlashVersionAtLeast(8, 0, 0) && !e && c.useExpressInstall,
        g = f ? la: b,
        b = "<object ",
        m = "&SWFId=" + d + "&callback=" + ma + "&allowedDomain=" + document.location.hostname;
        k._instances[d] = this;
        if (a && (e || f) && g) {
            b += 'id="' + d + '" ';
            b = n.ie ? b + ('classid="' + na + '" ') : b + ('type="' + oa + '" data="' + w(g) + '" ');
            b += 'width="100%" height="100%">';
            n.ie && (b += '<param name="movie" value="' + w(g) + '"/>');
            for (var j in c.fixedAttributes) pa.hasOwnProperty(j) && (b += '<param name="' + w(j) + '" value="' + w(c.fixedAttributes[j]) + '"/>');
            for (var h in c.flashVars) j = c.flashVars[h],
            "string" === typeof j && (m += "&" + w(h) + "=" + w(encodeURIComponent(j)));
            m && (b += '<param name="flashVars" value="' + m + '"/>');
            a.innerHTML = b + "</object>";
            this.swf = document.getElementById(d)
        } else this.publish("wrongflashversion", {
            fireOnce: !0
        }),
        this.fire("wrongflashversion", {
            type: "wrongflashversion"
        })
    }
    function S(a) {
        this.swfContainerId = F("uploader");
        this.queue = this.swfReference = null;
        this.buttonState = "up";
        this.config = {
            enabled: !0,
            multipleFiles: !0,
            appendNewFiles: !0,
            fileFilterFunction: null,
            buttonClassNames: {
                hover: "uploader-button-hover",
                active: "uploader-button-active",
                disabled: "uploader-button-disabled",
                focus: "uploader-button-selected"
            },
            containerClassNames: {
                hover: "uphotBg"
            },
            fileFilters: W,
            fileFieldName: "FileData",
            simLimit: 1,
            retryCount: 3,
            postVarsPerFile: {},
            selectButtonLabel: "\u9009\u62e9\u6587\u4ef6",
            swfURL: "/v/swf/FlashUploader.swf",
            uploadURL: ""
        };
        v.apply(this, arguments)
    }
    function T(a) {
        this.buttonBinding = this.queue = this.fileInputField = null;
        this.config = {
            enabled: !0,
            multipleFiles: !0,
            appendNewFiles: !0,
            fileFilterFunction: null,
            dragAndDropArea: document,
            buttonClassNames: {
                hover: "uploader-button-hover",
                active: "uploader-button-active",
                disabled: "uploader-button-disabled",
                focus: "uploader-button-selected"
            },
            fileFilters: K,
            fileFieldName: "FileData",
            simLimit: 1,
            retryCount: 3,
            postVarsPerFile: {},
            selectButtonLabel: "\u9009\u62e9\u6587\u4ef6",
            uploadURL: ""
        };
        v.apply(this, arguments)
    }
    function D(a) {
        this.bytesSpeed = this.bytesPrevLoaded = 0;
        this.bytesSpeeds = [];
        this.preTime = this.remainTime = 0;
        this.config = {
            id: "",
            name: "",
            size: "",
            type: "",
            dateCreated: "",
            dateModified: "",
            uploader: ""
        };
        v.apply(this, arguments)
    }
    function x() {
        this.uploadInfo = {};
        this.recommTags = [];
        this.config = {
            enabled: !0,
            multipleFiles: !1,
            appendNewFiles: !1,
            fileFilterFunction: null,
            buttonClassNames: {
                hover: "uploader-button-hover",
                active: "uploader-button-active",
                disabled: "uploader-button-disabled",
                focus: "uploader-button-selected"
            },
            fileFieldName: "FileData",
            simLimit: 1,
            retryCount: 3,
            prefix: "upload-body-",
            postVarsPerFile: {},
            selectButtonLabel: "\u9009\u62e9\u6587\u4ef6",
            swfURL: "/v/swf/FlashUploader.swf",
            uploadURL: ""
        };
        v.apply(this, arguments)
    }
    function aa() {
        this.options = {
            Lay: null,
            Color: "#000",
            Opacity: 50,
            zIndex: 1900
        };
        this.Lay = document.body.insertBefore(document.createElement("div"), document.body.childNodes[0]);
        this.Color = this.options.Color;
        this.Opacity = parseInt(this.options.Opacity);
        this.zIndex = parseInt(this.options.zIndex);
        with(this.Lay.style) display = "none",
        zIndex = this.zIndex,
        left = top = 0,
        position = "fixed",
        width = height = "100%";
        if (6 == n.ie) this.Lay.style.position = "absolute",
        this._resize = h(function() {
            this.Lay.style.width = Math.max(document.documentElement.scrollWidth, document.documentElement.clientWidth) + "px";
            this.Lay.style.height = Math.max(document.documentElement.scrollHeight, document.documentElement.clientHeight) + "px"
        },
        this),
        this.Lay.innerHTML = '<iframe style="position:absolute;top:0;left:0;width:100%;height:100%;filter:alpha(opacity=0);"></iframe>'
    }
    var da = 0,
    ga = " ",
    O = "{",
    P = "}",
    ha = /(~-(\d+)-~)/g,
    ia = /\{LBRACE\}/g,
    ja = /\{RBRACE\}/g,
    ea = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#x27;",
        "/": "&#x2F;",
        "`": "&#x60;"
    },
    qa = Array.isArray && /\{\s*\[(?:native code|function)\]\s*\}/i.test(Array.isArray) ? Array.isArray: function(a) {
        return "array" === G(a)
    };
    v.prototype = {
        _isApplySuperClass: !0,
        initializer: function() {},
        get: function(a) {
            return this.config[a]
        },
        set: function(a, b) {
            var c;
            a && "undefined" !== typeof b && a in this.config && (this.config[a] = b, c = a + "Change", this._evt && c in this._evt.events && this.fire(c))
        }
    };
    var n = function(a) {
        var b = function(a) {
            var b = 0;
            return parseFloat(a.replace(/\./g,
            function() {
                return 1 == b++?"": "."
            }))
        },
        c = window,
        d = c && c.navigator,
        e = {
            ie: 0,
            opera: 0,
            gecko: 0,
            webkit: 0,
            safari: 0,
            chrome: 0,
            mobile: null,
            air: 0,
            phantomjs: 0,
            air: 0,
            ipad: 0,
            iphone: 0,
            ipod: 0,
            ios: null,
            android: 0,
            silk: 0,
            accel: !1,
            webos: 0,
            caja: d && d.cajaVersion,
            secure: !1,
            os: null,
            nodejs: 0
        },
        a = a || d && d.userAgent,
        d = (c = c && c.location) && c.href,
        c = 0,
        f,
        g,
        m;
        e.userAgent = a;
        e.secure = d && 0 === d.toLowerCase().indexOf("https");
        if (a) {
            if (/windows|win32/i.test(a)) e.os = "windows";
            else if (/macintosh|mac_powerpc/i.test(a)) e.os = "macintosh";
            else if (/android/i.test(a)) e.os = "android";
            else if (/symbos/i.test(a)) e.os = "symbos";
            else if (/linux/i.test(a)) e.os = "linux";
            else if (/rhino/i.test(a)) e.os = "rhino";
            if (/KHTML/.test(a)) e.webkit = 1;
            if (/IEMobile|XBLWP7/.test(a)) e.mobile = "windows";
            if (/Fennec/.test(a)) e.mobile = "gecko";
            if ((d = a.match(/AppleWebKit\/([^\s]*)/)) && d[1]) {
                e.webkit = b(d[1]);
                e.safari = e.webkit;
                if (/PhantomJS/.test(a) && (d = a.match(/PhantomJS\/([^\s]*)/)) && d[1]) e.phantomjs = b(d[1]);
                if (/ Mobile\//.test(a) || /iPad|iPod|iPhone/.test(a)) {
                    if (e.mobile = "Apple", (d = a.match(/OS ([^\s]*)/)) && d[1] && (d = b(d[1].replace("_", "."))), e.ios = d, e.os = "ios", e.ipad = e.ipod = e.iphone = 0, (d = a.match(/iPad|iPod|iPhone/)) && d[0]) e[d[0].toLowerCase()] = e.ios
                } else {
                    if (d = a.match(/NokiaN[^\/]*|webOS\/\d\.\d/)) e.mobile = d[0];
                    if (/webOS/.test(a) && (e.mobile = "WebOS", (d = a.match(/webOS\/([^\s]*);/)) && d[1])) e.webos = b(d[1]);
                    if (/ Android/.test(a)) {
                        if (/Mobile/.test(a)) e.mobile = "Android";
                        if ((d = a.match(/Android ([^\s]*);/)) && d[1]) e.android = b(d[1])
                    }
                    if (/Silk/.test(a)) {
                        if ((d = a.match(/Silk\/([^\s]*)\)/)) && d[1]) e.silk = b(d[1]);
                        if (!e.android) e.android = 2.34,
                        e.os = "Android";
                        if (/Accelerated=true/.test(a)) e.accel = !0
                    }
                }
                if ((d = a.match(/(Chrome|CrMo|CriOS)\/([^\s]*)/)) && d[1] && d[2]) {
                    if (e.chrome = b(d[2]), e.safari = 0, "CrMo" === d[1]) e.mobile = "chrome"
                } else if (d = a.match(/AdobeAIR\/([^\s]*)/)) e.air = d[0]
            }
            if (!e.webkit) if (/Opera/.test(a)) {
                if ((d = a.match(/Opera[\s\/]([^\s]*)/)) && d[1]) e.opera = b(d[1]);
                if ((d = a.match(/Version\/([^\s]*)/)) && d[1]) e.opera = b(d[1]);
                if (/Opera Mobi/.test(a) && (e.mobile = "opera", (d = a.replace("Opera Mobi", "").match(/Opera ([^\s]*)/)) && d[1])) e.opera = b(d[1]);
                if (d = a.match(/Opera Mini[^;]*/)) e.mobile = d[0]
            } else if ((d = a.match(/MSIE\s([^;]*)/)) && d[1]) e.ie = b(d[1]);
            else if (d = a.match(/Gecko\/([^\s]*)/)) if (e.gecko = 1, (d = a.match(/rv:([^\s\)]*)/)) && d[1]) e.gecko = b(d[1])
        }
        if (e.gecko || e.webkit || e.opera) {
            if (b = navigator.mimeTypes["application/x-shockwave-flash"]) if (b = b.enabledPlugin) f = b.description.replace(/\s[rd]/g, ".").replace(/[A-Za-z\s]+/g, "").split(".")
        } else if (e.ie) {
            try {
                g = new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6"),
                g.AllowScriptAccess = "always"
            } catch(j) {
                null !== g && (c = 6)
            }
            if (0 === c) try {
                m = new ActiveXObject("ShockwaveFlash.ShockwaveFlash"),
                f = m.GetVariable("$version").replace(/[A-Za-z\s]+/g, "").split(",")
            } catch(h) {}
        }
        if (qa(f)) {
            if (L(parseInt(f[0], 10))) e.flashMajor = f[0];
            if (L(parseInt(f[1], 10))) e.flashMinor = f[1];
            if (L(parseInt(f[2], 10))) e.flashRev = f[2]
        }
        return e
    } (),
    na = "clsid:d27cdb6e-ae6d-11cf-96b8-444553540000",
    oa = "application/x-shockwave-flash",
    ka = "10.0.22",
    la = "http://fpdownload.macromedia.com/pub/flashplayer/update/current/swf/autoUpdater.swf?" + Math.random(),
    ma = "SWF.eventHandler",
    pa = {
        align: "",
        allowFullScreen: "",
        allowNetworking: "",
        allowScriptAccess: "",
        base: "",
        bgcolor: "",
        loop: "",
        menu: "",
        name: "",
        play: "",
        quality: "",
        salign: "",
        scale: "",
        tabindex: "",
        wmode: ""
    };
    k.getFlashVersion = function() {
        return "" + n.flashMajor + "." + ("" + n.flashMinor) + "." + ("" + n.flashRev)
    };
    k.isFlashVersionAtLeast = function(a, b, c) {
        var d = parseInt(n.flashMajor, 10),
        e = parseInt(n.flashMinor, 10),
        f = parseInt(n.flashRev, 10),
        a = parseInt(a || 0, 10),
        b = parseInt(b || 0, 10),
        c = parseInt(c || 0, 10);
        return a === d ? b === e ? c <= f: b < e: a < d
    };
    k._instances = k._instances || {};
    k.eventHandler = function(a, b) {
        k._instances[a]._eventHandler(b)
    };
    k.prototype = {
        initializer: function() {},
        _eventHandler: function(a) {
            "swfReady" === a.type ? (this.publish("swfReady", {
                fireOnce: !0
            }), this.fire("swfReady", a)) : "log" !== a.type && this.fire(a.type, a)
        },
        callSWF: function(a, b) {
            b || (b = []);
            return this.swf[a] ? this.swf[a].apply(this.swf, b) : null
        },
        toString: function() {
            return "SWF " + this._id
        }
    };
    k.prototype.constructor = k; (function() {
        var a = function(a, b) {
            for (var c in b) a[c] = b[c]
        },
        b = function(a, b) {
            return function() {
                return b.apply(a, arguments)
            }
        },
        c = function(a, b, c) {
            a.addEventListener ? a.addEventListener(b, c, !1) : a.attachEvent ? a.attachEvent("on" + b, c) : a["on" + b] = c
        },
        d = function() {
            var a = document.createElement("div");
            return function(b) {
                a.innerHTML = b;
                b = a.firstChild;
                a.removeChild(b);
                return b
            }
        } (),
        e = function(a, b) {
            if (a.querySelectorAll) return a.querySelectorAll("." + b);
            for (var c = [], d = a.getElementsByTagName("*"), e = d.length, f = 0; f < e; f++) RegExp("(^| )" + b + "( |$)").test(d[f].className) && c.push(d[f]);
            return c
        },
        f = function() {
            var a = 9999;
            return function() {
                return a++
            }
        } (),
        g = function(d) {
            this._options = {
                button: null,
                action: "http://www.youku.com/QUpload/~ajax/listFolder",
                params: {
                    ps: 10,
                    pl: 1
                },
                albumData: null,
                onSubmit: function() {},
                onCancel: function() {},
                onClose: function() {},
                onShow: function() {}
            };
            a(this._options, d);
            this.data = {
                pageNumber: 1,
                totalPage: 1,
                albumData: []
            };
            this.panel = null;
            if (this._options.albumData) this.data.albumData = this._options.albumData;
            this.button = this._options.button;
            this.init();
            this.button && c(this.button, "click", b(this,
            function() {
                this.show()
            }))
        };
        a(g.prototype, {
            init: function() {
                var a = this.getTemplate();
                this.panel = d(a);
                this.pager = e(this.panel, "pages")[0];
                this.qPager = e(this.panel, "qPager")[0];
                this.listAll = e(this.panel, "list-all")[0];
                this.listSelected = e(this.panel, "list-selected")[0];
                this.submitBtn = e(this.panel, "submit-btn")[0];
                this.cancelBtn = e(this.panel, "cancel-btn")[0];
                this.closeBtn = e(this.panel, "close")[0];
                this.selectAllBtn = e(this.panel, "all-btn")[0];
                this.selectedBtn = e(this.panel, "selected-btn")[0];
                this.preBtn = e(this.panel, "pre")[0];
                this.nextBtn = e(this.panel, "next")[0];
                this.layer = new h;
                this.panel.style.zIndex = this.layer.zIndex + 1;
                this.panel.style.display = "none";
                document.body.appendChild(this.panel);
                this.bindStaticEvent()
            },
            show: function(a) {
                this.getData(a ? a: this._options.params, b(this, this.render))
            },
            render: function(a) {
                var d = parseInt(a.pageNo) || 1,
                e = parseInt(a.totalPage) || 0,
                a = a.items || [];
                this.data.pageNumber = d;
                this.data.totalPage = e;
                this.renderPager(d, e);
                this.renderAlbumList(a);
                this.preBtn.innerHTML = 1 == d ? '<span><em class="ico_pre"></em>\u4e0a\u4e00\u9875</span>': '<a href="#" class="pre-btn"><em class="ico_pre"></em>\u4e0a\u4e00\u9875</a>';
                this.nextBtn.innerHTML = 0 != e && d != e ? '<a href="#" class="next-btn"><em class="ico_next"></em>\u4e0b\u4e00\u9875</a>': '<span><em class="ico_next"></em>\u4e0b\u4e00\u9875</span>';
                this.bindDynamicEvent();
                if (j) this.panel.style.marginTop = document.documentElement.scrollTop - 280 + "px",
                this.panel.style.marginLeft = document.documentElement.scrollLeft - 325 + "px",
                c(window, "scroll", b(this,
                function() {
                    this.panel.style.marginTop = document.documentElement.scrollTop - this.panel.offsetHeight / 2 + "px";
                    this.panel.style.marginLeft = document.documentElement.scrollLeft - this.panel.offsetWidth / 2 + "px"
                }));
                if ("block" != this.panel.style.display) this.layer.show(),
                this.panel.style.display = "block"
            },
            bindStaticEvent: function() {
                c(this.selectAllBtn, "click", b(this,
                function(a) {
                    if ("current" != (a.target || a.srcElement).className) {
                        for (var a = e(this.listAll, "album-ck"), b = 0; b < a.length; b++) a[b].checked = !1;
                        this.selectedBtn.className = "";
                        this.listSelected.style.display = "none";
                        this.selectAllBtn.className = "current";
                        this.listAll.style.display = "block";
                        this.qPager.style.display = "block"
                    }
                }));
                c(this.selectedBtn, "click", b(this,
                function(a) {
                    if ("current" != (a.target || a.srcElement).className) this.selectAllBtn.className = "",
                    this.listAll.style.display = "none",
                    this.qPager.style.display = "none",
                    this.renderSelectedPanel(),
                    this.selectedBtn.className = "current",
                    this.listSelected.style.display = "block"
                }));
                c(this.submitBtn, "click", b(this, this.onSubmit));
                c(this.cancelBtn, "click", b(this, this.onCancel));
                c(this.closeBtn, "click", b(this, this.close))
            },
            bindDynamicEvent: function() {
                for (var a = e(this.listAll, "album-ck"), d = 0; d < a.length; d++) c(a[d], "click", b(this,
                function(a) {
                    var b = a.target || a.srcElement,
                    a = {},
                    c = !1;
                    if (b.checked) if (a.folderId = b.value, a.folderName = b.title, 10 > this.data.albumData.length) {
                        for (b = 0; b < this.data.albumData.length; b++) if (this.data.albumData[b].folderId == a.folderId) {
                            c = !0;
                            break
                        }
                        c || this.data.albumData.push(a)
                    } else b.checked = !1,
                    alert("\u6700\u591a\u53ef\u900910\u4e2a\u4e13\u8f91")
                }));
                a = this.pager.getElementsByTagName("a");
                for (d = 0; d < a.length; d++) c(a[d], "click", b(this,
                function(a) {
                    var b = (a.target || a.srcElement).id;
                    a.preventDefault ? a.preventDefault() : a.returnValue = !1;
                    this.show({
                        ps: 10,
                        pl: b
                    })
                })); (a = e(this.qPager, "pre-btn")[0]) && c(a, "click", b(this,
                function() {
                    var a = this.data.pageNumber - 1;
                    0 < a && this.show({
                        ps: 10,
                        pl: a
                    })
                })); (a = e(this.qPager, "next-btn")[0]) && c(a, "click", b(this,
                function() {
                    var a = this.data.pageNumber + 1;
                    0 < a && this.show({
                        ps: 10,
                        pl: a
                    })
                }))
            },
            renderSelectedPanel: function() {
                var a = this.data.albumData,
                d = "<ul>";
                if (0 < a.length) for (var f = 0; f < a.length; f++) d += '<li class="' + (1 === f % 2 ? "even": "odd") + '"><div><input type="checkbox" checked="true" class="album-ck" value="',
                d += a[f].folderId + '" title="' + a[f].folderName + '"></div><span>',
                d += a[f].folderName + "</span></li>";
                this.listSelected.innerHTML = d + "</ul>";
                a = e(this.listSelected, "album-ck");
                for (f = 0; f < a.length; f++) c(a[f], "click", b(this,
                function(a) {
                    var a = a.target || a.srcElement,
                    b = a.parentNode;
                    if (a && !a.checked) {
                        for (var c = 0; c < this.data.albumData.length; c++) this.data.albumData[c].folderId == a.value && this.data.albumData.splice(c, 1);
                        for (; b;) {
                            if ("li" === b.tagName.toLowerCase()) {
                                b.parentNode.removeChild(b);
                                break
                            }
                            b = b.parentNode
                        }
                    }
                }))
            },
            renderPager: function(a, b) {
                function c(a, b) {
                    var d = "";
                    a <= b && (d = '<li><a href="javascript:void(0)" id="' + a + '">' + a + "</a></li>");
                    return d
                }
                var d = "";
                if (10 > b) for (var e = 1; e < b + 1; e++) d = a == e ? d + ('<li class="current"><span>' + e + "</span></li>") : d + ('<li><a href="javascript:void(0)" id="' + e + '">' + e + "</a></li>");
                else if (5 < a) d = d + '<li><a href="javascript:void(0)" id="1">1</a></li><li class="pass">...</li>' + c(a - 2, b),
                d += c(a - 1, b),
                d = d + ('<li class="current"><span>' + a + "</span></li>") + c(a + 1, b),
                d += c(a + 2, b),
                b > a + 2 && (b > a + 3 && (d += '<li class="pass">...</li>'), d += '<li><a href="javascript:void(0)" id="' + b + '">' + b + "</a></li>");
                else {
                    for (e = 1; 10 > e; e++) d = a == e ? d + ('<li class="current"><span>' + e + "</span></li>") : d + ('<li><a href="javascript:void(0)" id="' + e + '">' + e + "</a></li>");
                    d += '<li class="pass">...</li><li"><a href="javascript:void(0)" id="' + b + '">' + b + "</a></li>"
                }
                this.pager.innerHTML = d
            },
            renderAlbumList: function(a) {
                var b = "<ul>";
                if (a && 0 < a.length) for (var c = 0; c < a.length; c++) b += '<li class="' + (1 === c % 2 ? "even": "odd") + '"><div><input type="checkbox" class="album-ck" value="',
                b += a[c].folderId + '" title="' + a[c].folderName + '"></div><span>',
                b += a[c].folderName + "</span></li>";
                this.listAll.innerHTML = b + "</ul>"
            },
            getTemplate: function() {
                var a;
                return '<div class="popwin" ><div class="listEditBox"><div class="tab"><div class="menus"><ul><li class="current all-btn">\u5168\u90e8</li><li class="selected-btn">\u5df2\u9009</li></ul></div><div class="close"></div></div><div class="line_dot"></div><div class="list"><div class="list-all"></div><div class="list-selected" style="display:none"></div></div><div class="pager"><div class="action"><div class="form_btn form_btn_m form_btnmaj_m"><span class="form_btn_text submit-btn" style="width:60px;">\u786e\u5b9a</span></div><div class="form_btn form_btn_m form_btnsub_m"><span class="form_btn_text cancel-btn" style="width:60px;">\u53d6\u6d88</span></div></div><div class="qPager"><ul class="turn"><li class="pre" title="\u4e0a\u4e00\u9875"><a><em class="ico_pre"></em>\u4e0a\u4e00\u9875</a></li><li class="next" title="\u4e0b\u4e00\u9875"><a href="#" class="next-btn"><em class="ico_next"></em>\u4e0b\u4e00\u9875</a></li></ul><ul class="pages"></ul></div></div></div><div class="bg"></div></div>'
            },
            getData: function(a, b) {
                new Ajax.Request(this._options.action, {
                    method: "post",
                    onComplete: function(a) {
                        a = eval("(" + a.responseText + ")");
                        b(a)
                    },
                    parameters: a
                })
            },
            setAlbumData: function(a) {
                this.data.albumData = a
            },
            getAlbumData: function() {
                return this.data.albumData || []
            },
            onSubmit: function() {
                this._options.onSubmit(this.getAlbumData());
                this.close()
            },
            onCancel: function() {
                this._options.onCancel();
                this.close()
            },
            close: function() {
                this._options.onClose();
                this.panel.style.display = "none";
                this.layer.close()
            }
        });
        var m = document.all ? !0 : !1,
        j = m && 6 == /MSIE (\d)\.0/i.exec(navigator.userAgent)[1],
        h = function(c) {
            this.options = {
                Lay: null,
                Color: "#000",
                Opacity: 50,
                zIndex: f()
            };
            a(this.options, c);
            this.Lay = document.body.insertBefore(document.createElement("div"), document.body.childNodes[0]);
            this.Color = this.options.Color;
            this.Opacity = parseInt(this.options.Opacity);
            this.zIndex = parseInt(this.options.zIndex);
            with(this.Lay.style) display = "none",
            zIndex = this.zIndex,
            left = top = 0,
            position = "fixed",
            width = height = "100%";
            if (j) this.Lay.style.position = "absolute",
            this._resize = b(this,
            function() {
                this.Lay.style.width = Math.max(document.documentElement.scrollWidth, document.documentElement.clientWidth) + "px";
                this.Lay.style.height = Math.max(document.documentElement.scrollHeight, document.documentElement.clientHeight) + "px"
            }),
            this.Lay.innerHTML = '<iframe style="position:absolute;top:0;left:0;width:100%;height:100%;filter:alpha(opacity=0);"></iframe>'
        };
        a(h.prototype, {
            show: function() {
                j && (this._resize(), window.attachEvent("onresize", this._resize));
                with(this.Lay.style) m ? filter = "alpha(opacity:" + this.Opacity + ")": opacity = this.Opacity / 100,
                backgroundColor = this.Color,
                display = "block"
            },
            close: function() {
                this.Lay.style.display = "none";
                j && window.detachEvent("onresize", this._resize)
            }
        });
        window.AlbumSelector = g
    })();
    W = [];
    K = [];
    var ba = {
        "-300": {
            field: "title",
            info: "\u6807\u9898\u4e0d\u53ef\u4ee5\u4e3a\u7a7a"
        },
        "-301": {
            field: "title",
            info: "\u6807\u9898\u6700\u591a\u5141\u8bb880\u4e2a\u5b57"
        },
        "-303": {
            field: "title",
            info: "\u6807\u9898\u542b\u6709\u7981\u5fcc\u8bcd\u6c47"
        },
        "-310": {
            field: "description",
            info: "\u89c6\u9891\u7b80\u4ecb\u6700\u591a2000\u4e2a\u5b57"
        },
        "-311": {
            field: "description",
            info: "\u89c6\u9891\u7b80\u4ecb\u542b\u6709\u7981\u5fcc\u8bcd\u6c47"
        },
        "-320": {
            field: "tags",
            info: "\u6807\u7b7e\u4e0d\u53ef\u4ee5\u4e3a\u7a7a"
        },
        "-321": {
            field: "tags",
            info: "\u6700\u591a\u53ef\u4ee5\u6dfb\u52a010\u4e2a\u89c6\u9891\u6807\u7b7e"
        },
        "-322": {
            field: "tags",
            info: "\u5355\u4e2a\u6807\u7b7e\u6700\u591a20\u4e2a\u5b57"
        },
        "-323": {
            field: "tags",
            info: "\u5355\u4e2a\u6807\u7b7e\u6700\u5c111\u4e2a\u5b57"
        },
        "-324": {
            field: "tags",
            info: "\u6807\u7b7e\u542b\u6709\u7981\u5fcc\u8bcd\u6c47"
        },
        "-325": {
            field: "tags",
            info: "\u6807\u7b7e\u542b\u6709\u65e0\u6548\u5b57\u7b26"
        },
        "-334": {
            field: "category_id",
            info: "\u5206\u7c7b\u4e0d\u53ef\u4ee5\u4e3a\u7a7a"
        },
        "-340": {
            field: "password",
            info: "\u5bc6\u7801\u4e0d\u80fd\u4e3a\u7a7a"
        },
        "-341": {
            field: "password",
            info: "\u5bc6\u7801\u6700\u591a32\u4e2a\u5b57\u7b26"
        },
        "-342": {
            field: "password",
            info: "\u89c2\u770b\u5bc6\u7801\u5fc5\u987b\u5b57\u6bcd\u6570\u5b57\u7ec4\u6210\uff0c\u6700\u591a32\u4f4d"
        },
        "-360": {
            field: "password",
            info: "\u4fdd\u5b58\u5bc6\u7801\u5931\u8d25"
        },
        "-361": {
            field: "tags",
            info: "\u4fdd\u5b58\u6807\u7b7e\u5931\u8d25"
        },
        "-371": {
            field: "original",
            info: "\u8bf7\u9009\u62e9\u7248\u6743\u7c7b\u522b"
        },
        "-372": {
            field: "privacy",
            info: "\u8bf7\u9009\u62e9\u9690\u79c1\u7c7b\u522b"
        },
        "-374": {
            field: "category_id",
            info: "\u8bf7\u9009\u62e9\u4e00\u4e2a\u5206\u7c7b"
        }
    },
    ca = "\u4f7f\u7528\u8c37\u6b4c\u548c\u706b\u72d0\u6d4f\u89c8\u5668\u4e0a\u4f20\u89c6\u9891\u53ef\u4ee5\u5728\u4e00\u5468\u5185\u65ad\u70b9\u7eed\u4f20,\u4f7f\u7528\u8c37\u6b4c\u6216\u706b\u72d0\u7b49\u6d4f\u89c8\u5668\uff0c\u5c06\u89c6\u9891\u6587\u4ef6\u76f4\u63a5\u62d6\u62fd\u5230\u9875\u9762\u5185\u5c31\u53ef\u4ee5\u5f00\u59cb\u4e0a\u4f20\u7684\u54e6~,\u4f7f\u7528IE8\u6216\u66f4\u9ad8\u7248\u672c\u7684\u6d4f\u89c8\u5668\u4e0a\u4f20\u89c6\u9891\uff0c\u5c06\u4f1a\u66f4\u52a0\u5feb\u901f\u7a33\u5b9a~,\u4f7f\u7528\u8c37\u6b4c\u6216\u706b\u72d0\u7b49\u652f\u6301html5\u4e0a\u4f20\u7684\u6d4f\u89c8\u5668\uff0c\u4e0a\u4f20\u5355\u4e2a\u89c6\u9891\u7684\u6700\u5927\u5bb9\u91cf\u652f\u6301\u52302G\uff01,\u4e0a\u4f20\u4e2d\u65ad\u65f6\uff0c\u82e5\u4f7f\u7528\u7684\u662f\u8c37\u6b4c\u6216\u706b\u72d0\u7b49\u652f\u6301html5\u4e0a\u4f20\u7684\u6d4f\u89c8\u5668\uff0c\u518d\u6b21\u9009\u62e9\u540c\u4e00\u6587\u4ef6\u662f\u53ef\u4ee5\u4ece\u4e2d\u65ad\u5904\u7ee7\u7eed\u4f20\u7684~,\u4f7f\u7528\u4f18\u9177\u5ba2\u6237\u7aef\uff0c\u4e0d\u4f46\u652f\u6301\u6279\u91cf\u4e0a\u4f20\uff0c\u800c\u4e14\u5355\u4e2a\u89c6\u9891\u7684\u5bb9\u91cf\u6700\u5927\u652f\u630110G\uff01,\u4e0a\u4f20\u539f\u521b\u89c6\u9891\uff0c\u52a0\u5165\u4f18\u9177\u5206\u4eab\u8ba1\u5212\uff0c\u53ef\u4ee5\u83b7\u5f97\u5206\u6210\u6536\u76ca\u54e6~<a href='http://hz.youku.com/red/click.php?tp=1&cp=4008719&cpp=1000658&url=http://share.youku.com'  target='_blank'>\u67e5\u770b\u8be6\u60c5>></a>,\u5728\u81ea\u5df1\u7684\u7f51\u7ad9\u4e0a\uff0c\u901a\u8fc7\u4f18\u9177\u5f00\u653e\u5e73\u53f0\u5f15\u7528\u89c6\u9891\uff0c\u53ef\u4ee5\u4e3a\u89c6\u9891\u64ad\u653e\u63d0\u4f9b\u514d\u5e7f\u544a\u670d\u52a1~<a href='http://hz.youku.com/red/click.php?tp=1&cp=4008762&cpp=1000658&url=http://open.youku.com/services/info?serid=1' target='_blank'>\u67e5\u770b\u8be6\u60c5>></a>,\u4f7f\u7528iDo\u53ef\u4ee5\u8f7b\u677e\u526a\u8f91\u3001\u7f8e\u5316\u89c6\u9891\u3001\u5236\u4f5c\u56fe\u7247MV\uff0c\u4e3b\u9898\u3001\u6ee4\u955c\u3001\u80cc\u666f\u97f3\u4e50\u968f\u5fc3\u914d\uff0c\u8ba9\u4f60\u7684\u89c6\u9891\u66f4\u7cbe\u5f69\uff01<a href='http://hz.youku.com/red/click.php?tp=1&cp=4009595&cpp=1000833&url=http://mobile.youku.com/index/iDo' target='_blank'>\u67e5\u770b\u8be6\u60c5>></a>,\u901a\u8fc7\u624b\u673a\u62cd\u5ba2\u5ba2\u6237\u7aef\u62cd\u6444\u3001\u4e0a\u4f20\u89c6\u9891\uff0c\u4e0d\u4f46\u53ef\u4ee5\u7f16\u8f91\u7279\u6548\u3001\u5feb\u901f\u5206\u4eab\uff0c\u800c\u4e14\u8d85\u7701\u6d41\u91cf\u5462~".split(",");
    k.isFlashVersionAtLeast(10, 0, 45);
    var J = !1,
    U = !1,
    ra = window.FormData ? !0 : !1,
    A = !1,
    E = "flash",
    V;
    "undefined" != typeof File && "undefined" != typeof(new XMLHttpRequest).upload && (J = !0);
    if (J && ("slice" in File.prototype || "mozSlice" in File.prototype || "webkitSlice" in File.prototype)) U = !0;
    A = J && (ra || U);
    S.prototype = {
        constructor: S,
        name: "uploader",
        buttonState: "up",
        swfContainerId: null,
        swfReference: null,
        queue: null,
        initializer: function() {
            this.publish("fileselect");
            this.publish("uploadstart");
            this.publish("fileuploadstart");
            this.publish("uploadprogress");
            this.publish("totaluploadprogress");
            this.publish("uploadcomplete");
            this.publish("alluploadscomplete");
            this.publish("uploaderror");
            this.publish("mouseenter");
            this.publish("mouseleave");
            this.publish("mousedown");
            this.publish("mouseup");
            this.publish("click")
        },
        render: function(a) {
            a && (this.renderUI(a), this.bindUI())
        },
        renderUI: function(a) {
            this.contentBox = a;
            this.contentBox.style.position = "relative";
            var b = B(p("<div id='{swfContainerId}' style='position:absolute;top:0px; left: 0px; margin: 0; padding: 0; border: 0; width:100%; height:100%'></div>", {
                swfContainerId: this.swfContainerId
            }));
            b.style.width = a.offsetWidth + "px";
            b.style.height = a.offsetHeight + "px";
            this.contentBox.appendChild(b);
            this.swfReference = new k(b, this.get("swfURL"), {
                version: "10.0.45",
                fixedAttributes: {
                    wmode: "transparent",
                    allowScriptAccess: "always",
                    allowNetworking: "all",
                    scale: "noscale"
                }
            })
        },
        bindUI: function() {
            this.swfReference.on("swfReady",
            function() {
                this.setMultipleFiles();
                this.setFileFilters();
                this.triggerEnabled();
                this.after("multipleFilesChange", this.setMultipleFiles, this);
                this.after("fileFiltersChange", this.setFileFilters, this);
                this.after("enabledChange", this.triggerEnabled, this)
            },
            this);
            this.swfReference.on("fileselect", this.updateFileList, this);
            this.swfReference.on("mouseenter",
            function() {
                this.setContainerClass("hover", !0)
            },
            this);
            this.swfReference.on("mouseleave",
            function() {
                this.setContainerClass("hover", !1)
            },
            this)
        },
        setContainerClass: function(a, b) {
            b ? o(this.contentBox, this.get("containerClassNames")[a]) : r(this.contentBox, this.get("containerClassNames")[a])
        },
        setFileFilters: function() {
            this.swfReference && 0 < this.get("fileFilters").length && this.swfReference.callSWF("setFileFilters", [this.get("fileFilters")])
        },
        setMultipleFiles: function() {
            this.swfReference && this.swfReference.callSWF("setAllowMultipleFiles", [this.get("multipleFiles")])
        },
        triggerEnabled: function() {
            this.get("enabled") ? (this.swfReference.callSWF("enable"), this.swfReference.swf.setAttribute("aria-disabled", "false")) : (this.swfReference.callSWF("disable"), this.swfReference.swf.setAttribute("aria-disabled", "true"))
        },
        updateFileList: function(a) {
            this.swfReference.swf.focus();
            for (var a = a.fileList,
            b = [], c = this.swfReference, d = 0; d < a.length; d++) {
                var e = {};
                e.id = a[d].fileId;
                e.name = a[d].fileReference.name;
                e.size = a[d].fileReference.size;
                e.type = a[d].fileReference.type;
                e.dateCreated = a[d].fileReference.creationDate;
                e.dateModified = a[d].fileReference.modificationDate;
                e.uploader = c;
                b.push(new D(e))
            }
            0 < b.length && this.fire("fileselect", {
                fileList: b
            });
            u(4007035)
        },
        uploadEventHandler: function(a) {
            switch (a.type) {
            case "file:uploadstart":
                this.fire("fileuploadstart", a);
                break;
            case "file:uploadprogress":
                this.fire("uploadprogress", a);
                break;
            case "uploaderqueue:totaluploadprogress":
                this.fire("totaluploadprogress", a);
                break;
            case "file:uploadcomplete":
                this.fire("uploadcomplete", a);
                break;
            case "uploaderqueue:alluploadscomplete":
                this.queue = null;
                this.fire("alluploadscomplete", a);
                break;
            case "file:uploaderror":
            case "uploaderqueue:uploaderror":
                this.fire("uploaderror", a);
                break;
            case "file:uploadcancel":
            case "uploaderqueue:uploadcancel":
                this.fire("uploadcancel", a)
            }
        },
        upload: function(a, b, c) {
            var b = b || this.get("uploadURL"),
            c = c || this.get("postVarsPerFile"),
            d = a.id,
            c = c.hasOwnProperty(d) ? c[d] : c;
            a instanceof D && (a.on("uploadstart", this.uploadEventHandler, this), a.on("uploadprogress", this.uploadEventHandler, this), a.on("uploadcomplete", this.uploadEventHandler, this), a.on("uploaderror", this.uploadEventHandler, this), a.on("uploadcancel", this.uploadEventHandler, this), a.startUpload(b, c, this.get("fileFieldName")))
        }
    };
    T.prototype = {
        constructor: T,
        name: "uploader",
        buttonBinding: null,
        fileInputField: null,
        queue: null,
        initializer: function() {
            this.publish("fileselect");
            this.publish("uploadstart");
            this.publish("fileuploadstart");
            this.publish("uploadprogress");
            this.publish("totaluploadprogress");
            this.publish("uploadcomplete");
            this.publish("alluploadscomplete");
            this.publish("uploaderror");
            this.publish("dragenter");
            this.publish("dragover");
            this.publish("dragleave");
            this.publish("drop")
        },
        render: function(a) {
            a && (this.renderUI(a), this.bindUI())
        },
        renderUI: function(a) {
            this.contentBox = a;
            this.fileInputField = B("<input type='file' style='visibility:hidden; width:0px; height: 0px;'>");
            this.contentBox.appendChild(this.fileInputField)
        },
        bindUI: function() {
            this.bindSelectButton();
            this.setMultipleFiles();
            this.setFileFilters();
            this.bindDropArea();
            this.triggerEnabled();
            this.after("multipleFilesChange", this.setMultipleFiles, this);
            this.after("fileFiltersChange", this.setFileFilters, this);
            this.after("enabledChange", this.triggerEnabled, this);
            this.after("dragAndDropAreaChange", this.bindDropArea, this);
            i(this.fileInputField, "change", h(this.updateFileList, this))
        },
        rebindFileField: function() {
            this.fileInputField.parentNode.removeChild(this.fileInputField);
            this.fileInputField = B("<input type='file' style='visibility:hidden; width:0px; height: 0px;'>");
            this.contentBox.appendChild(this.fileInputField);
            this.setMultipleFiles();
            this.setFileFilters();
            i(this.fileInputField, "change", h(this.updateFileList, this))
        },
        bindDropArea: function() {
            var a = this.get("dragAndDropArea");
            null !== a && (i(a, "drop", h(this.ddEventHandler, this)), i(a, "dragenter", h(this.ddEventHandler, this)), i(a, "dragover", h(this.ddEventHandler, this)), i(a, "dragleave", h(this.ddEventHandler, this)))
        },
        bindSelectButton: function() {
            this.buttonBinding = h(this.openFileSelectDialog, this);
            i(this.contentBox, "click", this.buttonBinding)
        },
        ddEventHandler: function(a) {
            a = a || window.event;
            a.preventDefault ? a.preventDefault() : a.returnValue = !1;
            a.stopPropagation ? a.stopPropagation() : a.cancelBubble = !0;
            switch (a.type) {
            case "dragenter":
                this.fire("dragenter");
                break;
            case "dragover":
                this.fire("dragover");
                break;
            case "dragleave":
                this.fire("dragleave");
                break;
            case "drop":
                //if (!islogin()) return login("Uploader.prototype.callBackURL"),
                !1;
                for (var a = a.dataTransfer.files,
                b = [], c = 0; c < a.length; c++) b.push(new t(a[c]));
                0 < b.length && this.fire("fileselect", {
                    fileList: b
                });
                u(4007100);
                this.fire("drop")
            }
        },
        setButtonClass: function(a, b) {
            b ? o(this.contentBox, this.get("buttonClassNames")[a]) : r(this.contentBox, this.get("buttonClassNames")[a])
        },
        setMultipleFiles: function() { ! 0 === this.get("multipleFiles") && this.fileInputField.setAttribute("multiple", "multiple")
        },
        setFileFilters: function() {
            var a = this.get("fileFilters");
            0 < a.length ? this.fileInputField.setAttribute("accept", a.join(",")) : this.fileInputField.setAttribute("accept", "")
        },
        triggerEnabled: function() {
            if (this.get("enabled") && null === this.buttonBinding) this.bindSelectButton(),
            this.setButtonClass("disabled", !1);
            else if (!this.get("enabled") && this.buttonBinding) R(this.contentBox, "click", this.buttonBinding),
            this.buttonBinding = null,
            this.setButtonClass("disabled", !0)
        },
        updateFileList: function(a) {
            for (var a = a.target.files,
            b = [], c = 0; c < a.length; c++) b.push(new t(a[c]));
            0 < b.length && this.fire("fileselect", {
                fileList: b
            });
            this.rebindFileField();
            u(4007036)
        },
        uploadEventHandler: function(a) {
            switch (a.type) {
            case "file:uploadstart":
                this.fire("fileuploadstart", a);
                break;
            case "file:uploadprogress":
                this.fire("uploadprogress", a);
                break;
            case "uploaderqueue:totaluploadprogress":
                this.fire("totaluploadprogress", a);
                break;
            case "file:uploadcomplete":
                this.fire("uploadcomplete", a);
                break;
            case "uploaderqueue:alluploadscomplete":
                this.queue = null;
                this.fire("alluploadscomplete", a);
                break;
            case "file:uploaderror":
            case "uploaderqueue:uploaderror":
                this.fire("uploaderror", a);
                break;
            case "file:uploadcancel":
            case "uploaderqueue:uploadcancel":
                this.fire("uploadcancel", a)
            }
        },
        openFileSelectDialog: function(a) {
            this.fileInputField.click && a.target != this.fileInputField && this.fileInputField.click()
        },
        upload: function(a, b, c) {
            var b = b || this.get("uploadURL"),
            c = c || this.get("postVarsPerFile"),
            d = a.id,
            c = c.hasOwnProperty(d) ? c[d] : c;
            a instanceof t && (a.on("uploadstart", this.uploadEventHandler, this), a.on("uploadprogress", this.uploadEventHandler, this), a.on("uploadcomplete", this.uploadEventHandler, this), a.on("uploaderror", this.uploadEventHandler, this), a.on("uploadcancel", this.uploadEventHandler, this), a.startUpload(b, c, this.get("fileFieldName")))
        }
    };
    D.prototype = {
        constructor: D,
        name: "file",
        initializer: function() {
            this.id = F("file")
        },
        swfEventHandler: function(a) {
            if (a.id === this.get("id")) switch (a.type) {
            case "uploadstart":
                this.fire("uploadstart", {
                    uploader: this.get("uploader")
                });
                break;
            case "uploadprogress":
                var b = (new Date).getTime(),
                c = (b - this.preTime) / 1E3,
                d = 0;
                if (1 <= c || 0 == this.bytesPrevLoaded) {
                    this.bytesSpeed = Math.round((a.bytesLoaded - this.bytesPrevLoaded) / c);
                    this.bytesPrevLoaded = a.bytesLoaded;
                    this.preTime = b;
                    5 < this.bytesSpeeds.length && this.bytesSpeeds.shift();
                    this.bytesSpeeds.push(this.bytesSpeed);
                    for (b = 0; b < this.bytesSpeeds.length; b++) d += this.bytesSpeeds[b];
                    this.bytesSpeed = Math.round(d / this.bytesSpeeds.length);
                    this.remainTime = Math.ceil((a.bytesTotal - a.bytesLoaded) / this.bytesSpeed)
                }
                this.fire("uploadprogress", {
                    originEvent: a,
                    bytesLoaded: a.bytesLoaded,
                    bytesSpeed: this.bytesSpeed,
                    bytesTotal: a.bytesTotal,
                    remainTime: this.remainTime,
                    percentLoaded: Math.min(100, Math.round(1E4 * a.bytesLoaded / a.bytesTotal) / 100)
                });
                break;
            case "uploadcomplete":
                this.fire("uploadfinished", {
                    originEvent: a
                });
                break;
            case "uploadcompletedata":
                this.fire("uploadcomplete", {
                    originEvent: a,
                    data: a.data
                });
                break;
            case "uploadcancel":
                this.fire("uploadcancel", {
                    originEvent: a
                });
                break;
            case "uploaderror":
                this.fire("uploaderror", {
                    originEvent: a,
                    status: a.status,
                    statusText: a.message,
                    original: a.original
                })
            }
        },
        startUpload: function(a, b, c) {
            if (this.get("uploader")) {
                var d = this.get("uploader"),
                c = c || "FileData",
                e = this.get("id"),
                b = b || null;
                d.on("uploadstart", this.swfEventHandler, this);
                d.on("uploadprogress", this.swfEventHandler, this);
                d.on("uploadcomplete", this.swfEventHandler, this);
                d.on("uploadcompletedata", this.swfEventHandler, this);
                d.on("uploaderror", this.swfEventHandler, this);
                this.remainTime = this.bytesSpeed = this.bytesPrevLoaded = 0;
                this.bytesSpeeds = [];
                if (!this.preTime) this.preTime = (new Date).getTime();
                d.callSWF("upload", [e, a, b, c])
            }
        },
        cancelUpload: function() {
            this.get("uploader") && (this.get("uploader").callSWF("cancel", [this.get("id")]), this.fire("uploadcancel"))
        }
    };
    var t = function(a) {
        this.remainTime = this.bytesSpeed = this.bytesStart = this.bytesPrevLoaded = 0;
        this.bytesSpeeds = [];
        this.retryTimes = this.preTime = 0;
        this.config = {
            id: "",
            name: "",
            size: "",
            type: "",
            dateCreated: "",
            dateModified: "",
            uploader: "",
            uploadURL: "",
            serverAddress: "",
            portionSize: 10485760,
            parameters: {},
            fileFieldName: "FileData",
            uploadMethod: "formUpload"
        };
        v.apply(this, arguments)
    };
    t.isValidFile = function(a) {
        return "undefined" != typeof File && a instanceof File
    };
    t.canUpload = function() {
        return "undefined" != typeof FormData
    };
    t.prototype = {
        constructor: t,
        name: "file",
        initializer: function(a) {
            var b = null,
            b = t.isValidFile(a) ? a: t.isValidFile(a.file) ? a.file: !1;
            this.get("id") || this.set("id", F("file"));
            if (b && t.canUpload()) {
                if (!this.file) this.file = b;
                this.get("name") || this.set("name", b.name || b.fileName);
                if (this.get("size") != (b.size || b.fileSize)) this.set("size", b.size || b.fileSize);
                this.get("type") || this.set("type", b.type);
                b.lastModifiedDate && !this.get("dateModified") && this.set("dateModified", b.lastModifiedDate)
            }
        },
        uploadEventHandler: function(a) {
            var b = this.xhr,
            c = this.get("uploadMethod");
            switch (a.type) {
            case "progress":
                var b = this.get("size"),
                c = this.bytesStart + a.loaded,
                d = (new Date).getTime(),
                e = (d - this.preTime) / 1E3,
                f = 0;
                if (1 <= e || 0 === this.bytesSpeeds.length) {
                    this.bytesSpeed = Math.round((c - this.bytesPrevLoaded) / e);
                    this.bytesPrevLoaded = c;
                    this.preTime = d;
                    5 < this.bytesSpeeds.length && this.bytesSpeeds.shift();
                    this.bytesSpeeds.push(this.bytesSpeed);
                    for (d = 0; d < this.bytesSpeeds.length; d++) f += this.bytesSpeeds[d];
                    this.bytesSpeed = Math.round(f / this.bytesSpeeds.length);
                    this.remainTime = Math.ceil((b - c) / this.bytesSpeed)
                }
                this.fire("uploadprogress", {
                    originEvent: a,
                    bytesLoaded: c,
                    bytesTotal: b,
                    bytesSpeed: this.bytesSpeed,
                    remainTime: this.remainTime,
                    percentLoaded: Math.min(100, Math.floor(1E4 * c / b) / 100)
                });
                break;
            case "load":
                "resumeUpload" !== c && 200 <= b.status && 299 >= b.status ? (c = eval("(" + a.target.responseText + ")"), c.upload_server_name ? this.fire("uploadcomplete", {
                    originEvent: a,
                    data: a.target.responseText
                }) : c.file_transfered ? this.streamUpload(c.file_transfered) : this.fire("uploaderror", {
                    originEvent: a,
                    status: b.status,
                    statusText: b.statusText,
                    original: "http"
                })) : "resumeUpload" === c && 308 == b.status ? (a = /bytes=(\d+)-(\d+)/.exec(b.getResponseHeader("Range")), this.streamUpload(parseInt(a[2]))) : "resumeUpload" === c && 404 == b.status ? this.streamUpload() : this.fire("uploaderror", {
                    originEvent: a,
                    status: b.status,
                    statusText: b.statusText,
                    original: "http"
                });
                break;
            case "error":
                if ("formUpload" !== c && 360 > this.retryTimes) {
                    this.retryTimes++;
                    var g = this;
                    10 > this.retryTimes ? this.resumeUpload() : (this.timeoutHandler && clearTimeout(this.timeoutHandler), this.timeoutHandler = setTimeout(function() {
                        g.resumeUpload()
                    },
                    1E4))
                } else this.fire("uploaderror", {
                    originEvent: a,
                    status: b.status,
                    statusText: b.statusText,
                    original: "io"
                });
                break;
            case "abort":
                this.fire("uploadcancel", {
                    originEvent: a
                });
                break;
            case "readystatechange":
                this.fire("readystatechange", {
                    readyState: a.target.readyState,
                    originEvent: a
                })
            }
        },
        resetXhr: function() {
            if (this.xhr) {
                try {
                    this.xhr.upload.removeEventListener("progress", this.boundEventHandler),
                    this.xhr.upload.removeEventListener("error", this.boundEventHandler),
                    this.xhr.upload.removeEventListener("abort", this.boundEventHandler),
                    this.xhr.removeEventListener("load", this.boundEventHandler),
                    this.xhr.removeEventListener("error", this.boundEventHandler),
                    this.xhr.removeEventListener("readystatechange", this.boundEventHandler)
                } catch(a) {}
                this.xhr = null
            }
        },
        startUpload: function(a, b, c) {
            var d = this.get("uploadMethod");
            this.set("uploadURL", I(b, a));
            this.set("parameters", b);
            this.set("fileFieldName", c);
            this.remainTime = this.bytesSpeed = this.bytesPrevLoaded = 0;
            this.bytesSpeeds = [];
            this.resetXhr();
            switch (d) {
            case "formUpload":
                this.formUpload();
                break;
            case "streamUpload":
                this.streamUpload();
                break;
            case "resumeUpload":
                this.resumeUpload()
            }
        },
        formUpload: function() {
            this.resetXhr();
            this.xhr = new XMLHttpRequest;
            this.boundEventHandler = h(this.uploadEventHandler, this);
            var a = new FormData,
            b = this.get("fileFieldName"),
            c = this.get("uploadURL"),
            d = this.xhr,
            e = d.upload;
            this.set("uploadMethod", "formUpload");
            this.bytesStart = 0;
            if (!this.preTime) this.preTime = (new Date).getTime();
            a.append(b, this.file);
            d.addEventListener("loadstart", this.boundEventHandler, !1);
            e.addEventListener("progress", this.boundEventHandler, !1);
            d.addEventListener("load", this.boundEventHandler, !1);
            d.addEventListener("error", this.boundEventHandler, !1);
            e.addEventListener("error", this.boundEventHandler, !1);
            e.addEventListener("abort", this.boundEventHandler, !1);
            d.addEventListener("abort", this.boundEventHandler, !1);
            d.addEventListener("loadend", this.boundEventHandler, !1);
            d.addEventListener("readystatechange", this.boundEventHandler, !1);
            d.open("POST", c, !0);
            d.send(a);
            this.fire("uploadstart", {
                xhr: d
            })
        },
        streamUpload: function(a) {
            this.resetXhr();
            this.xhr = new XMLHttpRequest;
            this.boundEventHandler = h(this.uploadEventHandler, this);
            var a = a || 0,
            b = null,
            c = 0;
            this.get("fileFieldName");
            var d = this.get("size");
            this.get("parameters");
            var e = this.get("uploadURL"),
            f = this.xhr,
            g = f.upload;
            this.set("uploadMethod", "streamUpload");
            this.bytesStart = a;
            if (a < d) b = this.sliceFile(this.file, a),
            c = b.size;
            if (!this.preTime) this.preTime = (new Date).getTime(),
            this.bytesPrevLoaded = a;
            c = "bytes " + (Math.min(a, d) + 1) + "-" + Math.min(a + c, d) + "/" + d;
            f.addEventListener("loadstart", this.boundEventHandler, !1);
            g.addEventListener("progress", this.boundEventHandler, !1);
            f.addEventListener("load", this.boundEventHandler, !1);
            f.addEventListener("error", this.boundEventHandler, !1);
            g.addEventListener("error", this.boundEventHandler, !1);
            g.addEventListener("abort", this.boundEventHandler, !1);
            f.addEventListener("abort", this.boundEventHandler, !1);
            f.addEventListener("loadend", this.boundEventHandler, !1);
            f.addEventListener("readystatechange", this.boundEventHandler, !1);
            f.open("POST", e, !0);
            f.setRequestHeader("Content-Range", c);
            f.send(b);
            0 === a && this.fire("uploadstart", {
                xhr: f
            })
        },
        resumeUpload: function() {
            this.resetXhr();
            this.xhr = new XMLHttpRequest;
            this.boundEventHandler = h(this.uploadEventHandler, this);
            var a = this.get("uploadURL"),
            b = this.xhr;
            this.set("uploadMethod", "resumeUpload");
            b.addEventListener("loadstart", this.boundEventHandler, !1);
            b.addEventListener("load", this.boundEventHandler, !1);
            b.addEventListener("error", this.boundEventHandler, !1);
            b.addEventListener("abort", this.boundEventHandler, !1);
            b.addEventListener("loadend", this.boundEventHandler, !1);
            b.addEventListener("readystatechange", this.boundEventHandler, !1);
            b.open("GET", a, !0);
            b.setRequestHeader("Content-Range", "bytes */*");
            b.send(null)
        },
        sliceFile: function(a, b) {
            var c = this.get("portionSize"),
            b = b || 0;
            return a.slice ? a.slice(b, b + c) : a.webkitSlice ? a.webkitSlice(b, b + c) : a.mozSlice ? a.mozSlice(b, b + c) : a
        },
        cancelUpload: function() {
            this.xhr && (this.xhr.abort(), this.resetXhr())
        }
    };
    A ? (V = T, E = "html5") : (V = S, E = "flash");
    x.applyTo = function(a, b) {
        if (!a || "SWF.eventHandler" != a) return null;
        try {
            return k.eventHandler.apply(k, b)
        } catch(c) {
            return null
        }
    };
    x.FIRSTUPLOAD = 1 !=
    function(a) {
        for (var a = a + "=",
        b = document.cookie.split(";"), c = 0; c < b.length; c++) {
            for (var d = b[c];
            " " == d.charAt(0);) d = d.substring(1, d.length);
            if (0 == d.indexOf(a)) return d.substring(a.length, d.length)
        }
        return null
    } ("_up_q_t_");
    x.prototype = {
        constructor: x,
        name: "uploader",
        initializer: function() {
            this.startPanel = document.getElementById("upload-start");
            this.containerPanel = document.getElementById("upload-container");
            this.template = document.getElementById("upload-template").innerHTML;
            this.uploadLayer = document.getElementById("uploadLayer");
            this.layer = new aa;
            this.fileUploader = new V(this.config);
            this.fileUploader.render(this.getNode("uploadHot", this.startPanel));
            this.fileUploader.on("uploadprogress", this.uploadProgress, this);
            this.fileUploader.on("uploadcomplete", this.uploadComplete, this);
            this.fileUploader.on("uploaderror", this.uploadError, this);
            this.fileUploader.on("fileselect", this.fileSelect, this);
            this.showTips();
            i(window, "beforeunload", h(this.unloadHandler, this));
            //i(this.uploadLayer, "click", true)
            this.loginInit(this.uploadLayer)
        },
        loginInit: function(a) {
            true ? document.getElementById("uploadLayer").style.display = "none": i(a, "click", this.uploadLayers)
        },
        uploadLayers: function() {
            true
        },
        callBackURL: function() {
            window.location.reload();
            return ! 1
        },
        startUpload: function(a) {
            var b = this.get("prefix") + a.get("id"),
            c = B(p("<div id='{contentBoxId}'></div>", {
                contentBoxId: b
            }));
            c.innerHTML = this.template;
            this.uploadInfo[b] = {
                serverAddress: "",
                serverName: "",
                uploadToken: "",
                fileUploaded: !1,
                metaSaved: !1,
                uploadComplete: !1,
                metaData: {},
                albumData: [],
                file: a,
                vid: null,
                disabled: !1,
                tagDisabled: !1,
                progressNode: this.getNode("upload-progress", c),
                successNode: this.getNode("upload-success", c)
            };
            this.albumSelector = this.createAlbumSelector(b);
            this.renderUI(b);
            this.bindUI(b);
            A ? this.startPanel.style.display = "none": (this.startPanel.style.height = "1px", this.startPanel.style.width = "1px");
            this.containerPanel.appendChild(c);
            this.createUploadTask(b)
        },
        renderUI: function(a) {
            for (var b = this.uploadInfo[a].progressNode, c = this.uploadInfo[a].file, d = this.getNode("upload-form", b), c = c.get("name").replace(/(.*)\.\S*/, "$1"), e = window.tags ? window.tags.replace(/\s+/g, ",").split(",") : [], f = 0; f < e.length; f++) {
                var g = N(s(e[f]));
                if (1 <= g && 20 >= g) this.renderTag({
                    title: "",
                    name: s(e[f])
                },
                a),
                this.uploadInfo[a].tagDisabled = !0,
                this.getNode("meta-tags", b).setAttribute("disabled", !0)
            }
            a = d.preTitle.value;
            this.getNode("upTitle", b).innerHTML = H(a + c, 80);
            d.title.value = H(a + c, 80)
        },
        bindUI: function(a) {
            var b = this.uploadInfo[a].progressNode,
            c = this.getNode("upload-form", b),
            d = this.getNode("last-info", b),
            e = this.getNode("meta-cate", b),
            f = this.getNode("meta-cate-list", b),
            g = this.getNode("meta-original", b),
            m = this.getNode("meta-privacy", b),
            j = this.getNode("meta-share", b),
            fa = this.getNode("meta-sync", b),
            z = this.getNode("meta-save", b),
            o = this.getNode("top-save", b),
            r = this.getNode("upload-cancel", b),
            Q = this.getNode("meta-album", b),
            Z = y(b, "handler-qtips"),
            /*
            f = f.getElementsByTagName("a"),
            k = this.getNode("meta-original-list", b).getElementsByTagName("dd"),
            s = this.getNode("meta-privacy-list", b).getElementsByTagName("dd"),
            p = this.getNode("meta-share-list", b).getElementsByTagName("dd"),
            l = this.getNode("meta-sync-list", b).getElementsByTagName("dd"),
            n = this.getNode("meta-tags", b),
            t = this.getNode("meta-tags-my", b).getElementsByTagName("a"),
            */
            u = "keyup",
            u = "onpropertychange" in c.description ? "oninput" in c.description ? "keyup": "propertychange": "input",
            q = 0;
            /*
            for (; q < f.length; q++) i(f[q], "click", h(this.cateSelectHandler, this, {
                type: "click",
                nodeId: a
            }));
            for (q = 0; q < k.length; q++) i(k[q], "click", h(this.selectorHandler, this, {
                type: "original",
                nodeId: a
            })),
            i(k[q], "mouseover", h(this.selectorHandler, this, {
                type: "mouseover",
                nodeId: a
            }));
            for (q = 0; q < s.length; q++) i(s[q], "click", h(this.selectorHandler, this, {
                type: "privacy",
                nodeId: a
            })),
            i(s[q], "mouseover", h(this.selectorHandler, this, {
                type: "mouseover",
                nodeId: a
            }));
            for (q = 0; q < p.length; q++) i(p[q], "click", h(this.selectorHandler, this, {
                type: "share",
                nodeId: a
            })),
            i(p[q], "mouseover", h(this.selectorHandler, this, {
                type: "mouseover",
                nodeId: a
            }));
            for (q = 0; q < l.length; q++) i(l[q], "click", h(this.selectorHandler, this, {
                type: "sync",
                nodeId: a
            })),
            i(l[q], "mouseover", h(this.selectorHandler, this, {
                type: "mouseover",
                nodeId: a
            }));
            for (q = 0; q < t.length; q++) i(t[q], "click", h(this.addTag, this, {
                type: "myTag",
                nodeId: a
            }));
            for (q = 0; q < Z.length; q++) i(Z[q], "click", h(this.qtipsHandler, this, {
                type: "click",
                nodeId: a
            }));
            i(d, "click", h(this.lastVideoHander, this, {
                type: "click",
                nodeId: a
            }));
            i(z, "click", h(this.saveMetaInfo, this, {
                type: "click",
                nodeId: a
            }));
            i(o, "click", h(this.saveMetaInfo, this, {
                type: "click",
                nodeId: a
            }));
            i(r, "click", h(this.cancelUploadHandler, this, {
                type: "click",
                nodeId: a
            }));
            i(Q, "click", h(this.albumHandler, this, {
                type: "click",
                nodeId: a
            }));
            i(c.title, "keyup", h(this.titleHandler, this, {
                type: "keyup",
                nodeId: a
            }));
            i(c.title, "blur", h(this.titleHandler, this, {
                type: "blur",
                nodeId: a
            }));
            i(c.title, "focus", h(this.titleHandler, this, {
                type: "focus",
                nodeId: a
            }));
            i(c.description, u, h(this.descriptionHandler, this, {
                type: "keyup",
                nodeId: a
            }));
            i(c.description, "focus", h(this.descriptionHandler, this, {
                type: "focus",
                nodeId: a
            }));
            i(c.description, "blur", h(this.descriptionHandler, this, {
                type: "blur",
                nodeId: a
            }));
            i(c.password, "keyup", h(this.passwordHandler, this, {
                type: "keyup",
                nodeId: a
            }));
            i(c.password, "blur", h(this.passwordHandler, this, {
                type: "blur",
                nodeId: a
            }));
            i(c.password, "focus", h(this.passwordHandler, this, {
                type: "focus",
                nodeId: a
            }));
            i(e, "click", h(this.cateBtnHandler, this, {
                type: "click",
                nodeId: a
            }));
            i(g, "click", h(this.selectorBtnHandler, this, {
                type: "original",
                nodeId: a
            }));
            i(m, "click", h(this.selectorBtnHandler, this, {
                type: "privacy",
                nodeId: a
            }));
            i(j, "click", h(this.selectorBtnHandler, this, {
                type: "share",
                nodeId: a
            }));
            i(fa, "click", h(this.selectorBtnHandler, this, {
                type: "sync",
                nodeId: a
            }));
            i(n, u, h(this.tagsHandler, this, {
                type: "input",
                nodeId: a
            }));
            i(n, "keydown", h(this.tagsHandler, this, {
                type: "keydown",
                nodeId: a
            }));
            i(n, "blur", h(this.tagsHandler, this, {
                type: "blur",
                nodeId: a
            }));
            i(n, "focus", h(this.tagsHandler, this, {
                type: "focus",
                nodeId: a
            }));
            i(this.getNode("meta-tags-box", b), "click", h(this.tagsBoxHandler, this, {
                type: "click",
                nodeId: a
            }));
            */
            this.d_handler = h(this.documentHandler, this, {
                type: "click",
                nodeId: a
            });
            i(document, "click", this.d_handler)
        },
        saveMetaInfo: function(a, b) {
            var c = a || window.event,
            d = b.nodeId,
            e = this.uploadInfo[d].progressNode;
            this.getNode("upload-form", e);
            var f = this.getNode("meta-save", e),
            g = this.getNode("meta-save-message", e),
            m = this.getNode("meta-tags-box", e),
            j = this,
            h = this.getMetaData(d);
            this.preventDefault(c);
            this.stopPropagation(c);
            if (this.uploadInfo[d].disabled || C(m, "form_input_error")) return ! 1;
            this.getNode("error-tags", e).style.display = "none";
            h.isSave ? this.completeUpload(d, !0) : (o(f, "form_btnsub_l"), f.getElementsByTagName("span")[0].innerHTML = "\u4fdd\u5b58\u4e2d...", this.disable(d), g.style.display = "none", this.request("http://www.youku.com/QUpload/~ajax/save/", {
                method: "post",
                parameters: h.params,
                onComplete: function(a) {
                    try {
                        var c = eval("(" + a.responseText + ")");
                        c && c.vid ? (j.uploadInfo[d].metaData = h.params, j.completeUpload(d, !0)) : (j.showMetaErrors(c.e, b), r(f, "form_btnsub_l"), f.getElementsByTagName("span")[0].innerHTML = "\u4fdd\u3000\u5b58", j.enable(d))
                    } catch(e) {
                        r(f, "form_btnsub_l"),
                        f.getElementsByTagName("span")[0].innerHTML = "\u4fdd\u3000\u5b58",
                        o(g, "save_error"),
                        g.innerHTML = "\u4fdd\u5b58\u5931\u8d25",
                        g.style.display = "",
                        j.enable(d)
                    }
                },
                onFailure: function() {
                    r(f, "form_btnsub_l");
                    f.getElementsByTagName("span")[0].innerHTML = "\u4fdd\u3000\u5b58";
                    o(g, "save_error");
                    g.innerHTML = "\u4fdd\u5b58\u5931\u8d25";
                    g.style.display = "";
                    j.enable(d)
                }
            }))
        },
        getTagNames: function(a) {
            for (var a = (a = this.getNode("meta-tags-box", a)) ? a.getElementsByTagName("span") : [], b = [], c, d = 0; d < a.length; d++)(c = a[d].innerHTML) && b.push(c);
            return b.join(",")
        },
        getMetaData: function(a) {
            var b = this.getNode("upload-form", this.uploadInfo[a].progressNode),
            c = this.uploadInfo[a].metaData,
            d = !0,
            e = !0,
            f = {
                title: b.title.value,
                description: b.description.value,
                category_id: b.category_id.value,
                folderIds: b.folderIds.value,
                original: b.original.value,
                share: b.share.value,
                sync: b.sync.value,
                privacy: b.privacy.value,
                password: b.password.value,
                upload_token: this.uploadInfo[a].uploadToken,
                vid: this.uploadInfo[a].vid,
                re_tags: this.implodeTags()
            };
            if (b.tags.value) f.tags = b.tags.value;
            if (this.uploadInfo[a].disabled) return ! 1;
            "\u4e3a\u4f60\u7684\u89c6\u9891\u53d6\u4e2a\u6807\u9898\u5427" == f.title && (f.title = "");
            "\u4e3a\u4f60\u7684\u89c6\u9891\u53d6\u4e2a\u6807\u9898\u5427" == f.title && (f.title = "");
            "1-32\u4f4d\u6570\u5b57\u3001\u5b57\u6bcd\uff0c\u533a\u5206\u5927\u5c0f\u5199" == f.password && (f.password = "");
            for (var g in c) if (e = !1, f[g] != c[g]) {
                d = !1;
                break
            }
            return {
                isSave: d && !e,
                params: f
            }
        },
        completeUpload: function(a, b) {
            var c = this.uploadInfo[a].progressNode,
            d = this.getNode("meta-save", c),
            e = this.getNode("meta-save-message", c);
            this.getNode("upload-form", c);
            var f = this,
            g = b ? !0 : this.getMetaData(a).isSave;
            if (!b && this.uploadInfo[a].disabled) return ! 1;
            g && this.uploadInfo[a].fileUploaded ? (o(d, "form_btnsub_l"), d.getElementsByTagName("span")[0].innerHTML = "\u5b8c\u6210\u4e0a\u4f20\u4e2d...", e.style.display = "none", this.disable(a), this.request("http://www.youku.com/QUpload/~ajax/complete/", {
                parameters: {
                    upload_token: this.uploadInfo[a].uploadToken,
                    upload_server_ip: this.uploadInfo[a].serverName,
                    client: E
                },
                method: "post",
                onComplete: function(b) {
                    try {
                        var c = eval("(" + b.responseText + ")");
                        c && c.vid ? f.renderSuccessPanel(a) : (r(d, "form_btnsub_l"), d.getElementsByTagName("span")[0].innerHTML = "\u4fdd\u3000\u5b58", o(e, "save_error"), e.innerHTML = "\u4fdd\u5b58\u5931\u8d25", e.style.display = "", f.enable(a))
                    } catch(g) {
                        r(d, "form_btnsub_l"),
                        d.getElementsByTagName("span")[0].innerHTML = "\u4fdd\u3000\u5b58",
                        o(e, "save_error"),
                        e.innerHTML = "\u4fdd\u5b58\u5931\u8d25",
                        e.style.display = "",
                        f.enable(a)
                    }
                },
                onFailure: function() {
                    r(d, "form_btnsub_l");
                    d.getElementsByTagName("span")[0].innerHTML = "\u4fdd\u3000\u5b58";
                    o(e, "save_error");
                    e.innerHTML = "\u4fdd\u5b58\u5931\u8d25";
                    e.style.display = "";
                    f.enable(a)
                }
            })) : (!g && this.uploadInfo[a].fileUploaded ? (e.style.display = "none", this.getNode("upTips", c).style.display = "block") : (r(d, "form_btnsub_l"), d.getElementsByTagName("span")[0].innerHTML = "\u4fdd\u3000\u5b58", o(e, "save_tips"), e.innerHTML = "<em></em>\u4fdd\u5b58\u6210\u529f\uff0c\u8bf7\u7b49\u5f85\u6587\u4ef6\u4e0a\u4f20\u5b8c\u6210", e.style.display = ""), this.enable(a))
        },
        disable: function(a) {
            var b = this.uploadInfo[a].progressNode,
            c = this.getNode("upload-form", b);
            if (!this.uploadInfo[a].disabled) this.uploadInfo[a].tagDisabled || this.getNode("meta-tags", b).setAttribute("disabled", !0),
            c.title.setAttribute("disabled", !0),
            c.description.setAttribute("disabled", !0),
            c.password.setAttribute("disabled", !0),
            this.uploadInfo[a].disabled = !0
        },
        enable: function(a) {
            var b = this.uploadInfo[a].progressNode,
            c = this.getNode("upload-form", b);
            if (this.uploadInfo[a].disabled) this.uploadInfo[a].tagDisabled || this.getNode("meta-tags", b).removeAttribute("disabled", !1),
            c.title.removeAttribute("disabled", !1),
            c.description.removeAttribute("disabled", !1),
            c.password.removeAttribute("disabled", !1),
            this.uploadInfo[a].disabled = !1
        },
        cancelUpload: function(a) {
            var b = this.uploadInfo[a].file;
            b && b.cancelUpload && b.cancelUpload();
            this.showTips();
            this.uploadInfo[a] && delete this.uploadInfo[a];
            R(document, "click", this.d_handler);
            this.containerPanel.innerHTML = "";
            A ? this.startPanel.style.display = "block": (this.startPanel.style.height = "auto", this.startPanel.style.width = "970px");
            u(4007042)
        },
        cancelUploadHandler: function(a, b) {
            var c = a || window.event,
            d = b.nodeId,
            e = document.getElementById("upload-qwindow"),
            f = this.getNode("winclose", e),
            g = this.getNode("form_btnmaj_s", e),
            m = this.getNode("form_btnsub_s", e),
            j = this;
            e.style.display = "none";
            this.preventDefault(c);
            this.stopPropagation(c);
            if (this.uploadInfo[d].disabled) return ! 1;
            this.uploadInfo[d] && !this.uploadInfo[d].uploadComplete ? (c = function(a) {
                var b = document.getElementById("upload-qwindow"),
                a = a || window.event; (a = (a.target || a.srcElement).getAttribute("data-action")) && "submit" == a && j.cancelUpload(d);
                b.style.display = "none";
                j.layer && j.layer.close()
            },
            f.onclick = c, g.onclick = c, m.onclick = c, this.layer.show(), e.style.display = "block") : this.cancelUpload(d)
        },
        albumHandler: function(a, b) {
            var c = a || window.event,
            d = b.nodeId,
            e = b.type;
            this.preventDefault(c);
            this.stopPropagation(c);
            if (this.uploadInfo[d].disabled) return ! 1;
            this.removeSuccessMessage(d);
            switch (e) {
            case "click":
                this.albumSelector.setAlbumData(this.uploadInfo[d].albumData),
                this.albumSelector.show()
            }
        },
        createAlbumSelector: function(a) {
            var b = this;
            return new AlbumSelector({
                button: null,
                onSubmit: function(c) {
                    b.setAlbumData(c, a)
                }
            })
        },
        setAlbumData: function(a, b) {
            var c = this.uploadInfo[b].progressNode,
            d = this.getNode("meta-album-list", c),
            e = this.getNode("meta-album", c),
            c = this.getNode("upload-form", c),
            f = [],
            g = [];
            if (this.uploadInfo[b].disabled) return ! 1;
            if (a.length) {
                for (var m = 0; m < a.length; m++) g.push(a[m].folderId),
                f.push(a[m].folderName);
                this.uploadInfo[b].albumData = a;
                if (d) d.innerHTML = f.join().slice(0, 8) + '...<span class="special">\u7b49' + a.length + "\u4e2a\u4e13\u8f91</span> ",
                c.folderIds.value = g.join(),
                e.innerHTML = "\u4fee\u6539"
            } else this.uploadInfo[b].albumData = [],
            d.innerHTML = "",
            c.folderIds.value = "",
            e.innerHTML = "\u6dfb\u52a0\u5230\u4e13\u8f91"
        },
        qtipsHandler: function(a) {
            a = a || window.event;
            a = (a.target || a.srcElement).parentNode;
            a.parentNode.removeChild(a);
            a = new Date;
            a.setTime(a.getTime() + 2592E6);
            a = "; expires=" + a.toGMTString();
            document.cookie = "_up_q_t_=1" + a + "; path=/";
            x.FIRSTUPLOAD = !1
        },
        qwindowHandler: function(a, b) {
            var c = b.nodeId,
            d = b.action,
            e = document.getElementById("upload-qwindow");
            switch (d) {
            case "close":
                e.style.display = "none";
                break;
            case "submit":
                e.style.display = "none";
                this.cancelUpload(c);
                break;
            case "cancel":
                e.style.display = "none"
            }
            this.layer && this.layer.close()
        },
        renderSuccessPanel: function(a) {
            var b = this.uploadInfo[a].progressNode,
            c = this.uploadInfo[a].successNode,
            d = this.uploadInfo[a].md5;
            this.getNode("upload-form", b);
            var e = this.getNode("form_btnmaj_l", c),
            f = this.uploadInfo[a].metaData,
            g = this.getNode("meta-cate", b).getElementsByTagName("span")[0].innerHTML,
            m = this.getNode("meta-original", b).getElementsByTagName("span")[0].innerHTML,
            j = this.getNode("meta-privacy", b).getElementsByTagName("span")[0].innerHTML,
            o = this.getNode("meta-share", b).getElementsByTagName("span")[0].innerHTML,
            z = this.getNode("meta-sync", b).getElementsByTagName("span")[0].innerHTML,
            r = this.getNode("meta-album-list", b).innerHTML,
            k = document.getElementById("upload-qwindow"),
            Q = this.getNode("lotteryActivity", c),
            s,
            n = "";
            if (f.tags) {
                s = f.tags.split(",");
                for (var p = 0; p < s.length; p++) n += "<span>" + s[p] + "</span>"
            }
            if (k) k.style.display = "none";
            this.layer && this.layer.close();
            k = this.getNode("normal1", c);
            s = this.getNode("normal2", c);
            p = this.getNode("special1", c);
            if (f.title.match(/UGC\u65b0\u4eba\u5956/i) && null != p) p.style.display = "block",
            k.style.display = "none",
            s.style.display = "none";
            this.getNode("meta-title", c).innerHTML = f.title;
            this.getNode("meta-description", c).innerHTML = f.description.replace(/\r\n|\r|\n/g, "<br/>");
            this.getNode("meta-tags", c).innerHTML = n;
            this.getNode("meta-category_id", c).innerHTML = g;
            this.getNode("meta-original", c).innerHTML = m;
            this.getNode("meta-privacy", c).innerHTML = j;
            this.getNode("meta-sync", c).innerHTML = z;
            this.getNode("meta-share", c).innerHTML = o;
            this.getNode("meta-folderIds", c).innerHTML = r;
            b.style.display = "none";
            c.style.display = "block";
            J && localStorage.getItem(d) && localStorage.removeItem(d);
            R(document, "click", this.d_handler);
            delete this.uploadInfo[a];
            i(e, "click", h(function() {
                this.containerPanel.innerHTML = "";
                A ? this.startPanel.style.display = "block": (this.startPanel.style.height = "auto", this.startPanel.style.width = "970px");
                this.showTips();
                u(4007066)
            },
            this));
            i(Q, "click", h(function() {
                var a = "http://hz.youku.com/red/click.php?tp=1&cp=4009938&cpp=1000658&rand=" + Math.random() + "&url=#"; (new Image(1, 1)).src = a;
                lottery({
                    id: 26
                });
                setTimeout(function() {
                    var a = $$(".qwindow").last();
                    a.style.height = a.getHeight() - 1 + "px"
                },
                100)
            },
            this))
        },
        showTips: function() {
            /*
            var a = document.getElementById("ab_852");
            if (!a || !a.innerHTML) a = ca[Math.floor(Math.random() * ca.length)],
            document.getElementById("tips-box").innerHTML = p('<p></p><ul><li class="uploadF_12"><em>&nbsp;</em>{tip}</li></ul>', {
                tip: a
            })
            */
        },
        showSaveError: function(a, b) {
            var c = this.getNode("meta-save-message", a);
            o(c, "save_error");
            c.innerHTML = b;
            c.style.display = ""
        },
        showMetaErrors: function(a, b) {
            for (var c = this.uploadInfo[b.nodeId].progressNode, d = y(c, "error"), e = this.getNode("upload-form", c), f = 0; f < d.length; f++) d[f].style.display = "none";
            if (!a || !a.code || !ba[a.code]) return this.showSaveError(c, "\u4fdd\u5b58\u5931\u8d25"),
            !1;
            d = ba[a.code];
            f = this.getNode("error-" + d.field, c);
            if (!f) return this.showSaveError(c, "\u4fdd\u5b58\u5931\u8d25"),
            !1;
            f.innerHTML = d.info;
            switch (d.field) {
            case "password":
                f.style.display = "inline";
                o(e[d.field], "form_input_error");
                break;
            case "category_id":
                f.style.display = "block";
                break;
            case "description":
                if ("-310" == a.code) f.innerHTML = p("\u7b80\u4ecb\u6700\u591a2000\u4e2a\u5b57\uff0c\u5f53\u524d\u5df2\u8f93\u5165{num}\u4e2a\u5b57", {
                    num: e.description.value.length
                });
                o(e.description, "form_input_error");
                f.style.display = "block";
                break;
            case "title":
                if ("-301" == a.code) f.innerHTML = p("\u6807\u9898\u6700\u591a80\u4e2a\u5b57\uff0c\u5f53\u524d\u5df2\u8f93\u5165{num}\u4e2a\u5b57", {
                    num: e.title.value.length
                });
                o(e.title, "form_input_error");
                f.style.display = "block";
                break;
            case "privacy":
                break;
            case "tags":
                f.style.display = "block";
                o(this.getNode("meta-tags-box", c), "form_input_error");
                break;
            default:
                f.style.display = "block",
                o(e[d.field], "form_input_error")
            }
            return ! 0
        },
        tagsBoxHandler: function(a, b) {
            var c = b.nodeId,
            d = b.type,
            e = this.uploadInfo[c].progressNode;
            if (this.uploadInfo[c].disabled) return ! 1;
            this.removeSuccessMessage(c);
            switch (d) {
            case "click":
                this.getNode("meta-tags", e).focus()
            }
        },
        tagsHandler: function(a, b) {
            var c = a || window.event,
            d = c.target || c.srcElement,
            e = b.nodeId,
            f = b.type,
            g = this.uploadInfo[e].progressNode,
            m = this.getNode("upload-form", g),
            j = [",", " ", "\uff0c", "\u3000"],
            h = [];
            if (this.uploadInfo[e].disabled) return ! 1;
            this.removeSuccessMessage(e);
            switch (f) {
            case "keydown":
                if (8 === (c.keyCode || c.which || 0) && !d.value) if (e = y(g, "upSelect"), 0 < e.length) {
                    e = e[e.length - 1];
                    h = e.getAttribute("data-tag-class");
                    f = e.getAttribute("data-tag-name");
                    g = this.getNode(h, g);
                    e.parentNode.removeChild(e);
                    if (g) g.parentNode.style.display = "";
                    m.tags.value = this.getTagNames(m);
                    d.value = f;
                    this.preventDefault(c)
                }
                break;
            case "focus":
                this.showQtips("tags", g);
                r(this.getNode("meta-tags-box", g), "form_input_error");
                this.getNode("error-tags", g).style.display = "none";
                break;
            default:
                if (c.propertyName && "value" != c.propertyName.toLowerCase()) return ! 1;
                if ("" != s(d.value)) {
                    for (var i = d.value,
                    k = "",
                    p = 0,
                    h = []; i.length;) {
                        for (var n = -1,
                        k = 0; k < j.length; k++) {
                            var t = i.indexOf(j[k]); - 1 !== t && ( - 1 === n && (n = t), n = Math.min(n, t))
                        }
                        if ( - 1 === n) break;
                        else if (0 === n) {
                            i = i.slice(1);
                            continue
                        }
                        k = i.slice(0, n);
                        p = N(s(k));
                        if (1 <= p && 20 >= p) h.push(k),
                        i = i.slice(n + 1);
                        else break
                    }
                    if (i) if (j = this.getNode("error-tags", g), n = N(s(i)), 0 != p && 1 > p || "blur" == f && 1 > n) {
                        if (j.innerHTML = "\u5355\u4e2a\u6807\u7b7e\u6700\u5c111\u4e2a\u5b57", j.style.display = "block", o(this.getNode("meta-tags-box", g), "form_input_error"), d.value != i) d.value = i,
                        this.preventDefault(c)
                    } else if (0 != p && 20 < p || 20 < n) {
                        if (j.innerHTML = "\u5355\u4e2a\u6807\u7b7e\u6700\u591a20\u4e2a\u5b57", j.style.display = "block", o(this.getNode("meta-tags-box", g), "form_input_error"), d.value != i) d.value = i,
                        this.preventDefault(c)
                    } else if (r(this.getNode("meta-tags-box", g), "form_input_error"), j.style.display = "none", "blur" == f) this.renderTag({
                        title: "",
                        name: s(i)
                    },
                    e),
                    this.getRecommendTags(m.title.value, e, content = "", m.tags.value),
                    d.value = "",
                    this.preventDefault(c);
                    else {
                        if (d.value != i) d.value = i,
                        this.preventDefault(c)
                    } else d.value = "",
                    this.preventDefault(c);
                    for (k = 0; k < h.length; k++) this.renderTag({
                        title: "",
                        name: s(h[k])
                    },
                    e),
                    this.getRecommendTags(m.title.value, e, content = "", m.tags.value)
                } else if (c = m.tags.value.split(","), j = this.getNode("error-tags", g), 0 < c.length) r(this.getNode("meta-tags-box", g), "form_input_error"),
                j.style.display = "none"
            }
        },
        showQtips: function(a, b) {
            if (x.FIRSTUPLOAD && b) {
                this.getNode("qtips-" + a, b);
                for (var c = y(b, "qtips"), d = 0; d < c.length; d++) c[d].style.display = C(c[d], "qtips-" + a) ? "block": "none"
            }
        },
        addTag: function(a, b) {
            var c = a || window.event,
            d = c.target || c.srcElement,
            e = b.nodeId,
            f = this.getNode("upload-form", this.uploadInfo[e].progressNode).tags.value.split(",");
            this.preventDefault(c);
            this.stopPropagation(c);
            if (this.uploadInfo[e].disabled || this.uploadInfo[e].tagDisabled) return ! 1;
            if (10 > f.length) this.add_hz(b.type),
            d.parentNode.style.display = "none";
            this.renderTag({
                title: d.className,
                name: d.innerHTML
            },
            e, "add")
        },
        add_hz: function(a) {
            var b = "";
            "myTag" == a ? b = 4007059 : "recTag" == a && (b = 4007060);
            a = new Image;
            b = "http://hz.youku.com/red/click.php?tp=1&cp=" + b + "&cpp=1000658&" + (new Date).getTime();
            a.src = b;
            a.onload = function() {
                return ! 1
            }
        },
        removeTag: function(a, b) {
            var c = a || window.event,
            c = (c.target || c.srcElement).parentNode,
            d = this.uploadInfo[b].progressNode,
            e = this.getNode("upload-form", d);
            c.getElementsByTagName("span");
            var f = c.getAttribute("data-tag-class");
            if (this.uploadInfo[b].disabled || this.uploadInfo[b].tagDisabled) return ! 1;
            c.parentNode.removeChild(c);
            if (f) this.getNode(f, d).parentNode.style.display = "";
            e.tags.value = this.getTagNames(e);
            this.getNode("meta-tags", d).focus();
            if (!e.tags.value) r(this.getNode("meta-tags-box", d), "form_input_error"),
            this.getNode("error-tags", d).style.display = "none"
        },
        renderTag: function(a, b) {
            var c = this.uploadInfo[b].progressNode,
            d = this.getNode("meta-tags", c),
            e = this.getNode("upload-form", c),
            f = e.tags.value.split(","),
            g = this.getNode("error-tags", c);
            if (this.uploadInfo[b].disabled) return ! 1;
            this.removeSuccessMessage(b);
            10 <= f.length ? (g.innerHTML = "\u6807\u7b7e\u6700\u591a\u4e3a10\u4e2a", g.style.display = "block") : (f = B(p("<div class='upSelect' data-tag-name='{name}' data-tag-class='{title}'><span>{name}</span><p title='\u79fb\u9664\u8be5\u6807\u7b7e' class='handler' style='clear:right' ></p></div>", a)), d.parentNode.insertBefore(f, d), i(this.getNode("handler", f), "click", h(this.removeTag, this, b)), e.tags.value = this.getTagNames(e), r(this.getNode("meta-tags-box", c), "form_input_error"), g.style.display = "none")
        },
        selectorBtnHandler: function(a, b) {
            var c = a || window.event,
            d = b.nodeId,
            e = b.type,
            f = this.uploadInfo[d].progressNode;
            this.getNode("meta-password", f);
            this.getNode("upload-form", f);
            var g;
            this.preventDefault(c);
            this.stopPropagation(c);
            if (this.uploadInfo[d].disabled) return ! 1;
            this.removeSuccessMessage(d);
            switch (e) {
            case "privacy":
                g = this.getNode("meta-privacy-list", f);
                this.getNode("meta-cate-list", f).style.display = "none";
                this.getNode("meta-original-list", f).style.display = "none";
                this.getNode("meta-share-list", f).style.display = "none";
                this.getNode("meta-sync-list", f).style.display = "none";
                break;
            case "original":
                g = this.getNode("meta-original-list", f);
                this.getNode("meta-cate-list", f).style.display = "none";
                this.getNode("meta-privacy-list", f).style.display = "none";
                this.getNode("meta-share-list", f).style.display = "none";
                this.getNode("meta-sync-list", f).style.display = "none";
                break;
            case "sync":
                g = this.getNode("meta-sync-list", f);
                this.getNode("meta-cate-list", f).style.display = "none";
                this.getNode("meta-original-list", f).style.display = "none";
                this.getNode("meta-privacy-list", f).style.display = "none";
                this.getNode("meta-share-list", f).style.display = "none";
                break;
            case "share":
                g = this.getNode("meta-share-list", f),
                this.getNode("meta-cate-list", f).style.display = "none",
                this.getNode("meta-original-list", f).style.display = "none",
                this.getNode("meta-privacy-list", f).style.display = "none",
                this.getNode("meta-sync-list", f).style.display = "none"
            }
            g.style.display = "block" == g.style.display ? "none": "block"
        },
        selectorHandler: function(a, b) {
            var c = a || window.event,
            c = c.target || c.srcElement,
            d = b.nodeId,
            e = b.type,
            f = this.uploadInfo[d].progressNode,
            g = this.getNode("upload-form", f),
            h = this.getNode("meta-password", f),
            j = c.getAttribute("data-value");
            if (this.uploadInfo[d].disabled) return ! 1;
            this.removeSuccessMessage(d);
            switch (e) {
            case "privacy":
                d = this.getNode("meta-privacy", f);
                d = d.getElementsByTagName("span")[0];
                g.privacy.value = j;
                d.innerHTML = c.innerHTML;
                this.getNode("meta-privacy-list", f).style.display = "none";
                c = this.getNode("error-password", f);
                if ("password" == j) {
                    if (h.style.display = "block", C(h, "form_input_error")) c.style.display = "block"
                } else h.style.display = "none",
                c.style.display = "none";
                "anybody" != j ? (this.getNode("Synctd", f).style.display = "none", syncNode = this.getNode("meta-sync", f), d = syncNode.getElementsByTagName("span")[0], d.innerHTML = "\u89c6\u9891\u4e0d\u540c\u6b65\u5230\u571f\u8c46", g.sync.value = "0", o(this.getNode("Syncyk", f), "ddHover")) : (this.getNode("Synctd", f).style.display = "block", r(this.getNode("Syncyk", f), "ddHover"), 0 == g.sync.value ? (r(this.getNode("Synctd", f), "ddHover"), o(this.getNode("Syncyk", f), "ddHover")) : (r(this.getNode("Syncyk", f), "ddHover"), o(this.getNode("Synctd", f), "ddHover")));
                break;
            case "original":
                d = this.getNode("meta-original", f);
                d = d.getElementsByTagName("span")[0];
                g.original.value = j;
                d.innerHTML = c.innerHTML;
                this.getNode("meta-original-list", f).style.display = "none";
                break;
            case "sync":
                d = this.getNode("meta-sync", f);
                d = d.getElementsByTagName("span")[0];
                g.sync.value = j;
                d.innerHTML = c.innerHTML;
                this.getNode("meta-sync-list", f).style.display = "none";
                break;
            case "share":
                d = this.getNode("meta-share", f);
                d = d.getElementsByTagName("span")[0];
                g.share.value = j;
                d.innerHTML = c.innerHTML;
                this.getNode("meta-share-list", f).style.display = "none";
                break;
            case "mouseover":
                f = c.parentNode.getElementsByTagName("dd");
                for (g = 0; g < f.length; g++) r(f[g], "ddHover");
                o(c, "ddHover")
            }
        },
        cateListHandler: function(a, b) {
            var c = b.nodeId,
            d = b.type,
            e = this.getNode("meta-cate-list", this.uploadInfo[c].progressNode);
            if (this.uploadInfo[c].disabled) return ! 1;
            this.removeSuccessMessage(c);
            switch (d) {
            case "blur":
                e.style.display = "none"
            }
        },
        cateSelectHandler: function(a, b) {
            var c = a || window.event,
            d = c.target || c.srcElement,
            e = b.nodeId,
            f = b.type,
            g = this.uploadInfo[e].progressNode,
            h = this.getNode("upload-form", g),
            j = this.getNode("meta-cate-list", g),
            i = this.getNode("meta-cate", g).getElementsByTagName("span")[0],
            k = d.getAttribute("data-value");
            this.preventDefault(c);
            this.stopPropagation(c);
            if (this.uploadInfo[e].disabled) return ! 1;
            this.removeSuccessMessage(e);
            switch (f) {
            case "click":
                i.innerHTML = d.innerHTML,
                h.category_id.value = k,
                j.style.display = "none",
                this.getNode("error-category_id", g).style.display = "none"
            }
        },
        renderRecTags: function(a, b) {
            var c = this.getNode("meta-tags-rec", this.uploadInfo[b].progressNode),
            d = "",
            e = 0,
            f = 0;
            if (this.uploadInfo[b].disabled) return ! 1;
            if (0 < a.length) {
                for (d += '<p >\u63a8\u8350\u6807\u7b7e:</p><div class="uplabel_select">'; e < a.length; e++) d += "<span class='upLabel_list'><a href='#' class='rec-tag-" + e + "'>" + a[e][0] + "</a></span>";
                c.innerHTML = d + '</div><div class="clear"></div>';
                for (c = c.getElementsByTagName("a"); f < c.length; f++) i(c[f], "click", h(this.addTag, this, {
                    type: "recTag",
                    nodeId: b
                }))
            } else c.innerHTML = d
        },
        cateBtnHandler: function(a, b) {
            var c = a || window.event,
            d = b.nodeId,
            e = b.type,
            f = this.uploadInfo[d].progressNode,
            g = this.getNode("meta-cate-list", f),
            h = g.getElementsByTagName("a"),
            j = this.getNode("upload-form", f).category_id.value;
            this.preventDefault(c);
            this.stopPropagation(c);
            if (this.uploadInfo[d].disabled) return ! 1;
            this.removeSuccessMessage(d);
            switch (e) {
            case "click":
                if (this.getNode("meta-privacy-list", f).style.display = "none", this.getNode("meta-original-list", f).style.display = "none", this.getNode("meta-share-list", f).style.display = "none", this.getNode("meta-sync-list", f).style.display = "none", "block" == g.style.display) g.style.display = "none";
                else {
                    if (j) for (c = 0; c < h.length; c++) d = h[c].getAttribute("data-value"),
                    h[c].className = d == j ? "selected": "";
                    g.style.display = "block"
                }
            }
        },
        passwordHandler: function(a, b) {
            var c = b.nodeId,
            d = b.type,
            e = this.uploadInfo[c].progressNode,
            f = this.getNode("upload-form", e),
            e = this.getNode("error-password", e),
            g = s(f.password.value);
            if (this.uploadInfo[c].disabled) return ! 1;
            this.removeSuccessMessage(c);
            "focus" == d ? (r(f.password, "form_input_error"), e.style.display = "none") : (c = g.length, g && 32 < c ? (e.innerHTML = p("\u5bc6\u7801\u6700\u591a32\u4f4d\uff0c\u5f53\u524d\u5df2\u8f93\u5165{num}\u4e2a\u5b57", {
                num: c
            }), o(f.password, "form_input_error"), e.style.display = "inline") : g && !/^[a-zA-Z0-9]{1,32}$/.test(g) ? (e.innerHTML = "\u5bc6\u7801\u53ea\u80fd\u4f7f\u7528\u6570\u5b57\u3001\u5b57\u6bcd", o(f.password, "form_input_error"), e.style.display = "inline") : "blur" == d && !g ? (e.innerHTML = p("\u8bf7\u586b\u5199\u5bc6\u7801"), o(f.password, "form_input_error"), e.style.display = "inline") : (r(f.password, "form_input_error"), e.style.display = "none"))
        },
        descriptionHandler: function(a, b) {
            var c = a || window.event,
            d = b.nodeId,
            e = b.type,
            f = this.uploadInfo[d].progressNode,
            g = this.getNode("upload-form", f),
            h = this.getNode("description-hidden", f);
            if (this.uploadInfo[d].disabled) return ! 1;
            this.removeSuccessMessage(d);
            switch (e) {
            case "keyup":
                if (c.propertyName && "value" != c.propertyName.toLowerCase()) return ! 1;
                if (6 != n.ie) h.value = g.description.value,
                h.scrollTop = 0,
                h.scrollTop = 9E4,
                c = h.scrollTop,
                g.description.style.height = Math.min(Math.max(c, 60), 200) + "px",
                g.description.style.overflow = 200 < c ? "auto": "hidden";
                break;
            case "focus":
                this.showQtips("description", f)
            }
            c = g.description.value.length;
            d = p("\u7b80\u4ecb\u6700\u591a2000\u4e2a\u5b57\uff0c\u5f53\u524d\u5df2\u8f93\u5165{num}\u4e2a\u5b57", {
                num: c
            });
            f = this.getNode("error-description", f);
            2E3 < c ? (o(g.description, "form_input_error"), f.innerHTML = d, f.style.display = "block") : (r(g.description, "form_input_error"), f.innerHTML = "", f.style.display = "none")
        },
        titleHandler: function(a, b) {
            var c = b.nodeId;
            this.uploadInfo[c].file.get("name").replace(/(.*)\.\S*/, "$1");
            var d = b.type,
            e = this.uploadInfo[c].progressNode,
            f = this.getNode("upload-form", e),
            g = this.getNode("upTitle", e);
            if (this.uploadInfo[c].disabled) return ! 1;
            this.removeSuccessMessage(c);
            var h = s(f.title.value),
            j = h.length,
            i = p("\u6807\u9898\u6700\u591a80\u4e2a\u5b57\uff0c\u5f53\u524d\u5df2\u8f93\u5165{num}\u4e2a\u5b57", {
                num: j
            }),
            k = this.getNode("error-title", e);
            switch (d) {
            case "keyup":
                g.innerHTML = H(h, 80);
                80 < j ? (k.innerHTML = i, k.style.display = "block", o(f.title, "form_input_error")) : (k.style.innerHTML = "", k.style.display = "none", r(f.title, "form_input_error"));
                break;
            case "blur":
                j ? 80 < j ? (k.innerHTML = i, k.style.display = "block", o(f.title, "form_input_error")) : (k.style.innerHTML = "", k.style.display = "none", r(f.title, "form_input_error"), this.getRecommendTags(h, c, content = "", tags = f.tags.value)) : (k.innerHTML = "\u8bf7\u586b\u5199\u6807\u9898\uff0c\u6700\u591a80\u4e2a\u5b57", k.style.display = "block", o(f.title, "form_input_error"));
                break;
            case "focus":
                this.showQtips("title", e),
                k.style.innerHTML = "",
                k.style.display = "none",
                r(f.title, "form_input_error")
            }
        },
        removeSuccessMessage: function(a) {
            if (this.uploadInfo[a]) this.getNode("meta-save-message", this.uploadInfo[a].progressNode).style.display = "none"
        },
        getVideoInfo: function(a) {
            var b = this.uploadInfo[a].vid,
            c = this;
            if (this.uploadInfo[a].disabled) return ! 1;
            this.removeSuccessMessage(a);
            this.request("/QVideo/~ajax/getVideoInfo?vid=" + b, {
                method: "get",
                parameters: {},
                onComplete: function(b) {
                    b = eval("(" + b.responseText + ")");
                    c.setVideoInfo(b, a)
                },
                onFailure: function() {}
            })
        },
        lastVideoHander: function(a, b) {
            var c = a || window.event,
            d = c.target || c.srcElement,
            e = b.nodeId,
            f = this,
            g = this.uploadInfo[e].vid;
            this.preventDefault(c);
            this.stopPropagation(c);
            if (this.uploadInfo[e].disabled) return ! 1;
            this.removeSuccessMessage(e);
            this.request(d.href + "?vid=" + g, {
                method: "get",
                parameters: {},
                onComplete: function(a) {
                    a = eval("(" + a.responseText + ")");
                    f.setVideoInfo(a, e)
                },
                onFailure: function() {}
            });
            u(4007045)
        },
        unloadHandler: function(a) {
            var a = a || window.event,
            b = !0,
            c;
            for (c in this.uploadInfo) {
                b = !1;
                break
            }
            if (!b) return a.returnValue = "\u60a8\u6b63\u5728\u4e0a\u4f20\u89c6\u9891\uff0c\u5173\u95ed\u6b64\u9875\u9762\u5c06\u4f1a\u4e2d\u65ad\u4e0a\u4f20\uff0c\u5efa\u8bae\u60a8\u7b49\u5f85\u4e0a\u4f20\u5b8c\u6210\u540e\u518d\u5173\u95ed\u6b64\u9875\u9762"
        },
        documentHandler: function(a, b) {
            var c = this.uploadInfo[b.nodeId].progressNode,
            d = this.getNode("meta-cate-list", c),
            e = this.getNode("meta-original-list", c),
            f = this.getNode("meta-privacy-list", c),
            g = this.getNode("meta-sync-list", c),
            h = this.getNode("meta-share-list", c),
            c = this.getNode("error-tags", c);
            if (d && "block" == d.style.display) d.style.display = "none";
            if (c && "\u6807\u7b7e\u6700\u591a\u4e3a10\u4e2a" == s(c.innerHTML)) c.style.display = "none";
            if (e && "block" == e.style.display) e.style.display = "none";
            if (f && "block" == f.style.display) f.style.display = "none";
            if (g && "block" == g.style.display) g.style.display = "none";
            if (h && "block" == h.style.display) h.style.display = "none"
        },
        setVideoInfo: function(a, b) {
            var c = this.uploadInfo[b].progressNode,
            d = this.getNode("upload-form", c),
            e = this.getNode("meta-cate-list", c),
            f = this.getNode("meta-original-list", c),
            g = this.getNode("meta-privacy-list", c),
            h = this.getNode("meta-sync-list", c),
            i = this.getNode("meta-share-list", c),
            e = e.getElementsByTagName("a"),
            f = f.getElementsByTagName("dd"),
            g = g.getElementsByTagName("dd"),
            h = h.getElementsByTagName("dd"),
            i = i.getElementsByTagName("dd"),
            k = this.getNode("meta-cate", c),
            n = this.getNode("meta-original", c),
            o = this.getNode("meta-privacy", c),
            p = this.getNode("meta-sync", c),
            t = this.getNode("meta-share", c),
            u = this.getNode("meta-tags-box", c),
            u = y(u, "upSelect"),
            v = y(d, "error"),
            x = y(d, "form_input_error"),
            w = [];
            s(a.tags) && (w = s(a.tags).split(" "));
            var l = window.tags ? window.tags.replace(/\s+/g, ",").split(",") : [];
            0 < l.length && (w = w.concat(l));
            for (l = 0; l < v.length; l++) v[l].style.display = "none";
            for (l = 0; l < x.length; l++) r(x[l], "form_input_error");
            v = d.preTitle.value;
            this.getNode("upTitle", c).innerHTML = v + a.title;
            this.getNode("meta-password", c).style.display = "none";
            d.title.value = v + a.title;
            d.category_id.value = a.cates;
            d.tags.value = "";
            d.original.value = a.sourceType & 1 ? 1 : 0;
            1 == a.publicType ? (d.privacy.value = "friend", this.getNode("Synctd", c).style.display = "none", d.sync.value = 0) : 4 == a.publicType ? (d.privacy.value = "password", this.getNode("Synctd", c).style.display = "none", d.sync.value = 0) : d.privacy.value = "anybody";
            void 0 == a.share && (a.share = 0);
            d.share.value = a.share;
            d.password.value = "";
            if (200 < a.memo.length) d.description.style.overflow = "auto";
            d.description.value = a.memo;
            for (l = 0; l < e.length; l++) if (e[l].getAttribute("data-value") == a.cates) k.getElementsByTagName("span")[0].innerHTML = e[l].innerHTML;
            for (l = 0; l < f.length; l++) if (f[l].getAttribute("data-value") == d.original.value) n.getElementsByTagName("span")[0].innerHTML = f[l].innerHTML;
            for (l = 0; l < t.length; l++) if (i[l].getAttribute("data-value") == a.share) t.getElementsByTagName("span")[0].innerHTML = i[l].innerHTML;
            for (l = 0; l < p.length; l++) if (h[l].getAttribute("data-value") == a.sync) t.getElementsByTagName("span")[0].innerHTML = i[l].innerHTML;
            for (l = 0; l < u.length; l++) u[l].parentNode.removeChild(u[l]);
            for (l = 0; l < g.length; l++) if (g[l].getAttribute("data-value") == d.privacy.value && (o.getElementsByTagName("span")[0].innerHTML = g[l].innerHTML, "password" == d.privacy.value)) this.getNode("meta-password", c).style.display = "block";
            for (l = 0; l < w.length; l++) this.renderTag({
                title: "",
                name: s(w[l])
            },
            b, "add");
            a.foldersInfo && 0 < a.foldersInfo.length && this.setAlbumData(a.foldersInfo, b)
        },
        getRecommendTags: function(a, b, c, d) {
            var e = this,
            c = c ? c: "",
            d = d ? d: "";
            this.request("http://www.youku.com/QUpload/~ajax/getRecommendTags/", {
                method: "get",
                parameters: {
                    title: H(a, 80),
                    content: c,
                    tags: d,
                    format: "json"
                },
                onComplete: function(a) {
                    a = eval("(" + a.responseText + ")");
                    e.renderRecTags(a, b);
                    e.joinTags(a)
                },
                onFailure: function() {}
            })
        },
        joinTags: function(a) {
            if (a) for (var b = 0; b < a.length; b++) this.recommTags.push(a[b][0])
        },
        implodeTags: function() {
            var a = "";
            this.recommTags && (a = this.recommTags.join(","));
            return a
        },
        createUploadTask: function(a) {
            var b = this.uploadInfo[a].file;
            var c = this,
            d = b.get("name") + b.get("size") + b.get("type") + window.UID,
            e = CryptoJS.MD5(d).toString();
            (d = localStorage.getItem(e)) ? (d = d.split("-"), this.uploadInfo[a].uploadToken = d[0], this.uploadInfo[a].serverAddress = d[1], this.uploadInfo[a].vid = d[2], this.uploadInfo[a].md5 = e, this.getVideoInfo(a), this.getRecommendTags(b.get("name").replace(/(.*)\.\S*/, "$1"), a), this.uploadFile(b, d[1], d[0], "resumeUpload")) : this.request("http://www.youku.com/QUpload/~ajax/create/", {
                method: "get",
                parameters: {
                    fileSize: b.get("size"),
                    fileName: b.get("name"),
                    fileType: b.get("type"),
                    fileDateModified: b.get("dateModified") + "",
                    client: E
                },
                onComplete: function(d) {
                    var d = eval("(" + d.responseText + ")"),
                    g = d.upload_token,
                    h = d.vid,
                    d = "";
                    if (g) if (c.getRecommendTags(b.get("name").replace(/(.*)\.\S*/, "$1"), a), c.uploadInfo[a].uploadToken = g, c.uploadInfo[a].vid = h, U) {
                        var i = new XMLHttpRequest,
                        d = I({
                            upload_token: g
                        },
                        "http://upload.youku.com/api/get_server_address/");
                        i.open("post", d, !0);
                        i.onerror = function() {
                            c.uploadFile(b, "upload.youku.com", g, "formUpload")
                        };
                        i.onload = function() {
                            try {
                                var d = eval("(" + i.responseText + ")").server_address;
                                d ? (localStorage.setItem(e, g + "-" + d + "-" + h), c.uploadInfo[a].serverAddress = d, c.uploadInfo[a].md5 = e, c.uploadFile(b, d, g, "streamUpload")) : c.uploadFile(b, "upload.youku.com", g, "formUpload")
                            } catch(f) {
                                c.uploadFile(b, "upload.youku.com", g, "formUpload")
                            }
                        };
                        i.send()
                    } else c.uploadFile(b, "upload.youku.com", g, "formUpload");
                    else d = c.getNode("upload-start-error", this.startPanel),
                    c.cancelUpload(a),
                    d.innerHTML = "\u521b\u5efa\u4e0a\u4f20\u4efb\u52a1\u5931\u8d25\uff0c\u8bf7\u5c1d\u8bd5\u91cd\u65b0\u4e0a\u4f20",
                    d.style.display = "block"
                },
                onFailure: function() {
                    var b = c.getNode("upload-start-error", this.startPanel);
                    c.cancelUpload(a);
                    b.innerHTML = "\u521b\u5efa\u4e0a\u4f20\u4efb\u52a1\u5931\u8d25\uff0c\u8bf7\u5c1d\u8bd5\u91cd\u65b0\u4e0a\u4f20";
                    b.style.display = "block"
                }
            })
        },
        uploadFile: function(a, b, c, d) {
            alert('b:'+ b);
            var e = "",
            c = {
                upload_token: c,
                client: E
            },
            e = b ? "http://" + b + "/api/": "http://upload.youku.com/api/",
            e = "formUpload" == d ? e + "upload_form_data/": e + "upload/";
            d && a instanceof t && a.set("uploadMethod", d);
            this.fileUploader.upload(a, e, c)
        },
        request: function(a, b) {
            var c = {
                method: "get",
                parameters: {},
                onComplete: function() {},
                onFailure: function() {}
            },
            d;
            for (d in c) b && b[d] && (c[d] = b[d]);
            new Ajax.Request(a, c);
        },
        uploadProgress: function(a) {
            var b = a.target.get("id"),
            b = this.uploadInfo[this.get("prefix") + b].progressNode,
            c = this.formatSpeed(a.bytesSpeed),
            d = this.formatBytes(a.bytesLoaded),
            e = this.formatBytes(a.bytesTotal),
            f = this.formatTime(a.remainTime),
            a = Math.min(99.99, a.percentLoaded);
            100 > a && (a = parseFloat(a).toFixed(2));
            d = Math.min(d, e);
            d = parseFloat(d).toFixed(2);
            e = parseFloat(e).toFixed(2);
            this.getNode("bar", b).style.width = a + "%";
            this.getNode("f_36", b).innerHTML = a + "%";
            this.getNode("speed", b).innerHTML = "\u4e0a\u4f20\u901f\u5ea6\uff1a" + c;
            if (f) this.getNode("time", b).innerHTML = "\u5269\u4f59\u65f6\u95f4\uff1a" + f;
            this.getNode("uploaded", b).innerHTML = "\u5df2\u4e0a\u4f20\uff1a" + d + "MB/" + e + "MB"
        },
        uploadComplete: function(a) {
            var b = a.target.get("id"),
            b = this.get("prefix") + b,
            c = this.uploadInfo[b].progressNode,
            d = a.target.get("size"),
            a = eval("(" + a.data + ")"),
            d = this.formatBytes(d);
            this.getNode("bar", c).style.width = "100%";
            this.getNode("f_36", c).innerHTML = "100%";
            this.getNode("uploaded", c).innerHTML = "\u5df2\u4e0a\u4f20\uff1a" + d + "MB/" + d + "MB";
            this.getNode("time", c).innerHTML = "\u5269\u4f59\u65f6\u95f4\uff1a0";
            if (a.upload_server_name) this.uploadInfo[b].serverName = a.upload_server_name,
            this.uploadInfo[b].fileUploaded = !0,
            this.completeUpload(b)
        },
        uploadError: function() {
            A || u(4007213)
        },
        getNode: function(a, b) {
            return y(b || this.containerPanel, a)[0] || null
        },
        getStyle: function(a, b) {
            return Element.getStyle(a, b)
        },
        getDimensions: function(a) {
            return Element.getDimensions(a)
        },
        fileSelect: function(a) {
            var a = a.fileList,
            b = 0,
            c;
            for (c in this.uploadInfo) b++;
            if (b == this.get("simLimit") || a.length > this.get("simLimit")) return ! 1;
            for (c = 0; c < a.length; c++) this.validateFile(a[c]) && this.startUpload(a[c])
        },
        validateFile: function(a) {
            var b = a.get("name"),
            c = a.get("size"),
            d = -1 !== b.indexOf(".") ? b.replace(/.*[.]/, "").toLowerCase() : "",
            e = K,
            f = !1,
            g = "";
            this.getNode("upload-start-error", this.startPanel).style.display = "none";
            if (a instanceof D && 2147483648 < c) g = p("\u60a8\u7684\u89c6\u9891\u6587\u4ef6\u5927\u5c0f\u8d85\u8fc7{fileSize}\u4e86\uff0c\u8bf7\u4f7f\u7528\u6700\u5927\u652f\u630110G\u89c6\u9891\u7684\u4f18\u9177\u5ba2\u6237\u7aef\u4e0a\u4f20^_^", {
                fileSize: "2G"
            });
            else if (a instanceof t && 2147483648 < c) g = p("\u60a8\u7684\u89c6\u9891\u6587\u4ef6\u5927\u5c0f\u8d85\u8fc7{fileSize}\u4e86\uff0c\u8bf7\u4f7f\u7528\u6700\u5927\u652f\u630110G\u89c6\u9891\u7684\u4f18\u9177\u5ba2\u6237\u7aef\u4e0a\u4f20^_^", {
                fileSize: "2G"
            });
            else {
                e.length || (f = !0);
                for (a = 0; a < e.length; a++) e[a].toLowerCase() == "." + d && (f = !0);
                f || (g = p("\u89c6\u9891\u6587\u4ef6\u683c\u5f0f\u4e0d\u652f\u6301\uff01\u652f\u6301\u7684\u6587\u4ef6\u683c\u5f0f\uff1awmv, avi, dat, asf, rm, rmvb, ram, mpg, mpeg, 3gp, mov, mp4, m4v, dvix, dv, dat, mkv, flv, vob, ram, qt, divx, cpk, fli, flc, mod", {
                    fileName: b
                }))
            }
            if (!f && g) this.getNode("upload-start-error", this.startPanel).innerHTML = g,
            this.getNode("upload-start-error", this.startPanel).style.display = "block";
            return f
        },
        formatSpeed: function(a) {
            var b = 0;
            1024 <= Math.round(a / 1024) ? (b = Math.round(100 * (a / 1048576)) / 100, b = Math.max(0, b), b = isNaN(b) ? 0 : parseFloat(b).toFixed(2), a = b + "MB/s") : (b = Math.round(100 * (a / 1024)) / 100, b = Math.max(0, b), b = isNaN(b) ? 0 : parseFloat(b).toFixed(2), a = b + "KB/s");
            return a
        },
        formatBytes: function(a) {
            a = Math.round(100 * (a / 1048576)) / 100;
            return a = isNaN(a) ? 0 : parseFloat(a).toFixed(2)
        },
        formatTime: function(a) {
            var b = a || 0,
            c = Math.floor(b / 3600),
            a = Math.floor((b - 3600 * c) / 60),
            b = Math.floor(b - 3600 * c - 60 * a),
            c = "" + (!isNaN(c) && 0 < c ? c + "\u5c0f\u65f6": ""),
            c = c + (!isNaN(a) && 0 < a ? a + "\u5206": "");
            return c += !isNaN(b) && 0 < b ? b + "\u79d2": ""
        },
        preventDefault: function(a) {
            a.preventDefault ? a.preventDefault() : a.returnValue = !1
        },
        stopPropagation: function(a) {
            a.stopPropagation ? a.stopPropagation() : a.cancelBubble = !0
        }
    };
    aa.prototype = {
        show: function() {
            6 == n.ie && (this._resize(), window.attachEvent("onresize", this._resize));
            with(this.Lay.style) 0 < n.ie ? filter = "alpha(opacity:" + this.Opacity + ")": opacity = this.Opacity / 100,
            backgroundColor = this.Color,
            display = "block"
        },
        close: function() {
            this.Lay.style.display = "none";
            6 == n.ie && window.detachEvent("onresize", this._resize)
        }
    };
    window.Uploader = x
})();