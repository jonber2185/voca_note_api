# VocaNote API

[한국어](README.ko.md)

Backend API server for **[VocaNote](https://github.com/jonber2185/VocaNote-web)**, a vocabulary note-taking service. Users can create word sets, add and manage words, get AI-generated word analysis (definitions/examples via Gemini), and search public sets.

## Tech Stack

| Layer | Technology |
|---|---|
| Flask | web framework |
| Flask-JWT-Extended | authentication via HTTP-only cookies (access/refresh tokens) |
| MySQL (PyMySQL) | relational data (users, sets, sessions) |
| MongoDB (PyMongo) | word data |
| Google Gemini (`google-genai`) | word/definition analysis |
| Gunicorn | production WSGI server |

## API Overview

| Prefix | Description |
|---|---|
| `POST /auth/login` | Log in, sets JWT cookies |
| `POST /auth/refresh` | Refresh access token |
| `POST /auth/logout` | Log out, clears cookies |
| `GET /user/me` | Get current user |
| `POST /user/create` | Register a new user |
| `POST /user/update_password` | Change password |
| `POST /user/delete` | Delete account |
| `GET/POST /set/<user_id>` | List / create word sets |
| `GET/PATCH/DELETE /set/<user_id>/<set_id>` | Get / update / delete a set |
| `POST /words/analyze` | AI-analyze a list of words |
| `GET/POST/PATCH /words/<user_id>/<set_id>` | List / add / edit words in a set |
| `GET /words/<user_id>/<set_id>/example` | Get example sentences |
| `DELETE /words/<user_id>/<set_id>/<word_id>` | Delete a word |
| `GET /search?q=` | Search users/sets |

## Setup

### Requirements

- Python 3.10+
- MySQL database
- MongoDB database
- Google Gemini API key

### Installation

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
FRONT_URL=http://localhost:3000
JWT_SECRET_KEY=your-secret-key

MySQL_HOST=localhost
MySQL_USER=your-mysql-user
MySQL_PASSWORD=your-mysql-password
MySQL_NAME=your-database-name
MySQL_PORT=3306

Mongo_ID=your-mongo-username
Mongo_PASSWORD=your-mongo-password

GEMINI_API_KEY=your-gemini-api-key
```

### Run

```bash
# Development
python app.py

# Production
gunicorn app:app
```


## Authentication

Auth uses JWT access/refresh tokens stored in `HttpOnly`, `Secure`, `SameSite=None` cookies, suitable for cross-origin frontend setups.

