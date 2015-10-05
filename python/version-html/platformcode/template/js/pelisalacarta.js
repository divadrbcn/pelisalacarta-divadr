//Vars
var Navegacion = [];
var ItemList = "";
var UltimoRequest = "";
var UltimoRequestTime = 0;
var Opciones = {};
var ItemFocus ="";
var TiempoCache =2000;
var Tecla ={"keyCode":0,"Time":0, "Char":""};
var websocket="";
var PlotInterval = "";


//Eventos
window.onload = function() {
    Dispose();
    WebSocketConnect();
    DescargarContenido("");
};
window.onresize = function() {
    Dispose();
};

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
          while (document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children[index-1].children[0].className =="Separador"){
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
          while (document.activeElement.parentNode.parentNode.parentNode.parentNode.parentNode.children[index+1].children[0].className =="Separador"){
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


//Popups
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
  document.getElementById("Contenedor").children[0].children[0].children[0].focus();
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
  AbrirLista(Title,atob(Lista))
}

function AbrirLista(Title,Lista) {
  document.getElementById("Overlay").style.display="block"
  document.getElementById("Lista-titulo").innerHTML = Title;
  document.getElementById("Lista").innerHTML ='<ul class="Lista" data-role="listview" >' + Lista + '</ul>';
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

function AbrirAlert(Title,Text) {
  document.getElementById("Overlay").style.display="block";
  document.getElementById("Alert-popup").style.display="block";
  document.getElementById("Alert-Text").innerHTML = Text
  document.getElementById("Alert-Titulo").innerHTML = Title;
  document.getElementById("Alert-popup").children[3].children[0].focus()
  document.getElementById("Alert-popup").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("Alert-popup").offsetHeight / 2 + "px"
}

function AbrirAlertYesNo(Title,Text) {
  document.getElementById("Overlay").style.display="block";
  document.getElementById("AlertYesNo-popup").style.display="block";
  document.getElementById("AlertYesNo-Text").innerHTML = Text
  document.getElementById("AlertYesNo-Titulo").innerHTML = Title
  document.getElementById("AlertYesNo-popup").children[3].children[0].focus()
  document.getElementById("AlertYesNo-popup").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("AlertYesNo-popup").offsetHeight / 2 + "px"
}


function AbrirKeyboard(Title,Text,Password) {
  if (Title === "") {Title = "Teclado";}
  if (Password == "True") {document.getElementById("Keyboard-Text").type = "password"}
  else {document.getElementById("Keyboard-Text").type = "text"}
  document.getElementById("Overlay").style.display="block";
  document.getElementById("Keyboard-popup").style.display="block";
  document.getElementById("Keyboard-Text").value = Text
  document.getElementById("Keyboard-Titulo").innerHTML = Title
  document.getElementById("Keyboard-popup").children[2].children[0].children[0].focus()
  document.getElementById("Keyboard-popup").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("Keyboard-popup").offsetHeight / 2 + "px"
}

function AbrirProgress(Title,Text,Porcent) {
  document.getElementById("Overlay").style.display="block";
  document.getElementById("ProgressBar-popup").style.display="block";
  document.getElementById("ProgressBar-Text").innerHTML = Text
  document.getElementById("ProgressBar-Titulo").innerHTML = Title
  document.getElementById("ProgressBar-Cancelled").checked = "";
  document.getElementById("ProgressBar-Abance").style.width = Porcent + "%";
  document.getElementById("ProgressBar-popup").children[4].children[0].focus()
  document.getElementById("ProgressBar-popup").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("ProgressBar-popup").offsetHeight / 2 + "px"
}

function UpdateProgress(Title,Text,Porcent) {
  document.getElementById("ProgressBar-Text").innerHTML = Text
  if (document.getElementById("ProgressBar-Cancelled").checked !="") {
    document.getElementById("ProgressBar-Titulo").innerHTML = Title + " " + Porcent + "% - Cancelando...";
  } else {
  document.getElementById("ProgressBar-Titulo").innerHTML = Title + " " + Porcent + "%";
  }
  document.getElementById("ProgressBar-Abance").style.width = Porcent + "%";
}

function CerrarProgress() {
  document.getElementById("Overlay").style.display="none";
  document.getElementById("ProgressBar-popup").style.display="none";
  ItemFocus.focus()
}

function AbrirConfig(Secciones,Lista){
  document.getElementById("Config-secciones").innerHTML = Secciones
  document.getElementById("Config").innerHTML = Lista;
  document.getElementById("Config-Titulo").innerHTML = "Opciones";
  document.getElementById("Config-General").style.display="block";
  document.getElementById("Config").scrollTop = 0;
  document.getElementById("Overlay").style.display="block";
  document.getElementById("Config-popup").style.display="block";
  document.getElementById("Config-popup").children[2].children[0].focus()
  document.getElementById("Config-popup").style.top = document.getElementById("Pagina").offsetHeight / 2 - document.getElementById("Config-popup").offsetHeight / 2 + "px"
}


//Funciones
function Dispose() {
    Height = document.getElementById("Pagina").offsetHeight;
    header = document.getElementById("Header").offsetHeight;
    footer = document.getElementById("Pie").offsetHeight;
    panelheight = Height - header - footer;
    document.getElementById('Contenido').style.height = panelheight + "px"}

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
        setTimeout('WebSocketSend("' + data + '")', 500);
        return;
    } else {
        websocket.send(data);
    }
}


