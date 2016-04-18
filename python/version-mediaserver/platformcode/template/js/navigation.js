window.onkeydown =  function(e){
  if (e.keyCode==27){CerrarDialogos();}
  try{
    if(e.target.tagName=="BODY"){BodyKeyDown(e)}
    if(e.target.id=="Loading"){LoadingKeyDown(e)}
    
    if(e.target.parentNode.id=="Lista-popup"){ListaKeyDown(e)}
    if(e.target.parentNode.id=="Alert-popup"){AlertKeyDown(e)}  
    if(e.target.parentNode.id=="Keyboard-popup"){KeyboardKeyDown(e)}  
    if(e.target.parentNode.id=="AlertYesNo-popup"){AlertYesNoKeyDown(e)} 
    if(e.target.parentNode.id=="Servidor-popup"){ServidorKeyDown(e)} 
    if(e.target.parentNode.id=="ProgressBar-popup"){ProgressKeyDown(e)} 
    if(e.target.parentNode.id=="Config-popup"){ConfigKeyDown(e)}
    
    if(e.target.parentNode.parentNode.id=="Alert-popup"){AlertKeyDown(e)}
    if(e.target.parentNode.parentNode.id=="AlertYesNo-popup"){AlertYesNoKeyDown(e)}
    if(e.target.parentNode.parentNode.id=="Servidor-popup"){ServidorKeyDown(e)}
    if(e.target.parentNode.parentNode.id=="Keyboard-popup"){KeyboardKeyDown(e)}
    if(e.target.parentNode.parentNode.id=="ProgressBar-popup"){ProgressKeyDown(e)}
    if(e.target.parentNode.parentNode.id=="Config-popup"){ConfigKeyDown(e)}
    
    if(e.target.parentNode.parentNode.parentNode.id=="Contenedor"){ListItemKeyDown(e)}
    if(e.target.parentNode.parentNode.parentNode.id=="Keyboard-popup"){KeyboardKeyDown(e)}
    
    if(e.target.parentNode.parentNode.parentNode.parentNode.id=="Lista-popup"){ListaKeyDown(e)}
    if(e.target.parentNode.parentNode.parentNode.parentNode.id=="Config-popup"){ConfigKeyDown(e)}
    
    if(e.target.parentNode.parentNode.parentNode.parentNode.parentNode.id=="Pie"){BodyKeyDown(e)}
    
    if(e.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.id=="Servidor-popup"){ServidorKeyDown(e)}
    if(e.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.id=="Config-popup"){ConfigKeyDown(e)}
  
  }catch(err) {} 
}

function ListItemKeyDown(e){
  switch (e.keyCode) {
    case 96:
    case 97:
    case 98:
    case 99:
    case 100:
    case 101:
    case 102:
    case 103:
    case 104:
    case 105:
      Buscar(e.keyCode)
      break;
    case 93: //Menu
      e.preventDefault();
      if (e.target.parentNode.children.length ==2){
        e.target.parentNode.children[1].onclick.apply(e.target.parentNode.children[1]);
        ItemFocus = e.target;
      }
      break;
    case 8: //Atras
      e.preventDefault();
      if (Navegacion.length >1){Back();}
      else{HED.helpers.quit();}
      break;
    
    case 37: //Left
      e.preventDefault();
      index = Array.prototype.indexOf.call(document.activeElement.parentNode.children, document.activeElement);
      document.activeElement.parentNode.children[index-1].focus();
      break;
    
    case 38: //UP
      e.preventDefault();
      index = Array.prototype.indexOf.call(document.getElementById("itemlist").children, document.activeElement.parentNode);
      if (index ==0){index = document.getElementById("itemlist").children.length}
      document.activeElement.parentNode.parentNode.children[index-1].children[0].focus();
      break;
    
    case 39: //RIGHT
      e.preventDefault();
      index = Array.prototype.indexOf.call(document.activeElement.parentNode.children, document.activeElement);
      document.activeElement.parentNode.children[index+1].focus();
      break;
      
    case 40: //DOWN
      e.preventDefault();
      index = Array.prototype.indexOf.call(document.getElementById("itemlist").children, document.activeElement.parentNode);
      if (index+1 ==document.getElementById("itemlist").children.length){index = -1}
      document.activeElement.parentNode.parentNode.children[index+1].children[0].focus();
      break;
  }
}

