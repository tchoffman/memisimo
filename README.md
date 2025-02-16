# memisimo
Toy messaging application

## Start the FastAPI App for Local Development
Run via Uvicorn:
```
uvicorn src.message_api:app --reload
```

See API documentation at:
http://127.0.0.1:8000/docs

## curl examples (see docs above for more)

### Send SMS Message
```
curl -X POST http://localhost:8000/webhook/sms \
  -H "Content-Type: application/json" \
  -d '{
    "from": "+18045551234",
    "to": "+12016661234",
    "type": "sms",
    "xillio_id": "message-1",
    "body": "text message",
    "attachments": null,
    "timestamp": "2024-11-01T14:00:00Z"
  }'
```

### Send MMS Message
```
curl -X POST http://localhost:8000/webhook/mms \
  -H "Content-Type: application/json" \
  -d '{
    "from": "+18045551234",
    "to": "+12016661234",
    "type": "mms",
    "xillio_id": "message-2",
    "body": "text message",
    "attachments": ["attachment-url"],
    "timestamp": "2024-11-01T14:00:00Z"
  }'
```

### Send Email Message
```
curl -X POST http://localhost:8000/webhook/email \
  -H "Content-Type: application/json" \
  -d '{
    "from": "user@memisimo.com",
    "to": "contact@gmail.com",
    "type": "email",
    "xillio_id": "message-2",
    "body": "<html><body>html is <b>allowed</b> here </body></html>",
    "attachments": ["attachment-url"],
    "timestamp": "2024-11-01T14:00:00Z"
  }'
```
## Inspect Local DB

- Start SQLite with `sqlite3 ./memisimo.db
- Run SQL Commands

```
.tables                  -- Show all tables
SELECT * FROM messages;  -- View messages table
SELECT * FROM contacts;  -- View contacts table
.schema                 -- View database schema
.quit                   -- Exit SQLite CLI
```

## SQLite Browser (optional utility)
- Install SQLite Browser with `brew install --cask db-browser-for-sqlite`
- then... `open -a "DB Browser for SQLite" ./memisimo.db`

## Debug Endpoint for DB
- `curl http://localhost:8000