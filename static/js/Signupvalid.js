const register = document.getElementById('register')
const surname = document.getElementById('surname')
const othernames = document.getElementById('othernames')
const username = document.getElementById('username')
const password = document.getElementById('password')
const password2 = document.getElementById('password2')
const uphone = document.getElementById('contact')
const uemail = document.getElementById('email')
const staff_type = document.getElementById('staff_type')
const errorElement= document.getElementById('error')
const sex = document.getElementById('gender')

validateform(register)
function validateform(register){
    if (allLetter(surname)){
        if (allLetters(othernames)){
            if (gender(sex)){
                if (allnumeric(uphone)){
                    if (ValidateEmail(uemail)){
                        if (checkPasswords(password,password2)){

                        }
                    }
                }
            }
        }
        register.addEventListener('submit', function(event){
        event.preventDefault();
    })
    }
}

function allLetter(uname){ 
    var letters = /^[A-Za-z]+$/;
    if (uname.value.match(letters))
        {
            return true;
        }
    else
        {
            return false;
        }
}

function allLetters(uname1){ 
    var letters = /^[A-Za-z ]+$/;
    if (uname1.value.match(letters))
        {
            return true;
        }
    else
        {
            return false;
        }
}


function gender(sex){
    if (sex.value === 'Male' || sex.value == 'Female')
        {
            return true;
        }
    else
        {
            return false;
        }
    }

function allnumeric(uphone){ 
    var numbers = /^[0-9]+$/;
    if (uphone.value.match(numbers))
        {
            return true;
        }
    else
        {
            return false;
        }
}

function ValidateEmail(uemail){
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (uemail.value.match(mailformat))
        {
            return true;
        }
    else
        {
            return false;
        }
}

function checkPasswords(Pass1,Pass2){
    if (Pass1 === Pass2)
        {
            return true;
        }
    else
        {
            alert ("Passwords are not the Same!");
            return false;
        }
}