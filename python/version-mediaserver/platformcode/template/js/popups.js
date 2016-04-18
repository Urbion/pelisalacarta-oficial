
function AbrirLoading(){
  document.getElementById("Loading-Text").innerHTML = "Cargando...";
  document.getElementById("Overlay").style.display="block";
  document.getElementById("Loading").style.display="block";
  document.getElementById("Loading").children[0].focus();
  document.getElementById("Loading").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("Loading").offsetHeight / 2 + "px"
}
function CerrarLoading(){
  document.getElementById("Loading").style.display="none";
  document.getElementById("Overlay").style.display="none";
  try{ 
    ItemFocus.focus()
  }catch(e){
    try{ 
      document.getElementById("Contenedor").children[0].children[0].children[0].focus();
    }catch(e){
    }
  }
}

function CerrarDialogos() {
  document.getElementById('Overlay').style.display='none';
  document.getElementById("Loading").style.display="none";
  document.getElementById("Lista-popup").style.display="none";
  document.getElementById("Config-popup").style.display="none";
  document.getElementById("Player-popup").style.display="none";
  document.getElementById("Alert-popup").style.display="none";
  document.getElementById("AlertYesNo-popup").style.display="none";
  document.getElementById("Keyboard-popup").style.display="none";
  document.getElementById("ProgressBar-popup").style.display="none";
  try{ 
    ItemFocus.focus()
  }catch(e){
    try{ 
      document.getElementById("Contenedor").children[0].children[0].children[0].focus();
    }catch(e){
    }
  }
}

function AbrirMenu(Title,Lista) {
  AbrirLista("",{"title":Title},atob(Lista))
}

function AbrirLista(id,data,Lista) {
  document.getElementById("Overlay").style.display="block"
  document.getElementById("Lista-titulo").innerHTML = data["title"];
  document.getElementById("Lista-popup").RequestID = id
  document.getElementById("Lista").innerHTML ='<ul class="Lista">' + Lista + '</ul>';
  document.getElementById("Lista-popup").style.display="block";
  document.getElementById("Lista").children[0].children[0].children[0].focus()
  document.getElementById("Lista-popup").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("Lista-popup").offsetHeight / 2 + "px"  
}

function AbrirPlayer(Title,Player) {
  document.getElementById("Overlay").style.display="block"
  document.getElementById("Player-titulo").innerHTML = atob(Title);
  document.getElementById("Player").innerHTML = Player;
  document.getElementById("Player-popup").style.display="block";
  document.getElementById("Player-popup").children[0].focus()
  document.getElementById("Player-popup").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("Player-popup").offsetHeight / 2 + "px"  
  
  setTimeout(function() {
        document.getElementById("Player-popup").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("Player-popup").offsetHeight / 2 + "px"  
  }, 500);
}

function AbrirAlert(id,data) {

  document.getElementById("Overlay").style.display="block";
  document.getElementById("Alert-popup").style.display="block";
  document.getElementById("Alert-popup").RequestID = id
  document.getElementById("Alert-Text").innerHTML = data["text"].replace(new RegExp("\n", 'g'), "<br/>")
  document.getElementById("Alert-Titulo").innerHTML = data["title"];
  document.getElementById("Alert-popup").children[3].children[0].focus()
  document.getElementById("Alert-popup").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("Alert-popup").offsetHeight / 2 + "px"
}

function AbrirAlertYesNo(id,data){
  document.getElementById("Overlay").style.display="block";
  document.getElementById("AlertYesNo-popup").style.display="block";
  document.getElementById("AlertYesNo-popup").RequestID = id
  document.getElementById("AlertYesNo-Text").innerHTML = data["text"].replace(new RegExp("\n", 'g'), "<br/>")
  document.getElementById("AlertYesNo-Titulo").innerHTML = data["title"];
  document.getElementById("AlertYesNo-popup").children[3].children[0].focus()
  document.getElementById("AlertYesNo-popup").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("AlertYesNo-popup").offsetHeight / 2 + "px"
}


