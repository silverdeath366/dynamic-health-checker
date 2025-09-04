### Dynamic Health Checker

A lightweight Python monitor that checks CPU and memory usage and sends alerts to Telegram.

---

### Features
- **CPU and memory checks** using `psutil`
- **Telegram alerts** via Bot API
- **Container-ready** (Dockerfile provided)
- **Kubernetes manifests** for quick deployment

---

### Requirements
- Python 3.12+
- `psutil`, `requests` (installed via `requirements.txt`)
- Telegram Bot token and a chat ID

---

### Environment Variables
- **TELEGRAM_BOT_TOKEN**: Your Telegram bot token
- **TELEGRAM_CHAT_ID**: Chat ID (user or group) to receive alerts

Example (Linux/macOS/WSL):
```bash
export TELEGRAM_BOT_TOKEN="<token>"
export TELEGRAM_CHAT_ID="<chat_id>"
```

---

### Local Run
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python monitor.py
```

---

### Configure Thresholds
Current defaults (edit `monitor.py`):
```python
CPU_THRESHOLD = 1
MEM_THRESHOLD = 1
```
Increase these to realistic values (e.g., 80 for CPU, 85 for memory) based on your needs.

---

### Docker
Build and run locally:
```bash
# Build
docker build -t dynamic-health-checker:latest .

# Run
docker run --rm \
  -e TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" \
  -e TELEGRAM_CHAT_ID="$TELEGRAM_CHAT_ID" \
  dynamic-health-checker:latest
```

The container entrypoint runs `python monitor.py`.

---

### Kubernetes
Manifests are in `manifests/`.

1) Update the image in `manifests/monitor-deployment.yaml` if needed:
```yaml
containers:
  - name: monitor
    image: silverdeath366/monitor:latest  # change if using your own image
```

2) Provide environment variables. Example patch:
```yaml
env:
  - name: TELEGRAM_BOT_TOKEN
    valueFrom:
      secretKeyRef:
        name: telegram-secrets
        key: bot_token
  - name: TELEGRAM_CHAT_ID
    valueFrom:
      secretKeyRef:
        name: telegram-secrets
        key: chat_id
```

3) Apply:
```bash
kubectl apply -f manifests/monitor-deployment.yaml
```

Note: The provided `monitor-service.yaml` exposes port 80 -> 8080, but the app does not serve HTTP traffic. You can skip creating the Service or remove the port mapping unless you plan to add an HTTP endpoint.

---

### Telegram Setup
1) Create a bot via `@BotFather` and obtain the token
2) Get your chat ID (e.g., by messaging the bot and using a tool like `@userinfobot` or checking updates via Bot API)
3) Set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`

---

### Troubleshooting
- "Telegram credentials missing": Ensure both env vars are set
- No alerts received: Verify the bot can message the chat (for groups, the bot must be added)
- High noise: Raise `CPU_THRESHOLD`/`MEM_THRESHOLD`

---

### Repository Structure
- `monitor.py`: Health checks and Telegram alerts
- `Dockerfile`: Container build
- `requirements.txt`: Python dependencies
- `manifests/`: Kubernetes Deployment and (optional) Service

