/* All recommendations and links are rendered before enhancement. */
(() => {
  'use strict';
  const looks = [...document.querySelectorAll('[data-look]')];
  const panels = [...document.querySelectorAll('[data-look-panel]')];
  if (looks.length && panels.length) {
    const choose = key => {
      panels.forEach(panel => { panel.hidden = panel.dataset.lookPanel !== key; });
      looks.forEach(link => link.setAttribute('aria-current', String(link.dataset.look === key)));
    };
    choose(looks[0].dataset.look);
    looks.forEach((link, index) => {
      link.addEventListener('click', event => { event.preventDefault(); choose(link.dataset.look); });
      link.addEventListener('keydown', event => {
        if (!['ArrowRight','ArrowLeft','Home','End'].includes(event.key)) return;
        event.preventDefault();
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? looks.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + looks.length) % looks.length;
        looks[next].focus(); choose(looks[next].dataset.look);
      });
    });
  }
  const finder = document.querySelector('[data-finder]');
  if (finder) {
    const query = new URL(location.href).searchParams;
    const groups = [...finder.querySelectorAll('[data-finder-group]')];
    const kind = ['single','paired'].includes(query.get('kind')) ? query.get('kind') : 'single';
    const theme = ['nature','minimal','playful','retro'].includes(query.get('theme')) ? query.get('theme') : 'nature';
    finder.querySelector(`[name=kind][value=${kind}]`).checked = true;
    finder.querySelector(`[name=theme][value=${theme}]`).checked = true;
    const update = (write = true) => {
      const kind = finder.querySelector('[name=kind]:checked').value;
      const theme = finder.querySelector('[name=theme]:checked').value;
      groups.forEach(group => { group.hidden = group.dataset.finderGroup !== `${kind}:${theme}`; });
      if (write) {
        const next = new URL(location.href); next.searchParams.set('kind',kind); next.searchParams.set('theme',theme);
        history.replaceState(null,'',next); document.dispatchEvent(new Event('keeper:selectionchange'));
      }
    };
    finder.querySelector('.ed-finder-controls').hidden = false;
    finder.addEventListener('change', () => update()); update(false);
  }
  document.querySelectorAll('[data-demo-form]').forEach(form => form.addEventListener('submit', event => event.preventDefault()));
  const inspiration = document.querySelector('[data-inspiration-gallery]');
  if (inspiration) {
    const cards = [...inspiration.querySelectorAll('[data-inspiration-category]')];
    const filters = [...inspiration.querySelectorAll('[data-inspiration-filter]')];
    const count = inspiration.querySelector('[data-inspiration-count]');
    const choose = (category, write = true) => {
      cards.forEach(card => { card.hidden = category !== 'all' && card.dataset.inspirationCategory !== category; });
      filters.forEach(link => link.setAttribute('aria-current', String(link.dataset.inspirationFilter === category)));
      count.textContent = `${cards.filter(card => !card.hidden).length} / ${cards.length}`;
      if (write) {
        const url = new URL(location.href);
        category === 'all' ? url.searchParams.delete('idea') : url.searchParams.set('idea', category);
        url.hash = 'photo-ideas';
        history.replaceState(null, '', url);
        document.dispatchEvent(new Event('keeper:selectionchange'));
      }
    };
    filters.forEach(link => link.addEventListener('click', event => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault(); choose(link.dataset.inspirationFilter);
    }));
    const linked = cards.find(card => '#'+card.id === location.hash || [...card.querySelectorAll('.ed-idea-anchor')].some(anchor => '#'+anchor.id === location.hash));
    const requested = new URL(location.href).searchParams.get('idea');
    const category = linked?.dataset.inspirationCategory || (filters.some(link => link.dataset.inspirationFilter === requested) ? requested : 'all');
    choose(category, false);
    if (linked) requestAnimationFrame(() => linked.scrollIntoView({block:'start'}));
  }
  const diary = document.querySelector('.ed-diary-dialog');
  if (diary && typeof diary.showModal === 'function') {
    const cards = [...document.querySelectorAll('.ed-diary-card')];
    const filters = [...document.querySelectorAll('[data-diary-filter]')];
    const count = document.querySelector('[data-diary-count]');
    const allowed = ['all','friends','family','pets','street','outdoors','details'];
    let active = null;
    let opener = null;
    const visible = () => cards.filter(card => !card.hidden);
    const filter = (topic, write = true) => {
      cards.forEach(card => { card.hidden = topic !== 'all' && card.dataset.diaryCategory !== topic; });
      filters.forEach(link => link.setAttribute('aria-current', String(link.dataset.diaryFilter === topic)));
      if (count) count.textContent = `${visible().length} / ${cards.length}`;
      if (write) {
        const url = new URL(location.href);
        topic === 'all' ? url.searchParams.delete('topic') : url.searchParams.set('topic', topic);
        url.hash = 'photo-diary';
        history.replaceState(null, '', url);
        document.dispatchEvent(new Event('keeper:selectionchange'));
      }
    };
    const show = card => {
      active = card;
      const source = card.querySelector('img');
      const image = diary.querySelector('[data-diary-large]');
      image.src = card.querySelector('[data-diary-photo]').href;
      image.alt = source.alt;
      image.width = source.width;
      image.height = source.height;
      diary.querySelector('#diary-title').textContent = card.querySelector('h3').textContent;
      diary.querySelector('[data-diary-description]').textContent = card.querySelector('.ed-diary-caption').textContent;
      diary.querySelector('[data-diary-position]').textContent = `${visible().indexOf(card) + 1} / ${visible().length}`;
      const url = new URL(diary.querySelector('[data-diary-gallery]').href);
      url.searchParams.set('topic', card.dataset.diaryCategory);
      url.hash = card.id;
      diary.querySelector('[data-share-url]').dataset.shareUrl = url.href;
      diary.querySelector('[data-copy-url]').dataset.copyUrl = url.href;
      diary.querySelector('[data-share-status]').textContent = '';
    };
    const move = direction => {
      const list = visible();
      show(list[(list.indexOf(active) + direction + list.length) % list.length]);
    };
    cards.forEach(card => card.querySelector('[data-diary-photo]').addEventListener('click', event => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault(); opener = event.currentTarget; show(card); diary.showModal();
    }));
    filters.forEach(link => link.addEventListener('click', event => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault(); filter(link.dataset.diaryFilter);
    }));
    diary.querySelector('[data-diary-close]').addEventListener('click', () => diary.close());
    diary.querySelector('[data-diary-prev]').addEventListener('click', () => move(-1));
    diary.querySelector('[data-diary-next]').addEventListener('click', () => move(1));
    diary.addEventListener('keydown', event => {
      if (event.target.matches('input,textarea')) return;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') { event.preventDefault(); move(event.key === 'ArrowLeft' ? -1 : 1); }
    });
    diary.addEventListener('click', event => { if (event.target === diary) { const rect = diary.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) diary.close(); } });
    diary.addEventListener('close', () => opener?.focus({preventScroll:true}));
    if (filters.length) {
      const topic = new URL(location.href).searchParams.get('topic');
      filter(allowed.includes(topic) ? topic : 'all', false);
      const linked = cards.find(card => '#'+card.id === location.hash);
      if (linked) {
        if (linked.hidden) filter(linked.dataset.diaryCategory, false);
        requestAnimationFrame(() => linked.scrollIntoView({block:'center'}));
      }
    }
  }
})();
