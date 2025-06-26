from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, F
from .models import User, Stock, UserStock, Watchlist, StockPriceHistory
from .forms import UserRegistrationForm, UserLoginForm, StockPurchaseForm
import requests
import json
from decimal import Decimal
from django.conf import settings
from datetime import datetime, timedelta
import pytz

# Tiingo API Configuration
TIINGO_API_KEY = '76502c062c45182ffaa1ced745d0b24d30e8625c'
TIINGO_BASE_URL = 'https://api.tiingo.com/tiingo'

def get_stock_data(ticker):
    """Fetch stock data from Tiingo API"""
    try:
        url = f"{TIINGO_BASE_URL}/daily/{ticker}/prices"
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'token': TIINGO_API_KEY,
            'resampleFreq': 'daily',
            'format': 'json'
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[-1]  # Get latest data
        return None
    except Exception as e:
        return None

def get_stock_history(ticker, start_date=None, end_date=None):
    """Fetch historical stock data from Tiingo API"""
    try:
        url = f"{TIINGO_BASE_URL}/daily/{ticker}/prices"
        headers = {
            'Content-Type': 'application/json'
        }
        
        params = {
            'token': TIINGO_API_KEY,
            'format': 'json'
        }
        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date
            
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []

def get_stock_news(ticker, limit=10):
    """Fetch news for a specific stock from Tiingo API"""
    try:
        # Use the correct endpoint format from documentation
        url = "https://api.tiingo.com/tiingo/news"
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Format parameters according to documentation
        params = {
            'token': TIINGO_API_KEY,
            'tickers': ticker.lower(),  # Use lowercase as per documentation
            'limit': limit,
            'sortBy': 'publishedDate'
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            news_data = response.json()
            
            # Process and format the news data
            formatted_news = []
            for article in news_data:
                formatted_article = {
                    'title': article.get('title', 'No title'),
                    'description': article.get('description', 'No description'),
                    'url': article.get('url', '#'),
                    'publishedDate': article.get('publishedDate', ''),
                    'source': article.get('source', 'Unknown'),
                    'tags': article.get('tags', []),
                    'tickers': article.get('tickers', [])
                }
                formatted_news.append(formatted_article)
            
            return formatted_news[:limit]
        return []
    except Exception as e:
        return []

def get_general_market_news(limit=10):
    """Fetch general market news when specific stock news is not available"""
    try:
        url = "https://api.tiingo.com/tiingo/news"
        headers = {
            'Content-Type': 'application/json'
        }
        
        params = {
            'token': TIINGO_API_KEY,
            'limit': limit,
            'sortBy': 'publishedDate'
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            news_data = response.json()
            
            # Process and format the news data
            formatted_news = []
            for article in news_data:
                formatted_article = {
                    'title': article.get('title', 'No title'),
                    'description': article.get('description', 'No description'),
                    'url': article.get('url', '#'),
                    'publishedDate': article.get('publishedDate', ''),
                    'source': article.get('source', 'Unknown'),
                    'tags': article.get('tags', []),
                    'tickers': article.get('tickers', []),
                    'is_general': True
                }
                formatted_news.append(formatted_article)
            
            return formatted_news[:limit]
        return []
    except Exception as e:
        return []

def get_intraday_data(ticker):
    """Fetch intraday data from Tiingo API"""
    try:
        url = f"https://api.tiingo.com/iex/{ticker}/prices"
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'token': TIINGO_API_KEY,
            'resampleFreq': '1hour',
            'format': 'json'
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []

def calculate_price_stats(history_data):
    """Calculate high, low, and other stats from history data"""
    if not history_data:
        return {}
    
    prices = [float(day['close']) for day in history_data]
    highs = [float(day['high']) for day in history_data]
    lows = [float(day['low']) for day in history_data]
    
    return {
        'day_high': max(highs[-1:]) if highs else 0,
        'day_low': min(lows[-1:]) if lows else 0,
        'week_high': max(highs[-7:]) if len(highs) >= 7 else max(highs) if highs else 0,
        'week_low': min(lows[-7:]) if len(lows) >= 7 else min(lows) if lows else 0,
        'month_high': max(highs[-30:]) if len(highs) >= 30 else max(highs) if highs else 0,
        'month_low': min(lows[-30:]) if len(lows) >= 30 else min(lows) if lows else 0,
        'year_high': max(highs[-252:]) if len(highs) >= 252 else max(highs) if highs else 0,
        'year_low': min(lows[-252:]) if len(lows) >= 252 else min(lows) if lows else 0,
    }

def get_stock_metadata(ticker):
    """Fetch stock metadata from Tiingo API"""
    try:
        url = f"{TIINGO_BASE_URL}/daily/{ticker}"
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'token': TIINGO_API_KEY
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

def search_tiingo_stocks(query):
    """Search for stocks using Tiingo's search functionality"""
    try:
        url = f"https://api.tiingo.com/tiingo/utilities/search"
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'token': TIINGO_API_KEY,
            'query': query,
            'isExactMatch': 'false'
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []

def create_or_update_stock(ticker_data, price_data=None):
    """Create or update stock in database with Tiingo data"""
    try:
        ticker = ticker_data.get('ticker', '').upper()
        if not ticker:
            return None
            
        # Get or create stock
        stock, created = Stock.objects.get_or_create(
            ticker=ticker,
            defaults={
                'name': ticker_data.get('name', ticker),
                'description': ticker_data.get('description', ''),
                'exchange': ticker_data.get('exchangeCode', ''),
                'currency': 'USD'
            }
        )
        
        # Update with latest price data if available
        if price_data:
            stock.current_price = Decimal(str(price_data.get('close', 0)))
            stock.save()
            
        return stock
    except Exception as e:
        return None

def home(request):
    """Home page view"""
    popular_stocks = Stock.objects.all()[:10]
    return render(request, 'crud/home.html', {'popular_stocks': popular_stocks})

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'crud/register.html', {'form': form})

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'crud/login.html', {'form': form})

