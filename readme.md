# Chats app

## Setup

1. Create .env file
    ```bash
    cp .example.env .env
    ```
1. Build the project
   ```bash
   # Using makefile
   make build
   # Docker directly
   docker compose build
   ```
1. Run
   ```bash
   # Using makefile
   make up
   # Docker directly
   docker compose up
   ```

## Open the app
Go to http://localhost:8000/ , default login / pw combo is `admin / admin`
