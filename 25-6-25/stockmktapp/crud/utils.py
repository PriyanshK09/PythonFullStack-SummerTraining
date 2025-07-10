import requests
import json
from django.conf import settings
from decimal import Decimal
from datetime import datetime
from .models import Stock, UserStock
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Tiingo API Configuration
TIINGO_API_KEY = '76502c062c45182ffaa1ced745d0b24d30e8625c'
TIINGO_BASE_URL = 'https://api.tiingo.com/tiingo'

def get_tiingo_api_key():
    """Get Tiingo API key from settings or fallback"""
    return getattr(settings, 'TIINGO_API_KEY', TIINGO_API_KEY)

def get_stock_metadata(ticker):
    """Get stock metadata from Tiingo API"""
    try:
        api_key = get_tiingo_api_key()
        url = f"{TIINGO_BASE_URL}/daily/{ticker.upper()}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {api_key}'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                return {
                    'ticker': data.get('ticker', ticker.upper()),
                    'name': data.get('name', ticker.upper()),
                    'description': data.get('description', ''),
                    'exchange': data.get('exchangeCode', ''),
                    'currency': 'USD'
                }
    except Exception as e:
        print(f"Error fetching metadata for {ticker}: {e}")
    return None

def get_stock_data(ticker):
    """Get current stock price data from Tiingo API"""
    try:
        api_key = get_tiingo_api_key()
        url = f"{TIINGO_BASE_URL}/daily/{ticker.upper()}/prices"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {api_key}'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                latest = data[-1]  # Get the most recent data
                return {
                    'ticker': ticker.upper(),
                    'close': latest.get('close', 0),
                    'open': latest.get('open', 0),
                    'high': latest.get('high', 0),
                    'low': latest.get('low', 0),
                    'volume': latest.get('volume', 0),
                    'date': latest.get('date', '')
                }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
    return None

def get_stock_history(ticker, start_date, end_date):
    """Get historical stock data from Tiingo API"""
    try:
        api_key = get_tiingo_api_key()
        url = f"{TIINGO_BASE_URL}/daily/{ticker.upper()}/prices"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {api_key}'
        }
        params = {
            'startDate': start_date,
            'endDate': end_date
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data if data else []
    except Exception as e:
        print(f"Error fetching history for {ticker}: {e}")
    return []

def get_intraday_data(ticker):
    """Get intraday data (placeholder - Tiingo requires paid plan for real-time)"""
    try:
        # For demo purposes, return recent daily data
        api_key = get_tiingo_api_key()
        url = f"{TIINGO_BASE_URL}/daily/{ticker.upper()}/prices"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {api_key}'
        }
        params = {
            'resampleFreq': '1Day'
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data[-10:] if data else []  # Last 10 days
    except Exception as e:
        print(f"Error fetching intraday data for {ticker}: {e}")
    return []

def get_stock_news(ticker, limit=10):
    """Get stock-specific news from Tiingo API"""
    try:
        api_key = get_tiingo_api_key()
        url = f"https://api.tiingo.com/tiingo/news"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {api_key}'
        }
        params = {
            'tickers': ticker.upper(),
            'limit': limit,
            'offset': 0
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data if data else []
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
    return []

def get_general_market_news(limit=5):
    """Get general market news from Tiingo API"""
    try:
        api_key = get_tiingo_api_key()
        url = f"https://api.tiingo.com/tiingo/news"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {api_key}'
        }
        params = {
            'limit': limit,
            'offset': 0
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data if data else []
    except Exception as e:
        print(f"Error fetching general market news: {e}")
    return []

def create_or_update_stock(metadata, price_data=None):
    """Create or update stock in database"""
    try:
        if not metadata:
            return None
            
        ticker = metadata.get('ticker', '').upper()
        if not ticker:
            return None
            
        # Get or create stock
        stock, created = Stock.objects.get_or_create(
            ticker=ticker,
            defaults={
                'name': metadata.get('name', ticker),
                'description': metadata.get('description', ''),
                'exchange': metadata.get('exchange', ''),
                'currency': metadata.get('currency', 'USD')
            }
        )
        
        # Update price if provided
        if price_data and price_data.get('close'):
            stock.current_price = Decimal(str(price_data.get('close', 0)))
            stock.save()
            
        return stock
    except Exception as e:
        print(f"Error creating/updating stock: {e}")
        return None

def search_tiingo_stocks(query):
    """Search for stocks using Tiingo API (basic implementation)"""
    try:
        # Since Tiingo doesn't have a direct search endpoint,
        # we'll try to get metadata for the query as a ticker
        metadata = get_stock_metadata(query)
        if metadata:
            return [metadata]
    except Exception as e:
        print(f"Error searching stocks: {e}")
    return []

def calculate_price_stats(history_data):
    """Calculate price statistics from historical data"""
    if not history_data:
        return {}
        
    try:
        prices = [float(day.get('close', 0)) for day in history_data if day.get('close')]
        if not prices:
            return {}
            
        return {
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_price': sum(prices) / len(prices),
            'price_change': prices[-1] - prices[0] if len(prices) > 1 else 0,
            'price_change_percent': ((prices[-1] - prices[0]) / prices[0] * 100) if len(prices) > 1 and prices[0] != 0 else 0
        }
    except Exception as e:
        print(f"Error calculating price stats: {e}")
        return {}

def send_transaction_receipt(user, transaction):
    """Send transaction receipt email to user"""
    try:
        # Calculate total amount
        total_amount = transaction.quantity * transaction.buy_price
        
        # Calculate portfolio value
        user_stocks = UserStock.objects.filter(user=user, transaction_type='BUY')
        portfolio_value = Decimal('0.00')
        for stock_holding in user_stocks:
            if stock_holding.stock.current_price:
                portfolio_value += stock_holding.quantity * stock_holding.stock.current_price
        
        # Email context
        context = {
            'user': user,
            'transaction': transaction,
            'total_amount': total_amount,
            'portfolio_value': portfolio_value,
        }
        
        # Email subject
        if transaction.transaction_type == 'BUY':
            subject = f'✅ Purchase Confirmed - {transaction.stock.ticker} | StockFolio'
        else:
            subject = f'💰 Sale Confirmed - {transaction.stock.ticker} | StockFolio'
        
        # Render email templates
        text_content = render_to_string('crud/emails/transaction_receipt.txt', context)
        html_content = render_to_string('crud/emails/transaction_receipt.html', context)
        
        # Create email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        email.send()
        
        return True
    except Exception as e:
        print(f"Failed to send transaction receipt email: {e}")
        return False

def test_email_configuration():
    """Test email configuration by sending a test email"""
    try:
        from django.core.mail import send_mail
        
        send_mail(
            'StockFolio Test Email',
            'This is a test email to verify your email configuration is working.',
            settings.DEFAULT_FROM_EMAIL,
            ['priyanshkhare0908@gmail.com'],
            fail_silently=False,
        )
        return True, "Test email sent successfully!"
    except Exception as e:
        return False, f"Failed to send test email: {str(e)}"