📓 Digital Diary — Python SLA Mini Project

A secure and feature-rich Digital Diary application developed using Python.
This project includes two implementations:

🖥️ Command-Line Version (CLI) — secure, lightweight, testable
🎨 GUI Version (Tkinter) — modern desktop interface with enhanced usability
🔗 Repository

GitHub:
https://github.com/Rudra070509/DDMain

🎥 Project Demo Video : https://drive.google.com/file/d/1LQoZcK2b4fuj8loGrDETquoMkfynFaaW/view?usp=sharing


📌 Project Overview

The Digital Diary allows users to securely write, manage, and search personal entries.
It uses password protection, local storage, and follows clean coding + OOP principles.

✨ Features
🔐 Security
Master password protected (SHA-256 hashing)
Secure login before accessing diary
📝 Entry Management
Add diary entries with timestamp
View entries in reverse chronological order
Delete entries using ID
🔍 Search & Filter
Search by keyword
Search by date
Filter by mood (GUI version)
💾 Storage
Data stored locally in JSON format
Persistent across sessions
🎨 GUI Features (Tkinter Version)
Dark theme (navy + accent colors)
Mood selector
Live clock
Word count
Export entries to .txt
🧪 Testing
Unit tests implemented using unittest
🛠️ Tech Stack
Category	Technology
Language	Python 3
Libraries	hashlib, json, os, datetime, tkinter, unittest
Version Control	Git + GitHub
Architecture	Modular + OOP
🚀 How to Run
🔹 1. Clone the Repository
git clone https://github.com/Rudra070509/DDMain.git
cd DDMain
🔹 2. Check Python Installation
python --version
▶️ Run CLI Version
python main.py
First Run:
Set a master password
Stored securely using SHA-256
▶️ Run GUI Version
python part1_app_shell.py
Requirements:
All GUI files must be in same folder:
part1_app_shell.py
part2_editor.py
part3_search.py
🧪 Run Unit Tests
python -m unittest test_diary.py -v
📂 Project Structure
DDMain/
│
├── CLI VERSION
│   ├── main.py
│   ├── diary.py
│   ├── auth.py
│   ├── storage.py
│   ├── test_diary.py
│
├── GUI VERSION
│   ├── part1_app_shell.py
│   ├── part2_editor.py
│   ├── part3_search.py
│
├── entries.json / diary_entries.json
└── README.md
👥 Team Members & Contributions
Roll No	Name	Branch	Contribution
B056	Rudra	feature-storage	JSON storage, file handling, delete logic, repo setup
B065	Arif	feature-auth	Password hashing, authentication system, testing
B066	Ayush	feature-ui	CLI UI, Tkinter GUI, search, documentation
🌿 GitHub Collaboration Strategy
main
 ├── feature-storage
 ├── feature-auth
 └── feature-ui

✔ Feature branches used
✔ Pull Requests for merging
✔ No direct commits to main
✔ Proper commit messages

📸 Screenshots

(Add screenshots here before submission)

🎯 SLA Evaluation Coverage
Criteria	Covered
Problem & Functionality	✔ Working CLI + GUI
Code Quality	✔ Modular + OOP
GitHub Collaboration	✔ Branching + PRs
Documentation	✔ Complete README
Video	✔ Demo included
📄 License

This project was developed for Python SLA Mini Project submission
SVKM BHAGUBHAI MAFATLAL POLYTECHNIC AND COLLEGE OF ENGINEERING
Diploma in Computer Science Engineering [ B066 , B059 , B065 ]
