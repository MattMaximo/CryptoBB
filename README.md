# Crypto Backend

Best crypto backend ever made.

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 7778
```


#### Docker

```
docker build -t crypto-backend .
docker run --env-file .env -p 7778:7778 crypto-backend
```


