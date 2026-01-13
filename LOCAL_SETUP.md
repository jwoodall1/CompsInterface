# Local Setup & Documentation

This guide explains how to set up the project locally and connect to the remote VM database using an SSH tunnel.

## 1. Prerequisites
- **Python 3.10+**
- **Git**
- **SSH Client** (Installed by default on Windows 10+, macOS, and Linux)

## 2. Clone the Repository
Open a terminal (PowerShell or Bash) and run:
```bash
git clone https://github.com/jwoodall1/CompsInterface.git
cd CompsInterface
```

## 3. Environment Setup
Create a virtual environment and install dependencies:
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

## 4. SSH Port Forwarding (The "Tunnel")
To access the remote database without changing VM firewall rules, create a local tunnel.

Run this in a **separate terminal window** and keep it open:
```bash
ssh -L 5433:localhost:5432 user@stearns.mathcs.carleton.edu
```.
- This maps the remote DB (port 5432) to your local machine at port **5433**.

## 5 Run the Application
In primary terminal (with the virtual environment active):
```bash
python app.py
```
The app will be available at: [http://localhost:42069](http://localhost:42069)

---

- **Keeping it Alive**: If the SSH connection drops, the database connection will fail. Simply restart the SSH command.
