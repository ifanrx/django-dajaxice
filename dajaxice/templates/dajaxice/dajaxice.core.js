var Dajaxice = {
    {% with module=dajaxice_config.modules top='top' %}
    {% include "dajaxice/dajaxice_function_loop.js" %}
    {% endwith %}
    {% for name, module in dajaxice_config.modules.submodules.items %}
    {% include "dajaxice/dajaxice_module_loop.js" %},
    {% endfor %}

{% comment %}
    get_cookie: function(name)
    {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].toString().replace(/^\s+/, "").replace(/\s+$/, "");
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
{% endcomment %}
    get_cookie: function(a){var d=null;if(document.cookie&&""!=document.cookie)for(var e=document.cookie.split(";"),b=0;b<e.length;b++){var f=e[b].toString().replace(/^\s+/,"").replace(/\s+$/,"");if(f.substring(0,a.length+1)==a+"="){d=decodeURIComponent(f.substring(a.length+1));break}}return d},
{% comment %}
    call: function(dajaxice_function, method, dajaxice_callback, argv, custom_settings)
    {
        var custom_settings = custom_settings || {},
            error_callback = Dajaxice.get_setting('default_exception_callback');

        if('error_callback' in custom_settings && typeof(custom_settings['error_callback']) == 'function'){
            error_callback = custom_settings['error_callback'];
        }

        var send_data = 'argv='+encodeURIComponent(JSON.stringify(argv)),
            oXMLHttpRequest = new XMLHttpRequest,
            endpoint = dajaxice_endpoint+dajaxice_function+'/';

        if(method == 'GET'){
            endpoint = endpoint + '?' + send_data;
        }
        oXMLHttpRequest.open(method, endpoint);
        oXMLHttpRequest.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        oXMLHttpRequest.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        oXMLHttpRequest.setRequestHeader("X-CSRFToken", Dajaxice.get_cookie('{{ dajaxice_config.django_settings.CSRF_COOKIE_NAME }}'));
        oXMLHttpRequest.onreadystatechange = function() {
            if (this.readyState == XMLHttpRequest.DONE) {
                if(this.responseText == Dajaxice.EXCEPTION || !(this.status in Dajaxice.valid_http_responses())){
                    error_callback();
                }
                else{
                    var response;
                    try {
                        response = JSON.parse(this.responseText);
                    }
                    catch (exception) {
                        response = this.responseText;
                    }
                    dajaxice_callback(response);
                }
            }
        }
        if(method == 'POST'){
            oXMLHttpRequest.send(send_data);
        }
        else{
            oXMLHttpRequest.send();
        }
        return oXMLHttpRequest;
    },
{% endcomment %}
    call: function(b,d,f,c,a){a=a||{};var e=Dajaxice.get_setting("default_exception_callback");"error_callback"in a&&"function"==typeof a.error_callback&&(e=a.error_callback);c="argv="+encodeURIComponent(JSON.stringify(c));a=new XMLHttpRequest;b=dajaxice_endpoint+b+"/";"GET"==d&&(b=b+"?"+c);a.open(d,b);a.setRequestHeader("Content-Type","application/x-www-form-urlencoded");a.setRequestHeader("X-Requested-With","XMLHttpRequest");a.setRequestHeader("X-CSRFToken",Dajaxice.get_cookie("{{ dajaxice_config.django_settings.CSRF_COOKIE_NAME }}"));
a.onreadystatechange=function(){if(this.readyState==XMLHttpRequest.DONE)if(this.responseText!=Dajaxice.EXCEPTION&&this.status in Dajaxice.valid_http_responses()){var a;try{a=JSON.parse(this.responseText)}catch(b){a=this.responseText}f(a)}else e()};"POST"==d?a.send(c):a.send();return a},

    setup: function(settings)
    {
        this.settings = settings;
    },

    get_setting: function(key){
        if(this.settings == undefined || this.settings[key] == undefined){
            return Dajaxice.default_settings[key];
        }
        return this.settings[key];
    },

    valid_http_responses: function(){
        return {200: null, 301: null, 302: null, 304: null}
    },

    EXCEPTION: '{{ dajaxice_config.DAJAXICE_EXCEPTION }}',
    default_settings: {'default_exception_callback': function(){ }}
};

window['Dajaxice'] = Dajaxice;

