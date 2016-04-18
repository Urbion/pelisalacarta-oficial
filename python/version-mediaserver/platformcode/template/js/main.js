window.onload = function() {
    Dispose();
    WebSocketConnect();
    DescargarContenido("");
};
window.onresize = function() {
    Dispose();
};
