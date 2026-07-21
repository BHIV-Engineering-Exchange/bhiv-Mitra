# MITRA Universal Companion

MITRA is a Universal Companion interface designed for the BHIV ecosystem. It is framework-agnostic, built with standard HTML5, Vanilla JavaScript (ES6 Modules), and Shadow DOM CSS isolation.

## Key Features

- **Universal Companion UI**: Bottom-right floating action button with pulsing animation and online status dot.
- **Multiple Layout Modes**: Floating, Dock Left, Dock Right, Expanded, Collapse, and Minimize.
- **Capability Launcher**: Grid of 9 reusable capability cards (Analyze, OCR, Translate, Summarize, Image, PDF, Replay, Health, Settings) for delegating tasks.
- **Runtime Orchestration**: Event Bus architecture (`src/services/eventBus.js`) connecting UI to `runtimeService.js`, `controlPlane.js`, and `capabilityRuntime.js`.
- **Persistent Context**: `contextStore.js` backed by `localStorage` to preserve conversation history across host application page switches (`uniguru.html`, `samachar.html`, `gurukul.html`, `setu.html`).
- **Activity & Health Monitoring**: Live status indicator (Idle, Thinking, Running Capability, Completed, Failed) and Runtime Health Panel (Latency, Status, Version, Last Sync).
- **Mobile Responsive**: Fully responsive UI with auto-scaling for mobile, tablet, and desktop viewports.

## Project Structure

```
/src
  /components
    ActivityIndicator.js
    CapabilityLauncher.js
    ConversationPanel.js
    DockController.js
    Footer.js
    Header.js
    HealthPanel.js
    MITRAButton.js
    MITRAWindow.js
    NotificationBadge.js
    NotificationCenter.js
  /services
    contextStore.js
    controlPlane.js
    eventBus.js
    RuntimeService.js
  /mock
    capabilityRuntime.js
  mitra-companion.js
/styles
  mitra-companion.css
/pages
  uniguru.html
  samachar.html
  gurukul.html
  setu.html
```

## How to Run

Because the project uses standard ES6 modules (`import`/`export`), it must be served over HTTP:

```bash
python -m http.server 8000
```

Open `http://localhost:8000/pages/uniguru.html` in your browser. Navigating between host pages preserves MITRA's history and UI state.