{% comment %}
/**
* XMLHttpRequest.js Copyright (C) 2011 Sergey Ilinsky (http://www.ilinsky.com)
*
* This work is free software; you can redistribute it and/or modify
* it under the terms of the GNU Lesser General Public License as published by
* the Free Software Foundation; either version 2.1 of the License, or
* (at your option) any later version.
*
* This work is distributed in the hope that it will be useful,
* but without any warranty; without even the implied warranty of
* merchantability or fitness for a particular purpose. See the
* GNU Lesser General Public License for more details.
*
* You should have received a copy of the GNU Lesser General Public License
* along with this library; if not, write to the Free Software Foundation, Inc.,
* 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
*/
{% endcomment %}
{% if dajaxice_config.DAJAXICE_XMLHTTPREQUEST_JS_IMPORT %}
(function(){function s(){this._object=!window.XMLHttpRequest||u?new window.ActiveXObject("Microsoft.XMLHTTP"):window.XMLHttpRequest.isNormalizedObject?new n:new window.XMLHttpRequest;this._listeners=[]}function a(){return new s}function p(e){a.onreadystatechange&&a.onreadystatechange.apply(e);e.dispatchEvent({type:"readystatechange",bubbles:!1,cancelable:!1,timeStamp:(new Date).getTime()})}function t(a){try{a.responseText=a._object.responseText}catch(c){}try{var d;var g=a._object,b=g.responseXML,
h=g.responseText;k&&h&&b&&!b.documentElement&&g.getResponseHeader("Content-Type").match(/[^\/]+\/[^\+]+\+xml/)&&(b=new window.ActiveXObject("Microsoft.XMLDOM"),b.async=!1,b.validateOnParse=!1,b.loadXML(h));d=b&&(k&&0!=b.parseError||!b.documentElement||b.documentElement&&"parsererror"==b.documentElement.tagName)?null:b;a.responseXML=d}catch(f){}try{a.status=a._object.status}catch(l){}try{a.statusText=a._object.statusText}catch(m){}}function q(a){a._object.onreadystatechange=new window.Function}var n=
window.XMLHttpRequest,r=!!window.controllers,k=!!window.document.namespaces,u=k&&window.navigator.userAgent.match(/MSIE 7.0/);a.prototype=s.prototype;r&&n.wrapped&&(a.wrapped=n.wrapped);a.isNormalizedObject=!0;a.UNSENT=0;a.OPENED=1;a.HEADERS_RECEIVED=2;a.LOADING=3;a.DONE=4;a.prototype.UNSENT=a.UNSENT;a.prototype.OPENED=a.OPENED;a.prototype.HEADERS_RECEIVED=a.HEADERS_RECEIVED;a.prototype.LOADING=a.LOADING;a.prototype.DONE=a.DONE;a.prototype.readyState=a.UNSENT;a.prototype.responseText="";a.prototype.responseXML=
null;a.prototype.status=0;a.prototype.statusText="";a.prototype.priority="NORMAL";a.prototype.onreadystatechange=null;a.onreadystatechange=null;a.onopen=null;a.onsend=null;a.onabort=null;a.prototype.open=function(e,c,d,g,b){var h=e.toLowerCase();if("connect"==h||"trace"==h||"track"==h)throw Error(18);delete this._headers;3>arguments.length&&(d=!0);this._async=d;var f=this,l=this.readyState,m=null;k&&d&&(m=function(){l!=a.DONE&&(q(f),f.abort())},window.attachEvent("onunload",m));a.onopen&&a.onopen.apply(this,
arguments);4<arguments.length?this._object.open(e,c,d,g,b):3<arguments.length?this._object.open(e,c,d,g):this._object.open(e,c,d);this.readyState=a.OPENED;p(this);this._object.onreadystatechange=function(){if(!r||d)f.readyState=f._object.readyState,t(f),f._aborted?f.readyState=a.UNSENT:f.readyState==a.DONE&&(delete f._data,q(f),k&&d&&window.detachEvent("onunload",m),l!=f.readyState&&p(f),l=f.readyState)}};a.prototype.send=function(e){a.onsend&&a.onsend.apply(this,arguments);arguments.length||(e=null);
e&&e.nodeType&&(e=window.XMLSerializer?(new window.XMLSerializer).serializeToString(e):e.xml,this._headers["Content-Type"]||this._object.setRequestHeader("Content-Type","application/xml"));this._data=e;a:if(this._object.send(this._data),r&&!this._async)for(this.readyState=a.OPENED,t(this);this.readyState<a.DONE;)if(this.readyState++,p(this),this._aborted)break a};a.prototype.abort=function(){a.onabort&&a.onabort.apply(this,arguments);this.readyState>a.UNSENT&&(this._aborted=!0);this._object.abort();
q(this);this.readyState=a.UNSENT;delete this._data};a.prototype.getAllResponseHeaders=function(){return this._object.getAllResponseHeaders()};a.prototype.getResponseHeader=function(a){return this._object.getResponseHeader(a)};a.prototype.setRequestHeader=function(a,c){this._headers||(this._headers={});this._headers[a]=c;return this._object.setRequestHeader(a,c)};a.prototype.addEventListener=function(a,c,d){for(var g=0,b;b=this._listeners[g];g++)if(b[0]==a&&b[1]==c&&b[2]==d)return;this._listeners.push([a,
c,d])};a.prototype.removeEventListener=function(a,c,d){for(var g=0,b;(b=this._listeners[g])&&(b[0]!=a||b[1]!=c||b[2]!=d);g++);b&&this._listeners.splice(g,1)};a.prototype.dispatchEvent=function(a){a={type:a.type,target:this,currentTarget:this,eventPhase:2,bubbles:a.bubbles,cancelable:a.cancelable,timeStamp:a.timeStamp,stopPropagation:function(){},preventDefault:function(){},initEvent:function(){}};"readystatechange"==a.type&&this.onreadystatechange&&(this.onreadystatechange.handleEvent||this.onreadystatechange).apply(this,
[a]);for(var c=0,d;d=this._listeners[c];c++)d[0]!=a.type||d[2]||(d[1].handleEvent||d[1]).apply(this,[a])};a.prototype.toString=function(){return"[object XMLHttpRequest]"};a.toString=function(){return"[XMLHttpRequest]"};window.Function.prototype.apply||(window.Function.prototype.apply=function(a,c){c||(c=[]);a.__func=this;a.__func(c[0],c[1],c[2],c[3],c[4]);delete a.__func});window.XMLHttpRequest=a})();
{% endif %}

