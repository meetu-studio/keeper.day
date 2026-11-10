/* Language URLs are static pages; browser detection only chooses an entry. */
(() => {
  'use strict';
  const context = JSON.parse(document.querySelector('#keeper-i18n').textContent);
  const languages = Object.keys(context.languages);
  const key = 'keeper-language-v1';
  let locale = context.locale;
  let messages = context.messages;
  const normalized = value => languages.includes(value?.toLowerCase().split('-')[0]) ? value.toLowerCase().split('-')[0] : null;
  const explicitPath = location.pathname.match(/^\/(zh|ja|ko)(?:\/|$)/)?.[1];
  const pagePath = location.pathname.replace(/^\/(zh|ja|ko)(?=\/|$)/,'').replace(/^\//,'') || 'index.html';
  const unknown = context.page === '404.html' && pagePath !== '404.html';
  const requested = new URL(location.href).searchParams.get('lang');
  let saved;
  try { saved = localStorage.getItem(key); } catch (_) {}
  const browser = (navigator.languages?.length ? navigator.languages : [navigator.language]).map(normalized).find(Boolean) || 'en';
  const preferred = (unknown ? normalized(requested) : null) || explicitPath || normalized(requested) || normalized(saved) || browser;

  function url(input, language = locale, explicitEnglish = true) {
    const result = new URL(input, location.origin);
    if (result.origin !== location.origin) return result.href;
    const path = result.pathname.replace(/^\/(zh|ja|ko)(?=\/|$)/,'') || '/';
    result.pathname = (language === 'en' ? '' : '/'+language)+path;
    result.searchParams.delete('lang');
    if (language === 'en' && explicitEnglish) result.searchParams.set('lang','en');
    return result.href;
  }
  const t = (name, values = {}) => messages[name].replace(/\{(\w+)\}/g, (_, token) => String(values[token]));
  const persist = language => { try { localStorage.setItem(key,language); } catch (_) {} };

  if (!unknown && !explicitPath && preferred !== locale) {
    location.replace(url(location.href,preferred));
  }
  function localizeNotFound(language = preferred) {
    if (!unknown) return;
    const packet = document.querySelector('#keeper-not-found');
    if (!packet) return;
    const pages = JSON.parse(packet.textContent);
    const page = pages[language];
    locale = language;messages = page.messages;
    document.documentElement.lang = language === 'zh' ? 'zh-Hans' : language;
    document.documentElement.dataset.locale = language;
    document.title = page.title;
    document.body.innerHTML = page.body;
  }
  function refreshLinks() {
    document.querySelectorAll('[data-language]').forEach(link => {
      link.href = url(location.href,link.dataset.language);
      if (link.dataset.language === locale) link.setAttribute('aria-current','true');
      else link.removeAttribute('aria-current');
    });
  }
  window.KeeperI18n = {t,url,localizeNotFound,get locale(){return locale;}};
  document.addEventListener('DOMContentLoaded',refreshLinks);
  document.addEventListener('keeper:selectionchange',refreshLinks);
  window.addEventListener('hashchange',refreshLinks);
  window.addEventListener('popstate',refreshLinks);
  document.addEventListener('click',event => {
    const link = event.target.closest('[data-language]');
    if (!link || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const language = link.dataset.language;
    persist(language);
    link.href = url(location.href,language);
    if (unknown) {
      // Keep the original failing path and its 404 response; the query records a manual choice.
      const choice = new URL(location.href);choice.searchParams.set('lang',language);
      event.preventDefault();location.assign(choice.href);
    }
  });
})();
