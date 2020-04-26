# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from universal_gopher.models import *
from django import template
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction


def index(request):
    films = Movie.objects.all()[:3]
    last_films = Movie.objects.all()[3:6]
    more_films = Movie.objects.all()[6:9]
    return render(request, 'index.html', {'films':films, 'last_films':last_films,    'more_films':more_films})
    
def films(request):
    if request.method == 'GET' and 'sortby' in request.GET:
       sortby = request.GET['sortby']
    else:
       sortby = "title"

    col = ['A-Z', 'Z-A', 'rating', 'cert', 'year']
  
    if sortby == 'year' or sortby == 'rating' or sortby == 'Z-A':
        if sortby == "Z-A":
            sortby = "title"
        reverse='-'+sortby
        queryset = Movie.objects.all().order_by(reverse)
        return render(request, 'films.html', {'queryset':queryset ,'sortby':sortby, 'col':col})
    else:
        if sortby == "A-Z":
            sortby = "title"
        queryset = Movie.objects.all().order_by(sortby)
        return render(request, 'films.html', {'queryset':queryset , 'sortby':sortby, "col":col})   
    
    

    
    
def film(request):
    if request.method == 'GET' and 'imdbid'in request.GET:
        imdbid = request.GET['imdbid']
        film = Movie.objects.get(imdbid=imdbid)
        shows = Show.objects.filter(movie=film)
        split_show = zip(shows)
        show = list(split_show)
        return render(request, 'film.html', {'film':film, 'shows':shows})
        
    else:
        return render(request, '404.html')  
    

def register(request):
    return render(request, 'register.html')

    
def coming_soon(request):
    queryset = Comingsoon.objects.all()
    return render(request, 'comingsoon.html', {'queryset':queryset})   
  

    
def about(request):
    return render(request, 'about.html')

def price(request):
    return render(request, 'price.html')

def tickets(request):
    if request.method == 'GET' and 'show_id'in request.GET:
        show_id = request.GET['show_id']
        # Add show's id to the session
        request.session['show_id'] = show_id
        show = Show.objects.get(id=show_id)
        movie = show.movie
        
    else:
        return render(request, '404.html')    
    return render(request, 'tickets.html', {'show_id':show_id, 'movie':movie,'room': show.room_no, 'current_path': request.path})
    
def seating(request):
    if request.method == 'POST':
        show_id = request.session['show_id']
        show = Show.objects.get(id=show_id)
        movie = show.movie
        
        items = dict(request.POST.items())
        # Filter to only get standard seats
        sseats = dict((k, v) for k, v in items.items() if (k[-1] == 's' and k != 'csrfmiddlewaretoken'))
        stotal = 0 
        for item in list(sseats.values()):
            stotal += int(item[0])
        
        # Filter to select only VIP seats
        vseats = dict((k, v) for k, v in items.items() if (k[-1] == 'v' and k != 'csrfmiddlewaretoken'))
        vtotal = 0
        for item in list(vseats.values()):
            vtotal += int(item[0])
        
        # Get all booked seats for price calculations
        price_dict = dict((k, v) for k, v in items.items() if (k != 'csrfmiddlewaretoken'))
        price_to_pay = 0
        for k, v in price_dict.items():
            item = Ticket_Type.objects.get(name=k)
            if int(v) > 0:
                  price_to_pay += int(item.price)*int(v)

        # Total number of tickets
        request.session['tickets'] = vtotal+stotal
        request.session['price'] = price_to_pay

        # A list used to mark all taken seats
        bookings = Booking.objects.filter(show=show)
        taken_seats = []
        for booking in bookings:
            taken_seats.append(booking.seat_no.getSeatNo())

        # A list that generates all seats for a room
        seats = Seat.objects.filter(room_no=show.room_no)
        seats = list(map(lambda x: x.getSeatNo(), seats))
    else:
        return render(request, '404.html')    
    return render(request, 'seating.html', {'seats':seats, 'taken_seats':taken_seats, 'room': show.room_no, 
                    'movie':movie, 'current_path': request.path, 'ss':stotal, 'vs':vtotal, 'price':price_to_pay})
    
def payment(request):
    if request.method == 'POST':
        show = Show.objects.get(id=request.session['show_id'])
        movie = Show.objects.get(id=request.session['show_id']).movie

        items = dict(request.POST.items())
        # Remove the csrf token and convert the request to a list
        seats = [ k for k, v in items.items() if (k != "csrfmiddlewaretoken") ]
        # Convert seats from strings to integers
        seats = list(map(lambda x: int(x), seats))
        request.session['seats'] = seats
        price = request.session['price']

        seat_list = []
        row_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for seat_no in seats:
            row_seat = "Row " + row_letters[seat_no // 10] + " Seat " + str(seat_no % 10)
            seat_list.append(row_seat)
        seat_list.sort()

    return render(request, 'payment.html', {'seats':seat_list, 'movie':movie, 'room': show.room_no, 'current_path': request.path, 'price':price})

@transaction.atomic
def receipt(request):
    if request.method == 'POST' and request.session['show_id'] and request.session['seats']:
        items = dict(request.POST.items())
        
        show_id = request.session['show_id']
        seats = request.session['seats']
        tick = request.session['tickets']
        price = request.session['price']

        name = request.POST['Fname']
        email = request.POST.get('emailReceipt', False)

        show = Show.objects.get(id=show_id)
        guest = Customer.objects.get(id=1)

        display_card_number = "**** **** **** " + items['cardNo'][-4:]

        # Write bookings and receipts into a database
        for seat in seats:
            current_seat = Seat.objects.get(room_no=show.room_no, seat_no=seat)
            booking = Booking(seat_no=current_seat, show=show)
            booking.save()
            receipt = Receipt(title=show.movie, booking=booking, 
                      price_paid=price, username=guest, card_number=items['cardNo'])
            receipt.save()

        # Email formation for customer receipt
        email_string = "Dear, customer\n"
        email_string += "Your order details are: \n"
        email_string += "Order Number: " + str(booking.id) + "\n"
        email_string += "Movie title: " + str(show.movie) + "\n"
        email_string += "Time of showing: " + str(show.date_time) + "\n"
        email_string += "Number of tickets: " + str(tick) + "\n"
        email_string += "Room: " + str(show.room_no) + "\n"
        if len(seats) > 1:
            email_string += "Seats: " 
        else:
            email_string += "Seat: "
        for seat in seats:
            current_seat = Seat.objects.get(room_no=show.room_no, seat_no=seat)
            email_string += current_seat.rowAndSeat() + "; "
        email_string += "\n"
        email_string += "Total price: GBP" + str(price) + "\n"
        email_string += "Enjoy your visit at Gopher Films!"
        
        # Send an email if customer desires
        if email:    
            send_mail('Your Gopher Films Receipt', email_string, 'gopher@inbox.com',
             [email], fail_silently=True)

    else:
        return render(request, '404.html')  
    return render(request, 'receipt.html', {'items':items, 'show':show, 'tick':tick, 'card_no':display_card_number , 'price':price, 'name':name, 'order':booking.id})
    
def login(request):
    if request.method == 'POST' and 'username' in request.POST and 'password' in request.POST:
        
        # Correct password, and the user is marked "active"
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.create_user(username=username, password=password)
            user.save()
            # Redirect to a success page.
            return redirect("index.html")
    else:
       user = None
  
       
    return render(request, 'index.html', {'user':user})
    

def logout(request):
    auth.logout(request)
    return render(request, request.path)
