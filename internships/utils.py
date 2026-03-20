# utils.py
import random
from datetime import datetime
from django.utils import timezone
from .models import ApplicationCounter

def initialize_application_counter():
    if ApplicationCounter.objects.exists():
        return


def initialize_application_counter():
    """
    Run this ONLY ONCE to initialize the counter system
    """

    # If already exists → don't recreate
    if ApplicationCounter.objects.exists():
        print("✅ Counter already initialized")
        return

    # 🔥 SET DEADLINE (IMPORTANT)
    end_time = datetime(
        2026, 3, 29, 18, 30, 0,
        tzinfo=timezone.get_current_timezone()
    )

    # Create record
    counter = ApplicationCounter.objects.create(
        base_count=100,
        end_time=end_time
    )

    start = counter.start_time
    end = counter.end_time

    # Total seconds
    total_seconds = (end - start).total_seconds()

    # Number of 30-min intervals
    total_intervals = int(total_seconds // 1800)

    increments = []

    for i in range(total_intervals):
        # 🎯 realistic variation
        value = random.randint(45, 55)
        increments.append(value)

    # Save increments
    counter.increments = increments
    counter.save()

    print("🔥 Counter initialized successfully!")
    print(f"Total intervals: {total_intervals}")