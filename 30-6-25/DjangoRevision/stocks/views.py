from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_http_methods
from .models import Stocks, Holding, Transaction, UserProfile
from django.db import transaction as db_transaction
from django.db import models

# # Create your views here.
import requests

from .models import Stocks
from .forms import CustomUserCreationForm

@login_required
def index(request) :
    return render(request ,  'index.html')



def getData(request) :
    nasdaq_tickers = [
        "AAPL",  # Apple Inc.
        "MSFT",  # Microsoft Corporation
        "GOOGL",  # Alphabet Inc. (Class A)
        "GOOG",  # Alphabet Inc. (Class C)
        "AMZN",  # Amazon.com Inc.
        "META",  # Meta Platforms Inc.
        "NVDA",  # NVIDIA Corporation
        "TSLA",  # Tesla Inc.
        "PEP",  # PepsiCo Inc.
        "INTC",  # Intel Corporation
        "CSCO",  # Cisco Systems Inc.
        "ADBE",  # Adobe Inc.
        "CMCSA",  # Comcast Corporation
        "AVGO",  # Broadcom Inc.
        "COST",  # Costco Wholesale Corporation
        "TMUS",  # T-Mobile US Inc.
        "TXN",  # Texas Instruments Inc.
        "AMGN",  # Amgen Inc.
        "QCOM",  # Qualcomm Incorporated
        "INTU",  # Intuit Inc.
        "PYPL",  # PayPal Holdings Inc.
        "BKNG",  # Booking Holdings Inc.
        "GILD",  # Gilead Sciences Inc.
        "SBUX",  # Starbucks Corporation
        "MU",  # Micron Technology Inc.
        "ADP",  # Automatic Data Processing Inc.
        "MDLZ",  # Mondelez International Inc.
        "ISRG",  # Intuitive Surgical Inc.
        "ADI",  # Analog Devices Inc.
        "MAR",  # Marriott International Inc.
        "LRCX",  # Lam Research Corporation
        "REGN",  # Regeneron Pharmaceuticals Inc.
        "ATVI",  # Activision Blizzard Inc.
        "ILMN",  # Illumina Inc.
        "WDAY",  # Workday Inc.
        "SNPS",  # Synopsys Inc.
        "ASML",  # ASML Holding N.V.
        "EBAY",  # eBay Inc.
        "ROST",  # Ross Stores Inc.
        "CTAS",  # Cintas Corporation
        "BIIB",  # Biogen Inc.
        "MELI",  # MercadoLibre Inc.
        "ORLY",  # O'Reilly Automotive Inc.
        "VRTX",  # Vertex Pharmaceuticals Inc.
        "DLTR",  # Dollar Tree Inc.
        "KHC",  # The Kraft Heinz Company
        "EXC",  # Exelon Corporation
        "FAST",  # Fastenal Company
        "JD",  # JD.com Inc.
        "CRWD"  # CrowdStrike Holdings Inc.
    ]

    headers = {
        'Content-Type': 'application/json'
    }
    token  =  "fced443141e501d554d0b38c4a34bba085172b1e"
    def getStock(ticker):
        url  = f"https://api.tiingo.com/tiingo/daily/{ticker}?token={token}"
        priceurl  =  f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?token={token}"
        requestResponse = requests.get(url, headers=headers )
        Metadata  = requestResponse.json()
        print(Metadata)
        priceData  = requests.get(priceurl , headers=headers)
        print(priceData.json())
        priceData =  priceData.json()[0]['close']

        # insert into SQL
        stock = Stocks(ticker  = Metadata['ticker']  , name  =  Metadata['name'] ,  description =  Metadata['description'] , curr_price  = priceData)
        stock.save()

    nasdaq_tickers =  nasdaq_tickers[11:30]
    for i in nasdaq_tickers :
        getStock(i)


    return HttpResponse("Stock Data Downloaded")


