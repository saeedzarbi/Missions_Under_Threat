# Missions_Under_Threat

**Missions Under Threat** is a simple web application simulating a secret agency's mission management system. This project is designed for educational purposes, providing an opportunity to identify and fix hidden vulnerabilities while exploring secure coding practices.

---

## Features

1. **User Registration**
   - Agents can sign up with a unique codename and a secret code.

2. **User Login**
   - Agents can log in using their codename and secret code.
   - A valid session is created upon successful login.

3. **Mission Management**
   - Agents can view their personal list of missions.
   - Agents can add new missions to their list.
   - Agents can view detailed information about individual missions.

4. **Mission Search**
   - Agents can search for specific missions using keywords.
   - Results display missions that contain the keyword.

5. **Logout**
   - Agents can securely log out, ending their session.

---

## Setup and Installation

### 1. Prerequisites
- Python 3.x installed on your system.
- A virtual environment (optional but recommended).

### 2. Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/saeedzarbi/Missions_Under_Threat
   cd missions-under-threat
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install flask
python app.py

Open your browser and navigate to:
http://127.0.0.1:5000