@login_required
def dashboard(request):
    """User dashboard view"""
    user_stocks = UserStock.objects.filter(user=request.user, transaction_type='BUY')
    portfolio_value = sum([stock.current_value for stock in user_stocks])
    watchlist = Watchlist.objects.filter(user=request.user)
    
    context = {
        'user_stocks': user_stocks,
        'portfolio_value': portfolio_value,
        'watchlist': watchlist,
        'balance': request.user.balance
    }
    return render(request, 'crud/dashboard.html', context)

@login_required
def stock_detail(request, ticker):
    """Enhanced stock detail view with history, charts, and news"""
    # Try to get stock from database first
    try:
        stock = Stock.objects.get(ticker=ticker.upper())
    except Stock.DoesNotExist:
        # If not in database, fetch from Tiingo API
        metadata = get_stock_metadata(ticker)
        if metadata:
            stock = create_or_update_stock(metadata)
            if not stock:
                messages.error(request, f'Stock {ticker} not found.')
                return redirect('search_stocks')
        else:
            messages.error(request, f'Stock {ticker} not found.')
            return redirect('search_stocks')
    
    # Get current stock data
    current_data = get_stock_data(ticker)
    if current_data:
        stock.current_price = Decimal(str(current_data.get('close', 0)))
        stock.save()
    
    # Get historical data for different periods
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Get 1 year of historical data
    start_date_1y = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    history_1y = get_stock_history(ticker, start_date_1y, end_date)
    
    # Get 1 month of historical data
    start_date_1m = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    history_1m = get_stock_history(ticker, start_date_1m, end_date)
    
    # Get 1 week of historical data
    start_date_1w = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    history_1w = get_stock_history(ticker, start_date_1w, end_date)
    
    # Calculate price statistics
    price_stats = calculate_price_stats(history_1y)
    
    # Get intraday data for today's chart
    intraday_data = get_intraday_data(ticker)
    
    # Get news - try specific stock news first, then general market news
    news = get_stock_news(ticker, 10)
    
    # If no specific stock news found, get general market news
    if not news:
        news = get_general_market_news(5)
    
    # Check if user owns this stock
    user_holdings = UserStock.objects.filter(user=request.user, stock=stock, transaction_type='BUY')
    total_shares = sum([holding.quantity for holding in user_holdings])
    
    # Calculate total value
    total_value = Decimal('0.00')
    if stock.current_price and total_shares > 0:
        total_value = stock.current_price * total_shares
    
    # Check if in watchlist
    in_watchlist = Watchlist.objects.filter(user=request.user, stock=stock).exists()
    
    context = {
        'stock': stock,
        'current_data': current_data,
        'history_1y': json.dumps(history_1y),
        'history_1m': json.dumps(history_1m),
        'history_1w': json.dumps(history_1w),
        'intraday_data': json.dumps(intraday_data),
        'price_stats': price_stats,
        'news': news,
        'user_holdings': user_holdings,
        'total_shares': total_shares,
        'total_value': total_value,
        'in_watchlist': in_watchlist
    }
    return render(request, 'crud/stock_detail.html', context)

