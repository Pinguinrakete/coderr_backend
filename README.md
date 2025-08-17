# KanMind Backend
 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 
## ![Features Icon](assets/icons/gear.png) Features
    • User registration and login
## ![Tech Stack Icon](assets/icons/stack.png) Tech Stack
    • Python 3.x
    • Django 4.x
    • Django REST Framework
    • SQLite / PostgreSQL (optional)
# ![Installation Icon](assets/icons/installation.png) Installation
## 1. Clone the repository:
git clone https://github.com/Pinguinrakete/coderr_backend.git
```bash
cd coderr_backend
```
## 2. Create virtual environment
# Windows
python -m venv env
```bash
source ".\env\Scripts\activate"
```  

# macOS/Linux
python3 -m venv env
```bash
source ".\env\bin\activate"
```  
## 3. Install dependencies
pip install -r requirements.txt  

python manage.py migrate  
python manage.py createsuperuser  
python manage.py runserver  

# ![Authentication Icon](assets/icons/authentication.png) Authentication
The API uses token-based authentication (TokenAuthentication). 
Each API request must include a valid token in the HTTP header: 

    Authorization: Token <your-token>

Only authenticated users with a valid token are granted access to the protected endpoints. 
# ![API Endpoints Icon](assets/icons//api.png) API Endpoints Documentations
## ![Authentication Icon](assets/icons/authentication.png) Authentication
    • POST    /api/registration/	 ➤ Register a new user. 
    • POST    /api/login/            ➤ Log in a user (returns auth token). 