# FastAPI-xAPI
FastAPI xAPI Server and Client

This repository provides a demonstration of how to set up a FastAPI server to receive and store xAPI statements in an SQLite database and a Python client to send xAPI statements to the server.

## Setup

1. Clone this repository.
2. Install required packages:
```bash
pip install fastapi[all] uvicorn requests sqlite
```
3. Start the FastAPI server:
```bash
uvicorn server:app --reload
```
4. In a separate terminal, run the client to send an xAPI statement:
```bash
python client.py
```

## Explanation

**xAPI**: The Experience API (xAPI) is a specification for collecting data about learning experiences, predominantly used in e-learning platforms.

**FastAPI**: A modern, high-performance web framework for building APIs with Python based on standard Python type hints.

### server.py

This file contains a FastAPI server set up to accept POST requests with xAPI statements, store them in an SQLite database, and retrieve them via GET requests.

### client.py

This script sends a sample xAPI statement to the server and prints the server's response.

## Note

This demonstration uses SQLite for persistent storage. For larger-scale production deployments, consider using more scalable database solutions and implementing additional security and performance optimizations.