function LoadingKeyDown(e){
  switch (e.keyCode) {
    case 8: //Atras
      CerrarLoading()
      e.preventDefault();
      break;
  }
}

function BodyKeyDown(e){
  switch (e.keyCode) {
    case 8: //Atras
      e.preventDefault();
      HED.window.get().destroy()
      break;
      
    case 37: //Left
      e.preventDefault();
      document.getElementById("itemlist").children[0].children[0].focus();
      break;
      
    case 38: //UP
      e.preventDefault(); 
      document.getElementById("itemlist").children[0].children[0].focus();
      break;
      
    case 39: //RIGHT
      e.preventDefault();
      document.getElementById("itemlist").children[0].children[0].focus();
      break;
      
    case 40: //DOWN
      e.preventDefault();
      document.getElementById("itemlist").children[0].children[0].focus();
      break;
  }
}

function ListaKeyDown(e){
  switch (e.keyCode) {
    case 8: //Atras
      e.preventDefault(); 
      CerrarDialogos()
      break;

    case 38: //UP
      e.preventDefault(); 
      index = Array.prototype.indexOf.call(document.activeElement.parentNode.parentNode.children, document.activeElement.parentNode);
      if (index !=0){document.activeElement.parentNode.parentNode.children[index-1].children[0].focus()}
      else{ document.activeElement.parentNode.parentNode.parentNode.parentNode.children[0].focus()}
      break;

    case 40: //DOWN
      e.preventDefault();
      if (e.target.parentNode.id=="Lista-popup"){document.activeElement.parentNode.children[2].children[0].children[0].children[0].focus()}
      else{
        index = Array.prototype.indexOf.call(document.activeElement.parentNode.parentNode.children, document.activeElement.parentNode);
        document.activeElement.parentNode.parentNode.children[index+1].children[0].focus();
      }
      break;
  }
}

function ConfigKeyDown(e){
  switch (e.keyCode) {
    case 8: //Atras
      if ((e.target.tagName != "INPUT" || (e.target.type != "text" && e.target.type != "password")) && e.target.tagName != "SELECT"){
        e.preventDefault(); 
        CerrarDialogos()
      }
      break;
      
    case 38: //UP
      e.preventDefault(); 
      if (e.target.parentNode.id=="Config-secciones"){document.activeElement.parentNode.parentNode.children[0].focus()};
      if (e.target.parentNode.id=="Config-botones"){
        for (x = 0; x < document.getElementById('Config-popup').children[3].children.length; x++) {
          if (document.getElementById('Config-popup').children[3].children[x].style.display !="none"){break;}
        }
        document.getElementById('Config-popup').children[3].children[x].children[document.getElementById('Config-popup').children[3].children[x].children.length-1].children[0].children[1].children[0].children[0].focus()
      }

      if (e.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.id=="Config"){
        index = Array.prototype.indexOf.call(document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children, document.activeElement.parentNode.parentNode.parentNode.parentNode);
        if (index >0){
          while (document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children[index-1].children[0].className =="Separador" || document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children[index-1].children[0].className =="LabelSeparador"){
            index --
          }
          document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children[index-1].children[0].children[1].children[0].children[0].focus()
        }else{
          document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.children[2].children[0].focus()
        }
      }    
      break;
      
    case 37: //Left
      if ((e.target.tagName != "INPUT" || (e.target.type != "text" && e.target.type != "password")) && e.target.tagName != "SELECT"){
        e.preventDefault(); 
        if (e.target.parentNode.parentNode.id=="Config-popup"){
          index = Array.prototype.indexOf.call(document.activeElement.parentNode.children, document.activeElement);
          document.activeElement.parentNode.children[index-1].focus();
        }
      }      
      break;
      
    case 39: //RIGHT
      if ((e.target.tagName != "INPUT" || (e.target.type != "text" && e.target.type != "password")) && e.target.tagName != "SELECT"){
        e.preventDefault(); 
        if (e.target.parentNode.parentNode.id=="Config-popup"){
        index = Array.prototype.indexOf.call(document.activeElement.parentNode.children, document.activeElement);
        document.activeElement.parentNode.children[index+1].focus();
        }
      }   
      break;
    
    case 40: //DOWN
      e.preventDefault(); 
      if (e.target.parentNode.id=="Config-popup"){document.activeElement.parentNode.children[2].children[0].focus()}
      if (e.target.parentNode.id=="Config-secciones"){
        for (x = 0; x < document.getElementById('Config-popup').children[3].children.length; x++) {
          if (document.getElementById('Config-popup').children[3].children[x].style.display !="none"){break;}
        }
        document.activeElement.parentNode.parentNode.children[3].children[x].children[0].children[0].children[1].children[0].children[0].focus()
      }
      if (e.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.id=="Config"){
        index = Array.prototype.indexOf.call(document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children, document.activeElement.parentNode.parentNode.parentNode.parentNode);
        if (index+1 < document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children.length){
          while (document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children[index+1].children[0].className =="Separador" || document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children[index+1].children[0].className =="LabelSeparador"){
            index ++
          }
          document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children[index+1].children[0].children[1].children[0].children[0].focus()
        }else{
          document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.children[4].children[0].focus()
        }
      }
      break;
  }
}

