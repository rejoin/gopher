from django.db import models
from django import forms
from django.contrib.auth.models import User


class Movie(models.Model):
    imdbid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    genre = models.CharField(max_length=100)
    rating = models.FloatField()
    plot = models.TextField()
    plot_outline = models.TextField()
    cert = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    country = models.CharField(max_length=200)
    year = models.IntegerField()
    image = models.CharField(max_length=100)
    
    def __str__(self):
         return self.title

class Room(models.Model):
    room_no = models.IntegerField(primary_key=True)
    
    def __str__(self):
        return str(self.room_no)

class Seat(models.Model):
    seat_no = models.IntegerField()
    room_no = models.ForeignKey(Room, to_field="room_no")
    type_multiplier = models.FloatField()
    
    def __str__(self):
         return "Room " + str(self.room_no) + ", Seat " + str(self.seat_no)
    
    def getSeatNo(self):
        return self.seat_no

    def rowAndSeat(self):
        row_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        return "Row " + row_letters[self.seat_no // 10] + " Seat " + str(self.seat_no % 10)

    class Meta:
        unique_together = ("room_no", "seat_no")

class Show(models.Model):
    movie = models.ForeignKey(Movie)
    date_time = models.DateTimeField()
    room_no = models.ForeignKey(Room, to_field="room_no")

    class Meta:
        unique_together = (("room_no", "date_time", "movie"),)
        
    def __str__(self):
        return str(self.date_time) + " | " + str(self.room_no) + " | " + str(self.movie)

class Booking(models.Model):
    # TODO change to seat
    seat_no = models.ForeignKey(Seat)
    show = models.ForeignKey(Show)

    def __str__(self):
        return str(self.show) + " | " + str(self.seat_no)

    class Meta:
        unique_together = (("show", "seat_no"),)

class Ticket_Type(models.Model):
    name = models.CharField(max_length=3, primary_key=True)    
    price = models.FloatField()
    
    def __str__(self):
        return str(self.name) + " " + str(self.price)

class Customer(models.Model):
    username = models.OneToOneField(User)
    full_name = models.CharField(max_length=100)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    card_type = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    card_name = models.CharField(max_length=50)
    card_expiry = models.CharField(max_length=4)

    def __str__(self):
        return str(self.username)
    
class Receipt(models.Model):
    title = models.ForeignKey(Movie, to_field="title")
    booking = models.ForeignKey(Booking)
    price_paid = models.FloatField()
    username = models.ForeignKey(Customer)
    card_number = models.CharField(max_length=16)

    def __str__(self):
        return str(self.id)
        
class Comingsoon(models.Model):
    imdbid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    cert = models.CharField(max_length=100)
    year = models.DateTimeField()
    plot_outline = models.TextField()
    image = models.CharField(max_length=400)
    genre = models.CharField(max_length=100)
