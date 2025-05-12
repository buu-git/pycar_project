from rest_framework.serializers import ModelSerializer
from cars.models import Rezerwacja, Car

class RezerwacjaSerializer(ModelSerializer):
    class Meta:
        model = Rezerwacja
        fields = ["id", "user", "cars", "date_start", "date_end"]


class CarsSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "name", "description", "color", "size", "car_type"]