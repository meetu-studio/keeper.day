/* Progressive enhancement only: purchase links and all content work without JS. */
(() => {
  'use strict';
  document.querySelectorAll('[data-sf-gallery]').forEach((gallery) => {
    const panels = [...gallery.querySelectorAll('[data-sf-panel]')];
    const controls = gallery.querySelector('.sf-thumbnails');
    const buttons = [...gallery.querySelectorAll('[data-sf-photo]')];
    const status = gallery.querySelector('[data-sf-gallery-status]');
    if (!panels.length || panels.length !== buttons.length || !controls) return;
    const select = (index, announce = true) => {
      panels.forEach((panel, i) => { panel.hidden = i !== index; });
      buttons.forEach((button, i) => {
        button.setAttribute('aria-pressed', String(i === index));
      });
      if (announce && status) {
        status.textContent = `Image ${index + 1} of ${panels.length}: ${panels[index].querySelector('figcaption')?.textContent || ''}`;
      }
    };
    buttons.forEach((button, index) => {
      button.addEventListener('click', () => select(index));
      button.addEventListener('keydown', (event) => {
        let target;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') target = (index + 1) % buttons.length;
        else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') target = (index - 1 + buttons.length) % buttons.length;
        else if (event.key === 'Home') target = 0;
        else if (event.key === 'End') target = buttons.length - 1;
        else return;
        event.preventDefault();
        buttons[target].focus();
        select(target);
      });
    });
    select(0, false);
    controls.hidden = false;
  });

  document.querySelectorAll('[data-design-catalog]').forEach((catalog) => {
    const search = catalog.querySelector('[data-design-search]');
    const cards = [...catalog.querySelectorAll('[data-design-card]')];
    const filters = [...catalog.querySelectorAll('[data-design-filter]')];
    let kind = 'all';
    const filter = () => {
      const words = search.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
      let count = 0;
      cards.forEach((card) => {
        const match = (kind === 'all' || card.dataset.kind === kind) && words.every(word => card.dataset.search.toLocaleLowerCase().includes(word));
        card.hidden = !match;
        count += Number(match);
      });
      catalog.querySelector('[data-design-count]').textContent = `${count} design${count === 1 ? '' : 's'} · $199 per camera + $30 worldwide shipping`;
      catalog.querySelector('[data-design-empty]').hidden = count !== 0;
    };
    search.addEventListener('input', filter);
    filters.forEach(button => button.addEventListener('click', () => {
      kind = button.dataset.designFilter;
      filters.forEach(choice => choice.setAttribute('aria-pressed', String(choice === button)));
      filter();
    }));
    catalog.querySelector('.kr-catalog-tools').hidden = false;
  });

  const selector = document.querySelector('[data-style-selector]');
  let currentShareUrl = location.href;
  if (selector) {
    const data = JSON.parse(document.querySelector('#keeper-design-data').textContent);
    const options = new Map(data.variants.map(v => [v.id, v]));
    const select = selector.querySelector('[data-style-select]');
    const productImage = document.querySelector('#sf-photo-0 img');
    const productCaption = document.querySelector('#sf-photo-0 figcaption');
    const originalImage = {src: productImage.getAttribute('src'), width:productImage.width, height:productImage.height};
    let pendingPair = '';
    const update = (id, updateUrl = true) => {
      const variant = options.get(id);
      const groupVariants = data.variants.filter(v => v.group === id && v.side);
      pendingPair = groupVariants.length ? id : '';
      const valid = id === 'classic' || !!variant;
      select.value = variant ? id : valid ? 'classic' : '';
      const display = variant || groupVariants[0];
      const name = variant ? `${variant.name} · ${id.toUpperCase()}` : pendingPair ? `${groupVariants[0].name.split(' · ')[0]} · choose a side` : 'Classic cream';
      selector.querySelector('[data-selected-name]').textContent = name;
      selector.querySelector('[data-selection-note]').textContent = pendingPair ? 'Choose A (left) or B (right). Each purchase includes one camera, not both.' : `One camera · ${variant?.side ? 'Side '+variant.side.toUpperCase()+(variant.side === 'a' ? ' (left)' : ' (right)')+' exterior' : variant ? variant.name+' exterior' : 'classic cream exterior'} · gift box, lanyard & manual.`;
      selector.querySelector('[data-selection-status]').textContent = !valid && !pendingPair ? 'That design number was not found. Classic cream is shown; choose a look before continuing.' : pendingPair ? 'Select a side to continue to checkout.' : 'Your selected exterior is included. $229 USD total with worldwide shipping.';
      selector.querySelector('[data-side-choices]').hidden = !pendingPair;
      productImage.src = display?.image || originalImage.src;
      productImage.width = display?.width || originalImage.width;
      productImage.height = display?.height || originalImage.height;
      productImage.alt = display ? `${name}. ${variant?.side ? 'Selected side '+variant.side.toUpperCase()+'. One camera per purchase.' : pendingPair ? 'A on the left, B on the right.' : 'One camera with this exterior.'}` : 'Classic cream Keeper camera';
      productCaption.textContent = name;
      document.querySelector('[data-sf-photo="0"] img').src = productImage.src;
      document.querySelector('[data-sf-photo="0"]').setAttribute('aria-label','Show selected look: '+name);
      document.querySelector('[data-sf-photo="0"]').click();
      const checkout = new URL(data.checkout);
      if (variant) checkout.searchParams.set('client_reference_id', 'keeper-'+id);
      document.querySelectorAll('[data-current-checkout]').forEach(link => {
        link.href = pendingPair || !valid ? '#choose-style' : checkout.href;
        link.dataset.variant = variant ? id : 'classic';
        link.setAttribute('aria-disabled', String(!!pendingPair || !valid));
        link.setAttribute('aria-label', pendingPair || !valid ? 'Choose your exterior before checkout' : `Buy one ${name} Keeper for $199 plus $30 shipping, $229 USD total`);
        const arrow = link.querySelector('span');
        const text = pendingPair || !valid ? 'Choose your look' : 'Buy '+(variant ? id.toUpperCase() : 'Keeper');
        link.replaceChildren(document.createTextNode(text));
        if (arrow) link.append(arrow);
      });
      currentShareUrl = 'https://keeper.day/camera.html'+(variant || pendingPair ? '?style='+encodeURIComponent(id) : '');
      if (updateUrl) {
        const url = new URL(location.href);
        if (variant || pendingPair) url.searchParams.set('style', id); else url.searchParams.delete('style');
        history.replaceState(null, '', url);
      }
    };
    selector.querySelector('.kr-select-control').hidden = false;
    select.addEventListener('change', () => update(select.value));
    selector.querySelectorAll('[data-pair-side]').forEach(button => button.addEventListener('click', () => update(pendingPair+'-'+button.dataset.pairSide)));
    document.querySelectorAll('[data-current-checkout]').forEach(link => link.addEventListener('click', event => {
      if (link.getAttribute('aria-disabled') === 'true') {
        event.preventDefault();
        selector.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
        (pendingPair ? selector.querySelector('[data-pair-side]') : select).focus();
      }
    }));
    const requested = new URL(location.href).searchParams.get('style');
    update(requested?.toLowerCase() || 'classic', false);
  }

  const copyLink = async (url, container) => {
    const status = container.querySelector('[data-share-status]');
    const previousFocus = document.activeElement;
    status.textContent = 'Copying link…';
    try {
      await Promise.race([navigator.clipboard.writeText(url), new Promise((_,reject) => setTimeout(() => reject(new Error('Clipboard unavailable')),1200))]);
      status.textContent = 'Link copied.';
    } catch {
      let field = container.querySelector('input');
      if (!field) {
        field = document.createElement('input');
        field.readOnly = true;
        field.setAttribute('aria-label', 'Link to copy');
        container.append(field);
      }
      field.value = url;field.focus();field.select();
      if (document.hasFocus() && document.execCommand('copy')) {
        field.remove();previousFocus?.focus({preventScroll:true});status.textContent = 'Link copied.';
      } else status.textContent = 'Select and copy this link.';
    }
  };
  document.querySelectorAll('.kr-share-actions').forEach(container => {
    container.hidden = false;
    container.querySelectorAll('button').forEach(button => button.addEventListener('click', async () => {
      const url = button.dataset.shareUrl || button.dataset.copyUrl || currentShareUrl;
      if ((button.hasAttribute('data-share-current') || button.hasAttribute('data-share-url')) && navigator.share) {
        try { await navigator.share({title:'Find your Keeper',text:'A little camera. A look of your own.',url}); }
        catch (error) { if (error.name !== 'AbortError') await copyLink(url,container); }
      } else await copyLink(url,container);
    }));
  });
})();
