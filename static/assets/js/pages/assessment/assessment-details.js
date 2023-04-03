//##### Overview-Page for Show & Hide:
let items = document.querySelectorAll(".s-card");

let close = document.querySelectorAll(".sg-close");

if (document.getElementById("info-1")){
    var info1 = document.getElementById("info-1");
    var info2 = document.getElementById("info-2");
    var info3 = document.getElementById("info-3");
    var info4 = document.getElementById("info-4");
    var info5 = document.getElementById("info-5");
    var info6 = document.getElementById("info-6");
}else{
    var info7 = document.getElementById("info-7");
    var info8 = document.getElementById("info-8");
    var info9 = document.getElementById("info-9");
    var info10 = document.getElementById("info-10");
    var info11 = document.getElementById("info-11");
    var info12 = document.getElementById("info-12");
    var info13 = document.getElementById("info-13");
}



items.forEach(function (item) {
  console.log(item);
  item.addEventListener("click", show);
});


close.forEach(function (item) {
  console.log(item);
  item.addEventListener("click", hide);
});


function hide () {
    if (document.getElementById("info-1")){
        info1.style.display = "none";
        info2.style.display = "none";
        info3.style.display = "none";
        info4.style.display = "none";
        info5.style.display = "none";
        info6.style.display = "none";
    }else{
        info7.style.display = "none";
        info8.style.display = "none";
        info9.style.display = "none";
        info10.style.display = "none";
        info11.style.display = "none";
        info12.style.display = "none";
        info13.style.display = "none";
    }
  window.scrollTo(0, -1000);
}


function show (e) {
  hide();
  switch (e.target.id) {
    case 'num-1':
        info1.style.display = "block";
        break;
    case 'num-2':
        info2.style.display = "block";
        break;
    case 'num-3':
        info3.style.display = "block";
        break;
    case 'num-4':
        info4.style.display = "block";
        break;
    case 'num-5':
        info5.style.display = "block";
        break;
    case 'num-6':
        info6.style.display = "block";
        break;
    case 'num-7':
        info7.style.display = "block";
        break;
    case 'num-8':
        info8.style.display = "block";
        break;
    case 'num-9':
        info9.style.display = "block";
        break;
    case 'num-10':
        info10.style.display = "block";
        break;
    case 'num-11':
        info11.style.display = "block";
        break;
    case 'num-12':
        info12.style.display = "block";
        break;
    case 'num-13':
        info13.style.display = "block";
        break;
  }
  e.preventDefault();
}