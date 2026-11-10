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

  const selector = document.querySelector('[data-style-selector]');
  let currentShareUrl = location.href;
  if (selector) {
    const data = JSON.parse(document.querySelector('#keeper-design-data').textContent);
    const options = new Map(data.variants.map(v => [v.id, v]));
    const overlay = document.querySelector('[data-pair-overlay]');
    let pairGroup = '';
    const productImage = document.querySelector('#sf-photo-0 img');
    const productCaption = document.querySelector('#sf-photo-0 figcaption');
    const originalImage = {src: productImage.getAttribute('src'), width:productImage.width, height:productImage.height};
    let pendingPair = '';
    const update = (id, updateUrl = true) => {
      const variant = options.get(id);
      const groupVariants = data.variants.filter(v => v.group === id && v.side);
      pendingPair = groupVariants.length ? id : '';
      const valid = id === 'classic' || !!variant;
      pairGroup = variant?.side ? variant.group : pendingPair;
      selector.querySelectorAll('[data-pick-style]').forEach(link => link.setAttribute('aria-current',String(link.dataset.pickStyle === id)));
      overlay.hidden = !pairGroup;
      document.querySelectorAll('[data-pair-side]').forEach(button => button.setAttribute('aria-pressed',String(button.dataset.pairSide === variant?.side)));
      const display = variant || groupVariants[0];
      const name = variant ? `${variant.name} · ${id.toUpperCase()}` : pendingPair ? t('choose_side_name',{name:groupVariants[0].name.split(' · ')[0]}) : valid ? t('classic_name') : t('choose_look');
      selector.querySelector('[data-selected-name]').textContent = name;
      const exterior = variant?.side ? t('side_exterior',{side:variant.side.toUpperCase(),position:t(variant.side==='a'?'left':'right')}) : variant ? t('exterior',{name:variant.name}) : t('classic_exterior');
      selector.querySelector('[data-selection-note]').textContent = !valid && !pendingPair ? t('invalid_design') : pendingPair ? t('pair_note') : t('selected_note',{exterior});
      selector.querySelector('[data-selection-status]').textContent = !valid && !pendingPair ? '' : pendingPair ? t('select_side') : t('selected_total');
      selector.querySelector('[data-side-choices]').hidden = !pairGroup;
      const purchaseContext = !valid && !pendingPair ? t('choose_look') : pairGroup ? (variant ? t('pair_selection',{id:id.toUpperCase(),side:variant.side.toUpperCase(),position:t(variant.side==='a'?'left':'right')}) : t('pair_note')) : t('one_selection',{name:variant ? id.toUpperCase() : t('classic_name')});
      document.querySelector('[data-image-selection]').textContent = purchaseContext;
      document.querySelector('[data-sticky-selection]').textContent = purchaseContext;
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
      const shared = new URL(url('/camera.html'+(variant || pendingPair || !valid ? '?style='+encodeURIComponent(id) : '')));
      shared.host = 'keeper.day';shared.protocol = 'https:';shared.port = '';
      currentShareUrl = shared.href;
      if (updateUrl) {
        const url = new URL(location.href);
        if (variant || pendingPair || !valid) url.searchParams.set('style', id); else url.searchParams.delete('style');
        history.replaceState(null, '', url);
      }
      document.dispatchEvent(new Event('keeper:selectionchange'));
    };
    document.querySelectorAll('[data-pair-side]').forEach(button => button.addEventListener('click', () => update(pairGroup+'-'+button.dataset.pairSide)));
    selector.querySelectorAll('[data-pick-style], .kr-choose, .kr-design-image').forEach(link => link.addEventListener('click', event => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      const id = link.dataset.pickStyle || new URL(link.href).searchParams.get('style');
      update(id);
      selector.querySelector('[data-selected-name]').setAttribute('tabindex','-1');
      selector.querySelector('[data-selected-name]').focus({preventScroll:true});
    }));
    document.querySelectorAll('[data-current-checkout]').forEach(link => link.addEventListener('click', event => {
      if (link.getAttribute('aria-disabled') === 'true') {
        event.preventDefault();
        selector.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
        (pendingPair ? selector.querySelector('[data-pair-side]') : selector.querySelector('[data-pick-style]')).focus();
      }
    }));
    addEventListener('popstate', () => update(new URL(location.href).searchParams.get('style') || 'classic', false));
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
