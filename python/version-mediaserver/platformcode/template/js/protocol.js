var default_settings = {}
function GetResponses(data) {
    response = JSON.parse(data)
    data = response["data"];
    switch (response["action"]) {
        case "connect":
            document.getElementById("Version").innerHTML = data["version"]
            document.getElementById("Date").innerHTML = data["date"]
            ID = response["id"]
            break;
        case "EndItems":
            for (h = 0; h < data["itemlist"].length; h++) {
              JsonItem = data["itemlist"][h]
              //[COLOR xxx][/COLOR]
              var re = /(\[COLOR ([^\]]+)\])(?:.*?)(\[\/COLOR\])/g; 
              var str = JsonItem["title"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["title"] = JsonItem["title"].replace(resultado[1],"<span style='color:"+resultado[2]+"'>")
                  JsonItem["title"] = JsonItem["title"].replace(resultado[3],"</span>")
              }
              
              //[B][/B]
              var re = /(\[B\])(?:.*?)(\[\/B\])/g; 
              var str = JsonItem["title"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["title"] = JsonItem["title"].replace(resultado[1],"<b>")
                  JsonItem["title"] = JsonItem["title"].replace(resultado[2],"</b>")
              }
              
              //[i][/i]
              var re = /(\[I\])(?:.*?)(\[\/I\])/g; 
              var str = JsonItem["title"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["title"] = JsonItem["title"].replace(resultado[1],"<i>")
                  JsonItem["title"] = JsonItem["title"].replace(resultado[2],"</i>")
              }
              //[COLOR xxx][/COLOR]
              var re = /(\[COLOR ([^\]]+)\])(?:.*?)(\[\/COLOR\])/g; 
              var str = JsonItem["plot"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["plot"] = JsonItem["plot"].replace(resultado[1],"<span style='color:"+resultado[2]+"'>")
                  JsonItem["plot"] = JsonItem["plot"].replace(resultado[3],"</span>")
              }
              
              //[B][/B]
              var re = /(\[B\])(?:.*?)(\[\/B\])/g; 
              var str = JsonItem["plot"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["plot"] = JsonItem["plot"].replace(resultado[1],"<b>")
                  JsonItem["plot"] = JsonItem["plot"].replace(resultado[2],"</b>")
              }
              
              //[i][/i]
              var re = /(\[I\])(?:.*?)(\[\/I\])/g; 
              var str = JsonItem["plot"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["plot"] = JsonItem["plot"].replace(resultado[1],"<i>")
                  JsonItem["plot"] = JsonItem["plot"].replace(resultado[2],"</i>")
              }
              
              if (JsonItem["action"]=="go_back"){
                Action = 'Back()'
              }else{
                Action = 'DescargarContenido(\''+ JsonItem["url"] +'\')'
              }
              if (JsonItem["thumbnail"].indexOf("http") != 0){JsonItem["thumbnail"] = data["host"] +"/local/"+encodeURIComponent(btoa(JsonItem["thumbnail"]))}
              if (data["mode"]==0){
                HtmlItem ='<li class="ListItemBanner"><a onblur="" onfocus="ItemFocus=this" onmouseover="this.focus()" class="ListItem {$ClassMenu}" href="javascript:void(0)" onclick="ItemFocus=this;'+Action+'"><div class="ListItem"><img class="ListItem" onerror="ImgError(this)" alt="'+data["host"]+'" src="'+JsonItem["thumbnail"]+'"></div><h3 class="ListItem">' + JsonItem["title"] + '</h3><p class="ListItem"></p></a>{$BotonMenu}</li>'
              }else if (data["mode"]==1){
                HtmlItem ='<li class="ListItemChannels"><a onblur="DesCargarInfo(this)" onfocus="ItemFocus=this" onmouseover="this.focus()" class="ListItem {$ClassMenu}" href="javascript:void(0)" onclick="ItemFocus=this;'+Action+'"><h3 class="ListItem">' + JsonItem["title"] + '</h3><div class="ListItem"><img class="ListItem" onerror="ImgError(this)" alt="'+data["host"]+'" src="'+JsonItem["thumbnail"]+'"></div></a>{$BotonMenu}</li>'
             
              }else if (data["mode"]==2){
                if (JsonItem["action"]=="go_back" || JsonItem["action"]=="search" || JsonItem["thumbnail"].indexOf("thumb_folder") != -1 || JsonItem["thumbnail"].indexOf("thumb_nofolder") != -1 || JsonItem["thumbnail"].indexOf("thumb_error") != -1){
                  HtmlItem ='<li class="ListItem"><a onfocus="DesCargarInfo(this);ItemFocus=this" onmouseover="this.focus()" class="ListItem {$ClassMenu}" href="javascript:void(0)" onclick="ItemFocus=this;'+Action+'"><div class="ListItem"><img class="ListItem" onerror="ImgError(this)" alt="'+data["host"]+'" src="'+JsonItem["thumbnail"]+'"><img class="Default" src="http://media.tvalacarta.info/pelisalacarta/squares/thumb_folder.png"></div><h3 class="ListItem">' + JsonItem["title"] + '</h3><p class="ListItem">' + JsonItem["plot"] + '</p></a>{$BotonMenu}</li>'
                }else{
                  HtmlItem ='<li class="ListItem"><a onblur="DesCargarInfo(this)" onfocus="CargarInfo(this);ItemFocus=this" onmouseover="this.focus()" class="ListItem {$ClassMenu}" href="javascript:void(0)" onclick="ItemFocus=this;'+Action+'"><div class="ListItem"><img class="ListItem" onerror="ImgError(this)" alt="'+data["host"]+'" src="'+JsonItem["thumbnail"]+'"><img class="Default" src="http://media.tvalacarta.info/pelisalacarta/squares/thumb_folder.png"></div><h3 class="ListItem">' + JsonItem["title"] + '</h3><p class="ListItem">' + JsonItem["plot"] + '</p></a>{$BotonMenu}</li>'
                }
              }
              Lista = "";
              for (x = 0; x < JsonItem["context"].length; x++) {
                Lista +=
                '<li class="Lista"><a href="javascript:void(0)" onmouseover="this.focus()" onclick="CerrarDialogos();DescargarContenido(\'' + JsonItem["context"][x]["url"] +
                '\')" class="Lista"><h3>' + JsonItem["context"][x]["title"] + '</h3></a></li>';
              }
              BotonMenu = '<a class="ListItemButton" href="javascript:void(0)" onmouseover="this.focus()" onclick=\'ItemFocus=this;AbrirMenu("Menu","'+btoa(Lista)+'")\'></a>';
              ClassMenu = "ListItemMenu"
              if (JsonItem["context"].length === 0) {
                  BotonMenu = "";
                  ClassMenu = "";
              }
              HtmlItem = HtmlItem.replace("{$BotonMenu}", BotonMenu);
              HtmlItem = HtmlItem.replace("{$ClassMenu}", ClassMenu);
              ItemList += HtmlItem;

            }

            if (Navegacion.length > 0) {
                if (Navegacion[Navegacion.length - 1].Url == UltimoRequest) {
                    Navegacion[Navegacion.length - 1].Time          = new Date().getTime() - UltimoRequestTime;
                    document.getElementById("Contenedor").innerHTML = '<ul class="ListItem" id="itemlist">' + ItemList + '</ul>';
                    if (Navegacion[Navegacion.length - 1].Time > TiempoCache){
                      Navegacion[Navegacion.length - 1].Data            = document.getElementById("Contenedor").innerHTML;
                    }
                    if (document.getElementById("Contenedor").children[0].children.length > Navegacion[Navegacion.length - 1].Focus){
                      document.getElementById("Contenedor").children[0].children[Navegacion[Navegacion.length - 1].Focus].children[0].focus();
                    }else{
                      document.getElementById("Contenedor").children[0].children[document.getElementById("Contenedor").children[0].children.length -1].children[0].focus();
                    }
                    document.getElementById("Contenedor").scrollTop = Navegacion[Navegacion.length - 1].Scroll;
                    
                } else {
                    Navegacion[Navegacion.length - 1].Scroll        = document.getElementById("Contenedor").scrollTop;
                    Navegacion[Navegacion.length - 1].Focus         = Array.prototype.indexOf.call(document.getElementById("itemlist").children, ItemFocus.parentNode);
                    Navegacion.push({});
                    Navegacion[Navegacion.length - 1].Titulo        = ItemFocus.children[1].textContent;
                    Navegacion[Navegacion.length - 1].Url           = UltimoRequest;
                    Navegacion[Navegacion.length - 1].Time          = new Date().getTime() - UltimoRequestTime;
                    document.getElementById("Contenedor").innerHTML = '<ul class="ListItem" id="itemlist">' + ItemList + '</ul>';
                    if (Navegacion[Navegacion.length - 1].Time > TiempoCache){
                      Navegacion[Navegacion.length - 1].Data            = document.getElementById("Contenedor").innerHTML;
                    }
                    document.getElementById("Contenedor").children[0].children[0].children[0].focus();
                    document.getElementById("Contenedor").scrollTop = 0;
                }
            } else {
                Navegacion.push({});
                Navegacion[Navegacion.length - 1].Titulo          = "Inicio";
                Navegacion[Navegacion.length - 1].Url             = UltimoRequest;
                Navegacion[Navegacion.length - 1].Time            = new Date().getTime() - UltimoRequestTime;
                Navegacion[Navegacion.length - 1].Scroll          = "";
                Navegacion[Navegacion.length - 1].Focus           = "";
                document.getElementById("Contenedor").innerHTML   = '<ul class="ListItem" id="itemlist">' + ItemList + '</ul>'
                if (Navegacion[Navegacion.length - 1].Time > TiempoCache){
                  Navegacion[Navegacion.length - 1].Data            = document.getElementById("Contenedor").innerHTML;
                }
                document.getElementById("Contenedor").children[0].children[0].children[0].focus();

            }
            
            
            ActualizarNavegacion()           
            EnviarDatos({"id":response["id"], "result":true });
            CerrarLoading()
            break;
        case "Refresh":
            Consulta = Navegacion[Navegacion.length - 1].Url;
            Navegacion[Navegacion.length - 1].Scroll = document.getElementById("Contenedor").scrollTop;
            Navegacion[Navegacion.length - 1].Focus  = Array.prototype.indexOf.call(document.getElementById("itemlist").children, ItemFocus.parentNode);
            DescargarContenido(Consulta);
            EnviarDatos({"id":response["id"], "result":true });
            break;
        case "Alert":
            CerrarLoading()
            AbrirAlert(response["id"],data)
            break;
        case "AlertYesNo":
            CerrarLoading()
            AbrirAlertYesNo(response["id"],data)
            break;
        case "ProgressBG":
            AbrirProgressBG(response["id"],data)
            EnviarDatos({"id":response["id"], "result":true });
            break;
        case "ProgressBGUpdate":
            UpdateProgressBG(response["id"],data)
            break;
        case "ProgressBGClose":
            CerrarProgressBG();
            EnviarDatos({"id":response["id"], "result":true });
            break;
        case "Progress":
            CerrarLoading()
            AbrirProgress(response["id"],data)
            EnviarDatos({"id":response["id"], "result":true });
            break;
        case "ProgressUpdate":
            UpdateProgress(response["id"],data)
            break;
        case "ProgressClose":
            CerrarProgress();
            EnviarDatos({"id":response["id"], "result":true });
            CerrarLoading()
            break;
        case "ProgressIsCanceled":
            EnviarDatos({"id":response["id"], "result":document.getElementById("ProgressBar-Cancelled").checked !="" });
            break;
        case "isPlaying":
            EnviarDatos({"id":response["id"], "result": document.getElementById("Player-popup").style.display=="block" || document.getElementById("Lista-popup").style.display=="block"});
            break;
        case "Keyboard":
            CerrarLoading()
            AbrirKeyboard(response["id"],data);
            break;
        case "List":
            CerrarLoading()
            Lista = "";
            for (x = 0; x < data["list"].length; x++) {
                Lista +=
                    '<li class="Lista"><a href="javascript:void(0)" onmouseover="this.focus()" onclick="CerrarDialogos();EnviarDatos({\'id\':\''+response["id"]+'\', \'result\':'+x+' })" class="Lista"><h3>' + data["list"][x] + '</h3></a></li>';
            }
            AbrirLista(response["id"],data,Lista)
            break;
        case "Play":
            EnviarDatos({"id":response["id"], "result":true });
            CerrarLoading()
            if(!new RegExp("^(.+://)").test(data["video_url"])){
             data["video_url"] = data["host"]+"/local/"+encodeURIComponent(btoa(Utf8.encode(data["video_url"])))+"/video.mp4"}
             
            else if(new RegExp("^(?:http\://.*?\.vkcache\.com)").test(data["video_url"])){
            
             data["video_url"] = data["host"]+"/netutv-"+encodeURIComponent(btoa(Utf8.encode(data["video_url"])))+".mp4"} 
            
            ProxyUrl = data["host"]+"/proxy/"+encodeURIComponent(btoa(Utf8.encode(data["video_url"])))+"/video.mp4"
            Lista  = '<li onmouseover="this.focus()" class="Lista"><a href="#" onmouseover="this.focus()" onclick="CerrarDialogos();Play(\''+data["video_url"]+'\',\''+btoa(data["title"])+'\')" class="Lista"><h3>Abrir Enlace</h3></a></li>';
            Lista += '<li onmouseover="this.focus()" class="Lista"><a href="#" onmouseover="this.focus()" onclick="CerrarDialogos();Play_VLC(\''+data["video_url"]+'\',\''+btoa(data["title"])+'\')" class="Lista"><h3>Plugin VLC</h3></a></li>';
            Lista += '<li onmouseover="this.focus()" class="Lista"><a href="#" onmouseover="this.focus()" onclick="CerrarDialogos();Play_HTML(\''+data["video_url"]+'\',\''+btoa(data["title"])+'\')" class="Lista"><h3>Video HTML</h3></a></li>';

            AbrirLista("",{"title": "Elige el Reproductor"},Lista)

            break;
        case "Update":
            DescargarContenido(data["url"]);
            CerrarLoading()
            break;
        case "HideLoading":
            CerrarLoading()
            break;
        case "OpenConfig":
            CerrarLoading()
            Opciones = {};
            default_settings = {}
            for (x = 0; x < data["items"].length; x++) {
                if (typeof(Opciones[data["items"][x]["category"]]) == 'undefined') {
                    Opciones[data["items"][x]["category"]] = "";
                }
                if (data["items"][x]["color"] != ""){
                  data["items"][x]["label"] = "<span style='color:"+data["items"][x]["color"]+"'>" + data["items"][x]["label"] + "</span>"
                }
                default_settings[data["items"][x]["id"]] = data["items"][x]["default"]
                switch (data["items"][x]["type"]) {
                    case "sep":
                        Opciones[data["items"][x]["category"]] +=
                            '<li class="ListItem"><div class="Separador"></div></li>';
                        break;
                    case "lsep", "label":
                        Opciones[data["items"][x]["category"]] +=
                            '<li class="ListItem"><div class="LabelSeparador">' + data["items"][x]["label"] + '</div></li>';
                        break;
                    case "text":
                        if (data["items"][x]["option"] == "hidden") {
                            Opciones[data["items"][x]["category"]] += '<li class="ListItem"><div class="ListItem"><h3 class="Ajuste">' + data["items"][x]["label"] + '</h3><span class="Control"><div class="Text"><input class="Text" onchange="ChangeSetting(this)" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" type="password" id="' + data["items"][x]["id"] + '" value="' + data["items"][x]["value"] + '"></div></span</div></li>';
                        } else {
                            Opciones[data["items"][x]["category"]] += '<li class="ListItem"><div class="ListItem"><h3 class="Ajuste">' + data["items"][x]["label"] + '</h3><span class="Control"><div class="Text"><input class="Text" onchange="ChangeSetting(this)" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" type="text" id="' + data["items"][x]["id"] + '" value="' + data["items"][x]["value"] + '"></div></span</div></li>';
                        }
                        break;
                    case "bool":
                        if (data["items"][x]["value"] == "true" || data["items"][x]["value"] == true) {
                            Opciones[data["items"][x]["category"]] += '<li class="ListItem"><div class="ListItem"><h3 class="Ajuste">' + data["items"][x]["label"] + '</h3><span class="Control"><div class="Check"><input class="Check" onchange="ChangeSetting(this)" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" type="checkbox" checked=checked id="' + data["items"][x]["id"] + '" value="' + data["items"][x]["value"] + '"></div></span</div></li>';
                        } else {
                            Opciones[data["items"][x]["category"]] += '<li class="ListItem"><div class="ListItem"><h3 class="Ajuste">' + data["items"][x]["label"] + '</h3><span class="Control"><div class="Check"><input class="Check" onchange="ChangeSetting(this)" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" type="checkbox" id="' + data["items"][x]["id"] + '" value="' + data["items"][x]["value"] + '"></div></span</div></li>';
                        }
                        break;
                    case "labelenum":
                        if (data["items"][x]["values"] === "" || typeof(data["items"][x]["values"]) === "undefined") {
                            Opcion = data["items"][x]["lvalues"].split("|");
                        } else {
                            Opcion = data["items"][x]["values"].split("|");
                        }
                        SOpciones = "";
                        for (y = 0; y < Opcion.length; y++) {
                            if (data["items"][x]["value"] == Opcion[y]) {
                                if (data["items"][x]["lvalues"] === "" || typeof(data["items"][x]["lvalues"]) === "undefined") {
                                    SOpciones += "<option selected=selected>" + data["items"][x]["values"].split("|")[y] +
                                        "</option>";
                                } else {
                                    SOpciones += "<option selected=selected>" + data["items"][x]["lvalues"].split("|")[y] +
                                        "</option>";
                                }
                            } else {
                                if (data["items"][x]["lvalues"] === "" || typeof(data["items"][x]["lvalues"]) === "undefined") {
                                    SOpciones += "<option>" + data["items"][x]["values"].split("|")[y] +
                                        "</option>";
                                } else {
                                    SOpciones += "<option>" + data["items"][x]["lvalues"].split("|")[y] + "</option>";
                                }
                            }
                        }
                        Opciones[data["items"][x]["category"]] += '<li class="ListItem"><div class="ListItem"><h3 class="Ajuste">' + data["items"][x]["label"] + '</h3><span class="Control"><div class="Select"><select class="Select" onchange="ChangeSetting(this)" name="labelenum" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" id="' + data["items"][x]["id"] + '">' + SOpciones + '</select></div></span</div></li>';
                        break;
                        
                    case "list":
                  
                        SOpciones = "";
                        for (y = 0; y < + data["items"][x]["lvalues"].length; y++) {
                            if (data["items"][x]["value"] == y) {
                              SOpciones += "<option selected=selected>" + data["items"][x]["lvalues"][y] + "</option>";
                            } else {
              
                              SOpciones += "<option>" + data["items"][x]["lvalues"][y] + "</option>";
                            }
                        }
                        Opciones[data["items"][x]["category"]] += '<li class="ListItem"><div class="ListItem"><h3 class="Ajuste">' + data["items"][x]["label"] + '</h3><span class="Control"><div class="Select"><select class="Select" onchange="ChangeSetting(this)" name="enum" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" id="' + data["items"][x]["id"] + '">' + SOpciones + '</select></div></span</div></li>';
                        break;
                    case "enum":
                        if (data["items"][x]["values"] === "" || typeof(data["items"][x]["values"]) === "undefined") {
                            Opcion = data["items"][x]["lvalues"].split("|");
                            for (y = 0; y < Opcion.length; y++) {
                                Opcion[y] = y;
                            }
                        } else {
                            Opcion = data["items"][x]["values"].split("|");
                        }
                        SOpciones = "";
                        for (y = 0; y < Opcion.length; y++) {
                            if (data["items"][x]["value"] == Opcion[y]) {
                                if (data["items"][x]["lvalues"] === "" || typeof(data["items"][x]["lvalues"]) === "undefined") {
                                    SOpciones += "<option selected=selected>" + data["items"][x]["values"].split("|")[y] +
                                        "</option>";
                                } else {
                                    SOpciones += "<option selected=selected>" + data["items"][x]["lvalues"].split("|")[y] +
                                        "</option>";
                                }
                            } else {
                                if (data["items"][x]["lvalues"] === "" || typeof(data["items"][x]["lvalues"]) === "undefined") {
                                    SOpciones += "<option>" + data["items"][x]["values"].split("|")[y] +
                                        "</option>";
                                } else {
                                    SOpciones += "<option>" + data["items"][x]["lvalues"].split("|")[y] + "</option>";
                                }
                            }
                        }
                        Opciones[data["items"][x]["category"]] += '<li class="ListItem"><div class="ListItem"><h3 class="Ajuste">' + data["items"][x]["label"] + '</h3><span class="Control"><div class="Select"><select class="Select" onchange="ChangeSetting(this)" name="enum" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" id="' + data["items"][x]["id"] + '">' + SOpciones + '</select></div></span</div></li>';
                        break;
                    default:
                        break;
                }

            }
            Secciones = "";
            Lista = "";
            
            for (var key in Opciones) {
                if (Opciones.hasOwnProperty(key)) {
                    if (Object.keys(Opciones).length > 1 || key !="undefined"){
                      Secciones += '<a href="javascript:void(0)" class="Boton" onmouseover="this.focus()" onclick="MostrarSeccion(\'' + key + '\')">' + key + '</a>\n';
                    }
                    Lista +=
                        '<ul class="ListItem" style="display:none" id="Config-' + key + '">' + Opciones[key] + '</ul>';
                }
            }
            AbrirConfig(response["id"],data, Secciones, Lista)
            break;

        default:
            break;
    }
}

