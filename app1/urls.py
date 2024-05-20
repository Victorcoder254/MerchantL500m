from django.urls import path
from .views import *


urlpatterns = [
    path("", index, name="index"),
    path("login/", user_login, name="login_user"),
    path("register/", register, name="register"),
    path("logout/", logout_user, name="logout"),
    path("bupro/", businessProfile, name="businessProfile"),
    path("forgot-pass/", forgot_password, name="forgot_password"),
    path("payment_channel/", payment_channel, name="payment_channel"),
    path("payments_remmitted/", payments_remmitted, name="payments_remmitted"),
    path(
        "make_liquidation_request/",
        make_liquidation_request,
        name="make_liquidation_request",
    ),
    path("liquidation_feedback/", liquidation_feedback, name="liquidation_feedback"),
    path(
        "blame_liquidation_feedback/<int:pk>/",
        blame_liquidation_feedback,
        name="blame_liquidation_feedback",
    ),
    path(
        "payment_channel/delete/<int:pk>/",
        delete_payment_channel,
        name="delete_payment_channel",
    ),
]
