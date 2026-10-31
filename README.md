# Behaviour-Based Web Session Deviation Detection

A lightweight security framework built with Python and Flask to monitor active web sessions and detect anomalous user behavior in real time.

---

## 📌 Project Overview

Traditional web applications rely almost entirely on perimeter authentication (usernames and passwords). While this verifies who logs in, it fails to monitor whether that user's behavior remains legitimate throughout the active session. If an account is hijacked or accessed by automated scripts post-login, the intrusion often goes unnoticed.

**Behaviour-Based Web Session Deviation Detection** addresses this security gap by continuously logging user navigation, evaluating request velocity within rolling time windows, and checking temporal access patterns. Activities exceeding predefined anomaly thresholds are automatically assigned a dynamic deviation score and flagged on an administrative dashboard.

---

## 🎯 Key Objectives

- Develop a session-monitored web application architecture using Python and Flask.
- Implement continuous background event tracking across endpoints into an SQLite database.
- Calculate dynamic heuristic deviation scores based on sliding request windows and off-hour access.
- Provide a clean, real-time administrative monitoring dashboard displaying session telemetry and risk status (`Normal` vs. `Suspicious`).

---

## ⚙️ How It Works (Detection Logic)

The system records route visits, timestamps, and active user identities into an event database, applying heuristic scoring rules upon each request:

| Monitored Condition | Trigger Rule | Assigned Score | Resulting Status |
| :--- | :--- | :---: | :---: |
| **Normal Request Velocity** | Request count < 10 inside the rolling 60-second window | `0` | **Normal** |
| **High-Frequency Request Burst** | Request count ≥ 10 inside the rolling 60-second window | `+50` | **Suspicious** |
| **Off-Hours Activity** | Access detected before 06:00 or after 23:00 | `+30` | **Normal** (if alone) |
| **Compound Anomaly** | Burst activity combined with off-hours access | `+80` | **Suspicious** |

> **Threshold:** Any session event accumulating a deviation score of **50 or higher** is categorized as **Suspicious**.

---

## 🛠️ Tech Stack & Prerequisites

- **Language:** Python 3.x
- **Web Framework:** Flask
- **Database:** SQLite3
- **Security:** Werkzeug Cryptography (`generate_password_hash`, `check_password_hash`)
- **Frontend:** HTML5, CSS3

---

## 🚀 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/](https://github.com/)<your-username>/behaviour-based-web-session-deviation-detection.git
cd behaviour-based-web-session-deviation-detection
