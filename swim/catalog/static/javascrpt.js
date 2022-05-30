function myFunction(imgs) {
    // Get the expanded image
    var expandImg = document.getElementById("expandedImg");
    // Get the image text
    var imgText = document.getElementById("imgtext");
    // Use the same src in the expanded image as the image being clicked on from the grid
    expandImg.src = imgs.src;
    // Use the value of the alt attribute of the clickable image as text inside the expanded image
    imgText.innerHTML = imgs.alt;
    // Show the container element (hidden with CSS)
    expandImg.parentElement.style.display = "block";
  }

const changePP = document.getElementById("changepp")
const buttonPP = document.getElementsByClassName('pbt')


function ppView() {
  
  if (changePP.style.display === "none") {
    changePP.style.display = "block";
  } else {
    changePP.style.display = "none";
  }
}
