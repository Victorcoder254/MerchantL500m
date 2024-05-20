from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import (
    authenticate,
    login as auth_login,
)  # Rename login function here


@login_required
def index(request):
    remitteds = PaymentsRemitted.objects.filter(user=request.user)
    pending_requests = LiquidationRequest.objects.filter(
        user=request.user, status="in_review"
    )
    Info_Messages = InfoMessage.objects.all()[:1]
    business_profile = BusinessProfile.objects.filter(
        user=request.user
    )  # Fetch the business profile queryset

    context = {
        "remitteds": remitteds,
        "pending_requests": pending_requests,
        "Info_Messages": Info_Messages,
        "business_profile": business_profile,  # Add the business profile queryset to the context
    }
    return render(request, "files/index.html", context)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Call the renamed login function

            # Check if the user has a business profile
            if BusinessProfile.objects.filter(user=user).exists():
                messages.success(request, "Login was successful. Welcome Back!!")
                return redirect("index")  # Redirect to index if business profile exists
            else:
                return redirect(
                    "businessProfile"
                )  # Redirect to business profile creation page

        else:
            messages.error(request, "Invalid Credentials 😞")

    return render(request, "files/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            return redirect("login_user")
    return render(request, "files/register.html")


@login_required
def logout_user(request):
    logout(request)
    return redirect("login_user")


def businessProfile(request):
    if request.method == "POST":
        # Retrieve form data
        business_name = request.POST.get("business_name")
        sector = request.POST.get("sector")
        description = request.POST.get("description")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")
        email_company = request.POST.get("email_company")
        business_license_image = request.FILES.get("business_license_image")

        # Check if a BusinessProfile with the same user already exists
        if BusinessProfile.objects.filter(user=request.user).exists():
            return HttpResponse("Business profile already exists")
        else:
            # Create and save the BusinessProfile instance
            business_profile = BusinessProfile.objects.create(
                user=request.user,
                business_name=business_name,
                sector=sector,
                description=description,
                address=address,
                phone_number=phone_number,
                email_company=email_company,
                business_license_image=business_license_image,
            )
            # Redirect to a different page after successful creation
            return redirect("index")  # Replace 'business_profile' with your URL name

    return render(request, "files/businessp.html")


def forgot_password(request):
    if request.method == "POST":
        # Retrieve form data
        Email = request.POST.get("Email")
        # Create and save the BusinessProfile instance

        resetpass = ResetPassword.objects.create(
            user=request.user,
            Email=Email,
        )
        resetpass.save()
        # Redirect to a different page after successful creation
        return redirect("login_user")  # Replace 'business_profile' with your URL name

    return render(request, "files/forgot-password.html")


def payment_channel(request):
    payment_details = PaymentChannel.objects.filter(user=request.user)
    if request.method == "POST":
        # Retrieve form data
        bank_name = request.POST.get("bank_name")
        bank_account_number = request.POST.get("bank_account_number")
        # Fetch BusinessProfile instance for the current user
        business_profile = BusinessProfile.objects.get(user=request.user)
        # Create and save the PaymentChannel instance
        payment_channel = PaymentChannel.objects.create(
            user=request.user,
            business_id=business_profile.business_id,
            bank_name=bank_name,
            bank_account_number=bank_account_number,
        )
        payment_channel.save()
        # Redirect to a different page after successful creation
        return redirect("payment_channel")  # Replace 'index' with your URL name
    return render(
        request, "files/payment_channel.html", {"payment_details": payment_details}
    )


def delete_payment_channel(request, pk):
    # Retrieve the payment channel object
    payment_channel = get_object_or_404(PaymentChannel, pk=pk)
    # Check if the user has permission to delete the payment channel
    if request.user == payment_channel.user:
        # Delete the payment channel
        payment_channel.delete()
    # Redirect to a different page after deletion
    return redirect("payment_channel")  #


def payments_remmitted(request):
    payments_remmitteds = PaymentsRemitted.objects.filter(user=request.user).order_by(
        "-date_created"
    )
    context = {"payments_remmitteds": payments_remmitteds}
    return render(request, "files/payments_remmitted.html", context)


def make_liquidation_request(request):
    liquidation_requests = LiquidationRequest.objects.filter(
        user=request.user, status="in_review"
    )
    processed_liquidation_requests = LiquidationRequest.objects.filter(
        user=request.user, status="processed"
    )[:3]
    condition_choices = LiquidationRequest.CONDITION_CHOICES  # Get condition choices

    if request.method == "POST":
        # Retrieve form data
        reason_for_liquidation = request.POST.get("reason_for_liquidation")
        estimated_value_of_goods = request.POST.get("estimated_value_of_goods")
        anticipated_amount = request.POST.get("anticipated_amount")
        goods_name = request.POST.get("goods_name")
        quantity_goods = request.POST.get("quantity_goods")
        condition_of_goods = request.POST.get("condition_of_goods")

        # Fetch BusinessProfile instance for the current user
        business_profile = BusinessProfile.objects.get(user=request.user)
        # Create and save the LiquidationRequest instance
        liquidation_request = LiquidationRequest.objects.create(
            user=request.user,
            business_id=business_profile.business_id,
            reason_for_liquidation=reason_for_liquidation,
            estimated_value_of_goods=estimated_value_of_goods,
            anticipated_amount=anticipated_amount,
            goods_name=goods_name,
            quantity_goods=quantity_goods,
            condition_of_goods=condition_of_goods,
        )
        # Add success message
        messages.success(
            request,
            "Liquidation request submitted successfully. We will get back to you soon. Check your Email!! and the feedback page",
        )
        # Redirect to a different page after successful creation
        return redirect(
            "make_liquidation_request"
        )  # Replace 'make_liquidation_request' with your URL name
    return render(
        request,
        "files/make_liquidation_request.html",
        {
            "liquidation_requests": liquidation_requests,
            "processed_liquidation_requests": processed_liquidation_requests,
            "condition_choices": condition_choices,  # Pass condition choices to the template
        },
    )


def liquidation_feedback(request):
    liquidation_feedbacks = LiquidationRequestFeedback.objects.filter(
        user=request.user
    ).order_by("-date_created")
    context = {"liquidation_feedbacks": liquidation_feedbacks}
    return render(request, "files/liquidation_feedback.html", context)


def blame_liquidation_feedback(request, pk):
    if request.method == "POST":
        # Retrieve form data
        counter_proposal = request.POST.get("counter_proposal")
        # Fetch BusinessProfile instance for the current user
        liquidation_request_feedback = LiquidationRequestFeedback.objects.get(
            user=request.user, pk=pk
        )
        # Create and save the PaymentChannel instance
        blame_request_feedback = BlameLRFeedback.objects.create(
            counter_proposal=counter_proposal,
            liquidation_request_feedback=liquidation_request_feedback,
        )
        blame_request_feedback.save()
        # Add success message
        messages.success(
            request,
            "Blame feedback submitted successfully. We will get back to you soon. Check your Email!!",
        )
        # Redirect to a different page after successful creation
        return redirect("liquidation_feedback")  # Replace 'index' with your URL name
    return render(request, "files/blame_liquidation_feedback.html")
