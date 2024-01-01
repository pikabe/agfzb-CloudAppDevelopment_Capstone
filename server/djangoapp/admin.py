from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel, CarDealer, DealerReview


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

# CarModelAdmin class
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', )  # Add other fields you want to display in the list view
    search_fields = ['name', 'description']
    inlines = [CarModelInline]

# CarMakeAdmin class with CarModelInline
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'dealer_id', 'car_type', 'year')  # Add other fields you want to display in the list view
    list_filter = ['car_make', 'car_type', 'year']
    search_fields = ['name', 'car_make__name']
    autocomplete_fields = ['car_make']  # Enables a dropdown for selecting the car make

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)


@admin.register(CarDealer)
class CarDealerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'city', 'st', 'zip')
    search_fields = ('full_name', 'city', 'st', 'zip')

@admin.register(DealerReview)
class DealerReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'dealership', 'purchase', 'sentiment', 'purchase_date')
    search_fields = ('name', 'dealership', 'car_make', 'car_model', 'purchase_date')
    list_filter = ('purchase', 'sentiment')







