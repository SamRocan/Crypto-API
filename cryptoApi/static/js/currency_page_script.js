console.log("Working");

function dark_light_mode(){
    var checkBox = document.getElementById("dark_light");

    if (checkBox.checked == true){
        console.log("Dark");
        document.body.style.background = '#040c1f';
        document.body.style.backgroundImage = 'linear-gradient(315deg, #3a496e 0%, #040c1f 74%)'
        containers = document.getElementsByClassName('currency-info-section')
        for (i = 0; i < containers.length; i++) {
            containers[i].style.color = 'rgba(233,233,233,0.8)';
        }

    } else {
        document.body.style.backgroundColor = '#f8f9d2';
        document.body.style.backgroundImage = 'linear-gradient(315deg, #f8f9d2 0%, #e8dbfc 74%)'
        for (i = 0; i < containers.length; i++) {
            containers[i].style.color = 'rgba(14, 50, 92, 0.6)';
        }
    }
}