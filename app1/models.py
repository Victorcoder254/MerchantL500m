from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

# BUSINESS PROFILE


class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_license_image = models.ImageField(upload_to="business_license_images")
    business_name = models.CharField(max_length=100, blank=True, null=True)
    sector = models.CharField(max_length=100)  # Adding sector field
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email_company = models.EmailField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    business_id = models.CharField(max_length=355, blank=True, null=True)  # New field

    def save(self, *args, **kwargs):
        if not self.business_id:  # Check if business_id is not already set
            # Combine username and created date to form business_id
            self.business_id = f"{self.user.username}_{self.business_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Business Profile"


# BUSINESS PROFILE

# PAYMENTS MODEL


class PaymentChannel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    business_id = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Payment Channel"


class PaymentsRemitted(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    business_id = models.ForeignKey(
        BusinessProfile, on_delete=models.CASCADE, blank=True, null=True
    )
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    amount = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    payment_description = models.TextField(blank=True, null=True)
    payment_success_message = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Payment Remitted for {self.business_id} by {self.user.username}"


# PAYMENTS MODELS


# Liquidation Requests


class LiquidationRequest(models.Model):
    STATUS_CHOICES = [("in_review", "In Review"), ("processed", "Processed")]
    CONDITION_CHOICES = [
        ("new", "New"),
        ("used_good", "Used - Good condition"),
        ("used_fair", "Used - Fair condition"),
        ("damaged", "Damaged"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    business_id = models.CharField(max_length=255, blank=True, null=True)
    request_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_review",
        blank=True,
        null=True,
    )
    reason_for_liquidation = models.TextField(blank=True, null=True)
    estimated_value_of_goods = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    anticipated_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    goods_name = models.CharField(max_length=1000, blank=True, null=True)
    quantity_goods = models.CharField(max_length=1000, blank=True, null=True)
    condition_of_goods = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default="new",
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.request_id:
            # Generate a random string of alphanumeric characters
            random_string = "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )
            # Combine username and random string to form request_id
            self.request_id = f"{self.user.username}_{random_string}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Liquidation Request - {self.request_id}"


class LiquidationRequestFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liquidation_request = models.ForeignKey(
        LiquidationRequest, on_delete=models.CASCADE
    )
    proposed_price_range = models.TextField(blank=True, null=True)
    expected_return_on_goods_sold = models.TextField(blank=True, null=True)
    details1 = models.TextField(blank=True, null=True)
    details2 = models.TextField(blank=True, null=True)
    details3 = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Liquidation Request Feedback for {self.liquidation_request.request_id}"


class BlameLRFeedback(models.Model):
    liquidation_request_feedback = models.ForeignKey(
        LiquidationRequestFeedback, on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    counter_proposal = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Blame Liquidation Request Feedback - {self.liquidation_request_feedback.id}"


# Liquidation Requests


# Messages to a User/Business


class BusinessMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Message to {self.user.username} - {self.subject}"


# Messages to a User/Business

# Notifications to all users


class Notification(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.subject


# Notifications to all users

# Info Messages


class InfoMessage(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.subject


# Info Messages


# METADATA FOR OUR WEBSITE


class Visitor(models.Model):
    ip_address = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Visitor at {self.timestamp} with IP {self.ip_address}"


# RESET PASSWORD


class ResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    Email = models.CharField(max_length=455, blank=True, null=True)

    def __str__(self):
        return self.Email
