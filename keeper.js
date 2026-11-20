// keeper.day, the 2026-11-20 design of the home page and the product page: the look picker both pages share,
// the language menu, the checkout click event and the chat button. Each page carries its looks (names, notes,
// pictures in its own language) and its checkout link in <script type="application/json" id="kd-looks">.
//
// The picker: a swatch, a nav card or a photograph on the wall picks a look; the picture, its name, its note
// and every Buy link follow it. The checkout keeps the live site's convention: no reference for Porcelain
// White, client_reference_id=keeper-<id> for every printed look. ?style=<id> opens the page with a look picked,
// the parameter every other page of the site already links with (/camera.html?style=st-12#choose-style).
// The language links belong to language.js: it rewrites them from the current address, so a picked look is
// kept in the address and carried to the other language.

const data = JSON.parse(document.getElementById('kd-looks')?.textContent || 'null');
if (data) picker(data);
languages();
checkoutEvents();
chat();

function picker({ checkout, initial, looks }) {
  const img = document.querySelector('[data-look-img]');
  const nameEl = document.querySelector('[data-look-name]');
  const noteEl = document.querySelector('[data-look-note]');
  const buys = [...document.querySelectorAll('[data-buy]')];
  const swatches = [...document.querySelectorAll('.swatch[data-look]')];
  if (!img || !swatches.length) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let current = initial;

  const checkoutFor = (id) => {
    const url = new URL(checkout);
    if (id !== 'classic') url.searchParams.set('client_reference_id', 'keeper-' + id);
    return url.href;
  };

  function select(id, { updateUrl = true } = {}) {
    const look = looks[id];
    if (!look || id === current) return;
    current = id;
    swatches.forEach((s) => { const on = s.dataset.look === id; s.setAttribute('aria-checked', String(on)); s.tabIndex = on ? 0 : -1; });
    if (nameEl) nameEl.textContent = look.name;
    if (noteEl) noteEl.textContent = look.note;
    buys.forEach((b) => { b.href = checkoutFor(id); b.dataset.variant = id; });
    const swap = () => { img.src = look.src; img.width = look.w; img.height = look.h; img.alt = look.alt; if (look.bg) img.parentElement.style.setProperty('--look-bg', look.bg); };
    if (reduced) swap();
    else {
      img.classList.add('is-swapping');
      const next = new Image();
      // the picture swaps once the new one has loaded, or after 600 ms whatever happens: decode() can stay
      // pending in a tab that is not painting, and the picture must never stay faded out. A forced layout
      // read starts the fade back from 0 without waiting for a frame; a later pick wins over an earlier one
      const loaded = new Promise((res) => { next.onload = next.onerror = res; });
      next.src = look.src;
      const done = () => { if (current !== id) return; swap(); void img.offsetWidth; img.classList.remove('is-swapping'); };
      Promise.race([loaded, new Promise((res) => setTimeout(res, 600))]).then(() => setTimeout(done, 80));
    }
    if (updateUrl) {
      const u = new URL(location.href);
      u.searchParams.delete('look');
      u.searchParams.set('style', id);
      history.replaceState(null, '', u);
      document.dispatchEvent(new Event('keeper:selectionchange'));
    }
  }

  swatches.forEach((s, i) => {
    s.addEventListener('click', () => select(s.dataset.look));
    s.addEventListener('keydown', (e) => {
      const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
      if (!step) return;
      e.preventDefault();
      const next = swatches[(i + step + swatches.length) % swatches.length];
      next.focus(); select(next.dataset.look);
    });
  });
  // the wall's photographs and the nav's look cards pick their look, then the link scrolls to the picker
  document.querySelectorAll('a[data-look]').forEach((a) => a.addEventListener('click', () => select(a.dataset.look)));
  // a link with a look (?style=st-12; ?look= from the first draft) opens with that look picked; the paired
  // design's group id (p-01) opens on its first side
  const params = new URL(location.href).searchParams;
  let fromUrl = (params.get('style') || params.get('look') || '').toLowerCase();
  if (!looks[fromUrl] && looks[fromUrl + '-a']) fromUrl += '-a';
  if (looks[fromUrl]) select(fromUrl, { updateUrl: false });
  // warm the cache once the reader comes near the picker, so a swap shows at once
  const warm = () => Object.values(looks).forEach((l) => { const i = new Image(); i.src = l.src; });
  (img.closest('section') || document.body).addEventListener('pointerenter', warm, { once: true });
}

function languages() {
  const menus = [...document.querySelectorAll('details.lang')];
  document.addEventListener('click', (e) => menus.forEach((m) => { if (m.open && !m.contains(e.target)) m.open = false; }));
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    menus.forEach((m) => { if (m.open) { m.open = false; m.querySelector('summary')?.focus(); } });
  });
}

// the live site's checkout event: a click on a Buy link to Stripe is not a purchase (Stripe confirms payment);
// gtag and clarity exist only once the reader has allowed the optional services
function checkoutEvents() {
  document.querySelectorAll('a[data-buy]').forEach((link) => link.addEventListener('click', () => {
    if (new URL(link.href, location.href).hostname !== 'buy.stripe.com') return;
    window.gtag?.('event', 'checkout_click', { placement: link.dataset.purchase, style: link.dataset.variant || 'classic', currency: 'USD', value: Number(document.body.dataset.orderTotal) });
    window.clarity?.('event', 'checkout_click');
  }));
}

// the footer's chat button appears once the chat (an optional service) has loaded, and opens it
function chat() {
  const button = document.querySelector('[data-open-chat]');
  if (!button) return;
  const ready = () => {
    const show = () => { button.hidden = false; };
    if (window.HubSpotConversations.widget.status().loaded) show();
    window.HubSpotConversations.on('widgetLoaded', show);
  };
  if (window.HubSpotConversations) ready();
  else window.hsConversationsOnReady = [...(window.hsConversationsOnReady || []), ready];
  button.addEventListener('click', () => window.HubSpotConversations?.widget?.open());
}