function AbrirKeyboard(id,data) {
  if (data["title"] === "") {data["title"] = "Teclado";}
  if (data["password"] == true) {document.getElementById("Keyboard-Text").type = "password"}
  else {document.getElementById("Keyboard-Text").type = "text"}
  document.getElementById("Keyboard-popup").RequestID = id
  document.getElementById("Overlay").style.display="block";
  document.getElementById("Keyboard-popup").style.display="block";
  document.getElementById("Keyboard-Text").value = data["text"]
  document.getElementById("Keyboard-Titulo").innerHTML = data["title"]
  document.getElementById("Keyboard-popup").children[2].children[0].children[0].focus()
  document.getElementById("Keyboard-popup").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("Keyboard-popup").offsetHeight / 2 + "px"
}

function AbrirProgressBG(id,data) {
  document.getElementById("ProgressBarBG-popup").style.display="block";
  document.getElementById("ProgressBarBG-popup").RequestID = id
  document.getElementById("ProgressBarBG-Text").innerHTML = data["text"];
  document.getElementById("ProgressBarBG-Titulo").innerHTML = data["title"];
  document.getElementById("ProgressBarBG-Abance").style.width = data["percent"] + "%";
}

function UpdateProgressBG(id,data) {
  document.getElementById("ProgressBarBG-Text").innerHTML = data["text"].replace(new RegExp("\n", 'g'), "<br/>")
  document.getElementById("ProgressBarBG-Titulo").innerHTML = data["title"]
  document.getElementById("ProgressBarBG-Abance").style.width = data["percent"] + "%";
}

function CerrarProgressBG() {
  document.getElementById("ProgressBarBG-popup").style.display="none";
}

function AbrirProgress(id,data) {
  document.getElementById("ProgressBar-popup").RequestID = id
  document.getElementById("Overlay").style.display="block";
  document.getElementById("ProgressBar-popup").style.display="block";
  document.getElementById("ProgressBar-Text").innerHTML = data["text"].replace(new RegExp("\n", 'g'), "<br/>")
  document.getElementById("ProgressBar-Titulo").innerHTML = data["title"]
  document.getElementById("ProgressBar-Cancelled").checked = "";
  document.getElementById("ProgressBar-Abance").style.width = data["percent"] + "%";
  document.getElementById("ProgressBar-popup").children[4].children[0].focus()
  document.getElementById("ProgressBar-popup").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("ProgressBar-popup").offsetHeight / 2 + "px"
}

function UpdateProgress(id,data) {
  document.getElementById("ProgressBar-Text").innerHTML = data["text"].replace(new RegExp("\n", 'g'), "<br/>")
  if (document.getElementById("ProgressBar-Cancelled").checked !="") {
    document.getElementById("ProgressBar-Titulo").innerHTML = data["title"] + " " + data["percent"] + "% - Cancelando...";
  } else {
  document.getElementById("ProgressBar-Titulo").innerHTML = data["title"] + " " + data["percent"] + "%";
  }
  document.getElementById("ProgressBar-Abance").style.width = data["percent"] + "%";
}

function CerrarProgress() {
  document.getElementById("Overlay").style.display="none";
  document.getElementById("ProgressBar-popup").style.display="none";
  ItemFocus.focus()
}

function AbrirConfig(id, data, Secciones,Lista){
  document.getElementById("Config-popup").RequestID = id
  document.getElementById("Config").innerHTML = Lista;
  document.getElementById("Config-Titulo").innerHTML = data["title"];
  if (Secciones != ""){
    document.getElementById("Config-secciones").innerHTML = Secciones
    document.getElementById("Config-secciones").style.display="block";
    document.getElementById("Config-General").style.display="block";
    
  } else {
    document.getElementById("Config-secciones").style.display="none";
    document.getElementById("Config-undefined").style.display="block";
    
  }
  
  document.getElementById("Overlay").style.display="block";
  document.getElementById("Config-popup").style.display="block";
  if (Secciones != ""){
    document.getElementById("Config-popup").children[2].children[0].focus()
    document.getElementById("Config-General").scrollTop = 0;
  } else {
    document.getElementById("Config-popup").children[4].children[0].focus()
    document.getElementById("Config-undefined").scrollTop = 0;
  }
  document.getElementById("Config-popup").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("Config-popup").offsetHeight / 2 + "px"
}