@login_required
def buy_stock(request, ticker):
    """Buy stock view"""
    # Try to get stock from database first
    try:
        stock = Stock.objects.get(ticker=ticker.upper())
    except Stock.DoesNotExist:
        # If not in database, fetch from Tiingo API
        metadata = get_stock_metadata(ticker)
        if metadata:
            stock = create_or_update_stock(metadata)
            if not stock:
                messages.error(request, f'Stock {ticker} not found.')
                return redirect('search_stocks')
        else:
            messages.error(request, f'Stock {ticker} not found.')
            return redirect('search_stocks')
    
    # Update stock price
    stock_data = get_stock_data(ticker)
    if stock_data:
        stock.current_price = Decimal(str(stock_data.get('close', 0)))
        stock.save()
    
    if not stock.current_price:
        messages.error(request, f'Unable to get current price for {ticker}.')
        return redirect('search_stocks')
    
    if request.method == 'POST':
        form = StockPurchaseForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            total_cost = quantity * stock.current_price
            
            if request.user.balance >= total_cost:
                # Create transaction
                UserStock.objects.create(
                    user=request.user,
                    stock=stock,
                    transaction_type='BUY',
                    quantity=quantity,
                    buy_price=stock.current_price
                )
                
                # Update user balance
                request.user.balance -= total_cost
                request.user.save()
                
                messages.success(request, f'Successfully bought {quantity} shares of {stock.ticker}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Insufficient balance!')
    else:
        form = StockPurchaseForm()
    
    return render(request, 'crud/buy_stock.html', {'stock': stock, 'form': form})

@login_required
def search_stocks(request):
    """Search stocks view with Tiingo API integration"""
    query = request.GET.get('q', '').strip()
    stocks = []
    
    if query:
        # First search in local database
        local_stocks = Stock.objects.filter(ticker__icontains=query)[:5]
        stocks.extend(local_stocks)
        
        # If not many results from local DB, search Tiingo API
        if len(stocks) < 3:
            tiingo_results = search_tiingo_stocks(query)
            
            for result in tiingo_results[:10]:  # Limit to 10 results
                ticker = result.get('ticker', '').upper()
                if ticker and not any(s.ticker == ticker for s in stocks):
                    # Get current price for the stock
                    price_data = get_stock_data(ticker)
                    stock = create_or_update_stock(result, price_data)
                    if stock:
                        stocks.append(stock)
    
    # Popular tickers for suggestions
    popular_tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX', 'AMD', 'INTC']
    
    return render(request, 'crud/search_stocks.html', {
        'stocks': stocks,
        'query': query,
        'popular_tickers': popular_tickers
    })

@login_required
def add_to_watchlist(request, ticker):
    """Add stock to watchlist"""
    # Try to get stock from database first
    try:
        stock = Stock.objects.get(ticker=ticker.upper())
    except Stock.DoesNotExist:
        # If not in database, fetch from Tiingo API
        metadata = get_stock_metadata(ticker)
        if metadata:
            stock = create_or_update_stock(metadata)
            if not stock:
                messages.error(request, f'Stock {ticker} not found.')
                return redirect('search_stocks')
        else:
            messages.error(request, f'Stock {ticker} not found.')
            return redirect('search_stocks')
    
    watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, stock=stock)
    
    if created:
        messages.success(request, f'{stock.ticker} added to watchlist!')
    else:
        messages.info(request, f'{stock.ticker} is already in your watchlist!')
    
    return redirect('stock_detail', ticker=ticker)

@login_required
def portfolio(request):
    """Portfolio view"""
    user_stocks = UserStock.objects.filter(user=request.user, transaction_type='BUY')
    total_value = sum([stock.current_value for stock in user_stocks])
    total_investment = sum([stock.total_investment for stock in user_stocks])
    total_profit_loss = total_value - total_investment
    
    context = {
        'user_stocks': user_stocks,
        'total_value': total_value,
        'total_investment': total_investment,
        'total_profit_loss': total_profit_loss
    }
    return render(request, 'crud/portfolio.html', context)