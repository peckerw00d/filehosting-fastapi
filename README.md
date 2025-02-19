
# File Hosting Application

This project is a web application for file storage with user authentication and personal file management.
## Installation

1. Ensure you have Docker and Docker Compose installed on your system.

2. Clone the repository:  

```bash
git clone https://github.com/peckerw00d/filehosting-fastapi.git
cd filehosting-fastapi
```

3. Start the application using Makefile: 

```bash
make up
```

Alternatively, you can use the following command

```bash
docker compose -f docker-compose.yaml up -d
```

4. The application will be available at http://localhost:8000  after successful startup. 

5. To stop and remove containers: 

```bash
make down
```

Or use:

```bash
docker compose -f docker-compose.yaml down && docker network prune --force
```

6. If you only want to stop the containers without removing them: 

```bash
make stop
```

Or:

```bash
docker compose -f docker-compose.yaml stop
```

All necessary environment variables are configured in the docker-compose.yaml file. Port 8000 is used for accessing the API.
## API Reference

#### Get all files

```http
  GET /files
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. Your session token |

#### Get file by URL

```http
  GET /files/${file_url}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `file_url`      | `string` | **Required**. URL of file to fetch |
| `Authorization` | `string` | **Required**. Your session token |

#### Download file by URL

```http
  GET /files/download/${file_url}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `file_url`      | `string` | **Required**. URL of file to download |
| `Authorization` | `string` | **Required**. Your session token |

#### Upload file

```http
  POST /files/upload-file
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `file`      | `UploadFile` | **Required**. File to upload |
| `Authorization` | `string` | **Required**. Your session token |

#### Delete file

```http
  DELETE /files/${file_url}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `file_url`      | `string` | **Required**. URL of file to delete |
| `Authorization` | `string` | **Required**. Your session token |

#### Register user 

```http
  POST /users/register
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. Username for registration |
| `email`      | `string` | **Required**. Email for registration |
| `password`      | `string` | **Required**. Password for registration |


#### Login user

```http
  POST /users/login
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. Required. Username for login |
| `password`      | `string` | **Required**. Password for login |

#### Logout user

```http
  POST /users/logout
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`      | `string` | **Required**. Your session token |

## Features

  - User authentication and session management
  - File upload and storage
  - File download and deletion
  - Personalized user storage space
  - Secure file access control
     

## Tech Stack

**Server:** FastAPI  
**Database:** PostgreSQL  
**Object Storage:** MinIO  
**Authentication:** Session-based (HTTP cookies)  
**ORM:** SQLAlchemy  
**Testing:** Pytest, Async testing utilities  
**Containerization:** Docker, Docker Compose  
**Configuration Management:** Pydantic Settings, Environment variables  
**Password Hashing:** Bcrypt  
**Middleware:** Custom session middleware for user authentication  
**Utilities:** Alembic for database migrations, UVicorn as the ASGI server  