function GetResponses(data) {
    JsonResponse = JSON.parse(data);
    switch (JsonResponse["Action"]) {
        case "Connect":
            document.getElementById("Version").innerHTML = JsonResponse["Version"]
            document.getElementById("Date").innerHTML = JsonResponse["Date"]
            break;
        case "EndItems":
            for (h = 0; h < JsonResponse["Itemlist"].length; h++) {
              JsonItem = JsonResponse["Itemlist"][h]
              //[COLOR xxx][/COLOR]
              var re = /(\[COLOR ([^\]]+)\])(?:.*?)(\[\/COLOR\])/g; 
              var str = JsonItem["Title"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["Title"] = JsonItem["Title"].replace(resultado[1],"<span style='color:"+resultado[2]+"'>")
                  JsonItem["Title"] = JsonItem["Title"].replace(resultado[3],"</span>")
              }
              
              //[B][/B]
              var re = /(\[B\])(?:.*?)(\[\/B\])/g; 
              var str = JsonItem["Title"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["Title"] = JsonItem["Title"].replace(resultado[1],"<b>")
                  JsonItem["Title"] = JsonItem["Title"].replace(resultado[2],"</b>")
              }
              
              //[i][/i]
              var re = /(\[I\])(?:.*?)(\[\/I\])/g; 
              var str = JsonItem["Title"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["Title"] = JsonItem["Title"].replace(resultado[1],"<i>")
                  JsonItem["Title"] = JsonItem["Title"].replace(resultado[2],"</i>")
              }
              //[COLOR xxx][/COLOR]
              var re = /(\[COLOR ([^\]]+)\])(?:.*?)(\[\/COLOR\])/g; 
              var str = JsonItem["Plot"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["Plot"] = JsonItem["Plot"].replace(resultado[1],"<span style='color:"+resultado[2]+"'>")
                  JsonItem["Plot"] = JsonItem["Plot"].replace(resultado[3],"</span>")
              }
              
              //[B][/B]
              var re = /(\[B\])(?:.*?)(\[\/B\])/g; 
              var str = JsonItem["Plot"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["Plot"] = JsonItem["Plot"].replace(resultado[1],"<b>")
                  JsonItem["Plot"] = JsonItem["Plot"].replace(resultado[2],"</b>")
              }
              
              //[i][/i]
              var re = /(\[I\])(?:.*?)(\[\/I\])/g; 
              var str = JsonItem["Plot"];
              while ((resultado= re.exec(str)) !== null) {
                  if (resultado.index === re.lastIndex) {
                      re.lastIndex++;
                  }
                  JsonItem["Plot"] = JsonItem["Plot"].replace(resultado[1],"<i>")
                  JsonItem["Plot"] = JsonItem["Plot"].replace(resultado[2],"</i>")
              }
              if (JsonItem["ItemAction"]=="go_back"){
                Action = 'Back()'
              }else{
                Action = 'DescargarContenido(\''+ JsonItem["Url"] +'\')'
              }
              if (JsonItem["Mode"]==0){
                HtmlItem ='<li class="ListItemBanner"><a onblur="" onfocus="ItemFocus=this" onmouseover="this.focus()" class="ListItem {$ClassMenu}" href="javascript:void(0)" onclick="ItemFocus=this;'+Action+'"><div class="ListItem"><img class="ListItem" onerror="ImgLocal(this)" alt="'+JsonItem["Host"]+'" src="'+JsonItem["Thumbnail"]+'"></div><h3 class="ListItem">' + JsonItem["Title"] + '</h3><p class="ListItem"></p></a>{$BotonMenu}</li>'
              }else if (JsonItem["Mode"]==1){
                HtmlItem ='<li class="ListItemChannels"><a onblur="DesCargarInfo(this)" onfocus="ItemFocus=this" onmouseover="this.focus()" class="ListItem {$ClassMenu}" href="javascript:void(0)" onclick="ItemFocus=this;'+Action+'"><h3 class="ListItem">' + JsonItem["Title"] + '</h3><div class="ListItem"><img class="ListItem" onerror="ImgLocal(this)" alt="'+JsonItem["Host"]+'" src="'+JsonItem["Thumbnail"]+'"></div></a>{$BotonMenu}</li>'
             
              }else if (JsonItem["Mode"]==2){
                if (JsonItem["ItemAction"]=="go_back" || JsonItem["ItemAction"]=="search" || JsonItem["Thumbnail"].indexOf("thumb_folder") != -1 || JsonItem["Thumbnail"].indexOf("thumb_nofolder") != -1 || JsonItem["Thumbnail"].indexOf("thumb_error") != -1){
                  HtmlItem ='<li class="ListItem"><a onfocus="DesCargarInfo(this);ItemFocus=this" onmouseover="this.focus()" class="ListItem {$ClassMenu}" href="javascript:void(0)" onclick="ItemFocus=this;'+Action+'"><div class="ListItem"><img class="ListItem" onerror="ImgError(this)" alt="'+JsonItem["Host"]+'" src="'+JsonItem["Thumbnail"]+'"><img class="Default" src="http://pelisalacarta.mimediacenter.info/squares/folder.png"></div><h3 class="ListItem">' + JsonItem["Title"] + '</h3><p class="ListItem">' + JsonItem["Plot"] + '</p></a>{$BotonMenu}</li>'
                }else{
                  HtmlItem ='<li class="ListItem"><a onblur="DesCargarInfo(this)" onfocus="CargarInfo(this);ItemFocus=this" onmouseover="this.focus()" class="ListItem {$ClassMenu}" href="javascript:void(0)" onclick="ItemFocus=this;'+Action+'"><div class="ListItem"><img class="ListItem" onerror="ImgError(this)" alt="'+JsonItem["Host"]+'" src="'+JsonItem["Thumbnail"]+'"><img class="Default" src="http://pelisalacarta.mimediacenter.info/squares/folder.png"></div><h3 class="ListItem">' + JsonItem["Title"] + '</h3><p class="ListItem">' + JsonItem["Plot"] + '</p></a>{$BotonMenu}</li>'
                }
              }
              Lista = "";
              for (x = 0; x < JsonItem["ContextMenu"]["Count"]; x++) {
                Lista +=
                '<li class="Lista"><a href="javascript:void(0)" onclick="CerrarDialogos();DescargarContenido(\'' + JsonItem["ContextMenu"]["Url" + x] +
                '\')" class="Lista"><h3>' + JsonItem["ContextMenu"]["Title" + x] + '</h3></a></li>';
              }
              BotonMenu = '<a class="ListItemButton" href="javascript:void(0)" onmouseover="this.focus()" onclick=\'ItemFocus=this;AbrirMenu("Menu","'+btoa(Lista)+'")\'></a>';
              ClassMenu = "ListItemMenu"
              if (JsonItem["ContextMenu"]["Count"] === 0) {
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
            
            EnviarDatos("OK");
            CerrarLoading()
            break;
        case "Refresh":
            Consulta = Navegacion[Navegacion.length - 1].Url;
            Navegacion[Navegacion.length - 1].Scroll = document.getElementById("Contenedor").scrollTop;
            Navegacion[Navegacion.length - 1].Focus  = Array.prototype.indexOf.call(document.getElementById("itemlist").children, ItemFocus.parentNode);
            DescargarContenido(Consulta);
            EnviarDatos("OK");
            break;
        case "Alert":
            CerrarLoading()
            AbrirAlert(JsonResponse["Title"],JsonResponse["Text"].replace(new RegExp("\n", 'g'), "<br/>"))
            break;
        case "AlertYesNo":
            CerrarLoading()
            AbrirAlertYesNo(JsonResponse["Title"],JsonResponse["Text"].replace(new RegExp("\n", 'g'), "<br/>"))
            break;
        case "Progress":
            CerrarLoading()
            AbrirProgress(JsonResponse["Title"],JsonResponse["Text"].replace(new RegExp("\n", 'g'), "<br/>"),JsonResponse["Progress"])
            EnviarDatos("OK");
            break;
        case "ProgressIsCanceled":
            EnviarDatos(document.getElementById("ProgressBar-Cancelled").checked !="");
            break;
        case "isPlaying":
            EnviarDatos(document.getElementById("Player-popup").style.display=="block" || document.getElementById("Lista-popup").style.display=="block");
            break;
        case "ProgressUpdate":
            UpdateProgress(JsonResponse["Title"],JsonResponse["Text"].replace(new RegExp("\n", 'g'), "<br/>"),JsonResponse["Progress"])
            break;
        case "ProgressClose":
            CerrarProgress();
            EnviarDatos("OK");
            CerrarLoading()
            break;
        case "Keyboard":
            CerrarLoading()
            AbrirKeyboard(JsonResponse["Title"], JsonResponse["Text"], JsonResponse["Password"]);
            break;
        case "List":
            CerrarLoading()
            Lista = "";
            for (x = 0; x < JsonResponse["List"]["Count"]; x++) {
                Lista +=
                    '<li class="Lista"><a href="javascript:void(0)" onmouseover="this.focus()" onclick="CerrarDialogos();EnviarDatos(\'' + x +
                    '\')" class="Lista"><h3>' + JsonResponse["List"]["Title" + x] + '</h3></a></li>';
            }
            AbrirLista(JsonResponse["Title"],Lista)
            break;
        case "Play":
            EnviarDatos("OK");
            CerrarLoading()
            if(!new RegExp("^(.+://)").test(JsonResponse["Url"])){
             JsonResponse["Url"] = JsonResponse["Host"]+"/local-"+encodeURIComponent(btoa(Utf8.encode(JsonResponse["Url"])))+".mp4"}
             
            else if(new RegExp("^(?:http\://.*?\.vkcache\.com)").test(JsonResponse["Url"])){
            
             JsonResponse["Url"] = JsonResponse["Host"]+"/netutv-"+encodeURIComponent(btoa(Utf8.encode(JsonResponse["Url"])))+".mp4"} 
            
            ProxyUrl = JsonResponse["Host"]+"/remote-"+encodeURIComponent(btoa(Utf8.encode(JsonResponse["Url"])))+".mp4"
            Lista  = '<li onmouseover="this.focus()" class="Lista"><a href="#" onmouseover="this.focus()" onclick="CerrarDialogos();Play(\''+JsonResponse["Url"]+'\',\''+btoa(JsonResponse["Title"])+'\')" class="Lista"><h3>Abrir Enlace</h3></a></li>';
            Lista += '<li onmouseover="this.focus()" class="Lista"><a href="#" onmouseover="this.focus()" onclick="CerrarDialogos();Play_VLC(\''+JsonResponse["Url"]+'\',\''+btoa(JsonResponse["Title"])+'\')" class="Lista"><h3>Plugin VLC</h3></a></li>';
            Lista += '<li onmouseover="this.focus()" class="Lista"><a href="#" onmouseover="this.focus()" onclick="CerrarDialogos();Play_HTML(\''+ProxyUrl+'\',\''+btoa(JsonResponse["Title"])+'\')" class="Lista"><h3>Video HTML</h3></a></li>';
            AbrirLista("Elige el Reproductor",Lista)

            break;
        case "Update":
            DescargarContenido(JsonResponse["Url"]);
            EnviarDatos("OK");
            CerrarLoading()
            break;
        case "HideLoading":
            CerrarLoading()
            break;
        case "OpenConfig":
            CerrarLoading()
            Opciones = {};
            for (x = 0; x < JsonResponse["Options"]["Count"]; x++) {
                if (typeof(Opciones[JsonResponse["Options"]["Category" + x]]) == 'undefined') {
                    Opciones[JsonResponse["Options"]["Category" + x]] = "";
                }
                switch (JsonResponse["Options"]["Type" + x]) {
                    case "sep":
                        Opciones[JsonResponse["Options"]["Category" + x]] +=
                            '<li class="ListItem" data-icon="false" ><div class="Separador" ></div></li>';
                        break;
                    case "text":
                        if (JsonResponse["Options"]["Option" + x] == "hidden") {
                            Opciones[JsonResponse["Options"]["Category" + x]] += '<li class="ListItem" ><div class="ListItem" ><h3 class="Ajuste" >' + JsonResponse["Options"]["Label" + x] + '</h3><span class="Control"><div class="Text"><input class="Text" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" type="password" id="' + JsonResponse["Options"]["Id" + x] + '" value="' + JsonResponse["Options"]["Value" + x] + '" ></div></span</div></li>';
                        } else {
                            Opciones[JsonResponse["Options"]["Category" + x]] += '<li class="ListItem" ><div class="ListItem" ><h3 class="Ajuste" >' + JsonResponse["Options"]["Label" + x] + '</h3><span class="Control"><div class="Text"><input class="Text" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" type="text" id="' + JsonResponse["Options"]["Id" + x] + '" value="' + JsonResponse["Options"]["Value" + x] + '" ></div></span</div></li>';
                        }
                        break;
                    case "bool":
                        if (JsonResponse["Options"]["Value" + x] == "true") {
                            Opciones[JsonResponse["Options"]["Category" + x]] += '<li class="ListItem" ><div class="ListItem" ><h3 class="Ajuste" >' + JsonResponse["Options"]["Label" + x] + '</h3><span class="Control"><div class="Check"><input class="Check" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" type="checkbox" checked=checked id="' + JsonResponse["Options"]["Id" + x] + '" value="' + JsonResponse["Options"]["Value" + x] + '" ></div></span</div></li>';
                        } else {
                            Opciones[JsonResponse["Options"]["Category" + x]] += '<li class="ListItem" ><div class="ListItem" ><h3 class="Ajuste" >' + JsonResponse["Options"]["Label" + x] + '</h3><span class="Control"><div class="Check"><input class="Check" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" type="checkbox" id="' + JsonResponse["Options"]["Id" + x] + '" value="' + JsonResponse["Options"]["Value" + x] + '" ></div></span</div></li>';
                        }
                        break;
                    case "enum":
                        if (JsonResponse["Options"]["Values" + x] === "") {
                            Opcion = JsonResponse["Options"]["Lvalues" + x].split("|");
                            for (y = 0; y < Opcion.length; y++) {
                                Opcion[y] = y;
                            }
                        } else {
                            Opcion = JsonResponse["Options"]["Values" + x].split("|");
                        }
                        SOpciones = "";
                        for (y = 0; y < Opcion.length; y++) {
                            if (JsonResponse["Options"]["Value" + x] == Opcion[y]) {
                                if (JsonResponse["Options"]["Lvalues" + x] === "") {
                                    SOpciones += "<option selected=selected>" + JsonResponse["Options"]["Values" + x].split("|")[y] +
                                        "</option>";
                                } else {
                                    SOpciones += "<option selected=selected>" + JsonResponse["Options"]["Lvalues" + x].split("|")[y] +
                                        "</option>";
                                }
                            } else {
                                if (JsonResponse["Options"]["Lvalues" + x] === "") {
                                    SOpciones += "<option>" + JsonResponse["Options"]["Values" + x].split("|")[y] +
                                        "</option>";
                                } else {
                                    SOpciones += "<option>" + JsonResponse["Options"]["Lvalues" + x].split("|")[y] + "</option>";
                                }
                            }
                        }
                        Opciones[JsonResponse["Options"]["Category" + x]] += '<li class="ListItem" ><div class="ListItem" ><h3 class="Ajuste" >' + JsonResponse["Options"]["Label" + x] + '</h3><span class="Control"><div class="Select"><select class="Select" onfocus="this.parentNode.parentNode.parentNode.className=\'ListItem ListItem-hover\'" onblur="this.parentNode.parentNode.parentNode.className=\'ListItem\'" id="' + JsonResponse["Options"]["Id" + x] + '" >' + SOpciones + '</select></div></span</div></li>';
                        break;
                    default:
                        break;
                }

            }
            Secciones = "";
            Lista = "";
            for (var key in Opciones) {
                if (Opciones.hasOwnProperty(key)) {
                    Secciones += '<a href="javascript:void(0)" class="Boton" onmouseover="this.focus()" onclick="MostrarSeccion(\'' + key + '\')">' + key + '</a>\n';
                    Lista +=
                        '<ul class="ListItem" style="display:none" id="Config-' + key + '">' + Opciones[key] + '</ul>';
                }
            }
            AbrirConfig(Secciones,Lista)

            break;

        default:
            break;
    }
}
function Play(Url,Title){
  window.open(Url);
}

