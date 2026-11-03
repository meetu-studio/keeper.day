const menuButton=document.getElementById('menu-toggle');
const siteNav=document.getElementById('site-nav');
if(menuButton&&siteNav){
  menuButton.addEventListener('click',()=>{
    const isOpen=siteNav.classList.toggle('open');
    menuButton.setAttribute('aria-expanded',String(isOpen));
  });
  siteNav.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{
    siteNav.classList.remove('open');
    menuButton.setAttribute('aria-expanded','false');
  }));
}
