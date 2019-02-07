(function() {
  var frame = document.querySelectorAll("pre.frame");
  for(var i = 0; i < frame.length; i++) {
    var framecode = frame[i].innerHTML
    paint(framecode, frame[i])
  }
  
  function paint(code, elem) {

    var otag = /(\u0026lt\u003b)([\w-]+)(.*?)(\u0026gt\u003b)/g;
    var ctag = /(\u0026lt\u003b\u002f)([\w-]+)(\u0026gt\u003b)/g;
    var attr = /(.+?)([\w-]+\s*)(\u003d\s*)((?:\u0026quot\u003b|\u0022|\u0027)?[\w\d\s-]+(?:\u0026quot\u003b|\u0022|\u0027)?)/g;

    var attr = /(.+?)([\w-]+\s*)(\u003d\s*)((?:(?:\u0026quot\u003b)?.*?(?:\u0026quot\u003b)?|\u0022*.*?\u0022*|\u0027*.*?\u0027*))/g;
    var painted = `${code}`.replace(attr, '$1<span class="attr">$2</span><span class="sign">$3</span><span class="attrv">$4</span>')
    painted = painted.replace(otag, '<span class="sign">$1</span><span class="tag">$2</span>$3<span class="sign">$4</span>')
    painted = painted.replace(ctag, '<span class="sign">$1</span><span class="tag">$2</span><span class="sign">$3</span>')
    elem.innerHTML = painted;
    //alert(painted);
  }
})()