"""Electricity rates used across the whole app. Change them here and every page follows."""

PEAK_RATE = 7.48      # ₱ per kWh
OFFPEAK_RATE = 3.55   # ₱ per kWh
PEAK_START = 8        # peak runs 8 AM ...
PEAK_END = 21         # ... until 9 PM (exclusive)

# Cost estimates for usage that hasn't been scheduled assume the peak rate,
# so "saved by scheduling" compares a schedule against running it at peak.
ESTIMATE_RATE = PEAK_RATE

# Daily total (kWh) above which the dashboard warns you.
DAILY_LIMIT_KWH = 35


def is_peak(hour):
    return PEAK_START <= int(hour) % 24 < PEAK_END


def rate_at(hour):
    return PEAK_RATE if is_peak(hour) else OFFPEAK_RATE


HOURLY_RATES = [rate_at(h) for h in range(24)]
OFFPEAK_HOURS = 24 - (PEAK_END - PEAK_START)


def hour_label(hour):
    hour = int(hour) % 24
    return f"{12 if hour % 12 == 0 else hour % 12} {'AM' if hour < 12 else 'PM'}"
