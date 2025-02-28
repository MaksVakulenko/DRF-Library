# SpaceReservation – Changes & Usage Guide

This README describes the modifications introduced to the SpaceReservation project and provides instructions on how to use the updated features. It covers changes to environment configuration, Docker setup, and database initialization.

---

## Overview

- **Database**: The project now uses PostgreSQL (via the `psycopg-binary` package) as the primary database. The connection settings are specified in the environment variables.
- **Docker Configuration**:  
  - A single Docker Compose file is used to build and run containers for the backend and PostgreSQL.
  - Volumes have been configured for persistent storage of static files, media, and database data.
- **Environment Variables**:  
  - The `.env` file now includes settings for PostgreSQL.
  - The database selection is controlled by the `DJANGO_DB` variable.
- **Initialization Script (`init.sql`)**:  
  - This script creates the PostgreSQL database and grants privileges to the specified user.
- **Healthchecks**:  
  - The backend container now have special endpoint for healthcheck
- **Docker Compose Override**:  
  - (Optional) A secondary Compose file (`docker-compose-local.yaml`) may be used for local development or debugging with postgres in docker.

---

## Changes Introduced

### 1. Environment Variables (`.env`)
- **Database Settings**:
  - `DJANGO_DB` is now set to `postgresql` (comment out `sqlite`).
  - PostgreSQL connection variables (`POSTGRES_HOST`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB_PORT`) are defined.


> **Note:**  
> Make sure to update your `.env` file with the correct values before running the project.

### 2. Docker Configuration
- **docker-compose.yaml**:  
  The Compose file defines the following services:
  - **db**: Uses the official PostgreSQL 16.0 image. The container name is set to `library-postgres`, and it mounts `init.sql` to automatically initialize the database.
  - **backend**: Builds the backend image using `./docker/backend/Dockerfile`, mounts the source code from `./src`, and sets up volumes for static files and media.
  - **Volumes & Networks**:  
    Volumes are configured for static files, media, and database data. A custom Docker network (`library-network`) is created.

### 3. Database Initialization (`init.sql`)
- The `init.sql` script is automatically executed by the PostgreSQL container. It performs the following actions:
  - Creates the database (`library_db`).
  - Grants all privileges on all tables in the public schema to the `admin` user.
  
> **Example `init.sql`:**
> ```sql
> CREATE DATABASE library_db;
> GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
> ```

### 4. Backend Entrypoint Script
- **server-entrypoint.sh**:
  - Changes to the backend directory.
  - Runs Django migrations.
  - Collects static files.
  - Finally, starts the Django development server (or Gunicorn for production).
  

### 5. Healthcheck Configuration
- The backend service in `docker-compose.yaml` includes a healthcheck that pings the `/api/health/` endpoint.
- If you wish to disable continuous healthchecks after startup, adjust the `interval`, `timeout`, or `retries` values accordingly.

---

## How to Use the Changes

### Running the Project with Docker

1. **Update Environment Variables:**
   - Copy `.env.sample` to `.env` and update the values as needed:
     ```bash
     cp .env.sample .env
     ```

2. **Build and Start Containers:**
   - Run the following command to build the images and start all containers:
     ```bash
     docker-compose up --build
     ```

3. **Database Initialization:**
   - The PostgreSQL container will execute the `init.sql` file on startup to create the database and set permissions.


### Using the Alternative Docker Compose File
- If you want to use Django Project from IDE with postgres from docker, please use docker-compose-local and specify this file for docker-compose commands,
ex:
  ```bash
  docker-compose -f docker-compose-local.yaml up --build
  ```
  # SpaceReservation Project – Changes & Usage Guide

This guide summarizes the modifications introduced to the SpaceReservation project and explains how to use these changes. It covers updated environment configurations, Docker setup, database initialization, and how to select between different database backends.

---

## Overview of Changes

1. **Environment Variables and Database Selection**  
   - The project now supports both SQLite and PostgreSQL backends.  
   - The `DJANGO_DB` environment variable controls which database is used:
     - Set `DJANGO_DB=sqlite` for a local SQLite database.
     - Set `DJANGO_DB=postgresql` for a PostgreSQL database.
### Database Host Selection for PostgreSQL

- **If using setup DB + Django from Docker**: Set `POSTGRES_HOST=library-postgres` (the container name).
- **If running Django locally and DB in docker**: Set `POSTGRES_HOST=localhost`.
     ```ini
     # Django:
     SECRET_KEY=_eSHIGrn*@OSo!H1hDISxl4hH8wj90La

     # Stripe:
     STRIPE_SECRET_KEY='your_secret_key'
     STRIPE_PUBLISHABLE_KEY='your_publishable_key'

     # Database selection:
     # Please specify which database you would like to use and comment out the other option:
     #DJANGO_DB=sqlite
     DJANGO_DB=postgresql

     # PostgreSQL (for Docker deployment):
     POSTGRES_HOST=library-postgres      # This is the container name for the PostgreSQL service
     POSTGRES_DB=library_db                # Database name
     POSTGRES_USER=admin
     POSTGRES_PASSWORD=some_password
     POSTGRES_DB_PORT=5432
     ```