@login_required
def stocks(request):
    query = request.GET.get('q', '').strip()
    if query:
        stocks = Stocks.objects.filter(
            models.Q(name__icontains=query) | models.Q(ticker__icontains=query)
        )
    else:
        stocks = Stocks.objects.all()
    context = {'data': stocks}
    return render(request, 'market.html', context)


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def logoutView(request) :
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    holdings = Holding.objects.filter(user=request.user, shares__gt=0).select_related('stock')
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:10]

    portfolio_value = sum(h.shares * h.stock.curr_price for h in holdings)
    total_balance = user_profile.balance + portfolio_value

    context = {
        'username': request.user.username,
        'balance': round(user_profile.balance, 2),
        'portfolio_value': round(portfolio_value, 2),
        'total_balance': round(total_balance, 2),
        'holdings': [
            {
                'ticker': h.stock.ticker,
                'name': h.stock.name,
                'shares': h.shares,
                'value': round(h.shares * h.stock.curr_price, 2)
            } for h in holdings
        ],
        'recent_activity': [
            {
                'action': t.action,
                'ticker': t.stock.ticker,
                'amount': t.amount,
                'price': round(t.price, 2),
                'date': t.date.strftime('%Y-%m-%d %H:%M')
            } for t in transactions
        ]
    }
    return render(request, 'dashboard.html', context)

def index(request):
    if request.user.is_authenticated:
        context = {
            'username': request.user.username,
            'portfolio_value': 15000,
            'holdings': [
                {'ticker': 'AAPL', 'shares': 10, 'value': 2000},
                {'ticker': 'GOOGL', 'shares': 5, 'value': 1500},
            ],
            'recent_activity': [
                {'action': 'Bought', 'ticker': 'AAPL', 'amount': 5, 'date': '2025-07-01'},
                {'action': 'Sold', 'ticker': 'TSLA', 'amount': 2, 'date': '2025-06-30'},
            ]
        }
        return render(request, 'dashboard.html', context)
    else:
        return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
@require_POST
def buy_stock(request):
    ticker = request.POST.get('ticker')
    stock = Stocks.objects.get(ticker=ticker)
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            raise ValueError
    except (ValueError, TypeError):
        messages.error(request, "Please enter a valid quantity.")
        return redirect('stocks')

    total_price = stock.curr_price * quantity

    if user_profile.balance < total_price:
        messages.error(request, "Insufficient balance.")
        return redirect('stocks')

    with db_transaction.atomic():
        holding, _ = Holding.objects.get_or_create(user=request.user, stock=stock)
        holding.shares += quantity
        holding.save()
        user_profile.balance -= total_price
        user_profile.save()
        Transaction.objects.create(
            user=request.user,
            stock=stock,
            action='BUY',
            amount=quantity,
            price=stock.curr_price
        )
    messages.success(request, f"You bought {quantity} share(s) of {ticker}!")
    return redirect('stocks')

@login_required
@require_POST
def sell_stock(request):
    ticker = request.POST.get('ticker')
    stock = Stocks.objects.get(ticker=ticker)
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            raise ValueError
    except (ValueError, TypeError):
        messages.error(request, "Please enter a valid quantity.")
        return redirect('stocks')

    try:
        holding = Holding.objects.get(user=request.user, stock=stock)
    except Holding.DoesNotExist:
        messages.error(request, "You don't own this stock.")
        return redirect('stocks')

    if holding.shares < quantity:
        messages.error(request, "Not enough shares to sell.")
        return redirect('stocks')

    with db_transaction.atomic():
        holding.shares -= quantity
        holding.save()
        user_profile.balance += stock.curr_price * quantity
        user_profile.save()
        Transaction.objects.create(
            user=request.user,
            stock=stock,
            action='SELL',
            amount=quantity,
            price=stock.curr_price
        )
    messages.success(request, f"You sold {quantity} share(s) of {ticker}!")
    return redirect('stocks')

@login_required
@require_http_methods(["GET", "POST"])
def add_balance(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        try:
            amount = float(request.POST.get("amount", 0))
            if amount > 0:
                user_profile.balance += amount
                user_profile.save()
                messages.success(request, f"${amount} added to your balance!")
            else:
                messages.error(request, "Please enter a positive amount.")
        except ValueError:
            messages.error(request, "Invalid amount.")
        return redirect('dashboard')
    return render(request, "add_balance.html", {"balance": user_profile.balance})