function Play_VLC(Url,Title){
  HtmlItem =
      '<div class="VideoCaja"><div class="VideoContenido"><object classid="clsid:9BE31822-FDAD-461B-AD51-BE1D1C159921" codebase="http://downloads.videolan.org/pub/videolan/vlc/latest/win32/axvlc.cab" id="vlc" events="False" style="width:100%; height:100%"><param name="Src" value="' +
      Url +
      '"></param><param name="ShowDisplay" value="True" ></param><param name="AutoLoop" value="no"></param><param name="AutoPlay" value="yes"></param><embed type="application/x-google-vlc-plugin" name="vlcfirefox" autoplay="yes" loop="no" width="100%" height="100%" target="' +
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
  if (obj.src.indexOf("http://") == 0){
  
  if (obj.src.indexOf(obj.alt) !== 0){
    obj.src=obj.alt+"/image-"+encodeURIComponent(btoa(obj.src))
  }else{obj.style.display="none";obj.parentNode.children[1].style.display="inline-block"}
  }else{ImgLocal(obj)}
}
function ImgLocal(obj){
  if (obj.src.indexOf(obj.alt) !== 0){
    obj.src=obj.alt+"/local-"+encodeURIComponent(btoa(obj.src))
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
                    JsonAjustes[Objetos[x].id] = Objetos[x].selectedIndex.toString();
                    break;
            }
        }
        EnviarDatos(JSON.stringify(JsonAjustes));
    } else {
        EnviarDatos("-1");
    }
    
    AbrirLoading()
}

