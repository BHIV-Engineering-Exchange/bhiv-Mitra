export class Header {
  constructor(onMinimize, onDock, onAvatarChange) {
    this.element = document.createElement('div');
    this.element.className = 'mitra-header';

    this.element.innerHTML = `
      <div class="mitra-title">
        <div class="mitra-status-dot"></div>
        <div class="mitra-header-avatar" style="width: 24px; height: 24px; border-radius: 50%; overflow: hidden; display: none; align-items: center; justify-content: center; margin-right: 8px;"></div>
        MITRA
      </div>
      <div class="mitra-controls">
        <button class="mitra-btn" id="btn-avatar" title="Change Avatar">
          <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/></svg>
        </button>
        <button class="mitra-btn" id="btn-dock" title="Dock">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zm-7-2h5v-5h-2v3h-3v2z"/></svg>
        </button>
        <button class="mitra-btn" id="btn-minimize" title="Minimize">
          <svg viewBox="0 0 24 24"><path d="M19 13H5v-2h14v2z"/></svg>
        </button>
      </div>
    `;

    this.element.querySelector('#btn-minimize').addEventListener('click', () => {
      if (onMinimize) onMinimize();
    });

    this.element.querySelector('#btn-dock').addEventListener('click', () => {
      if (onDock) onDock();
    });

    this.element.querySelector('#btn-avatar').addEventListener('click', () => {
      if (onAvatarChange) onAvatarChange();
    });
  }

  updateAvatar(avatarUrl, renderAvatarElement) {
    const container = this.element.querySelector('.mitra-header-avatar');
    container.innerHTML = '';
    if (avatarUrl) {
      container.style.display = 'inline-flex';
      const el = renderAvatarElement(avatarUrl);
      if (el) {
        el.style.width = '24px';
        el.style.height = '24px';
        container.appendChild(el);
      }
    } else {
      container.style.display = 'none';
    }
  }
}
