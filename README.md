# Django Application with Docker Compose

This README provides all the necessary instructions to set up, run, and test a Django application that uses Docker Compose for containerization and stores secrets in a `.env` file.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup Instructions](#setup-instructions)
3. [Running the Application](#running-the-application)
4. [Running Tests](#running-tests)
5. [Common Docker Commands](#common-docker-commands)
6. [Environment Variables](#environment-variables)
7. [Debugging Tips](#debugging-tips)

---

## Prerequisites

- Docker and Docker Compose installed on your machine.
- Python 3.10+ installed locally if you need to work outside Docker.
- A `.env` file with the required environment variables (see [Environment Variables](#environment-variables) section).

---

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/degisew/bank-account-management.git
   cd bank-account-management
   ```

2. Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
   Customize the values in the `.env` file as needed.

3. Build and start the Docker containers:
   ```bash
   docker-compose -f compose.dev.yaml up --build  # detached mode
   ```

---

## Running the Application

### Start the Server
Run the following command to start the Django development server:
```bash
docker-compose -f compose.dev.yaml up
```
This will:
- Start the Django app on `http://localhost:8000` (or another port if configured).
- Attach logs to the terminal.

To run the server in detached mode:
```bash
docker-compose -f compose.dev.yaml up -d --build
```

### Stop the Server
To stop the running containers:
```bash
docker-compose -f compose.dev.yaml down
```

---

## Running Tests

### Run Pytest
To execute tests using `pytest`:
```bash
docker-compose -f compose.dev.yaml exec web pytest
```
This ensures tests run in the containerized environment.


### Run Individual Tests
You can target specific test files or functions:
```bash
docker-compose exec web pytest path/to/test_file.py
```

---

## Common Docker Commands

- **Rebuild Containers:**
  ```bash
  docker-compose -f compose.dev.yaml up --build
  ```

- **Remove All Containers:**
  ```bash
  docker-compose -f compose.dev.yaml down
  ```

- **View Logs:**
  ```bash
  docker-compose -f compose.dev.yaml logs
  ```

- **Access Shell in the Web Container:**
  ```bash
  docker-compose exec web bash
  ```

---

## Environment Variables

The application uses a `.env` file to store secrets and environment-specific configurations. Below are common variables:

```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@db:5432/db_name
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Note:** Never commit the `.env` file to version control.

---

## Debugging Tips

- **Container Issues:** If containers fail to start, inspect logs using:
  ```bash
  docker-compose -f compose.dev.yaml logs
  ```

- **Database Migrations:** Run migrations inside the container:
  ```bash
  docker-compose exec web python manage.py migrate
  ```

- **Static Files:** Collect static files for production:
  ```bash
  docker-compose exec web python manage.py collectstatic --noinput
  ```

- **Database Shell:** Access the database shell:
  ```bash
  docker-compose exec db psql -U <db_user> <db_name>
  ```
