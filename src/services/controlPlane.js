import { eventBus } from './eventBus.js';

const API_BASE = 'https://mitra-backend-q1f3.onrender.com';
const API_KEY = 'bhiv-enterprise-key';

export class ControlPlane {
  async simulateResponse(text) {
    return this.sendMessage(text);
  }

  async sendMessage(text) {
    eventBus.emit('health.changed', { status: 'Busy' });
    try {
      const response = await fetch(`${API_BASE}/api/assistant`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': API_KEY
        },
        body: JSON.stringify({
          version: "3.0.0",
          input: { message: text },
          context: {
            platform: "web",
            device: "desktop",
            session_id: "mitra-session-1"
          }
        })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      
      let replyText = data.final_output?.reason || data.response || "Success";

      eventBus.emit('health.changed', { status: 'Healthy' });
      eventBus.emit('notification.received', {
        role: 'mitra',
        text: replyText
      });
      return data;
    } catch (err) {
      eventBus.emit('health.changed', { status: 'Error' });
      eventBus.emit('notification.received', {
        role: 'mitra',
        text: 'Error communicating with backend: ' + err.message
      });
      throw err;
    }
  }

  async sendCapability(capabilityName) {
    eventBus.emit('health.changed', { status: 'Busy' });
    try {
      const response = await fetch(`${API_BASE}/api/mitra/evaluate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': API_KEY
        },
        body: JSON.stringify({
          input: { message: `Execute capability: ${capabilityName}` }
        })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();

      eventBus.emit('health.changed', { status: 'Healthy' });
      return data;
    } catch (err) {
      eventBus.emit('health.changed', { status: 'Error' });
      throw err;
    }
  }
}
export const controlPlane = new ControlPlane();