{% comment %}
/*
json2.js
2013-05-26
https://github.com/douglascrockford/JSON-js
*/
{% endcomment %}
{% if dajaxice_config.DAJAXICE_JSON2_JS_IMPORT %}
"object"!==typeof JSON&&(JSON={});
(function(){function m(a){return 10>a?"0"+a:a}function r(a){s.lastIndex=0;return s.test(a)?'"'+a.replace(s,function(a){var c=u[a];return"string"===typeof c?c:"\\u"+("0000"+a.charCodeAt(0).toString(16)).slice(-4)})+'"':'"'+a+'"'}function p(a,l){var c,d,h,q,g=e,f,b=l[a];b&&"object"===typeof b&&"function"===typeof b.toJSON&&(b=b.toJSON(a));"function"===typeof k&&(b=k.call(l,a,b));switch(typeof b){case "string":return r(b);case "number":return isFinite(b)?String(b):"null";case "boolean":case "null":return String(b);
case "object":if(!b)return"null";e+=n;f=[];if("[object Array]"===Object.prototype.toString.apply(b)){q=b.length;for(c=0;c<q;c+=1)f[c]=p(c,b)||"null";h=0===f.length?"[]":e?"[\n"+e+f.join(",\n"+e)+"\n"+g+"]":"["+f.join(",")+"]";e=g;return h}if(k&&"object"===typeof k)for(q=k.length,c=0;c<q;c+=1)"string"===typeof k[c]&&(d=k[c],(h=p(d,b))&&f.push(r(d)+(e?": ":":")+h));else for(d in b)Object.prototype.hasOwnProperty.call(b,d)&&(h=p(d,b))&&f.push(r(d)+(e?": ":":")+h);h=0===f.length?"{}":e?"{\n"+e+f.join(",\n"+
e)+"\n"+g+"}":"{"+f.join(",")+"}";e=g;return h}}"function"!==typeof Date.prototype.toJSON&&(Date.prototype.toJSON=function(){return isFinite(this.valueOf())?this.getUTCFullYear()+"-"+m(this.getUTCMonth()+1)+"-"+m(this.getUTCDate())+"T"+m(this.getUTCHours())+":"+m(this.getUTCMinutes())+":"+m(this.getUTCSeconds())+"Z":null},String.prototype.toJSON=Number.prototype.toJSON=Boolean.prototype.toJSON=function(){return this.valueOf()});var t=/[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,
s=/[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,e,n,u={"\b":"\\b","\t":"\\t","\n":"\\n","\f":"\\f","\r":"\\r",'"':'\\"',"\\":"\\\\"},k;"function"!==typeof JSON.stringify&&(JSON.stringify=function(a,l,c){var d;n=e="";if("number"===typeof c)for(d=0;d<c;d+=1)n+=" ";else"string"===typeof c&&(n=c);if((k=l)&&"function"!==typeof l&&("object"!==typeof l||"number"!==typeof l.length))throw Error("JSON.stringify");return p("",{"":a})});
"function"!==typeof JSON.parse&&(JSON.parse=function(a,e){function c(a,d){var g,f,b=a[d];if(b&&"object"===typeof b)for(g in b)Object.prototype.hasOwnProperty.call(b,g)&&(f=c(b,g),void 0!==f?b[g]=f:delete b[g]);return e.call(a,d,b)}var d;a=String(a);t.lastIndex=0;t.test(a)&&(a=a.replace(t,function(a){return"\\u"+("0000"+a.charCodeAt(0).toString(16)).slice(-4)}));if(/^[\],:{}\s]*$/.test(a.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,"@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,
"]").replace(/(?:^|:|,)(?:\s*\[)+/g,"")))return d=eval("("+a+")"),"function"===typeof e?c({"":d},""):d;throw new SyntaxError("JSON.parse");})})();
{% endif %}
