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
    "from_address": "1234567890",
    "to_address": "0987654321",
    "body": "Test message",
    "timestamp": "2024-02-15T00:00:00Z",
    "xillio_id": "1234"
  }'
```

### Send MMS Message
```
curl -X POST http://localhost:8000/webhook/mms \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": "1234567890",
    "to_address": "0987654321",
    "body": "Test message with attachment",
    "timestamp": "2024-02-15T00:00:00Z",
    "xillio_id": "1234",
    "attachments": ["http://example.com/image.jpg"]
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