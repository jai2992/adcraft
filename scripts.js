var form_1 = document.querySelector(".form_1");
var form_2 = document.querySelector(".form_2");
var form_3 = document.querySelector(".form_3");

var form_1_btns = document.querySelector(".form_1_btns");
var form_2_btns = document.querySelector(".form_2_btns");
var form_3_btns = document.querySelector(".form_3_btns");

var form_1_next_btn = document.querySelector(".form_1_btns .btn_next");
var form_2_back_btn = document.querySelector(".form_2_btns .btn_back");
var form_2_next_btn = document.querySelector(".form_2_btns .btn_Craft");
var form_3_back_btn = document.querySelector(".form_3_btns .btn_back");

var form_2_progessbar = document.querySelector(".form_2_progessbar");
var form_3_progessbar = document.querySelector(".form_3_progessbar");

form_1_next_btn.addEventListener("click", function(){
    form_1.style.display = "none";
    form_2.style.display = "block";

    form_1_btns.style.display = "none";
    form_2_btns.style.display = "flex";

    form_2_progessbar.classList.add("active");
});

form_2_back_btn.addEventListener("click", function(){
    form_1.style.display = "block";
    form_2.style.display = "none";

    form_1_btns.style.display = "flex";
    form_2_btns.style.display = "none";

    form_2_progessbar.classList.remove("active");
});

const loading_overlay = document.getElementById("loading_overlay");
form_2_next_btn.addEventListener("click", function(){
    showLoadingOverlay();

    setTimeout(function() {
        hideLoadingOverlay();

        form_2.style.display = "none";
        form_3.style.display = "block";
        form_3_btns.style.display = "flex";
        form_2_btns.style.display = "none";
        form_3_progessbar.classList.add("active");
    }, 10000); // 10 seconds in milliseconds
});

function showLoadingOverlay() {
    loading_overlay.style.display = "block";
}

function hideLoadingOverlay() {
    loading_overlay.style.display = "none";
}

form_3_back_btn.addEventListener("click", function(){
    form_2.style.display = "block";
    form_3.style.display = "none";

    form_3_btns.style.display = "none";
    form_2_btns.style.display = "flex";

    form_3_progessbar.classList.remove("active");
});

function downloadImage() {
    const imageName = "./adcraft-backend/generated_img.png";

    const downloadLink = document.createElement('a');
    downloadLink.href = imageName;
    downloadLink.download = imageName;

    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

var element = document.getElementById("slogan");

function sendPostRequest() {
    var xhr = new XMLHttpRequest();
    var url = './gen';
    var brand = document.getElementById('brand').value;
    var category = document.getElementById('category').value;
    var slogan = document.getElementById('slogan').value;
    let sloganRadios = document.getElementsByName('slogan');
    
    function getSloganValue() {
        for(let i = 0; i < sloganRadios.length; i++) {
            if(sloganRadios[i].checked) {
                return sloganRadios[i].value;
            }
        }
    }
    
    let sloganValue = getSloganValue();
    if(sloganValue === 'yes') {
        console.log('Slogan is needed.');
    } else if(sloganValue === 'no') {
        console.log('Slogan is not needed.');
        slogan = '';
    }

    var textarea = document.getElementById("ad_background");

    function updateCategory() {
        if(textarea.value.trim() !== "") {
            category = textarea.value;
            console.log(textarea.value)
        }
    }
    updateCategory();
    console.log(category,brand,slogan);
    var data = JSON.stringify({
      brand: brand,
      slogan: slogan,
      category: category
    });

    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          console.log('Response:', xhr.responseText);
          console.log('Status Code:', xhr.status);
        } else {
          console.error('Error:', xhr.statusText);
          console.error('Status Code:', xhr.status);
        }
      }
    };

    xhr.send(data);
}

const imgElement = document.getElementById("img1");

setInterval(function() {
    imgElement.src = ".adcraft-backend/generated_img.png?timestamp=" + new Date().getTime();
}, 10000);

function populateOptions(selectElement, data) {
  for (var i = 0; i < data.length; i++) {
      var option = document.createElement("option");
      option.value = data[i];
      option.text = data[i];
      selectElement.add(option);
  }
}

var categorySelect = document.getElementById("category");
populateOptions(categorySelect, Object.keys(jsonData));

var sloganSelect = document.getElementById("slogan");
populateOptions(sloganSelect, jsonData[Object.keys(jsonData)[0]]);

categorySelect.addEventListener("change", updateSlogans);
