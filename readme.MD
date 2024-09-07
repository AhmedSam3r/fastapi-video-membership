# Video Membership Web App with FastAPI & AstraDB

This project is a **Video Membership Web Application** built using **FastAPI** and **NoSQL** with **AstraDB**. It offers features such as user authentication, video analytics, resumable videos, and a custom playlist feature. The project is based on the tutorial series from [Coding for Entrepreneurs](https://www.youtube.com/codingentrepreneurs), and this repository follows the key steps from the [video membership app tutorial](https://www.youtube.com/watch?v=KQ-u4RcFLBY).

## Features

- **User Authentication**: Sign up and log in functionality with secure, hashed passwords.
- **JWT Tokens**: JSON Web Tokens for authentication and session management.
- **Video Uploading**: Add videos to the platform with support for video URLs like YouTube.
- **Resumable Videos**: Users can pause videos and resume them from where they left off.
- **Playlist Management**: Users can create custom playlists and manage videos within them.
- **Search Engine**: Search functionality to find videos by title.
- **Video Analytics**: Monitor and log video watch events.

## Tech Stack

- **FastAPI**: The backend is built using FastAPI, a modern, fast web framework for Python.
- **Cassandra & AstraDB**: NoSQL database Cassandra, managed by AstraDB, to store user data, video information, and more.
- **Pydantic**: For data validation and serialization.
- **Jinja2 Templates**: For rendering HTML pages.
- **HTMX**: For handling asynchronous form submissions.
- **JWT**: For authentication and token management.
- **YouTube API**: Used for video embedding.

## Project Structure

```bash
.
├── app
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── routes
│   └── templates
├── notebooks
├── tests
├── requirements.txt
└── README.md
```

### Key Files and Directories

- `app/main.py`: Contains the main FastAPI application and routes.
- `app/auth.py`: Handles authentication, JWT token creation, and validation.
- `app/models.py`: Contains Pydantic models and database schemas.
- `app/routes`: Contains FastAPI routers and endpoints for different functionalities.
- `app/templates`: Jinja2 templates for rendering the HTML front end.
- `notebooks`: Jupyter notebooks for testing and experimenting with features.
- `tests`: Contains automated test cases.

## Getting Started

### Prerequisites

To run this project, ensure you have the following installed:

- **Python 3.8+**
- **FastAPI**
- **Cassandra/AstraDB**
- **Jinja2**
- **HTMX**

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/codingforentrepreneurs/video-membership.git
   cd video-membership
   ```

2. **Set up a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up AstraDB (Cassandra Database)**:
   - Create an AstraDB account: [Sign up here](https://dtsx.io/3lAUmnG).
   - Configure your database and get your connection credentials.
   - Ensure you set up environment variables for AstraDB connection in `app/config.py`.

5. **Run the application**:

   ```bash
   uvicorn app.main:app --reload
   ```

   The app will run locally at `http://127.0.0.1:8000`.

### Database Configuration

Ensure that you have AstraDB or a Cassandra instance running. In `app/config.py`, set up your connection credentials:

```python
ASTRA_DB_KEYSPACE = "your_keyspace"
ASTRA_DB_CLIENT_ID = "your_client_id"
ASTRA_DB_CLIENT_SECRET = "your_client_secret"
```

You can also use environment variables to securely store these credentials.

### Example API Endpoints

- `POST /signup/`: Create a new user account.
- `POST /login/`: Authenticate a user and return a JWT.
- `GET /videos/`: List all videos.
- `POST /videos/`: Add a new video (requires authentication).
- `GET /playlist/{id}`: View a playlist and its videos.

### Testing

To run the test cases:

```bash
pytest
```

## Useful Links

- [Coding for Entrepreneurs GitHub Repository](https://github.com/codingforentrepreneurs/video-membership)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [AstraDB Documentation](https://docs.datastax.com/en/astra/docs/)
