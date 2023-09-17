function showEmergente() {


    let ventana= document.getElementsByClassName("ventanaEmergente")[0]

    ventana.style.display="block";

}

function closeEmergente() {


    let ventana= document.getElementsByClassName("ventanaEmergente")[0]

    ventana.style.display="none";
    
}

function showInstaLogin() {

    let ventana= document.getElementsByClassName("ventanaEmergenteInsta")[0]

    ventana.style.display="flex";
    body.style.overflow="hidden";

}

function closeInstaLogin() {


    let ventana= document.getElementsByClassName("ventanaEmergenteInsta")[0]

    ventana.style.display="none";

    let body= document.getElementsByTagName("body")[0]

    body.style.overflow="scroll";
    
}