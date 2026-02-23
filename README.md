# 📚 BookWormers

> *My first production-deployed FastAPI application — built to learn, shipped to the world.*

BookWormers is a full-stack web application for managing and tracking your personal book library. It started as a learning project and ended as something I'm genuinely proud of — a real app, running on real infrastructure, serving real requests.

---

## ✨ Features

- **Add Books** — Log new books with title, author, genre, status, description, page count, and rating
- **Browse & Search** — View your entire library and filter by title, author, or reading status
- **Update Records** — Edit any book's details at any time
- **Delete Books** — Remove entries cleanly from the database
- **REST API** — A FastAPI backend with proper CORS support for seamless frontend integration
- **Production Deployment** — Frontend served via Nginx; backend managed as a persistent systemd service on AWS EC2

---


## 🧠 What I Learned

This project was more than just an app, it was a genuine education in how the web actually works.

Building BookWormers taught me how to configure PostgreSQL from scratch with proper user permissions, how to wrap a Python process in a systemd service so it never goes down, and how Nginx serves static files cleanly in production. I learned how to expose ports on AWS and wire a frontend to a backend running on real infrastructure - not localhost, but an actual server in the cloud.

But the most clarifying moment was understanding **DNS**. Every domain name —> `google.com`, anything, is just a human-readable pointer to an IP address. The DNS system resolves that name to its IP, and the ISP routes the traffic accordingly. Static IPs anchored to a domain make it all work seamlessly. Knowing that now, I see the internet differently.

This was my first time deploying a FastAPI application on AWS. It works. And that means everything.

---


## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + TypeScript (built with Lovable) |
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| Web Server | Nginx |
| Process Manager | systemd (bookwormers.service) |
| Cloud Host | AWS EC2 |

---

## 🏗️ Architecture Overview

```
Browser
  └── Nginx (serves React/dist static files)
        └── FastAPI (Uvicorn on 0.0.0.0:8000)
              └── PostgreSQL (bookwormers_db)
```

The frontend communicates with the backend via a configured `API_BASE_URL` pointing to the EC2 instance's public IP on port `8000`. The backend runs continuously as a systemd service that restarts automatically on failure.

---

## ⚙️ Backend Setup

### PostgreSQL Configuration

```sql
-- Create dedicated user and database
CREATE USER bookwormers_user WITH PASSWORD 'your_password';
CREATE DATABASE bookwormers_db OWNER bookwormers_user;
GRANT ALL PRIVILEGES ON DATABASE bookwormers_db TO bookwormers_user;
```

Authentication is configured via `pg_hba.conf` using `md5` or `trust` as appropriate for the environment.

### Running the API

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### systemd Service

The backend is registered as a systemd service (`bookwormers.service`) configured to always restart, ensuring the API stays alive across reboots and failures.

```ini
[Service]
ExecStart=uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
```

```bash
sudo systemctl enable bookwormers
sudo systemctl start bookwormers
```

---

## 🌐 Frontend Setup

The React frontend was built using [Lovable](https://lovable.dev) and compiled for production:

```bash
npm run build
sudo cp -r dist/* /usr/share/nginx/html/
```

Nginx serves the static files and the app connects to the FastAPI backend via the configured API base URL.

---

## ☁️ AWS Deployment Notes

- Hosted on an **AWS EC2** instance
- The **Security Group** was configured to open the necessary ports (e.g., `80` for HTTP, `8000` for the API)
- `API_BASE_URL` in the frontend was updated to match the EC2 public IP and exposed port
- Backend was fully configured and running before the frontend was deployed

---

## 📁 Project Structure

```
bookwormers/
├── backend/
│   ├── main.py          # FastAPI app entry point
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── database.py      # DB connection config
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   └── App.tsx
│   └── package.json
└── README.md
```

---

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/books` | Retrieve all books |
| `GET` | `/books/{id}` | Retrieve a single book |
| `POST` | `/books` | Add a new book |
| `PUT` | `/books/{id}` | Update a book |
| `DELETE` | `/books/{id}` | Delete a book |

---

## 🙏 Acknowledgements

Built with curiosity, late nights, and the stubborn belief that the best way to learn infrastructure is to actually ship something to it.

---

*First FastAPI app. First AWS deployment. Not the last.*
