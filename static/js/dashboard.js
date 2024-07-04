// set date and time for dashboard
    var date = new Date();
    var currentDate = date.toISOString().substring(0,10);
    var currentTime = date.toISOString().substring(11,16);

    document.getElementById('currentDate').value = currentDate;
    document.getElementById('currentTime').value = currentTime;


// select an active tab
    const icons = document.querySelector(".dash-icon");
    icons.classList.add("active")