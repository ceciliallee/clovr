// Load in animation
document.addEventListener("DOMContentLoaded", function () {
    var header = document.getElementById("body");
    header.classList.add("loaded");
  });


/* Navbar */

// get the hamburger element
var hamburger = document.getElementById("hamburger");

// get the menu element
var menu = document.getElementById("menu");

// get the overlay element
var overlay = document.getElementById("overlay");

// define toggle function
function toggleMenu() {
    // Either adds/removes active class from element
    menu.classList.toggle("active");
    overlay.classList.toggle("active");
}

// execute toggle function from hamburger on click
hamburger.addEventListener("click", toggleMenu);

// exuecute toggle function from menu on click
menu.addEventListener("click", toggleMenu);

// exuecute toggle function from overlay on click
overlay.addEventListener("click", toggleMenu);

