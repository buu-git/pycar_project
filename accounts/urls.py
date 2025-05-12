from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views

app_name = 'accounts'

urlpatterns = [
    path("cars/", views.carlist, name="car_list"),
    path("register/", views.register, name="register"),
    path("", views.start_view, name="main_site"),
    path("contact/", views.contact_view, name="contact"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),


    # 🔽 Upewnij się, że to wygląda dokładnie tak:
    path("logout/", auth_views.LogoutView.as_view(
        next_page=reverse_lazy('accounts:main_site')
    ), name="logout"),
]
