from django.contrib import admin

from cars.models import Car, Rezerwacja

# Register your models here.
# tworzenie ModelAdmin jest preferowanym sposobem zarzadania modelem w panelu administratora
class RezerwacjaAdmin(admin.ModelAdmin):
    fields = ["id", "car", "user", "date_start", "date_end"]
    list_display = ["car", "user", "date_start", "date_end", "total_days", "total_price"]
    readonly_fields = ["id"]

class CarAdmin(admin.ModelAdmin):
    class CarAdmin(admin.ModelAdmin):
        fields = ["id", "name", "specification", "car_type", "image", "price"]
        list_display = ["id", "name", "specification", "car_type", "price"]
        readonly_fields = ["id"]

    def price(self, obj):
        return obj.cars.price  # cena za dzień

    def total_price(self, obj):
        return obj.total_days() * obj.cars.price

    def total_days(self, obj):
        return (obj.date_end - obj.date_start).days

admin.site.register(Car, CarAdmin)
admin.site.register(Rezerwacja, RezerwacjaAdmin)