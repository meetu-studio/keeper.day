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
})();
