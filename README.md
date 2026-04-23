📓 Digital Diary — Python SLA Mini Project

A secure and feature-rich Digital Diary application developed using Python.
This project includes two implementations:

🖥️ Command-Line Version (CLI) — secure, lightweight, testable
🎨 GUI Version (Tkinter) — modern desktop interface with enhanced usability

GitHub:
https://github.com/Rudra070509/DDMain

🎥 Project Demo Video : https://drive.google.com/file/d/1LQoZcK2b4fuj8loGrDETquoMkfynFaaW/view?usp=sharing


📌 Project Overview

The Digital Diary allows users to securely write, manage, and search personal entries.
It uses password protection, local storage, and follows clean coding + OOP principles.

✨ Features<br><br>

🔐 Security<br>
Master password protected (SHA-256 hashing)<br>
Secure login before accessing diary<br><br>

📝 Entry Management<br>
Add diary entries with timestamp<br>
View entries in reverse chronological order<br>
Delete entries using ID<br><br>

🔍 Search & Filter<br>
Search by keyword<br>
Search by date<br>
Filter by mood (GUI version)<br><br>

💾 Storage<br>
Data stored locally in JSON format<br>
Persistent across sessions<br><br>

🎨 GUI Features (Tkinter Version)<br>
Dark theme (navy + accent colors)<br>
Mood selector<br>
Live clock<br>
Word count<br>
Export entries to .txt<br><br>

🧪 Testing<br>
Unit tests implemented using unittest<br><br>

🛠️ Tech Stack<br><br>

Category | Technology<br>
Language | Python 3<br>
Libraries | hashlib, json, os, datetime, tkinter, unittest<br>
Version Control | Git + GitHub<br>
Architecture | Modular + OOP<br><br>

🚀 How to Run<br><br>

🔹 1. Clone the Repository<br>
git clone https://github.com/Rudra070509/DDMain.git<br>
cd DDMain<br><br>

🔹 2. Check Python Installation<br>
python --version<br><br>

▶️ Run CLI Version<br>
python main.py<br><br>

First Run:<br>
Set a master password<br>
Stored securely using SHA-256<br><br>

▶️ Run GUI Version<br>
python part1_app_shell.py<br><br>

Requirements:<br>
All GUI files must be in same folder:<br>
part1_app_shell.py<br>
part2_editor.py<br>
part3_search.py<br><br>

🧪 Run Unit Tests<br>
python -m unittest test_diary.py -v<br><br>

📂 Project Structure<br><br>

DDMain/<br>
│<br>
├── CLI VERSION<br>
│   ├── main.py<br>
│   ├── diary.py<br>
│   ├── auth.py<br>
│   ├── storage.py<br>
│   ├── test_diary.py<br>
│<br>
├── GUI VERSION<br>
│   ├── part1_app_shell.py<br>
│   ├── part2_editor.py<br>
│   ├── part3_search.py<br>
│<br>
├── entries.json / diary_entries.json<br>
└── README.md<br><br>

👥 Team Members & Contributions<br><br>

Roll No | Name | Branch | Contribution<br>
B056 | Rudra | feature-storage | JSON storage, file handling, delete logic, repo setup<br>
B065 | Arif | feature-auth | Password hashing, authentication system, testing<br>
B066 | Ayush | feature-ui | CLI UI, Tkinter GUI, search, documentation<br><br>

🌿 GitHub Collaboration Strategy<br><br>

main<br>
 ├── feature-storage<br>
 ├── feature-auth<br>
 └── feature-ui<br><br>

✔ Feature branches used<br>
✔ Pull Requests for merging<br>
✔ No direct commits to main<br>
✔ Proper commit messages<br>

📸 Screenshots



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
