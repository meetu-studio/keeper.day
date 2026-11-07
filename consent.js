(() => {
  'use strict';
  const KEY = 'keeper-optional-services-v1';
  const banner = document.querySelector('[data-consent-banner]');
  const template = document.querySelector('#optional-services');
  let loaded = false;
  let choice = null;
  try {
    const saved = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (saved && Date.now() - saved.at < 180 * 86400000) choice = saved.allow;
  } catch (_) { /* Core shopping works without browser storage. */ }
  function enableOptionalServices() {
    if (loaded || !template) return;
    loaded = true;
    template.content.querySelectorAll('script').forEach(source => {
      const script = document.createElement('script');
      [...source.attributes].forEach(attr => script.setAttribute(attr.name, attr.value));
      script.textContent = source.textContent;
      document.head.append(script);
    });
  }
  function save(allow) {
    choice = allow;
    try { localStorage.setItem(KEY, JSON.stringify({allow, at:Date.now()})); } catch (_) {}
    banner.hidden = true;
    if (allow) enableOptionalServices();
    else if (loaded) {
      // Remove this site's known optional cookies; never touch checkout/session cookies.
      document.cookie.split(';').map(item => item.trim().split('=')[0]).filter(name => /^(_ga|_gid|_gat|_fbp|_fbc|_clck|_clsk|__hstc|__hssc|__hssrc|hubspotutk|messagesUtk)/.test(name)).forEach(name => {
        ['', `; domain=${location.hostname}`, `; domain=.${location.hostname}`].forEach(domain => {
          document.cookie = `${name}=; Max-Age=0; path=/${domain}; SameSite=Lax`;
        });
      });
      location.reload();
    }
  }
  if (banner) banner.hidden = choice !== null;
  if (choice === true) enableOptionalServices();
  document.querySelectorAll('[data-consent-allow]').forEach(button => button.addEventListener('click', () => save(true)));
  document.querySelectorAll('[data-consent-decline]').forEach(button => button.addEventListener('click', () => save(false)));
  document.querySelectorAll('[data-open-consent]').forEach(button => button.addEventListener('click', () => {
    banner.hidden = false;
    banner.scrollIntoView({block:'center', behavior:'smooth'});
    banner.querySelector('button')?.focus({preventScroll:true});
  }));
})();
