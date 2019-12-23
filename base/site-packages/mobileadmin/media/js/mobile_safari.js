addEventListener("load", function() {
    setTimeout(updateLayout, 0);
}, false);

truncateRegistry = {};
function truncate(elements) {
    for (ele in elements) {
        if (!(ele in truncateRegistry)) {
            truncateRegistry[ele] = {
                'size': elements[ele],
                'content': $(ele).innerHTML,
            };
        }
    }
}
function truncateDot(mode) {
    for (name in truncateRegistry) {
        var element = $(name);
        var ele = truncateRegistry[name];
        if (mode == 'on') {
            if (ele['content'].length > ele['size']) {
                if (ele['size'] > 3) {
                    element.innerHTML = ele['content'].substring(0,(ele['size']-3)) + '...';
                } else {
                    element.innerHTML = ele['content'].substring(0,ele['size']);
                }
            }
        } else {
            element.innerHTML = ele['content'];
        }
    }
}

var currentWidth = 0;
function updateLayout() {
    switch(window.orientation) {
        case 0:
        case 180:
            var orient = "portrait";
            truncateDot('on');
        break;

        case 90:
        case -90:
            var orient = "landscape";
            truncateDot('off');
        break;
    }
    document.body.setAttribute("orient", orient);
    setTimeout(function() {
        window.scrollTo(0, 1);
    }, 100);            
}

function $(ele) {
    return document.getElementById(ele);
}
function hasClass(ele,cls) {
    return ele.className.match(new RegExp('(\\s|^)'+cls+'(\\s|$)'));
}
function addClass(ele,cls) {
    if (!this.hasClass(ele,cls)) ele.className += " "+cls;
}
function removeClass(ele,cls) {
    if (hasClass(ele,cls)) {
        var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
        ele.className=ele.className.replace(reg,' ');
    }
}
function addAndRemoveClass(ele,_new,_old) {
    addClass(ele,_new);
    removeClass(ele,_old);
}
function switch_tabs(tabLabels) {
    function toggle() {
        var toActivate = this.id.substr(1);
        var toDeactivate = tabLabels[toActivate];
        $(toDeactivate).removeAttribute('selected');
        $(toActivate).setAttribute('selected', 'true'); 
        addAndRemoveClass($(this.id), 'active', 'inactive');
        addAndRemoveClass($("_"+toDeactivate), 'inactive', 'active');
    }
    for (label in tabLabels) {
        $("_"+label).addEventListener("click", toggle, false);
    }
}
