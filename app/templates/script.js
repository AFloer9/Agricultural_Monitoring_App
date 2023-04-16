// Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

//user buttons:
//const button1 = document.querySelector("#button1");
//const button2 = document.querySelector("#button2");
//const button3 = document.querySelector("#button3");
//const button4 = document.querySelector("#button4");
//const button5 = document.querySelector("#button5");
//const button6 = document.querySelector("#button6");
//const button7 = document.querySelector("#button7");

//button click actions (code to run when clicked):
button1.onclick = showAccount;
//button2.onclick = showSeeds;
//button2.onclick = test1;
button3.onclick = showPlants;
button4.onclick = showWishlist;
button5.onclick = showSensors;
button6.onclick = showData;
button7.onclick = showWeather;

function test1(){
    const xhrobj = new XMLHttpRequest(); //make new request object
    const url = 'https://127.0.0.1:8000/seedvault'; //
    xhrobj.open("GET", url, true);
    xhrobj.onreadystatechange = function () {
        if(this.status == 200) {
            console.log(this.responseText);
        }
    }
    xhrobj.send();
}

function showAccount(){
    console.log("showAccount")

}

//display seedvault to user--iterate through JSON format for each seed? "i" less than total # of database indexes?
//showSeeds(SEEDVAULT)
//function showSeeds(url){
function showSeeds(){
    console.log("showSeeds"); //debug
    const url = 'https://127.0.0.1:8000/seedvault'; //
    fetch(url, { //first method
    //fetch('/seedvault/', //{ //first method
    //fetch('https://reqres.in/api/users'  //test API
        method: 'GET',                          //HTTP request method
        headers: {                              //HTTP headers
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            //'Access-Control-Allow-Origin': 'no-cors'
        },
       //body: JSON.stringify({

       //})  //passed data--XMLHTTP request to SEEDVAULT
    }
   )    
    //.then(res => res.json())                    //return response in JSON format
    .then(res => {
        return res.json()})                    //return result in JSON format
    .then (data => {console.log(data);})           //show returned data in console
    .catch(error => console.log("ERROR"))
    ///////////////////////////////////////////////////////
    //SEEDVAULT.open("GET", "https://127.0.0.1:8000/seedvault");    //second method
    //SEEDVAULT.send;
    //SEEDVAULT.responseType = "json";
    //SEEDVAULT.onload = () => {
    //    const data = SEEDVAULT.response
   //     console.log(data);
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