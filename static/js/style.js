// Activating the links
var nav_list = $('.nav-items');
var current = window.location.pathname;

for (var i=0; i<nav_list.children().length; i++){
  var child = nav_list.children()[i].children;
  if (child[0].getAttribute("href")==current){
      nav_list.children()[i].classList.add('active');
  }
  else{
    if (nav_list.children()[i].classList.contains('active')){
        nav_list.children()[i].classList.remove('active');
    }
  }  
}