from django.urls import path
from cars.views import CarsListView, CarsDetailView, reserve, my_reservations, delete_reservation
from . import views

urlpatterns = [
    path("<int:pk>/", CarsDetailView.as_view(), name="car_detail"),
    path("<int:car_id>/reserve/", reserve, name="cars_reserve"),
    path('', CarsListView.as_view(), name="car_list"),
    path("my-reservations/", my_reservations, name="my_reservations"),
    path("reservations/delete/<int:reservation_id>/", delete_reservation, name="delete_reservation"),
    path('invoice/<int:reservation_id>/', views.generate_invoice, name='generate_invoice'),
]
