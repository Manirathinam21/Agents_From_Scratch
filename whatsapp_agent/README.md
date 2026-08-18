```
uvicorn main:app --port 8000

```


### Flow

```
WhatsApp → Twilio → ngrok → FastAPI → Groq → WhatsApp
```

### 🧠 Mental Model (Lock This In)

| Source            | Sends `Body`? | Works? |
| ----------------- | ------------- | ------ |
| WhatsApp → Twilio | ✅ Yes         | ✅ YES  |
| curl (form-data)  | ✅ Yes         | ✅ YES  |
| FastAPI Swagger   | ❌ No          | ❌ NO   |

### Required setup checklist

    - FastAPI running

    - ngrok running

    - Twilio webhook pointing to ngrok

    - WhatsApp message sent from phone

### Curl command to test:

```curl

curl -X POST http://127.0.0.1:8000/whatsapp/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "Body=Hello from curl&From=whatsapp:+919999999999"

```

### Architecture

```

WhatsApp (User)
   ↓
Twilio Webhook
   ↓
FastAPI
   ↓
LangGraph App (with Sqlite memory)
   ├── Chat Agent (text + memory)
   ├── Vision Agent (image)
   └── Supervisor (routing)
```

## ngrok command:

```
ngrok http 8000
```