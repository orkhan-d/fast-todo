# Fast TO-DO
The modulo architecture app using FastAPI and Jinja

How to start:
1. Add .env file with the next variables:
  - DB_ADDRESS: address for database
  - JWT_SECRET: secret for JWT tokens
2. change data in docker-compose.yml app (like DB user, etc.)
3. Just run
```bash
docker compose build && dcoker compose up -d
```
to start and 
```bash
docker compose down
```
to stop