function DefaultConfig() {
        Objetos = document.getElementById("Config-popup").getElementsByTagName("input")
        
        for(x=0;x<Objetos.length;x++){
          switch (Objetos[x].type) {
                case "text":
                    Objetos[x].value = default_settings[Objetos[x].id]
                    break;
                case "password":
                    Objetos[x].value = default_settings[Objetos[x].id]
                    break;
                case "checkbox":
                    value = default_settings[Objetos[x].id]
                    if (value == true) {
                      value = "checked"
                    } else{
                      value = ""
                    }
                    Objetos[x].checked = value
                    break;
                case "select-one":
                    Objetos[x].selectedIndex = default_settings[Objetos[x].id]
                    break;
            }
        }
        Objetos = document.getElementById("Config-popup").getElementsByTagName("select")
        for(x=0;x<Objetos.length;x++){
          switch (Objetos[x].type) {
                case "select-one":
                    if (Objetos[x].name == "enum"){
                      Objetos[x].selectedIndex = default_settings[Objetos[x].id]
                    } else if (Objetos[x].name == "labelenum"){
                      Objetos[x].value = default_settings[Objetos[x].id]
                    }
                    break;
            }
        }

}
function GuardarConfig(Guardar) {
    var Ajustes = {};
    if (Guardar === true) {
        JsonAjustes = {};
        Objetos = document.getElementById("Config-popup").getElementsByTagName("input")
        
        for(x=0;x<Objetos.length;x++){
          switch (Objetos[x].type) {
                case "text":
                    JsonAjustes[Objetos[x].id] = Objetos[x].value;
                    break;
                case "password":
                    JsonAjustes[Objetos[x].id] = Objetos[x].value;
                    break;
                case "checkbox":
                    JsonAjustes[Objetos[x].id] = Objetos[x].checked.toString();
                    break;
                case "select-one":
                    JsonAjustes[Objetos[x].id] = Objetos[x].selectedIndex.toString();
                    break;
            }
        }
        Objetos = document.getElementById("Config-popup").getElementsByTagName("select")
        for(x=0;x<Objetos.length;x++){
          switch (Objetos[x].type) {
                case "select-one":
                    if (Objetos[x].name == "enum"){
                      JsonAjustes[Objetos[x].id] = Objetos[x].selectedIndex.toString();
                    } else if (Objetos[x].name == "labelenum"){
                      JsonAjustes[Objetos[x].id] = Objetos[x].value;
                    }
                    break;
            }
        }
        EnviarDatos({"id":document.getElementById("Config-popup").RequestID, "result":JsonAjustes });
    } else {
        EnviarDatos({"id":document.getElementById("Config-popup").RequestID, "result":false });
    }
    
    AbrirLoading()
}