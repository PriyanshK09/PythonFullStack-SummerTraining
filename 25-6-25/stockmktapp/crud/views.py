from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, F
from django.db import transaction  # Add this import
from .models import User, Stock, UserStock, Watchlist, StockPriceHistory
from .forms import UserRegistrationForm, UserLoginForm, StockPurchaseForm, StockSellForm
from .utils import (
    get_tiingo_api_key, get_stock_metadata, get_stock_data, 
    get_stock_history, get_intraday_data, get_stock_news, 
    get_general_market_news, create_or_update_stock, send_transaction_receipt,
    search_tiingo_stocks, calculate_price_stats
)
import requests
import json
from decimal import Decimal
from django.conf import settings
from datetime import datetime, timedelta
import pytz

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
                transaction = UserStock.objects.create(
                    user=request.user,
                    stock=stock,
                    transaction_type='BUY',
                    quantity=quantity,
                    buy_price=stock.current_price
                )
                
                # Update user balance
                request.user.balance -= total_cost
                request.user.save()
                
                # Send email receipt
                if request.user.email:
                    send_transaction_receipt(request.user, transaction)
                
                messages.success(request, f'Successfully bought {quantity} shares of {stock.ticker}! A receipt has been sent to your email.')
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

@login_required
def add_money(request):
    """Add money to user's wallet"""
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            if amount > 0:
                request.user.balance += amount
                request.user.save()
                messages.success(request, f'Successfully added ${amount:.2f} to your wallet!')
                return redirect('wallet')
            else:
                messages.error(request, 'Please enter a valid amount.')
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid amount.')
    
    return render(request, 'crud/add_money.html')

@login_required
def wallet(request):
    """Display wallet/balance information"""
    context = {
        'current_balance': request.user.balance,
        'recent_transactions': []  # You can add transaction history here later
    }
    return render(request, 'crud/wallet.html', context)

@login_required
def sell_stock(request, ticker):
    """Sell stock view"""
    try:
        stock = Stock.objects.get(ticker=ticker.upper())
    except Stock.DoesNotExist:
        messages.error(request, f'Stock {ticker} not found.')
        return redirect('portfolio')
    
    # Get user's holdings for this stock
    user_holdings = UserStock.objects.filter(
        user=request.user, 
        stock=stock, 
        transaction_type='BUY'
    )
    
    total_shares = sum([holding.quantity for holding in user_holdings])
    
    if total_shares == 0:
        messages.error(request, f'You do not own any shares of {ticker}.')
        return redirect('portfolio')
    
    # Update stock price
    stock_data = get_stock_data(ticker)
    if stock_data:
        stock.current_price = Decimal(str(stock_data.get('close', 0)))
        stock.save()
    
    if not stock.current_price:
        messages.error(request, f'Unable to get current price for {ticker}.')
        return redirect('portfolio')
    
    if request.method == 'POST':
        form = StockSellForm(request.POST)
        if form.is_valid():
            quantity_to_sell = form.cleaned_data['quantity']
            
            if quantity_to_sell > total_shares:
                messages.error(request, f'You only own {total_shares} shares of {ticker}.')
            else:
                # Calculate sale amount
                sale_amount = quantity_to_sell * stock.current_price
                
                # Create sell transaction
                transaction = UserStock.objects.create(
                    user=request.user,
                    stock=stock,
                    transaction_type='SELL',
                    quantity=quantity_to_sell,
                    buy_price=stock.current_price  # Using current price as sell price
                )
                
                # Update user balance
                request.user.balance += sale_amount
                request.user.save()
                
                # Send email receipt
                if request.user.email:
                    send_transaction_receipt(request.user, transaction)
                
                messages.success(request, f'Successfully sold {quantity_to_sell} shares of {stock.ticker} for ${sale_amount:.2f}! A receipt has been sent to your email.')
                return redirect('portfolio')
    else:
        form = StockSellForm()
    
    return render(request, 'crud/sell_stock.html', {
        'stock': stock, 
        'form': form, 
        'total_shares': total_shares
    })

@login_required
def test_email(request):
    """Test email functionality"""
    from .utils import test_email_configuration
    
    success, message = test_email_configuration()
    
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('dashboard')