function DescargarContenido(url) {
    AbrirLoading()
    ItemList = "";

    UltimoRequest = url;
    UltimoRequestTime = new Date().getTime();
    WebSocketSend("?" + url);
}

function EnviarDatos(dato) {
    WebSocketSend("!" + dato);
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
    Ruta +=" > " + NuevoItem
    }
    }

//    document.getElementById("Contenedor").children[0].children[0].children[0].children[2].innerHTML = "<span class='Atras'>"+Ruta+"</span>";
  }
}
var Utf8 = { // public method for url encoding
    encode: function(string) {
        string = string.replace(/\r\n/g, "\n");
        var utftext = "";
        for (var n = 0; n < string.length; n++) {
            var c = string.charCodeAt(n);
            if (c < 128) {
                utftext += String.fromCharCode(c);
            } else if ((c > 127) && (c < 2048)) {
                utftext += String.fromCharCode((c >> 6) | 192);
                utftext += String.fromCharCode((c & 63) | 128);
            } else {
                utftext += String.fromCharCode((c >> 12) | 224);
                utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                utftext += String.fromCharCode((c & 63) | 128);
            }
        }

        return utftext;
    }, // public method for url decoding
    decode: function(utftext) {
        var string = "";
        var i = 0;
        var c = c1 = c2 = 0;
        while (i < utftext.length) {
            c = utftext.charCodeAt(i);
            if (c < 128) {
                string += String.fromCharCode(c);
                i++;
            } else if ((c > 191) && (c < 224)) {
                c2 = utftext.charCodeAt(i + 1);
                string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
                i += 2;
            } else {
                c2 = utftext.charCodeAt(i + 1);
                c3 = utftext.charCodeAt(i + 2);
                string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
                i += 3;
            }
        }
        return string;
    }
};