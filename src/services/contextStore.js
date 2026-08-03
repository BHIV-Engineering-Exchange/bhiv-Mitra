import { eventBus } from './eventBus.js';

export class ContextStore {
  constructor() {
    this.storageKey = 'mitra_context_store';
    this.state = this.loadState();
    
    eventBus.on('context.updated', (newState) => {
      this.state = { ...this.state, ...newState };
      this.saveState();
    });
  }

  loadState() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      if (stored) {
        const parsed = JSON.parse(stored);
        return {
          history: [],
          dockMode: 'floating',
          replays: [],
          avatar: null,
          position: null,
          ...parsed
        };
      }
    } catch (e) {
      console.warn('[MITRA] Failed to load context from localStorage', e);
    }
    return {
      history: [],
      dockMode: 'floating',
      replays: [],
      avatar: null,
      position: null
    };
  }

  saveState() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.state));
      eventBus.emit('context.saved', { timestamp: new Date().toISOString() });
    } catch (e) {
      console.warn('[MITRA] Failed to save context to localStorage', e);
    }
  }

  addMessage(role, text, metadata = {}) {
    this.state.history.push({
      role,
      text,
      timestamp: new Date().toISOString(),
      ...metadata
    });
    this.saveState();
  }

  getHistory() {
    return this.state.history || [];
  }

  addReplay(replayItem) {
    if (!this.state.replays) this.state.replays = [];
    this.state.replays.push(replayItem);
    this.saveState();
    eventBus.emit('replay.generated', replayItem);
  }

  getReplays() {
    return this.state.replays || [];
  }

  setDockMode(mode) {
    if (!mode) return;
    const validMode = (mode === 'left' || mode === 'right' || mode === 'floating') ? mode : 'floating';
    this.state.dockMode = validMode;
    this.saveState();
  }

  getDockMode() {
    return this.state.dockMode || 'floating';
  }

  setAvatar(avatarDataUrl) {
    this.state.avatar = avatarDataUrl;
    this.saveState();
    eventBus.emit('avatar.changed', { avatar: avatarDataUrl });
  }

  getAvatar() {
    return this.state.avatar || null;
  }

  setPosition(position) {
    if (!position || position.left == null || position.top == null) return;
    this.state.position = position;
    this.saveState();
    eventBus.emit('position.changed', { position });
  }

  getPosition() {
    return this.state.position || null;
  }
}

export const contextStore = new ContextStore();
