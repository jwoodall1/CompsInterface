# Local Setup & Documentation

This guide explains how to set up the project locally and connect to the remote VM database using an SSH tunnel.

## 1. Prerequisites
- **Python 3.10+**
- **Git**
- **SSH Client** (Installed by default on Windows 10+, macOS, and Linux)

## 2. SSH into stearns:
To access the remote database, and run the website, log into stearns via ssh as follows:

```bash
ssh user@stearns.mathcs.carleton.edu
```.
- or use VS code's ssh extension

## 3. Clone the Repository
Open a terminal (PowerShell or Bash) and run:
```bash
git clone https://github.com/jwoodall1/CompsInterface.git
cd CompsInterface
```

## 4. Download the credentials to log into the database from Drive:
Download the file at this link at place it in the home directory of CompsInterface.
https://drive.google.com/file/d/18gp3rMl0BIz2t9NfDIz7nGVxA4aEwziH/view?usp=sharing 

## 4. Environment Setup
Create a virtual environment and install dependencies:
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

## 5 Run the Application
In your terminal (with the virtual environment active):
```bash
python app.py
```
The app will be available at: [stearns.mathcs.carleton.edu:5132] on the lap computers.

---
