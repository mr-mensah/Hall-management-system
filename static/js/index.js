const sideMenu= document.querySelector("aside");
const menuBtn= document.querySelector("#menu-btn");
const closeBtn= document.querySelector("#close-btn");
const data_icon = document.querySelector(".data-icon");

// call active on pages with tables
console.log(window.location.pathname);
if (window.location.pathname == `/database`){
    data_icon.classList.add("active")
}


//show sidebar
    menuBtn.addEventListener('click', () => {
        sideMenu.style.display = 'block';
    })

//hide sidebar
    closeBtn.addEventListener('click', () => {
        sideMenu.style.display = 'none';
    })


const timeOut =document.querySelector("#TimeOut");
const signOut =document.querySelector(".sign-out");

// if (timeOut.value)