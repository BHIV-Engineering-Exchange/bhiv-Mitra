import { eventBus } from './eventBus.js';
import { contextStore } from './contextStore.js';
import { controlPlane } from './controlPlane.js';

export class RuntimeService {
  constructor() {
    this.context = contextStore;
    this.status = 'Disconnected';
    this.latency = '0ms';
  }

  async connectAll() {
    eventBus.emit('health.changed', { status: 'Connecting', latency: 'connecting...' });

    try {
      const startTime = Date.now();
      const res = await fetch('http://localhost:8000/health');
      const duration = Date.now() - startTime;

      if (res.ok) {
        this.status = 'Healthy';
        this.latency = `${duration}ms`;
        eventBus.emit('runtime.connected', {});
        eventBus.emit('health.changed', { status: 'Healthy', latency: this.latency });
        this.startHeartbeat();
        return true;
      }
    } catch (e) {
      this.status = 'Error';
      eventBus.emit('health.changed', { status: 'Error', latency: '--' });
    }
    return false;
  }

  startHeartbeat() {
    setInterval(async () => {
      try {
        const startTime = Date.now();
        const res = await fetch('http://localhost:8000/health');
        if (res.ok) {
          this.latency = `${Date.now() - startTime}ms`;
          if (this.status !== 'Busy') {
            this.status = 'Healthy';
            eventBus.emit('health.changed', { status: this.status, latency: this.latency });
          }
        }
      } catch (e) {
        this.status = 'Error';
        eventBus.emit('health.changed', { status: 'Error', latency: '--' });
      }
    }, 5000);
  }

  async sendCapabilityRequest(capabilityName) {
    this.status = 'Busy';
    eventBus.emit('health.changed', { status: 'Busy', latency: this.latency });
    const startTimestamp = new Date().toLocaleTimeString();
    eventBus.emit('capability.requested', { capability: capabilityName, timestamp: startTimestamp });
    eventBus.emit('runtime.thinking', {});

    const startTime = Date.now();
    eventBus.emit('capability.started', { capability: capabilityName, timestamp: startTimestamp });

    try {
      if (capabilityName === 'health') {
        const res = await fetch('http://localhost:8000/health/system');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const durationMs = Date.now() - startTime;
        eventBus.emit('capability.completed', { capability: capabilityName, duration: `${durationMs}ms`, result: 'System health loaded.' });
        contextStore.addReplay({ timestamp: new Date().toLocaleTimeString(), capability: capabilityName, status: 'SUCCESS', duration: `${durationMs}ms` });
        contextStore.addMessage('mitra', `System Health: ${JSON.stringify(data, null, 2)}`);
      } else if (capabilityName === 'settings') {
        const res = await fetch('http://localhost:8000/api/metrics/system', {
          headers: {
            "X-API-Key": "bhiv-enterprise-key"
          }
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const durationMs = Date.now() - startTime;
        eventBus.emit('capability.completed', { capability: capabilityName, duration: `${durationMs}ms`, result: 'System settings loaded.' });
        contextStore.addReplay({ timestamp: new Date().toLocaleTimeString(), capability: capabilityName, status: 'SUCCESS', duration: `${durationMs}ms` });
        contextStore.addMessage('mitra', `System Metrics: ${JSON.stringify(data, null, 2)}`);
      } else if (capabilityName === 'replay') {
        const replays = contextStore.getReplays();
        const lastReplay = replays[replays.length - 1];
        if (lastReplay && lastReplay.traceId) {
          const res = await fetch(`http://localhost:8000/api/replay/${lastReplay.traceId}`, {
            headers: {
              "X-API-Key": "bhiv-enterprise-key"
            }
          });
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          const data = await res.json();
          const durationMs = Date.now() - startTime;
          eventBus.emit('capability.completed', { capability: capabilityName, duration: `${durationMs}ms`, result: 'Replay loaded.' });
          contextStore.addMessage('mitra', `Replay Data: ${JSON.stringify(data, null, 2)}`);
        } else {
          throw new Error('No backend endpoint available for general trace history, and no local trace ID found.');
        }
      } else {
        const data = await controlPlane.sendCapability(capabilityName);
        const durationMs = Date.now() - startTime;
        const durationStr = `${(durationMs / 1000).toFixed(1)}s`;
        const endTimestamp = new Date().toLocaleTimeString();

        const resultText = `Capability [${capabilityName.toUpperCase()}] executed successfully via backend.`;

        eventBus.emit('capability.completed', { capability: capabilityName, duration: durationStr, result: resultText });
        contextStore.addReplay({ timestamp: endTimestamp, capability: capabilityName, status: 'SUCCESS', duration: durationStr, traceId: data.trace_id });
        contextStore.addMessage('mitra', `[Capability: ${capabilityName.toUpperCase()}] ${resultText} (Execution time: ${durationStr})`);
      }
    } catch (e) {
      if (e.name === 'AbortError' || e.message.includes('timeout')) {
        eventBus.emit('capability.timed_out', { capability: capabilityName, error: e.message });
      } else {
        eventBus.emit('capability.failed', { capability: capabilityName, error: e.message });
      }
      contextStore.addMessage('mitra', `[Capability: ${capabilityName.toUpperCase()}] Failed: ${e.message}`);
    } finally {
      this.status = 'Healthy';
      eventBus.emit('health.changed', { status: 'Healthy', latency: this.latency });
      eventBus.emit('runtime.idle', {});
    }
  }

  async sendMessage(text) {
    this.context.addMessage('user', text);
    this.status = 'Busy';
    eventBus.emit('health.changed', { status: 'Busy', latency: this.latency });
    eventBus.emit('runtime.thinking', {});

    try {
      await controlPlane.sendMessage(text);
    } catch (e) {
      // error handled in controlPlane
    } finally {
      this.status = 'Healthy';
      eventBus.emit('health.changed', { status: 'Healthy', latency: this.latency });
      eventBus.emit('runtime.idle', {});
    }
  }


}

export const runtimeService = new RuntimeService();
