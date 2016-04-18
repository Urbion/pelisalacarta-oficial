function WebSocketConnect() {
    if (websocket!=""){websocket.close()}
    document.getElementById("Conexion").innerHTML = "Conectando...";
    document.getElementById("Loading-Text").innerHTML = "Estableciendo conexión...";
    websocket = new WebSocket(WebSocketHost);
    websocket.onopen = function(evt) {
        document.getElementById("Loading-Text").innerHTML = "Cargando...";
        document.getElementById("Conexion").innerHTML = "Conectado";
    };

    websocket.onclose = function(evt) {
        document.getElementById("Conexion").innerHTML = "Desconectado";
    };

    websocket.onmessage = function(evt) {
        GetResponses(evt.data);
    };

    websocket.onerror = function(evt) {
        websocket.close();
    };
}

function WebSocketSend(data) {
    if (websocket.readyState != 1) {
        WebSocketConnect()
        setTimeout(WebSocketSend, 500, data);
        return;
    } else {
      data["id"] = ID
      websocket.send(JSON.stringify(data));
    }
}


function DescargarContenido(url) {
    AbrirLoading()
    ItemList = "";

    UltimoRequest = url;
    UltimoRequestTime = new Date().getTime();
    Send = {}
    Send["request"] = url
    WebSocketSend(Send);
}

function EnviarDatos(dato) {
    Send = {}
    Send["data"] = dato
    WebSocketSend(Send)
}
