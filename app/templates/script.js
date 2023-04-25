// Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

//const XHreq = new XMLHttpRequest(); //make new request object
//const url = 'https://127.0.0.1:5500/seedvault'; //

//user buttons--TOP ROW:
const button1 = document.querySelector("#button1");
const button2 = document.querySelector("#button2");
const button3 = document.querySelector("#button3");
const button4 = document.querySelector("#button4");
const button5 = document.querySelector("#button5");
const button6 = document.querySelector("#button6");
const button7 = document.querySelector("#button7");

//button click actions/functions called when button is clicked:
button1.onclick = showAccount;
button2.onclick = showSeeds;
button3.onclick = showPlants;
button4.onclick = showWishlist;
button5.onclick = showSensorTable;
button6.onclick = showData;
button7.onclick = appendData;

const XHreq = new XMLHttpRequest(); //make new request object
//display seedvault to user--iterate through JSON format for each seed? "i" less than total # of database indexes?

//"blocked by CORS policy: Response to preflight request doesn't pass access control check: It does not have HTTP ok status."
async function showSeeds(){
    console.log("showingSeeds"); //debug
    fetch("http://127.0.0.1.8000/seedvault/marigold", {    //AJAX--fetch url
    //fetch("http://127.0.0.1.5500/seedvault/marigold", {    //AJAX--fetch url
        method: 'GET',
        //method: 'HEAD',
        //method: 'POST',
        //mode: "no-cors",
        headers: {
            'Content-Type': 'application/json',
            //'Content-Type': 'text/xml',
            'Accept': 'application/json',
        },
    })    
    .then(response => response.json())    //return response in JSON format
    .then (response => console.log(response))
    .catch(error => console.log(error))
    }

    function appendData(data) {
        var mainContainer = document.getElementById("data");
        for (var i = 0; i < data.length; i++) {
            var div = document.createElement("div");
            div.innerHTML = 'seed_type: ' + data[i].firstName + ' ' + data[i].lastName;
            mainContainer.appendChild(div);
        }
}

function showAccount(){
    console.log("showAccount")
}

function showPlants(){
    console.log("showPlants") //debug
}

function showWishlist(){
    console.log("showWishlist") //debug
}

function showSensorTable(){
    console.log("showSensorTable") //debug
    const senstbl = document.createElement("table");
    const senstblbdy = document.createElement("tbdy");
    for (let i = 0; i<3; i++) {
        const row = document.createElement("tr");
        
        for (let j=0; j<data.length; j++) {
            const cell = document.createElement("td");
            const cellText = document.createTextNode('cell in row${i}, column ${j}');
            cell.appendChild(cellText);
            row.appendChild(cell);
        }

    }}

function showData(){
    console.log("showData") //debug
}

function showWeather(){
    console.log("showWeather") //debug
}