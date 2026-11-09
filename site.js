const mobileMenu = document.querySelector('.mobile-menu');
const keeperText = window.KeeperI18n.t;
mobileMenu?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => { mobileMenu.open = false; });
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && mobileMenu?.open) {
    mobileMenu.open = false;
    mobileMenu.querySelector('summary').focus();
  }
});
const preview = document.querySelector('#camera-preview');
const samplePhotos = {
  love: { path: '/assets/screen-love.webp', label: keeperText('preview_love') },
  pet: { path: '/assets/screen-pet.webp', label: keeperText('preview_pet') },
  blooms: { path: '/assets/screen-blooms.webp', label: keeperText('preview_blooms') }
};
document.querySelectorAll('[data-photo]').forEach((button) => {
  button.addEventListener('click', () => {
    const photo = samplePhotos[button.dataset.photo];
    preview.querySelectorAll('.screen-art, .mini-art').forEach((image) => { image.src = photo.path; });
    preview.setAttribute('aria-label', keeperText('preview_alt',{subject:photo.label}));
    document.querySelectorAll('[data-photo]').forEach((choice) => { choice.setAttribute('aria-pressed', String(choice === button)); });
  });
});
const chatButton = document.querySelector('#open-chat');
const chatStatus = document.querySelector('#chat-status');
function enableChat() {
  if (chatButton) chatButton.hidden = false;
}
if (window.HubSpotConversations) {
  enableChat();
} else {
  window.hsConversationsOnReady = [...(window.hsConversationsOnReady || []), enableChat];
}
chatButton?.addEventListener('click', () => {
  const widget = window.HubSpotConversations?.widget;
  if (widget?.status().loaded) {
    widget.open();
    chatStatus.textContent = '';
  } else {
    chatStatus.textContent = keeperText('chat_connecting');
  }
});
document.querySelectorAll('[data-preview]').forEach((previewPanel) => {
  previewPanel.querySelectorAll('[data-preview-key]').forEach((button) => {
    button.addEventListener('click', () => {
      const image = previewPanel.querySelector('figure img');
      image.src = button.dataset.previewSrc;
      image.alt = button.dataset.previewAlt;
      previewPanel.querySelector('[data-preview-title]:not(button)').textContent = button.dataset.previewTitle;
      previewPanel.querySelector('[data-preview-copy]:not(button)').textContent = button.dataset.previewCopy;
      previewPanel.querySelectorAll('[data-preview-key]').forEach((choice) => {
        choice.setAttribute('aria-pressed', String(choice === button));
      });
    });
  });
});
const filterGrid = document.querySelector('[data-filter-grid]');
if (filterGrid) {
  const cards = [...filterGrid.querySelectorAll('[data-category]')];
  document.querySelectorAll('[data-filter]').forEach((button) => {
    button.addEventListener('click', () => {
      cards.forEach((card) => { card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter; });
      document.querySelectorAll('[data-filter]').forEach((choice) => { choice.setAttribute('aria-pressed', String(choice === button)); });
      document.querySelector('.filter-status').textContent = keeperText('concept_count',{count:cards.filter((card) => !card.hidden).length});
    });
  });
}
// A checkout click is not a completed purchase; Stripe confirms payment.
document.querySelectorAll('[data-purchase]').forEach((link) => {
  link.addEventListener('click', () => {
    if (new URL(link.href, location.href).hostname !== 'buy.stripe.com') return;
    window.gtag?.('event', 'checkout_click', { placement: link.dataset.purchase, style: link.dataset.variant || 'classic', currency: 'USD', value: Number(document.body.dataset.orderTotal) });
    window.clarity?.('event', 'checkout_click');
  });
});
