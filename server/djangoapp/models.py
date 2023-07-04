from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake (models.Model):
    name = models.CharField(null=False, max_length=50)
    description = models.CharField(max_length=1000)
    def __str__(self):
        return "Car make name: " + self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    name = models.CharField(null=False, max_length=50)
    dealer_id = models.IntegerField()
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    CONVERTIBLE = 'convertible'
    MINIVAN = 'minivan'
    SPORTCAR = 'sport_car'
    CARTYPE = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (CONVERTIBLE, 'Convertible'),
        (MINIVAN, 'Minivan'),
        (SPORTCAR,'Sport Car')
    ]
    car_type = models.CharField(
        null=False,
        max_length=25,
        choices=CARTYPE,
        default=SEDAN
    )
    year = models.DateField(null=True)
    def __str__(self):
        return "Car Model name: " + self.name
# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        self.state = state
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name



# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, car_make, car_model, car_year, dealership, name, purchase, purchase_date, review, sentiment=None):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = sentiment
    def __str__(self):
        return "Review: " + self.review