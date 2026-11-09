/* Progressive enhancement only: purchase links and all content work without JS. */
(() => {
  'use strict';
  const {t,url} = window.KeeperI18n;
  const mobileBuy = document.querySelector('.sf-mobile-buy');
  if (mobileBuy && 'IntersectionObserver' in window) {
    const visibleActions = new Set();
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) visibleActions.add(entry.target);
        else visibleActions.delete(entry.target);
      });
      mobileBuy.hidden = visibleActions.size > 0;
    });
    document.querySelectorAll('.shutter-order [data-current-checkout], .sf-actions [data-current-checkout], .sf-final [data-current-checkout]').forEach(action => observer.observe(action));
  }
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
        status.textContent = t('gallery_status',{index:index+1,count:panels.length,label:panels[index].querySelector('figcaption')?.textContent || ''});
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
    const collections = {nature:['st-11','st-46','st-50','p-02','p-06','p-09'],minimal:['st-31','st-32','st-36','p-25','p-26','p-30'],playful:['st-01','st-13','st-27','p-13','p-21','p-22'],retro:['st-08','st-12','st-45','p-14','p-27','p-28']};
    let collection = collections[new URL(location.href).searchParams.get('collection')] || null;
    const filter = () => {
      const words = search.value.normalize('NFKC').toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
      let count = 0;
      cards.forEach((card) => {
        const match = (!collection || collection.includes(card.dataset.search.split(' ')[0])) && (kind === 'all' || card.dataset.kind === kind) && words.every(word => card.dataset.search.normalize('NFKC').toLocaleLowerCase().includes(word));
        card.hidden = !match;
        count += Number(match);
      });
      catalog.querySelector('[data-design-count]').textContent = t(count === 1 ? 'catalog_count_one' : 'catalog_count',{count});
      catalog.querySelector('[data-design-empty]').hidden = count !== 0;
    };
    search.addEventListener('input', () => { collection = null; filter(); });
    filters.forEach(button => button.addEventListener('click', () => {
      kind = button.dataset.designFilter; collection = null;
      filters.forEach(choice => choice.setAttribute('aria-pressed', String(choice === button)));
      filter();
    }));
    catalog.querySelector('.kr-catalog-tools').hidden = false; filter();
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
      const name = variant ? `${variant.name} · ${id.toUpperCase()}` : pendingPair ? t('choose_side_name',{name:groupVariants[0].name.split(' · ')[0]}) : t('classic_name');
      selector.querySelector('[data-selected-name]').textContent = name;
      const exterior = variant?.side ? t('side_exterior',{side:variant.side.toUpperCase(),position:t(variant.side==='a'?'left':'right')}) : variant ? t('exterior',{name:variant.name}) : t('classic_exterior');
      selector.querySelector('[data-selection-note]').textContent = pendingPair ? t('pair_note') : t('selected_note',{exterior});
      selector.querySelector('[data-selection-status]').textContent = !valid && !pendingPair ? t('invalid_design') : pendingPair ? t('select_side') : t('selected_total');
      selector.querySelector('[data-side-choices]').hidden = !pendingPair;
      productImage.src = display?.image || originalImage.src;
      productImage.width = display?.width || originalImage.width;
      productImage.height = display?.height || originalImage.height;
      productImage.alt = display ? t('product_alt',{name,details:variant?.side ? t('selected_side_alt',{side:variant.side.toUpperCase()}) : pendingPair ? t('pair_alt') : t('single_alt')}) : t('classic_alt');
      productCaption.textContent = variant?.side ? `${name} · ${t("selected_note", {exterior})}` : pendingPair ? `${name} · ${t("pair_note")}` : name;
      document.querySelector('[data-sf-photo="0"] img').src = productImage.src;
      document.querySelector('[data-sf-photo="0"]').setAttribute('aria-label',t('show_selected',{name}));
      document.querySelector('[data-sf-photo="0"]').click();
      const checkout = new URL(data.checkout);
      if (variant) checkout.searchParams.set('client_reference_id', 'keeper-'+id);
      document.querySelectorAll('[data-current-checkout]').forEach(link => {
        link.href = pendingPair || !valid ? '#choose-style' : checkout.href;
        link.dataset.variant = variant ? id : 'classic';
        link.setAttribute('aria-disabled', String(!!pendingPair || !valid));
        link.setAttribute('aria-label', pendingPair || !valid ? t('checkout_pick') : t('buy_aria',{name}));
        const arrow = link.querySelector('span');
        const text = pendingPair || !valid ? t('choose_look') : t('buy_label',{name:variant ? id.toUpperCase() : 'Keeper'});
        link.replaceChildren(document.createTextNode(text));
        if (arrow) link.append(arrow);
      });
      const shared = new URL(url('/camera.html'+(variant || pendingPair ? '?style='+encodeURIComponent(id) : '')));
      shared.host = 'keeper.day';shared.protocol = 'https:';shared.port = '';
      currentShareUrl = shared.href;
      if (updateUrl) {
        const url = new URL(location.href);
        if (variant || pendingPair) url.searchParams.set('style', id); else url.searchParams.delete('style');
        history.replaceState(null, '', url);
      }
      document.dispatchEvent(new Event('keeper:selectionchange'));
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
    status.textContent = t('copying');
    try {
      await Promise.race([navigator.clipboard.writeText(url), new Promise((_,reject) => setTimeout(() => reject(new Error('Clipboard unavailable')),1200))]);
      status.textContent = t('copied');
    } catch {
      let field = container.querySelector('input');
      if (!field) {
        field = document.createElement('input');
        field.readOnly = true;
        field.setAttribute('aria-label', t('copy_label'));
        container.append(field);
      }
      field.value = url;field.focus();field.select();
      if (document.hasFocus() && document.execCommand('copy')) {
        field.remove();previousFocus?.focus({preventScroll:true});status.textContent = t('copied');
      } else status.textContent = t('copy_manual');
    }
  };
  document.querySelectorAll('.kr-share-actions').forEach(container => {
    container.hidden = false;
    container.querySelectorAll('button').forEach(button => button.addEventListener('click', async () => {
      const url = button.dataset.shareUrl || button.dataset.copyUrl || currentShareUrl;
      if ((button.hasAttribute('data-share-current') || button.hasAttribute('data-share-url')) && navigator.share) {
        try { await navigator.share({title:t('share_title'),text:t('share_text'),url}); }
        catch (error) { if (error.name !== 'AbortError') await copyLink(url,container); }
      } else await copyLink(url,container);
    }));
  });
})();