function AlertKeyDown(e){
  switch (e.keyCode) {
    case 8: //Atras
      e.preventDefault(); 
      CerrarDialogos()
      break;
      
    case 38: //UP
      e.preventDefault(); 
      if (e.target.parentNode.parentNode.id=="Alert-popup"){document.activeElement.parentNode.parentNode.children[0].focus()}
      break;
      
    case 40: //DOWN
      e.preventDefault();
      if (e.target.parentNode.id=="Alert-popup"){document.activeElement.parentNode.children[3].children[0].focus()}
      break;
  }
}

function ProgressKeyDown(e){
  switch (e.keyCode) {
    case 8: //Atras
      e.preventDefault(); 
      CerrarDialogos()
      break;
      
    case 38: //UP
      e.preventDefault(); 
      if (e.target.parentNode.parentNode.id=="ProgressBar-popup"){document.activeElement.parentNode.parentNode.children[0].focus()}
      break;
      
    case 40: //DOWN
      e.preventDefault(); 
      if (e.target.parentNode.id=="ProgressBar-popup"){document.activeElement.parentNode.children[4].children[0].focus()}
      break;
  }
}

function AlertYesNoKeyDown(e){
  switch (e.keyCode) {
    case 8: //Atras
      e.preventDefault(); 
      CerrarDialogos()
      break;
    case 38: //UP
      e.preventDefault(); 
      if (e.target.parentNode.parentNode.id=="AlertYesNo-popup"){document.activeElement.parentNode.parentNode.children[0].focus()}
      break;
      
    case 37: //Left
      e.preventDefault(); 
      if (e.target.parentNode.parentNode.id=="AlertYesNo-popup"){
        index = Array.prototype.indexOf.call(document.activeElement.parentNode.children, document.activeElement);
        document.activeElement.parentNode.children[index-1].focus()
      }
      break;
      
    case 39: //RIGHT
      e.preventDefault(); 
      if (e.target.parentNode.parentNode.id=="AlertYesNo-popup"){
        index = Array.prototype.indexOf.call(document.activeElement.parentNode.children, document.activeElement);
        document.activeElement.parentNode.children[index+1].focus()
      }
      break;
      
    case 40: //DOWN
      e.preventDefault(); 
      if (e.target.parentNode.id=="AlertYesNo-popup"){document.activeElement.parentNode.children[3].children[0].focus()}
      break;
  }
}

