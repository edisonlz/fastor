(function(o){
if(!o || o.MHeader){ return; }

//global domain
document.domain = 'youku.com';

//define variable
var toDomain = function(s){ s = s.replace('http://', ''); if(s[s.length -1] == '/'){ s = s.substr(0, s.length-1); }; return s; }
var DOMAIN_NC = toDomain(nc_domain)
	,isTouch = 'createTouch' in document
	,clickevent = 'click'
	,UA = window.navigator.userAgent.toLowerCase()
	,isIOS = (/iphone|ipad|ipod|itouch|ios/g).test(UA)
	,isSONY = (
			UA.indexOf('sony') != -1
		  	|| ((/lt\d+/g).test(UA) && UA.indexOf('360browser'))
		  ) ? true : false;

//header class
var MHeader = {
	ids: {'headerbox': 'mheader_box', 'header': 'mheader'},
	dropmenuGroup: null,
	node: null,
	jsres: typeof(mheaderjs) == 'object' ? mheaderjs : null,
	ready: false,
	status: 'fixed',
	rule: 'fixed',
	init: function(){
		this.header = document.getElementById(this.ids.header);
		this.headerbox = document.getElementById(this.ids.headerbox);
		if(!this.header){ return; }
		this.headercss = document.getElementById('headercss');
		var csslink = document.createElement('link');
		if(csslink){
			csslink.type = 'text/css';
			csslink.rel = 'stylesheet';
			csslink.href = this.headercss.href;
			document.getElementsByTagName('head')[0].appendChild(csslink);
		}
		this.bind();
		//优先执行的功能不依赖资源加载
		this.Nav.init();
		//this.Search.initCore();//搜索功能
		//依赖打印代码中的资源声明打印
		if(!this.jsres){ return; }
		var _this = this, canrun = false, runed = false;;

		//运行时检测依赖脚本, 如加载立即运行
		var timer = setInterval(function(){

			if(_this.chkres('relyon')){
				canrun = true;
				clearInterval(timer);
				if(!runed){ _this.bindfns(); runed = true; }
			}
		}, 10);
		//domready后检测依赖脚本, 添加未包含的脚本, 并加载附加功能
		domReady(function(){
			clearInterval(timer); timer = null;
			canrun = canrun || _this.chkres('relyon');
			var addons = function(){
				_this.chkres('addons');
				_this.loadres('addons');
			}
			if(!canrun){
				_this.loadres('relyon', function(){
					var relyon = _this.jsres.relyon;
					for(var i=0; i<relyon.length; i++){
						if(relyon[i].ready !== true){ return; }
					}
					if(!runed){ _this.bindfns(); runed = true; }
					addons();
				});
			}else{
				if(!runed){ _this.bindfns(); runed = true; }
				addons();
			}

		});
	},
	bind: function(){
		var _this = this;
		domReady(function(){
			var timer = setInterval(function(){
				if(_this.ready){
					var t = null;
					var selector = 'textarea,input[txtfor!=headersearch],select';
					$(document)
					.on('focus', selector, function(){
						t = $(this);
						_this.unfix();
					})
					.on('blur', selector, function(){
						var n = $(this);//失焦获焦UI处理延时
						setTimeout(function(){
							//不是通过另一域获焦而失焦
							if(n.get(0) == t.get(0)){ _this.dofix(); }
						}, 50)
					});
					clearInterval(timer);
				}
			}, 25);
		});
	},
	bindfns: function(){
		this.ready = true;
		this.dropmenuGroup = new DropmenuGroup();
		//this.Search.init();
		this.Userlog.init();
		this.Looking.init();
		this.Channel.init();
	},
	dofix: function(){
		return this.changeRule('fixed');
	},
	unfix: function(){
		return this.changeRule('static');
	},
	changeRule: function(rule){
		if(rule != this.rule){
			this.rule = rule;
			this.changePos('setrule');
		}
		return this;
	},
	changePos: function(type){//@param type 按规则设置'setrule'，滚动中频发 'scroll'
		var ready = typeof($) == 'function' ? true : false;//jquery ready
		var headerbox = ready ? $(this.headerbox) : this.headerbox;

		if(this.rule == 'fixed' && this.status != 'fixed'){
			if(ready){ headerbox.css({'position': 'fixed'}); }
			else{ headerbox.style.position = 'fixed'; }
			this.status = 'fixed';
		}else if(this.rule == 'static' && this.status != 'static'){
			if(ready){ headerbox.css({'position': 'relative'});}
			else{ headerbox.style.position = 'relative';	}
			this.status = 'static';
		}

		return this;
	},
	loadres: function(key, callback){
		var res = this.jsres[key];
		var _this = this;
		var callback = typeof(callback) == 'function' ? callback : function(){};
		for(var i=0; i<res.length; i++){
			(function(i){
				if(res[i].ready === false){
					_this.jsres[key][i].ready = 'loading';
					addScript(_this.jsres[key][i].src, function(){
						_this.jsres[key][i].ready = true;
						callback();
					});
				}
			})(i);
		}
	},
	chkres: function(key){//同步加载状态下 检测依赖的JS资源
		var res = this.jsres[key];
		if(!res){ return true; }
		var _this = this;
		var scripts = document.getElementsByTagName('script');
		for(var i=0; i<scripts.length; i++){
			var script = scripts[i];
			for(var j=0; j<res.length; j++){
				if(script.src && script.src == res[j].src){

					(function(script, key, j){
						if(!_this.jsres[key][j].ready && eval(_this.jsres[key][j].condition)){
							_this.jsres[key][j].ready = true;
						}
					})(script, key, j);
				}
			}
		}
		for(var i=0; i<this.jsres[key].length; i++){
			if(this.jsres[key][i].ready !== true){
				return false;
			}
		}
		return true;
	}
}

MHeader.Userlog = {
	uid: 0,
	lock: false,
	init: function(){
		this.logbefore = $('#mheader_logbefore');
		this.logafter = $('#mheader_logafter');
		if(!this.logbefore.length || !this.logafter.length){return; }
		var handle = $('#mheader_userlog_handle');
		var panel = $('#mheader_userlog_panel');
		if(!handle.length || !panel.length){return; }
		/*this.dp = new Dropmenu({
			'group': MHeader.dropmenuGroup,
			'handle': handle,
			'panel': panel
		});*/
		this.update();
		this.bind();
	},
	bind: function(){
		var _this = this;
		this.logbefore.bind(clickevent, function(e){
			login();
		});
		$(document).bind('userchange', function(){
			_this.update();
		});
	},
	show: function(){
		if(this.dp){ this.dp.show(); }
		return this;
	},
	hide: function(){
		if(this.dp){ this.dp.hide(); }
		return this;
	},
	getLogStatus: function(){
		if(islogin()){ return true; }
		return false;
	},
	changest: function(type){
		var _this = this;
		if(type == 'login' && this.logbefore.css('display') == 'block'){
			this.logbefore.stop().animate({'opacity': 0}, 250, '', function(){
				_this.logbefore.hide();
				_this.logafter.css({'opacity': 0}).show().stop().animate({'opacity':1}, 250, '', function(){
				});
			});
		}else if(type == 'logout' && this.logafter.css('display') == 'block'){
			this.logafter.stop().animate({'opacity': 0}, 250, '', function(){
				_this.logafter.hide();
				_this.logbefore.css({'opacity': 0}).show().stop().animate({'opacity':1}, 250, '', function(){
				});
			});
		}
	},
	update: function(){
		var st = this.getLogStatus();
		this.uid = this.getUID();
		var _this = this;
		if(st){
			this.getUserinfo();
		}else{
			this.changest('logout');
			this.uid = 0;
		}
		return this;
	},
	drawUserinfo: function(html){
		this.lock = false;
		if(html == 'null'){ //exception
			this.changest('logout');
			this.uid = 0;
			return this;
		}else{
			var _this = this;
			var tmp = html.split('====================');
			var html_handle = tmp[0]
				,html_panel = tmp[1]
			$('#mheader_userlog_handle').html(html_handle);
			/*_this.dp.update(html_panel);
			$('#mheader_logout').bind(clickevent, function(e){
				//登出过快，面板消失， 小米浏览器会触发， 处于面板下部的点击行为
				logout(function(){
					setTimeout(function(){
						_this.hide();
					}, 200);
				});
				e.preventDefault();
				return false;
			});*/
			this.changest('login');
		}

		return this;
	},
	getUserinfo: function(){
		if(this.lock){ return; }
		this.lock = true;
		var url = 'http://'+ DOMAIN_NC + '/index_MHeaderJSONP?function[]=userinfo&callback[]=MHeader.Userlog.drawUserinfo'
		addScript(url, null, true);
	},
	getUID: function(){
		if(!islogin()){ return 0; }
		var ckie = Cookie.get('yktk');
		var uid = 0;
		if(ckie){
			try{
				var u_info = decode64(decodeURIComponent(ckie).split('|')[3]);
				if(u_info.indexOf(',') > -1 && u_info.indexOf('nn:') > -1 && u_info.indexOf('id:') > -1){
					uid = u_info.split(',')[0].split(':')[1];
				}
			}catch(e){ }
		}

		return parseInt(uid);
	}
}

MHeader.Looking = {
	scroller: null,
	init: function(){
		var handle = $('#mheader_looking_handle');
		var panel = $('#mheader_looking_panel');
		if(!handle.length || !panel.length){ return; }
		this.dp = new Dropmenu({
			'group': MHeader.dropmenuGroup,
			'handle': handle,
			'panel': panel
		});
		this.bind();
	},
	bind: function(){
		var _this = this;
		this.dp.setCallback('show', function(){
			_this.show();
		});

		var en = 'onorientationchange' in window ? 'orientationchange' : 'resize';
		addEvent(window, en, function(){
			if(_this.scroller){
				_this.scroller.refresh();
			}
		});

	},
	initScroller: function(){
		var list = $('#mheader_lookinglist');
		if(list.length){
			var w = 160, count=list.find('li').length, ul = list.find('ul');
			if(count != 0){
				ul.css({'width': w*count});
				this.scroller = new iScroll('mheader_lookinglist', {
					bounce:true,
					vScroll:false,
					hScrollbar:false,
					vScrollbar:false
				});
			}
		}
	},
	show: function(){
		if(!this.dp){ return this; }
		this.getList();
		this.dp.show();
		return this;
	},
	hide: function(){
		if(this.dp){ this.dp.hide(); }
		return this;
	},
	getList: function(){
		if(!this.dp){ return this; }
		this.dp.update('<div class="yk-panel-records">\
					   <div class="yk-records-loading"><i class="ico-loading"></i></div>\
					   </div>');
		var t = +new Date();
		var url = 'http://'+ DOMAIN_NC + '/index_MHeaderJSONP?function[]=looking&callback[]=MHeader.Looking.drawList&t=' + t;
		addScript(url, null, true);
	},
	drawList: function(html){
		this.dp.update(html);
		this.bindList();
		return this;
	},
	bindList: function(){
		var _this = this;
		var logafter = function(){ _this.show(); }
		//userlog
		var username = $('#mheader_looking_username');
		if(username.length){
			username.html(truncate(username.html(), 8, '...'));
		}
		$('#mheader_looking_login').bind(clickevent, function(e){
			login(function(){ logafter();	});
			return false;
		});
		$('#mheader_looking_login2').bind(clickevent, function(e){
			login(function(){ logafter(); });
			return false;
		});
		$('#mheader_looking_logout').bind(clickevent, function(e){
			//登出过快，面板消失， 小米浏览器会触发， 处于面板下部的点击行为
			logout(function(){
				setTimeout(function(){
					_this.hide();
				}, 200);
			});
			e.preventDefault();
			return false;
		});

		this.initScroller();

		return this;
	}
}
/*
MHeader.Search = {
	init: function(){
		var handle = $('#mheader_search_handle');
		var panel = $('#mheader_search_panel');
		if(!handle.length || !panel.length){ return; }
		this.dp = new Dropmenu({
			'group': MHeader.dropmenuGroup,
			'handle': handle,
			'panel': panel
		});
		this.bind();
	},
	bind: function(){
		var _this = this;
		var input2 = $('#mheader_search2').find('input');

		this.dp.setCallback('show', function(){
			if(isIOS){
				MHeader.unfix();
				document.body.scrollTop = 0;
				input2.focus();
			}else{
				if(isSONY){
					setTimeout(function(){
						input2.focus();
					}, 100);
				}else{
					input2.focus();
				}

			}
		});
		this.dp.setCallback('hide', function(){
			input2.blur();
		});
	},
	/*initCore: function(){
		var input1 = document.getElementById('mheader_search').getElementsByTagName('input')[0]
			,input2 = document.getElementById('mheader_search2').getElementsByTagName('input')[0]
			,s3 = document.getElementById('mheader_search3')
			,input3 = s3 ? s3.getElementsByTagName('input')[0] : null;
		var _this = this;
		var dofocus = function(input){
			if(isIOS){
				MHeader.unfix();
				document.body.scrollTop = 0;
			}
		}
		var fillkey = function(input){
			var val = input.value;
			if(input1 != input){ input1.value = val; }
			if(input2 != input){ input2.value = val; }
			if(input3){
				if(input3 != input){ input3.value = val; }
			}
		}

		//pad search
		addEvent(input1, 'focus', function(){
			dofocus(input1);
		});
		addEvent(input1, 'blur', function(){
			MHeader.dofix();
			fillkey(input1);
		});
		addEvent(input1, 'keyup', function(){
			fillkey(input1);
		});
		//phone panel search
		addEvent(input2, 'focus', function(){

		});
		addEvent(input2, 'blur', function(){
			MHeader.dofix();
			fillkey(input2);
		});
		addEvent(input2, 'keyup', function(){
			fillkey(input2);
		});
		//phone search
		if(input3){
			addEvent(input3, 'focus', function(){
				dofocus(input3);
			});
			addEvent(input3, 'blur', function(){
				MHeader.dofix();
				fillkey(input3);
			});
			addEvent(input3, 'keyup', function(){
				fillkey(input3);
			});
		}
	},
	doSearch: function(form){
		if(!form){ return false; }
		var input = form.getElementsByTagName('input')[0];
		var q = trim(input.value);
		var url = '';
		if(!q || q == input.defaultValue){
			url = 'http://www.soku.com?inner';
		}else{
			q = encodeURIComponent(q);
			url= form.action + '/q_'+q;
		}
		window.open(url);
		return false;
	}
}
*/
MHeader.Channel = {
	init: function(){
		var handle  =$('#mheader_channel_handle');
		var panel = $('#mheader_channel_panel');
		if(!handle.length || !panel.length){ return; }
		this.dp = new Dropmenu({
			'group': MHeader.dropmenuGroup,
			'handle': handle,
			'panel': panel
		});
	},
	show: function(){
		if(this.dp){ this.dp.show(); }
		return this;
	},
	hide: function(){
		if(this.dp){ this.dp.hide(); }
		return this;
	}
}

MHeader.Nav = {
	scroller: null,
	init: function(){
		var nav = document.getElementById('mheader_nav');
		if(!nav){ return; }
		this.bind();
	},
	bind: function(){
		var _this = this;

		this.initScroller();
		var box = document.getElementById('mheader_navbox')
		var cur = this.findCurrent();
		var inview = true;
		if(cur){
			var posbox = getElementPos(box).x
				,poscur = getElementPos(cur).x
				,wbox = box.offsetWidth;

			if( poscur >= (posbox + wbox)  //整个溢出
				|| (poscur+cur.offsetWidth) > (posbox + wbox) //半截不可见
			){
				inview = false;
			}
		}
		if(!inview){
			//居中
			var x = cur.offsetLeft + cur.offsetWidth/2 - box.offsetWidth/2;
			this.scroller.scrollTo(-x, 0, 0);
		}

		var en = 'onorientationchange' in window ? 'orientationchange' : 'resize';
		addEvent(window, en, function(){
			if(_this.scroller){
				var getWidth = function(){
					var w = 0;
					for(var i=0; i<lis.length; i++){
						w += (lis[i].offsetWidth + parseInt(getStyle(lis[i], 'marginRight')));
					}
					return w;
				}
				var ul = document.getElementById('mheader_navbox').getElementsByTagName('ul')[0]
					,lis = ul.getElementsByTagName('li');
				ul.style.width = getWidth() + 'px';
				_this.scroller.refresh();
			}
		});

	},
	initScroller: function(){
		var box = document.getElementById('mheader_navbox')
			,mr = 48
			,ul = box.getElementsByTagName('ul')[0]
			,lis = ul.getElementsByTagName('li');

		//margin-right 定义不同
		var getWidth = function(){
			var w = 0;
			for(var i=0; i<lis.length; i++){
				w += (lis[i].offsetWidth + parseInt(getStyle(lis[i], 'marginRight')));
			}
			return w;
		}

		ul.style.width = getWidth() + 'px';

		this.scroller = new iScroll('mheader_navbox', {
			bounce:true,
			vScroll:false,
			hScrollbar:false,
			vScrollbar:false
		});

	},
	findCurrent: function(){
		var box = document.getElementById('mheader_navbox')
			,ul = box.getElementsByTagName('ul')[0]
			,lis = ul.getElementsByTagName('li');
		var li = null;
		for(var i=0; i<lis.length; i++){
			var l = lis[i];
			if(l.className && l.className == 'current'){
				li = l;
				break;
			}
		}
		return li;
	}
}

var DropmenuGroup = function(){
	this.coll = [];
	this.bind();
}
DropmenuGroup.prototype = {
	bind: function(){
		var _this = this;
		var y0 = 0, y1 = 0;
		$(document).bind(isTouch ? 'touchstart' : 'click', function(e){
			_this.hideAll();
		});
	},
	getLength: function(){
		return this.coll.length;
	},
	isExist: function(dropmenu){
		var len = this.getLength();
		for(var i=0; i<len; i++){
			if(this.coll[i] == dropmenu){
				return true;
			}
		}
		return false;
	},
	add: function(dropmenu){
		if(dropmenu instanceof Dropmenu && !this.isExist(dropmenu)){
			this.coll.push(dropmenu);
		}
		return this;
	},
	remove: function(dropmenu){
		var len = this.getLength();
		for(var i=0; i<len; i++){
			if(this.coll[i] == dropmenu){
				this.coll.splice(i, 1);
				break;
			}
		}
		return true;
	},
	hideAll: function(){
		var len = this.getLength();
		for(var i=0; i<len; i++){
			this.coll[i].hide();
		}
		return this;
	},
	hideOther: function(dropmenu){
		var len = this.getLength();
		for(var i=0; i<len; i++){
			if(this.coll[i] != dropmenu){
				this.coll[i].hide();
			}
		}
		return this;
	}
}

var Dropmenu = function(params){
	var params = typeof(arguments[0]) == 'object' ? params : {}
	this.group = params.group ? params.group : new DropmenuGroup();
	this.handle = params.handle.length ? params.handle : null;
	this.panel = params.panel.length ? params.panel : null;
	this.callback = params.callback ? params.callback : {};
	this.mask = null;
	this.status = 'hide';
	if(!this.handle || !this.panel){ return; }
	this.classname = {'handle': 'yk-handle-expand',	'mask': 'yk-panel-mask'};
	this.callback =  {
		'show': typeof(this.callback.show) == 'function' ? this.callback.show : null,
		'hide':	typeof(this.callback.hide) == 'function' ? this.callback.hide : null
	}
	this.init();
}
Dropmenu.prototype = {
	init: function(){
		this.group.add(this);//向菜单组添加
		this.bind();
	},
	bind: function(){
		var _this = this;
		if(!isSONY){
			this.handle
			.bind('click', function(e){//ios headerfix !touchstart //widnow scroll 意外触发
				_this.toggle();
				return false;
			})
			.bind('touchstart', function(e){
				e.stopPropagation();
			});
		}else{
			this.handle.bind('touchstart', function(e){//sony phone //click 有时不触发
				_this.toggle();
				e.stopPropagation();
				return false;
			});
		}

		this.panel.bind('touchstart click', function(e){
			e.stopPropagation();
		});
	},
	setCallback: function(type, func){
		if(type == 'show' && typeof(func) == 'function'){ this.callback.show = func; }
		if(type == 'hide' && typeof(func) == 'function'){ this.callback.hide = func; }
		return this;
	},
	update: function(html){
		this.panel.html(html + '<iframe scrolling="0" frameborder="0" class="'+ this.classname.mask +'"></iframe>');
		return this;
	},
	show: function(){
		if(this.status == 'show'){ return this; }
		this.group.hideOther(this);
		this.handle.addClass(this.classname.handle);
		this.panel.show();
		if(!this.panel.find('.' + this.classname.mask).length){
			this.panel.append($('<iframe scrolling="0" frameborder="0" class="'+ this.classname.mask +'"></iframe>'));
		}
		this.status = 'show';
		H5Player.hide();
		if(this.callback.show){ this.callback.show(); }
		return this;
	},
	hide: function(){
		if(this.status == 'hide'){ return this; }
		this.handle.removeClass(this.classname.handle);
		this.panel.hide();
		this.status = 'hide';
		H5Player.show();
		if(this.callback.hide){ this.callback.hide(); }
		return this;
	},
	toggle: function(){
		var status = this.getStatus();
		if(status == 'hide'){ return this.show();	}
		else{ return this.hide(); }
	},
	getStatus: function(){
		return this.status;
	}
}

//private method
var domReady = function(callback){
	var timer = null;
	var isready = false;
	var callback = typeof(callback) == 'function' ? callback : function(){};
	if(document.addEventListener){
		document.addEventListener("DOMContentLoaded", function(){
			if(!isready){ isready = true; callback(); }
		}, false);
	}else if(document.attachEvent){
		document.attachEvent("onreadystatechange", function(){
			if((/loaded|complete/).test(document.readyState)){
				if(!isready){ isready = true; callback(); }
			}
		});
		if(window == window.top){
			timer = setInterval(function(){
				if(isready){ clearInterval(timer); timer=null; return; }
				try{
					document.documentElement.doScroll('left');
				}catch(e){
					return;
				}
				if(!isready){ isready = true; callback(); }
			},5);
		}
	}
}

var addScript = function(src, callback, isremove){
	if(typeof(arguments[0]) != 'string'){ return; }
	var callback = typeof(arguments[1]) == 'function' ? callback : function(){};
	var isremove = typeof(arguments[2]) == 'boolean' ? isremove : false;
	var head = document.getElementsByTagName('HEAD')[0];
	var script = document.createElement('SCRIPT');
	script.type = 'text/javascript';
	script.src = src;
	head.appendChild(script);
	if(!/*@cc_on!@*/0) {
		script.onerror = script.onload = function(){
			callback();
			if(isremove){ script.parentNode.removeChild(this); }
		}
	}else{
		script.onreadystatechange = function () {
			if (this.readyState == 'loaded' || this.readyState == 'complete') {
				callback();
				if(isremove){ this.parentNode.removeChild(this); }
			}
		}
	}
}

var addEvent = function(dom, eventname, func){
	if(window.addEventListener){
		if(eventname == 'mouseenter' || eventname == 'mouseleave'){
			function fn(e){
				var a = e.currentTarget, b = e.relatedTarget;
				if(!elContains(a, b) && a!=b){
					func.call(e.currentTarget,e);
				}
			}
			function elContains(a, b){
				try{ return a.contains ? a != b && a.contains(b) : !!(a.compareDocumentPosition(b) & 16); }catch(e){}
			}
			if(eventname == 'mouseenter'){
				dom.addEventListener('mouseover', fn, false);
			}else{
				dom.addEventListener('mouseout', fn, false);
			}
		}else{
			dom.addEventListener(eventname, func, false);
		}
	}else if(window.attachEvent){
		dom.attachEvent('on' + eventname, func);
	}
}

var cancelBubble = function(evt){
	var evt = window.event || evt;
	if(evt.stopPropagation){
		evt.stopPropagation();
	}else{
		evt.cancelBubble=true;
	}
	return false;
}

var preventDefault = function(evt){
	var evt = window.event || evt;
	if(evt.preventDefault){
		evt.preventDefault();
	}else{
		event.returnValue = false;
	}
	return false;
}

var getElementPos = function(o){
	var point = {x:0, y:0};
	if (o.getBoundingClientRect) {
		var x=0, y=0;
		try{
			var box = o.getBoundingClientRect();
			var D = document.documentElement;
			x = box.left + Math.max(D.scrollLeft, document.body.scrollLeft) - D.clientLeft;
			y = box.top + Math.max(D.scrollTop, document.body.scrollTop) - D.clientTop;
		}catch(e){}
		point.x = x;
		point.y = y;
	}else{
		function pageX(o){ try {return o.offsetParent ? o.offsetLeft +  pageX(o.offsetParent) : o.offsetLeft; } catch(e){ return 0; } }
		function pageY(o){ try {return o.offsetParent ? o.offsetTop + pageY(o.offsetParent) : o.offsetTop; } catch(e){ return 0; } }
		point.x = pageX(o);
		point.y = pageY(o);
	}
	return point;
}

var getMousePos = function(e){
	var point = {x:0, y:0};
	if(typeof window.pageYOffset != 'undefined') {
		point.x = window.pageXOffset;
		point.y = window.pageYOffset;
	}else if(typeof document.compatMode != 'undefined' && document.compatMode != 'BackCompat') {
		point.x = document.documentElement.scrollLeft;
		point.y = document.documentElement.scrollTop;
	}else if(typeof document.body != 'undefined') {
		point.x = document.body.scrollLeft;
		point.y = document.body.scrollTop;
	}
	point.x += e.clientX;
	point.y += e.clientY;

	return point;
}

var getStyle = function(obj, attribute){
	return obj.currentStyle ? obj.currentStyle[attribute] : document.defaultView.getComputedStyle(obj, false)[attribute];
}

var trim = function(s){
	s = s.replace( /^(\s*|　*)/, '');
	s = s.replace( /(\s*|　*)$/, '');
	return s;
}
//cn
var truncate = function(s,length, truncation){
	var reg = /[\u4e00-\u9fa5]/;
	var count = 0, t = '';
	for(var i=0, len=s.length; i<len; i++){
		var char = s.charAt(i);
		if(reg.test(char)){ count ++; }
		else{ count += 0.8;	}
		t += char;
		if(count>=len || count + 0.1 > length){
			if(i != len-1){ t+= truncation; } break;
		}
	}
	return t;
}

var hz = function(cp, cpp){
	var url = 'http://hz.youku.com/red/click.php?tp=1&cp=' + cp +'&cpp=' + cpp + '&tp='+Math.random()
	var img = new Image();
	img.src = url;
}

//for IOS video mask
var H5Player = {
	show: function(){
		if($('#player').length){
			$("#player").css('visibility','visible');
		}
	},
	hide: function(){
		if($('#player').length){
			$("#player").css('visibility','hidden');
		}
	}
}

var Cookie = {
	set: function (name, value, days){
		var expires = '';
		if (days){
			var date = new Date();
			date.setTime(date.getTime()+(days*24*60*60*1000));
			expires += date.toGMTString();
		}
		document.cookie = name+ '=' + value + expires+'; path=/';
	},
	get: function (name){
		var nameEQ = name + '=';
		var ca = document.cookie.split(';');
		for(var i=0;i < ca.length;i++){
			var c = ca[i];
			while (c.charAt(0)==' '){
				c = c.substring(1,c.length);
			}
			if(c.indexOf(nameEQ) == 0){
				return c.substring(nameEQ.length,c.length);
			}
		}
		return null;
	}
}

//init
o.MHeader = MHeader;
MHeader.init();

})(window);