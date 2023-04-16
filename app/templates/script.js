// Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

const XHreq = new XMLHttpRequest(); //make new request object
const url = 'https://127.0.0.1:8000/seedvault'; //

//user buttons:
const button1 = document.querySelector("#button1");
const button2 = document.querySelector("#button2");
const button3 = document.querySelector("#button3");
const button4 = document.querySelector("#button4");
const button5 = document.querySelector("#button5");
const button6 = document.querySelector("#button6");
const button7 = document.querySelector("#button7");

//button click actions:
button1.onclick = showAccount;
button2.onclick = showSeeds;
button3.onclick = showPlants;
button4.onclick = showWishlist;
button5.onclick = showSensors;
button6.onclick = showData;
button7.onclick = showWeather;

function showAccount(){
    console.log("showAccount")
}

//display seedvault to user--iterate through JSON format for each seed? "i" less than total # of database indexes?
//showSeeds(SEEDVAULT)
//function showSeeds(url){
function showSeeds(){
    console.log("showSeeds"); //debug
    fetch("https://127.0.0.1:8000/seedvault", { //first method
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(XHreq)  
    })    
    .then(res => res.json())
    .then (data => console.log(data))
    .catch(error => console.log("ERROR"))
    ///////////////////////////////////////////////////////
    //SEEDVAULT.open("GET", "https://127.0.0.1:8000/seedvault");    //second method
    //SEEDVAULT.send;
    //SEEDVAULT.responseType = "json";
    //SEEDVAULT.onload = () => {
    //    const data = SEEDVAULT.response
   //     console.log(data);
    }

    function appendData(data) {
        var mainContainer = document.getElementById("myData");
        for (var i = 0; i < data.length; i++) {
            var div = document.createElement("div");
            div.innerHTML = 'Name: ' + data[i].firstName + ' ' + data[i].lastName;
            mainContainer.appendChild(div);
        }
}

function showPlants(){
    console.log("showPlants") //debug
}

function showWishlist(){
    console.log("showWishlist") //debug
}

function showSensors(){
    console.log("showSensors") //debug
}

function showData(){
    console.log("showData") //debug
}

function showWeather(){
    console.log("showWeather") //debug
}