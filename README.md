# Coderr – Backend Description
This is the backend of Coderr, a platform for freelance services. The application distinguishes between two user roles: clients and providers.

## ![Features Icon](assets/icons/gear.png) Features

    • Registration, login, and an optional guest access  
    • Profile management for both user roles  
    • Providers can create, edit, and manage their service offerings  
    • Clients can place and manage orders, as well as rate providers  

The API serves as the foundation for seamless communication between the frontend and the database, ensuring a clear separation of user permissions and functionalities.

## ![Tech Stack Icon](assets/icons/stack.png) Tech Stack
    • Python 3.x
    • Django 4.x
    • Django REST Framework
    • SQLite / PostgreSQL (optional)
# ![Installation Icon](assets/icons/installation.png) Installation
## 1. Clone the repository:
git clone https://github.com/Pinguinrakete/coderr_backend.git .
```bash
```
## 2. Create a virtual environment to isolate our package dependencies locally
python -m venv env

### Windows
```bash
source ".\env\Scripts\activate"
```  

### macOS/Linux
```bash
source ".\env\bin\activate"
```  
## 3. Install dependencies
pip install -r requirements.txt  
python manage.py makemigrations  
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
    • POST    /api/registration/  ➤ Register a new user. 
    • POST    /api/login/         ➤ Log in a user (returns auth token). 

## ![Profile Icon](/assets/icons/profile.png) Profile
    • GET     /api/profile/<pk>/        ➤ Retrieves detailed information of a user profile 
                                           (for both customer and business users).
    • PATCH   /api/profile/<pk>/        ➤ Allows a user to update specific profile information. 
    • GET     /api/profiles/business>/  ➤ Returns a list of all business users on the platform.
    • GET     /api/boards/customer/     ➤ Returns a list of all customer profiles on the platform.

## ![Offers Icon](/assets/icons/offers.png) Offers
    • GET     /api/offers/  ➤ Returns a list of offers, each including an overview of details, 
                               minimum price, and shortest delivery time.
    • POST    /api/offers/  ➤ Creates a new offer with 3 required details. 
    • GET     /api/offers/<id>/  ➤ Retrieves details of a specific offer by ID.
    • PATCH   /api/offers/<id>/  ➤ Updates a specific offer; only the provided fields are overwritten.
    • DELETE  /api/offers/<id>/  ➤ Deletes a specific offer by ID.
    • GET     /api/offerdetails/<id>  ➤ Retrieves details of a specific offer detail.

## ![Orders Icon](/assets/icons/orders.png) Orders
    • GET     /api/orders/  ➤ Returns a list of orders created by the logged-in user as a 
                               customer or business partner.
    • POST    /api/orders/  ➤ Creates a new order based on offer details (OfferDetail).
    • PATCH   /api/orders/<id>/  ➤ Updates the status of a specific order 
                                    (e.g., 'in_progress', 'completed', 'cancelled').
    • DELETE  /api/orders/<id>/  ➤ Deletes a specific order; restricted to admin (staff) users.
    • GET     /api/order-count/<business_user_id>/  ➤ Returns the count of ongoing ('in_progress') 
                                                       orders for a specific business user.
    • GET     /api/completeted-order-count/<business_user_id> ➤ Returns the count of completed 
                                                ('completed') orders for a specific business user.

## ![Rewiews Icon](assets/icons/reviews.png) Rewiews
    • GET     /api/reviews/  ➤ Lists all available reviews.
    • POST    /api/reviews/  ➤ Creates a new review for a business user.
    • PATCH   /api/reviews/<id>/  ➤ Updates selected fields of an existing review.
    • DELETE  /api/reviews/<id>/  ➤ Deletes a specific review.

## ![Endpoint Icon](assets/icons/endpoint.png) Cross-cutting endpoints
    • GET     /api/base-info/  ➤ Retrieves general platform information, including number of reviews, 
                                  average rating, number of business users, and number of offers.

## ![License Icon](assets/icons/certificate.png) License
This project is intended exclusively for students of the Developer Akademie and is not licensed for public use or distribution. 