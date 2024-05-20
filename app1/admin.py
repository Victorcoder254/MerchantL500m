from django.contrib import admin
from .models import *


class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "business_name", "created")
    list_filter = ("created",)
    search_fields = ("user__username",)


admin.site.register(BusinessProfile, BusinessProfileAdmin)


class PaymentChannelAdmin(admin.ModelAdmin):
    list_display = ("user", "bank_name", "date_created")
    search_fields = ("user__username", "bank_name", "bank_account_number")
    list_filter = ("date_created",)


admin.site.register(PaymentChannel, PaymentChannelAdmin)


class PaymentsRemittedAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "business_id",
        "date_created",
    )
    search_fields = ("user__username", "business_id")
    list_filter = ("date_created",)


admin.site.register(PaymentsRemitted, PaymentsRemittedAdmin)


class LiquidationRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "request_id", "status", "created")
    search_fields = ("user__username", "request_id")
    list_filter = ("status", "created")


admin.site.register(LiquidationRequest, LiquidationRequestAdmin)


class BusinessMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "date_created", "subject")
    search_fields = ("user__username", "subject")
    list_filter = ("date_created",)


admin.site.register(BusinessMessage, BusinessMessageAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("date_created", "subject")
    search_fields = ("subject",)
    list_filter = ("date_created",)


admin.site.register(Notification, NotificationAdmin)


class LiquidationRequestFeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "liquidation_request", "date_created")
    search_fields = ("user__username", "liquidation_request__request_id")
    list_filter = ("date_created",)


admin.site.register(LiquidationRequestFeedback, LiquidationRequestFeedbackAdmin)


class BlameLRFeedbackAdmin(admin.ModelAdmin):
    list_display = ("liquidation_request_feedback", "date_created")
    search_fields = ("liquidation_request_feedback__liquidation_request__request_id",)
    list_filter = ("date_created",)


admin.site.register(BlameLRFeedback, BlameLRFeedbackAdmin)


class InfoMessageAdmin(admin.ModelAdmin):
    list_display = ("date_created", "subject")
    search_fields = ("subject",)
    list_filter = ("date_created",)


admin.site.register(InfoMessage, InfoMessageAdmin)


class VisitorAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "timestamp")
    search_fields = ("ip_address",)
    list_filter = ("timestamp",)


admin.site.register(Visitor, VisitorAdmin)


class ResetPasswordAdmin(admin.ModelAdmin):
    list_display = ("user", "date_created", "Email")
    search_fields = ("Email",)
    list_filter = ("date_created",)


admin.site.register(ResetPassword, ResetPasswordAdmin)
