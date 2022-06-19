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


      let saver = document.querySelector('.save') // 
            console.log("saver", saver)
            let saveId = saver.id.slice(4, saver.id.length)
            console.log("this is saveID" + saveId)
            
            saver.onclick = function () {

                save(saveId)


            }

            function save(id) {
              fetch(`/save_swim/${id}`, { //calls the django function on the id passed in
                  method: 'GET',
                  credentials: 'same-origin',
                  headers : { 
                      "X-CSRFToken": getCookie("csrftoken")
                     }
              })
              .then(response => { return response.json() } //
          )
              .then( data => {
                  sBut = document.querySelector(`#save${id}`)
                
                  if (data["ifsaved"] === True) {
                      console.log("true")
                      sbut.innerHTML = `<br><button type="button" id="save${id}" class="pbt btn btn-outline-info"><a href="{% url 'save_swim' ${id} %}">Save this swim</a></button>`
                  } else
                   {   sbut.innerHTML =  `<br><button type="button" id="save${id}" class="pbt btn btn-outline-info"><a href="{% url 'save_swim' ${id} %}">Save this swim</a></button>`
                      console.log("false")
                     
                    }
              
          })}


          function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;} 
                  