function Dispose() {
    Height = document.getElementById("Pagina").offsetHeight;
    header = document.getElementById("Header").offsetHeight;
    footer = document.getElementById("Pie").offsetHeight;
    panelheight = Height - header - footer;
    document.getElementById('Contenido').style.height = panelheight + "px"}


function Play(Url,Title){
  window.open(Url);
}

function Play_VLC(Url,Title){
  HtmlItem =
      '<div class="VideoCaja"><div class="VideoContenido"><object classid="clsid:9BE31822-FDAD-461B-AD51-BE1D1C159921" codebase="http://downloads.videolan.org/pub/videolan/vlc/latest/win32/axvlc.cab" id="vlc" events="False" style="width:100%; height:100%"><param name="Src" value="' +
      Url +
      '"></param><param name="ShowDisplay" value="True"></param><param name="AutoLoop" value="no"></param><param name="AutoPlay" value="yes"></param><embed type="application/x-google-vlc-plugin" name="vlcfirefox" autoplay="yes" loop="no" width="100%" height="100%" target="' +
      Url + '"></embed></object></div></div>';
  AbrirPlayer(Title,HtmlItem)

}

function Play_HTML(Url,Title){
  HtmlItem =
      '<div class="VideoCaja"><div class="VideoContenido"><video class="Reproductor" id="media" type="application/x-mplayer2" width="100%" height="100%" autoplay="true" controls="true" src="' +
      Url + '"></div></div>';
  AbrirPlayer(Title,HtmlItem)
}

function ImgError(obj){
  if (obj.src.indexOf("http") == 0){
  
  if (obj.src.indexOf(obj.alt) !== 0){
    obj.src=obj.alt+"/proxy/"+encodeURIComponent(btoa(obj.src))
  }else{
    obj.style.display="none";
    try{ 
        obj.parentNode.children[1].style.display="inline-block"
    }catch(e){
    }
  }
  }else{ImgLocal(obj)}
}

function ImgLocal(obj){
  if (obj.src.indexOf(obj.alt) !== 0){
    obj.src=obj.alt+"/local/"+encodeURIComponent(btoa(obj.src))
  }else{obj.style.display="none"}
}

function CargarInfo(obj) {
    if (obj.children[0].children[0].style.display == "none") {
        document.getElementById("Info-Img").src = obj.children[0].children[1].src
    } else {
        document.getElementById("Info-Img").src = obj.children[0].children[0].src
    }
    document.getElementById("Info-Plot").innerHTML = obj.children[2].innerHTML.replace(/\n/g,"<br>")
    document.getElementById("Info-Title").innerHTML   = obj.children[1].innerHTML
    document.getElementById("Info-Img").style.display="block"
    document.getElementById("Info-Plot").style.display="block"
    document.getElementById("Info-Title").style.display="block"
    document.getElementById("InfoVersion").style.display="none"
    
    document.getElementById('Info-Plot').scrollTop = 0
    a = document.getElementById('Info-Plot').scrollHeight
    clearInterval(PlotInterval)
    if (a > document.getElementById('Info-Plot').offsetHeight){
      document.getElementById("Info-Plot").innerHTML =  document.getElementById("Info-Plot").innerHTML + document.getElementById("Info-Plot").innerHTML
      PlotInterval = setInterval(function() {
        document.getElementById('Info-Plot').scrollTop += 1;
        if (document.getElementById('Info-Plot').scrollTop == a){
          document.getElementById('Info-Plot').scrollTop = 0 
        }
      }, 80);
    }
}

function DesCargarInfo(obj) {
    clearInterval(PlotInterval)
    document.getElementById("InfoVersion").style.display="block"
    document.getElementById("Info-Img").style.display="none"
    document.getElementById("Info-Plot").style.display="none"
    document.getElementById("Info-Title").style.display="none"
}

function MostrarSeccion(Seccion) {
    document.getElementById("Config").scrollTop = 0;
    for (var key in Opciones) {
        if (key == Seccion) {
            document.getElementById("Config-" + key).style.display ="block";
        } else {
            document.getElementById("Config-" + key).style.display ="none";
        }
    }
}

function Back() {
    if (Navegacion.length > 1) {
        Anterior = Navegacion[Navegacion.length - 2];
        if (typeof(Anterior.Data) == 'undefined') { 
            Navegacion.splice(Navegacion.length - 1, 1);
            DescargarContenido(Anterior.Url);
        } else {
            Navegacion.splice(Navegacion.length - 1, 1);
            document.getElementById("Contenedor").innerHTML = Anterior.Data;
            document.getElementById("Contenedor").children[0].children[Anterior.Focus].children[0].focus();
            document.getElementById("Contenedor").scrollTop =Anterior.Scroll;
            ActualizarNavegacion()

        }
    }
    

}
function  ChangeSetting(setting){ 
/**
  element
  node = setting
  while (node.className != "ListItem"){
  node = node.parentNode
  }
**/
}
function ActualizarNavegacion(){
  if (Navegacion.length > 1){
    var Ruta =""
    for (x = 0; x < Navegacion.length ; x++) {
    if (x == Navegacion.length -1){
    NuevoItem = "<span class='AtrasUltimo'>"+Navegacion[x].Titulo+"</span>"
    }else{
    NuevoItem = Navegacion[x].Titulo
    }
    if (Ruta ==""){

    Ruta =NuevoItem
    }else{
    Ruta +="> " + NuevoItem
    }
    }

//    document.getElementById("Contenedor").children[0].children[0].children[0].children[2].innerHTML = "<span class='Atras'>"+Ruta+"</span>";
  }
}