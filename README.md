# Hotspot Dating App Backend

This is the backend for the Hotspot Dating App built using FastAPI. The app focuses on enabling users to connect with each other when they are within specified geofenced hotspot locations, making it an exciting way for people to meet in real-world locations such as cafes, restaurants, and other public spaces.

## Features

- **User Registration and Authentication**: Secure user registration and login.
- **Profile Management**: Users can update their profiles, including adding and prioritizing photos.
- **Hotspot Management**: Admins can create and manage hotspot locations where users can connect.
- **Geofencing**: Users can only interact with others when they are within a defined hotspot.
- **Swiping Mechanism**: Users can swipe right or left on other users and match if both swipe right.
- **Undo Swipe**: Users can undo their last swipe.
- **Matches**: Users are notified of matches when both parties swipe right on each other.

## Tech Stack

- **FastAPI**: Modern, fast (high-performance), web framework for building APIs with Python 3.7+.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **PostgreSQL**: Advanced open source relational database.
- **Boto3**: AWS SDK for Python to interact with AWS services like S3.

## Getting Started

### Prerequisites

- Python 3.7+
- PostgreSQL
- AWS account (for S3)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/hotspot-dating-app-backend.git
    cd hotspot-dating-app-backend
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    Create a PostgreSQL database and update the `DATABASE_URL` in your `.env` file.

    ```bash
    DATABASE_URL=postgresql://username:password@localhost/dbname
    ```

5. **Set up AWS S3:**

    Update your AWS credentials and bucket name in the `config.py` file.

    ```python
    AWS_SERVER_PUBLIC_KEY = os.getenv("AWS_SERVER_PUBLIC_KEY")
    AWS_SERVER_SECRET_KEY = os.getenv("AWS_SERVER_SECRET_KEY")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    ```

6. **Run database migrations:**
    ```bash
    alembic upgrade head
    ```

7. **Start the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```

### Environment Variables

- `DATABASE_URL`: Database connection URL.
- `AWS_SERVER_PUBLIC_KEY`: AWS S3 public key.
- `AWS_SERVER_SECRET_KEY`: AWS S3 secret key.
- `S3_BUCKET_NAME`: AWS S3 bucket name.

### Security

- **Do not include sensitive information** in your public repository. Use environment variables and a `.env` file.
- **Regularly update dependencies** to mitigate known vulnerabilities.
- **Follow security best practices**, such as input validation and proper error handling.
- **Implement logging and monitoring** to detect and respond to suspicious activity.

### Contributing

Feel free to contribute to this project by opening a pull request or an issue.

## Contact

For any inquiries or issues, please contact [thegluping@gmail.com](mailto:thegluping@gmail.com).
