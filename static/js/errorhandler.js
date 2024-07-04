const closeBtn= document.querySelector("#close-btn");

closeBtn.addEventListener('click', () => {
   history.back();
})