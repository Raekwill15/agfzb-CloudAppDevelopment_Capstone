from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=30,) 
    description = models.CharField(max_length=255)

    def __str__(self):
        return f'Name: {self.name}'


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    CAR_TYPE = [
        ("Sedan" , "Sedan"),
        ("SUV" , "SUV"),
        ("Wagon", "Wagon"),
        ("Minivan", "Minivan"),
        ("Coupe" , "Coupe"),
        ("Sports Car" , "Sports Car"),
        ("Truck" , "Truck")
    ]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    dealer_id = models.IntegerField()
    car_type = models.CharField(max_length=10, choices=CAR_TYPE)
    year = models.DateField()

    def __str__(self):
        return f'Name: {self.name} Car Type: {self.car_type} Year: {self.year}'

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, id, dealer_id, city, state, st, address, zip,lat,long,short_name,full_name):
        # Dealer db_id
        self.id = id
        # Dealer id
        self.dealer_id = dealer_id
        # Dealer city
        self.city = city
        # Dealer state
        self.state = state
        # Location st
        self.st = st
        # Dealer address
        self.address = address
        # Dealer zip
        self.zip = zip
        # Dealer lat
        self.lat = lat
        # Dealer long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer full name
        self.full_name = full_name


    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, id, purchase_date='none', car_make='none', car_model='none', car_year='none', sentiment='none'):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year  
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return f"Dealership: {self.dealership}, Review: {self.review}, Sentiment: {self.sentiment}" 
