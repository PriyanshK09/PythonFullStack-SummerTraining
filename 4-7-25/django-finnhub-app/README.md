# Django Finnhub App

This project is a Django application that displays live NASDAQ prices using the Finnhub WebSocket API.

## Project Structure

```
django-finnhub-app
├── manage.py                # Command-line utility for administrative tasks
├── finnhub_project/         # Main Django project directory
│   ├── __init__.py          # Marks the directory as a Python package
│   ├── settings.py          # Configuration settings for the Django project
│   ├── urls.py              # URL patterns for the Django project
│   ├── wsgi.py              # Entry point for WSGI-compatible web servers
│   └── asgi.py              # Entry point for ASGI-compatible web servers
├── stock_app/               # Django application for stock prices
│   ├── __init__.py          # Marks the directory as a Python package
│   ├── admin.py             # Registers models with the Django admin site
│   ├── apps.py              # Configuration for the stock_app application
│   ├── models.py            # Defines data models for the application
│   ├── views.py             # View functions that handle requests
│   ├── urls.py              # URL patterns specific to the stock_app
│   ├── consumers.py         # WebSocket consumers for real-time updates
│   └── templates/           # HTML templates for the application
│       └── stock_app/
│           └── index.html   # Main page template displaying live prices
├── static/                  # Static files (CSS, JS)
│   ├── css/
│   │   └── style.css        # CSS styles for the application
│   └── js/
│       └── websocket.js     # JavaScript for WebSocket connection
├── requirements.txt         # Python package dependencies
└── README.md                # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd django-finnhub-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the development server:**
   ```
   python manage.py runserver
   ```

5. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

The application connects to the Finnhub WebSocket API to fetch live NASDAQ prices and displays them on the main page. The WebSocket connection is handled in the `websocket.js` file, and the live prices are rendered in the `index.html` template.

## License

This project is licensed under the MIT License.