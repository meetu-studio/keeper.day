/* Run in the preview/production page's isolated world. Results land in #release-qa.
   Scripts are stripped from sandboxed layout fixtures; interactive checks use the real page. */
(() => {
  document.querySelector('#release-qa')?.remove();
  const output = document.createElement('pre');
  output.id = 'release-qa';
  output.hidden = true;
  document.body.append(output);
  const routes = ['/', '/camera.html', '/gifting.html', '/support.html', '/moments.html', '/terms.html', '/privacy.html', '/together.html', '/styles.html', '/little-apps.html'];
  const widths = [320, 390, 430, 768, 1440];
  (async () => {
    const results = [];
    for (const route of routes) {
      const response = await fetch(route, {cache:'no-store'});
      const source = await response.text();
      const parsed = new DOMParser().parseFromString(source, 'text/html');
      parsed.querySelectorAll('script, noscript').forEach(el => el.remove());
      parsed.querySelectorAll('img').forEach(el => el.loading = 'eager');
      const base = parsed.createElement('base');
      base.href = new URL(route, location.origin).href;
      parsed.head.prepend(base);
      for (const width of widths) {
        const frame = document.createElement('iframe');
        frame.setAttribute('aria-hidden', 'true');
        frame.style.cssText = `position:fixed;left:-20000px;top:0;width:${width}px;height:1100px;border:0`;
        document.body.append(frame);
        const ready = new Promise(resolve => frame.onload = resolve);
        frame.srcdoc = '<!doctype html>' + parsed.documentElement.outerHTML;
        await ready;
        const doc = frame.contentDocument;
        await doc.fonts.ready;
        await Promise.all([...doc.images].map(img => img.decode().catch(() => null)));
        const overflow = [...doc.querySelectorAll('body *')].filter(el => {
          const box = el.getBoundingClientRect();
          const css = frame.contentWindow.getComputedStyle(el);
          return box.width > 0 && box.right > width + 1 && css.position !== 'fixed' && css.visibility !== 'hidden' && !el.closest('.sf-lightbox,[hidden],details:not([open])');
        }).slice(0,12).map(el => ({tag:el.tagName, cls:el.className, right:Math.round(el.getBoundingClientRect().right)}));
        results.push({route, width, status:response.status, title:doc.title,
          scrollWidth:doc.documentElement.scrollWidth,
          overflow,
          brokenImages:[...doc.images].filter(img => !img.complete || !img.naturalWidth).map(img => img.getAttribute('src')),
          h1:doc.querySelectorAll('h1').length,
          purchaseLinks:[...doc.querySelectorAll('[data-purchase]')].map(el => el.getAttribute('href'))});
        frame.remove();
      }
    }
    output.textContent = JSON.stringify({finished:true, results});
  })().catch(error => output.textContent = JSON.stringify({finished:false,error:String(error)}));
  return 'Layout QA started; read #release-qa after completion.';
})();
