# MDU — Module Dependency Update

## Frontend Dependency Map

```
src/mitra-companion.js  (entry point)
├── src/config.js                       ← NEW: global config (api-base-url)
├── src/services/RuntimeService.js
│   ├── src/services/eventBus.js
│   ├── src/services/contextStore.js
│   └── src/config.js
├── src/services/eventBus.js
├── src/services/controlPlane.js
│   ├── src/services/eventBus.js
│   ├── src/services/contextStore.js
│   └── src/config.js
├── src/components/MITRAButton.js
│   ├── src/components/NotificationBadge.js
│   └── src/services/eventBus.js
├── src/components/MITRAWindow.js
│   ├── src/components/Header.js
│   ├── src/components/ConversationPanel.js
│   │   └── src/components/MessageRenderer.js   ← NEW: canonical component
│   ├── src/components/Footer.js
│   ├── src/components/CapabilityLauncher.js
│   ├── src/components/HealthPanel.js
│   ├── src/components/ActivityIndicator.js
│   └── src/components/ExecutionStatusPanel.js  ← NEW: canonical component
├── src/components/NotificationCenter.js
└── src/components/DockController.js
    └── src/services/contextStore.js
```

## Backend API Endpoints Consumed

| Endpoint               | Method | Used By               |
|------------------------|--------|-----------------------|
| `/health`              | GET    | `RuntimeService.js`   |
| `/api/assistant`       | POST   | `controlPlane.js`     |
| `/api/mitra/evaluate`  | POST   | `controlPlane.js`     |

## External Dependencies

None. The frontend is vanilla JavaScript with zero npm dependencies. The backend uses FastAPI + optional LLM client libraries (managed by Raj).
