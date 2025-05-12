from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from weasyprint import HTML
from django.utils.timezone import now
import decimal
import tempfile

from cars.filters import CarsFilter
from cars.forms import RezerwacjaForm
from cars.models import Rezerwacja, Car
from cars.serializers import RezerwacjaSerializer, CarsSerializer

from rest_framework.viewsets import ModelViewSet


class CarsListView(FilterView):
    model = Car
    template_name = "car_list.html"
    context_object_name = "object_list"
    filterset_class = CarsFilter

    def get_queryset(self):
        return super().get_queryset()


class CarsDetailView(DetailView):
    model = Car
    template_name = "car_detail.html"
    context_object_name = "car"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        busy_ranges = [
            {"from": r.date_start.isoformat(), "to": r.date_end.isoformat()}
            for r in car.rezerwacje.all()
        ]
        context["form"] = RezerwacjaForm()
        context["busy_ranges"] = busy_ranges
        return context


@login_required
def reserve(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        raise Http404("Car with this ID does not exist.")

    if request.method == "POST":
        form = RezerwacjaForm(request.POST)
        if form.is_valid():
            date_start = form.cleaned_data["date_start"]
            date_end = form.cleaned_data["date_end"]

            if date_start > date_end:
                messages.error(request, "Start date cannot be later than end date.")
            elif car.if_reserved(date_start, date_end):
                messages.error(request, "This car is already reserved for the selected date range.")
            else:
                Rezerwacja.objects.create(
                    car=car,
                    user=request.user,
                    date_start=date_start,
                    date_end=date_end
                )
                messages.success(request, "Reservation successful.")
                return redirect("my_reservations")
        else:
            messages.error(request, "Invalid form data.")

        busy_ranges = [
            {"from": r.date_start.isoformat(), "to": r.date_end.isoformat()}
            for r in car.rezerwacje.all()
        ]
        return render(request, "car_detail.html", {
            "car": car,
            "form": form,
            "busy_ranges": busy_ranges
        })

    return HttpResponseForbidden("Only POST requests are allowed for this endpoint.")


def hello(request):
    return HttpResponse("Reserve your car now!")


class RezerwacjaViewSet(ModelViewSet):
    serializer_class = RezerwacjaSerializer
    queryset = Rezerwacja.objects.all()


class CarsViewSet(ModelViewSet):
    serializer_class = CarsSerializer
    queryset = Car.objects.all()


@login_required
def my_reservations(request):
    reservations = Rezerwacja.objects.filter(user=request.user)
    return render(request, 'my_reservations.html', {'reservations': reservations})


@require_POST
@login_required
def delete_reservation(request, reservation_id):
    try:
        reservation = Rezerwacja.objects.get(id=reservation_id, user=request.user)
        reservation.delete()
        messages.success(request, "Reservation canceled successfully.")
    except Rezerwacja.DoesNotExist:
        messages.error(request, "Reservation not found or access denied.")
    return redirect("my_reservations")


# ✅ FAKTURA PDF — ZAPEWNIENIE DOSTĘPU DO DANYCH SAMOCHODU
@login_required
def generate_invoice(request, reservation_id):
    try:
        reservation = Rezerwacja.objects.select_related('car').get(id=reservation_id, user=request.user)
    except Rezerwacja.DoesNotExist:
        raise Http404("Reservation not found.")

    # Obliczenia
    total_days = reservation.total_days()
    total_price = reservation.total_price()

    price_per_day = decimal.Decimal(total_price) / decimal.Decimal(total_days) if total_days else decimal.Decimal(0)

    vat_rate = decimal.Decimal('0.23')
    net_price = total_price / (1 + vat_rate)
    vat_amount = total_price - net_price

    # Render szablonu
    html_string = render_to_string('invoice_template.html', {
        'reservation': reservation,
        'date': now().strftime('%Y-%m-%d'),
        'total_days': total_days,
        'price_per_day': price_per_day,
        'total_price': total_price,
        'net_price': net_price,
        'vat_amount': vat_amount,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=invoice_{reservation_id}.pdf'

    with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
        HTML(string=html_string).write_pdf(target=tmp_file.name)
        tmp_file.seek(0)
        response.write(tmp_file.read())

    return response

