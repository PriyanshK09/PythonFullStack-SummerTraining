# eCommerce REST API

This project is a Django-based REST API for an eCommerce application. It provides endpoints for managing products, categories, user authentication, and cart functionality.

## Features

- **User Authentication**: Register and login users.
- **Product Management**: List all products and retrieve products by name.
- **Category Management**: Manage product categories.
- **Cart Functionality**: Add, update, and remove items from the shopping cart.

## Project Structure

```
ecommerce-rest-api/
├── manage.py
├── requirements.txt
├── ecommerce_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── authentication/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│       └── __init__.py
├── products/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│       └── __init__.py
├── categories/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│       └── __init__.py
├── cart/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── decorators.py
│   └── migrations/
│       └── __init__.py
├── utils/
│   ├── __init__.py
│   └── permissions.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ecommerce-rest-api
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Start the development server:
   ```
   python manage.py runserver
   ```

## Usage

- **User Registration**: POST `/api/auth/register/`
- **User Login**: POST `/api/auth/login/`
- **List Products**: GET `/api/products/`
- **Retrieve Product**: GET `/api/products/<product_name>/`
- **Manage Cart**: 
  - Add to Cart: POST `/api/cart/add/`
  - Update Cart: PUT `/api/cart/update/`
  - Remove from Cart: DELETE `/api/cart/remove/`
- **Manage Categories**: Use the respective endpoints in the categories app.

## License

This project is licensed under the MIT License.