function ServidorKeyDown(e){
  switch (e.keyCode) {
    case 8: //Atras
      if (e.target.tagName != "INPUT"){
        e.preventDefault(); 
        CerrarDialogos()
      }
      break;
      
    case 38: //UP
      e.preventDefault(); 
      if (e.target.parentNode.parentNode.id=="Servidor-popup"){
        document.getElementById('Servidor-popup').children[2].children[0].children[1].children[0].children[1].children[0].children[0].focus()
      }
      if (e.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.id=="Servidor-popup"){
        index = Array.prototype.indexOf.call(document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children, document.activeElement.parentNode.parentNode.parentNode.parentNode);
        if (index > 0){
          document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children[index-1].children[0].children[1].children[0].children[0].focus()
        }else{
          document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.children[0].focus()
        }
      }
      break;
      
    case 37: //Left
      e.preventDefault(); 
      if (e.target.parentNode.parentNode.id=="Servidor-popup"){
        index = Array.prototype.indexOf.call(document.activeElement.parentNode.children, document.activeElement);
        document.activeElement.parentNode.children[index-1].focus();
      }
      break;
      
    case 39: //RIGHT
      e.preventDefault(); 
      if (e.target.parentNode.parentNode.id=="Servidor-popup"){
        index = Array.prototype.indexOf.call(document.activeElement.parentNode.children, document.activeElement);
        document.activeElement.parentNode.children[index+1].focus();
      }

      break;
    
    case 40: //DOWN
      e.preventDefault(); 
      if (e.target.parentNode.id=="Servidor-popup"){document.activeElement.parentNode.children[2].children[0].children[0].children[0].children[1].children[0].children[0].focus()}
      if (e.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.id=="Servidor-popup"){
        index = Array.prototype.indexOf.call(document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children, document.activeElement.parentNode.parentNode.parentNode.parentNode);
        if (index+1 < document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children.length){
          document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children[index+1].children[0].children[1].children[0].children[0].focus()
        }else{
          document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.children[3].children[0].focus()
        }
      }
      break;
  }
}

function KeyboardKeyDown(e){
  switch (e.keyCode) {
    case 8: //Atras
      if (e.target.id != "Keyboard-Text"){
        e.preventDefault(); 
        CerrarDialogos()
      }
      break;
    case 38: //UP
      e.preventDefault(); 
      if (e.target.parentNode.parentNode.id=="Keyboard-popup"){document.activeElement.parentNode.parentNode.children[2].children[0].children[0].focus()}
      if (e.target.parentNode.parentNode.parentNode.id=="Keyboard-popup"){document.activeElement.parentNode.parentNode.parentNode.children[0].focus()}

      break;
      
    case 37: //Left
       
      if (e.target.parentNode.parentNode.id=="Keyboard-popup"){
        e.preventDefault();
        index = Array.prototype.indexOf.call(document.activeElement.parentNode.children, document.activeElement);
        document.activeElement.parentNode.children[index-1].focus()
      }
      break;
      
    case 39: //RIGHT
       
      if (e.target.parentNode.parentNode.id=="Keyboard-popup"){
        e.preventDefault();
        index = Array.prototype.indexOf.call(document.activeElement.parentNode.children, document.activeElement);
        document.activeElement.parentNode.children[index+1].focus()
      }
      break;
      
    case 40: //DOWN
      e.preventDefault(); 
      if (e.target.parentNode.id=="Keyboard-popup"){document.activeElement.parentNode.children[2].children[0].children[0].focus()}
      if (e.target.parentNode.parentNode.parentNode.id=="Keyboard-popup"){document.activeElement.parentNode.parentNode.parentNode.children[3].children[0].focus()}
      break;
  }
}

