
var myNav = document.getElementById('mynav');
window.onscroll = function () {
      "use strict";
       if (document.body.scrollTop >= 20 || document.documentElement.scrollTop >= 20 ) {
          myNav.classList.add("nav-colored");
          console.log($('ul.navbar-nav>li.nav-item>a.nav-link'));
          $('ul.navbar-nav>li.nav-item>a.nav-link').addClass('custom');
          myNav.classList.remove("nav-transparent");
      } 
      else {
          myNav.classList.add("nav-transparent");
          myNav.classList.remove("nav-colored");
          $('ul.navbar-nav>li.nav-item>a.nav-link').removeClass('custom');
      }
};

$(".ongray").hover(
  function(){$(this).addClass("g")},
  function(){$(this).removeClass("g");}
);

const getCookie = (name) => {
  const value = " " + document.cookie;
  console.log("value", `==${value}==`);
  const parts = value.split(" " + name + "=");
  return parts.length < 2 ? undefined : parts.pop().split(";").shift();
};

const setCookie = function (name, value, expiryDays, domain, path, secure) {
  const exdate = new Date();
  exdate.setHours(
    exdate.getHours() +
      (typeof expiryDays !== "number" ? 365 : expiryDays) * 24
  );
  document.cookie =
    name +
    "=" +
    value +
    ";expires=" +
    exdate.toUTCString() +
    ";path=" +
    (path || "/") +
    (domain ? ";domain=" + domain : "") +
    (secure ? ";secure" : "");
};


(() => {
  const $cookiesBanner = document.querySelector(".cookies-eu-banner");
  const $cookiesBannerButton = $cookiesBanner.querySelector("button");

  $cookiesBannerButton.addEventListener("click", () => {
    $cookiesBanner.remove();
  });
})();

const $cookiesBanner = document.querySelector(".cookies-eu-banner");
const $cookiesBannerButton = $cookiesBanner.querySelector("button");
const cookieName = "cookiesBanner";
const hasCookie = getCookie(cookieName);

if (!hasCookie) {
  $cookiesBanner.classList.remove("hidden");
}

$cookiesBannerButton.addEventListener("click", () => {
  setCookie(cookieName, "closed");
  $cookiesBanner.remove();
});


document.addEventListener('scroll', function() {
  document.querySelectorAll('.fade-in').forEach(function(el){
      const rect = el.getBoundingClientRect();
      if(rect.top < window.innerHeight - 150) {
          el.classList.add('visible');
      }
  });
  });
  document.addEventListener("DOMContentLoaded", function() {
  setTimeout(function(){
      document.querySelectorAll('.fade-in-on-load').forEach(function(el){
          el.classList.add('visible');
          triggerFadeIn();
      });
  }, 500); 
  });
  