from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Add any other fields you'd like for a car make

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()  # Refers to a dealer created in Cloudant database
    name = models.CharField(max_length=100)
    TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    car_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    year = models.DateField()

    def __str__(self):
        return f"{self.car_make.name} - {self.name}"


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
# class CarDealer:
#     def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
#         # Dealer address
#         self.address = address
#         # Dealer city
#         self.city = city
#         # Dealer Full Name
#         self.full_name = full_name
#         # Dealer id
#         self.id = id
#         # Location lat
#         self.lat = lat
#         # Location long
#         self.long = long
#         # Dealer short name
#         self.short_name = short_name
#         # Dealer state
#         self.st = st
#         # Dealer zip
#         self.zip = zip
#     def __str__(self):
#         return "Dealer name: " + self.full_name

class CarDealer(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)
    lat = models.FloatField()
    long = models.FloatField()
    short_name = models.CharField(max_length=255)
    st = models.CharField(max_length=255)
    zip = models.CharField(max_length=20)

    def __str__(self):
        return "Dealer name: " + self.full_name
    
# <HINT> Create a plain Python class `DealerReview` to hold review data
# class DealerReview(models.Model):
#     dealership = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     purchase = models.BooleanField()
#     review = models.TextField()
#     purchase_date = models.DateField()
#     car_make = models.CharField(max_length=255)
#     car_model = models.CharField(max_length=255)
#     car_year = models.IntegerField()
#     sentiment = models.CharField(max_length=255)
#     id = models.AutoField(primary_key=True)
#     def __str__(self):
#         return self.review
    
class DealerReview(models.Model):
    dealership = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    purchase = models.BooleanField()
    review = models.TextField()
    purchase_date = models.DateField()
    car_make = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    car_year = models.IntegerField()
    
    SENTIMENT_CHOICES = [
        ('POSITIVE', 'Positive'),
        ('NEUTRAL', 'Neutral'),
        ('NEGATIVE', 'Negative'),
    ]
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES)
    
    def __str__(self):
        return self.review
