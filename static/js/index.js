
const toggle = document.querySelector(".ham-menu");
const menu = document.querySelector(".navbar");
const menuButton = document.querySelector(".nav-section-2")

toggle.addEventListener("click", toggleMenu);

function toggleMenu(){
    if(menu.style.display){
        menu.style.display = "";
        menuButton.style.display = "";
    }
    else{
        menu.style.display = "flex";
        menuButton.style.display = "block";
    }
}

