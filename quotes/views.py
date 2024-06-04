from django.shortcuts import render, redirect
import requests
import json
from .models import Stock
from django.contrib import messages
from .forms import StockForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

def home(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_url = f'https://api.iex.cloud/v1/data/core/quote/{ticker}?token=pk_586d99bbdc9841178155bffbaf5769eb'
        try:
            response = requests.get(api_url)
            api = json.loads(response.content)[0]
            if api:
                pass
            else:
                api = "Error..."
        except Exception as e:
            print(e)
            api = "Error..."
        return render(request, "home.html", {'api': api})

    else:
        return render(request, "home.html", {'ticker': "Enter a Ticker Symbol Above..."})

    # pk_586d99bbdc9841178155bffbaf5769eb

def about(request):
    return render(request, 'about.html', {})

@login_required
def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added"))
            return redirect('add_stock')
    else:
        tickers = Stock.objects.all()
        output = []

        for ticker in tickers:
            api_url = f'https://api.iex.cloud/v1/data/core/quote/{str(ticker)}?token=pk_586d99bbdc9841178155bffbaf5769eb'
            try:
                response = requests.get(api_url)
                api = json.loads(response.content)[0]
                output.append(api)
                if api:
                    pass
                else:
                    api = "Error..."
            except Exception as e:
                api = "Error..."

        return render(request, 'add_stock.html', {'ticker': tickers, 'output': output})

@login_required
def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock Has Been Deleted!"))
    return redirect(delete_stock)

@login_required
def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Send email
        send_mail(
            f'Message from {name} via Contact Form',
            message,
            email,
            ['your_email@example.com'],
        )

        messages.success(request, 'Your message has been sent!')
        return render(request, 'contact.html')

    return render(request, 'contact.html')