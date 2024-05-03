# ZenithChat

Project Overview
ZenithChat is a chat application designed to provide a seamless and interactive communication platform for users. It allows participants to join chat rooms, send messages, and receive new messages.

Features
User Registration: Users can sign up by providing essential information such as email, username, and password.
User Authentication: Secure user authentication implemented using OAuth2PasswordBearer.
Real-Time Messaging: Users can join chat rooms and exchange messages in real time.
Chat Room Management: Users can create and manage chat rooms.
Message History: Users can view the history of messages in any chat room they are part of.

Technology Stack
FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) for Python.
Alembic: Database migrations tool for SQLAlchemy.
SQLite: Database for storing user and chat data.

Structure
```
.
├── alembic
│   ├── env.py
│   ├── __pycache__
│   │   └── env.cpython-310.pyc
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 08dcfe024022_pre_final_tables.py
│       └── __pycache__
│           └── 08dcfe024022_pre_final_tables.cpython-310.pyc
├── alembic.ini
├── app
│   ├── database
│   │   ├── database.py
│   │   ├── models.py
│   │   └── __pycache__
│   │       ├── database.cpython-310.pyc
│   │       └── models.cpython-310.pyc
│   ├── main.py
│   ├── __pycache__
│   │   ├── main.cpython-310.pyc
│   │   └── websocket_manager.cpython-310.pyc
│   ├── repositories
│   │   ├── chats_repository.py
│   │   ├── messages_repository.py
│   │   ├── __pycache__
│   │   │   ├── chats_repository.cpython-310.pyc
│   │   │   ├── messages_repository.cpython-310.pyc
│   │   │   └── users_repository.cpython-310.pyc
│   │   └── users_repository.py
│   ├── routers
│   │   ├── chats.py
│   │   ├── messages.py
│   │   ├── __pycache__
│   │   │   ├── chats.cpython-310.pyc
│   │   │   ├── messages.cpython-310.pyc
│   │   │   └── users.cpython-310.pyc
│   │   └── users.py
│   ├── serializers
│   │   ├── chats.py
│   │   ├── messages.py
│   │   ├── __pycache__
│   │   │   ├── chats.cpython-310.pyc
│   │   │   ├── messages.cpython-310.pyc
│   │   │   └── users.cpython-310.pyc
│   │   └── users.py
│   ├── sse_test.html
│   └── websocket_manager.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── sql_app.db

14 directories, 38 files
```

#Installation
Clone the Repository:
```
https://github.com/dimalbek/ZenithChat.git
cd ZenithChat
```

Set up a Virtual Environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install Dependencies:
```
pip install poetry # if not installed
poetry install
```

Initialize the Database:
```
alembic upgrade head
```

Run the Application:
```
uvicorn app.main:app --reload
```
The API will now be accessible at http://127.0.0.1:8000 .
You may check endpoints at http://127.0.0.1:8000/docs .

#API Endpoints:
API Endpoints
User Management:
POST /users/register: Register a new user.
POST /users/login: Log in a user and return a token.
GET /users/me: Retrieve information about yourslef.
PATCH /users/me: Update information about yourself.
GET /users/chats: Retrieve all chats you are part of.
Chat Management:
POST /chats/new/: Create a new chat room.
POST /chats/join/{chat_id}: Join an existing chat room.
GET /chats/all: Retrieve all chats with pagination.
Messages:
POST /{chat_id}: Send a message to a specific chat room.
GET /{chat_id}: Retrieve messages from a specific chat room.

Author
Developed by [Dinmukhamed Albek].
