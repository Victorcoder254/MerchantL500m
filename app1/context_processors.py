# your_app/context_processors.py

from .models import *  # Import your model


def navbar_data(request):
    # Fetch data from the database
    notifications = Notification.objects.all().order_by("date_created")[:5]
    user_messages = BusinessMessage.objects.none()  # Initialize queryset
    business_profile = None  # Initialize as None

    # Check if user is authenticated
    if request.user.is_authenticated:
        user_messages = BusinessMessage.objects.filter(user=request.user).order_by(
            "date_created"
        )[:5]
        business_profile = BusinessProfile.objects.filter(user=request.user).first()

    # Return a dictionary of data to add to the template context
    return {
        "notifications": notifications,  # Add more data as needed
        "user_messages": user_messages,  # Add more data as needed
        "business_profile": business_profile,  # Add more data as needed
    }
