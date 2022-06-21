
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
  $.ajax({
      method: "POST",
      url: `../../catalog/save_swim/${id}/`,
      headers : {  "X-CSRFToken": getCookie("csrftoken")  },
      data: {},
      success: function(data) {
      console.log(data) // check out how data is structured
      
      if (data["ifsaved"]["scount"] === true) {
       
        $('.savo').hide().replaceWith(`<button type="button" id="save${id}" class="savo pbt btn btn-outline-info">Unsave this swim</button>`)
    } else
     {         
      $('.savo').hide().replaceWith(`<button type="button" id="save${id}" class="savo pbt btn btn-outline-info">Save this swim</button>`)
       
      } 
  
                }
              })
            };


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
                  