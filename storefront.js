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
})();
