function myFunction() {
    alert("Hello from a static file!");
  }

function alertMessage() {
    alert("Alert in proper style");
}

function navFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
} 