function Buscar(keyCode) {
  switch (keyCode) {
    case 96:
      Tecla["keyCode"]=keyCode
      Tecla["Char"] = "0"
      break;
      
    case 97:
      Tecla["keyCode"]=keyCode
      Tecla["Char"] = "1"
      break;
      
    case 98:
      if (Tecla["keyCode"]==keyCode){
        switch (Tecla["Char"]){
          case "a":
            Tecla["Char"] = "b"
            break;
          case "b":
            Tecla["Char"] = "c"
            break;
          case "c":
            Tecla["Char"] = "2"
            break;
          case "2":
            Tecla["Char"] = "a"
            break;
        }
      }else{
        Tecla["keyCode"]=keyCode
        Tecla["Char"] = "a"
      }       
      break;
      
    case 99:
      if (Tecla["keyCode"]==keyCode){
        switch (Tecla["Char"]){
          case "d":
            Tecla["Char"] = "e"
            break;
          case "e":
            Tecla["Char"] = "f"
            break;
          case "f":
            Tecla["Char"] = "3"
            break;
          case "3":
            Tecla["Char"] = "d"
            break;
        }
      }else{
        Tecla["keyCode"]=keyCode
        Tecla["Char"] = "d"
      }   
      break;
      
    case 100:
      if (Tecla["keyCode"]==keyCode){
        switch (Tecla["Char"]){
          case "g":
            Tecla["Char"] = "h"
            break;
          case "h":
            Tecla["Char"] = "i"
            break;
          case "i":
            Tecla["Char"] = "4"
            break;
          case "4":
            Tecla["Char"] = "g"
            break;
        }
      }else{
        Tecla["keyCode"]=keyCode
        Tecla["Char"] = "g"
      }
      break;
      
    case 101:
      if (Tecla["keyCode"]==keyCode){
        switch (Tecla["Char"]){
          case "j":
            Tecla["Char"] = "k"
            break;
          case "k":
            Tecla["Char"] = "l"
            break;
          case "l":
            Tecla["Char"] = "5"
            break;
          case "5":
            Tecla["Char"] = "j"
            break;
        }
      }else{
        Tecla["keyCode"]=keyCode
        Tecla["Char"] = "j"
      }
      break;
      
    case 102:
      if (Tecla["keyCode"]==keyCode){
        switch (Tecla["Char"]){
          case "m":
            Tecla["Char"] = "n"
            break;
          case "n":
            Tecla["Char"] = "o"
            break;
          case "o":
            Tecla["Char"] = "6"
            break;
          case "6":
            Tecla["Char"] = "m"
            break;
        }
      }else{
        Tecla["keyCode"]=keyCode
        Tecla["Char"] = "m"
      }
      break;
      
    case 103:
      if (Tecla["keyCode"]==keyCode){
        switch (Tecla["Char"]){
          case "p":
            Tecla["Char"] = "q"
            break;
          case "q":
            Tecla["Char"] = "r"
            break;
          case "r":
            Tecla["Char"] = "s"
            break;
          case "s":
            Tecla["Char"] = "7"
            break;
          case "7":
            Tecla["Char"] = "p"
            break;
        }
      }else{
        Tecla["keyCode"]=keyCode
        Tecla["Char"] = "p"
      }
      break;
      
    case 104:
      if (Tecla["keyCode"]==keyCode){
        switch (Tecla["Char"]){
          case "t":
            Tecla["Char"] = "u"
            break;
          case "u":
            Tecla["Char"] = "u"
            break;
          case "v":
            Tecla["Char"] = "8"
            break;
          case "8":
            Tecla["Char"] = "t"
            break;
        }
      }else{
        Tecla["keyCode"]=keyCode
        Tecla["Char"] = "t"
      }
      break;
      
    case 105:
      if (Tecla["keyCode"]==keyCode){
        switch (Tecla["Char"]){
          case "x":
            Tecla["Char"] = "y"
            break;
          case "y":
            Tecla["Char"] = "z"
            break;
          case "z":
            Tecla["Char"] = "w"
            break;
          case "w":
            Tecla["Char"] = "9"
            break;
          case "9":
            Tecla["Char"] = "x"
            break;
        }
      }else{
        Tecla["keyCode"]=keyCode
        Tecla["Char"] = "x"
      }
      break;

  }
  for (x = 2; x < document.getElementById("itemlist").children.length; x++) {
  if ( document.getElementById("itemlist").children[x].children[0].children[1].innerHTML.toLowerCase().indexOf(Tecla["Char"])===0){
  document.getElementById("itemlist").children[x].children[0].focus()
  break;
  }
  }
  
  
}