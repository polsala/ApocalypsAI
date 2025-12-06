import argparse
import datetime
import math

def get_day_of_year(date_obj: datetime.date) -> int:
    """Calculates the day of the year for a given date."""
    return date_obj.timetuple().tm_yday

def calculate_equation_of_time(day_of_year: int) -> float:
    """
    Calculates the Equation of Time (EoT) in minutes.
    EoT is the difference between mean solar time and apparent solar time.
    A simplified approximation is used here.
    """
    # B in radians
    B = math.radians((360 / 365.242) * (day_of_year - 81))
    
    # EoT in minutes
    eot = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    return eot

def calculate_solar_noon_utc(date_obj: datetime.date, longitude: float) -> datetime.time:
    """
    Calculates the time of solar noon in UTC for a given date and longitude.
    
    Args:
        date_obj: The date for which to calculate solar noon.
        longitude: The longitude of the location (degrees, West is negative).
        
    Returns:
        A datetime.time object representing solar noon in UTC.
    """
    day_of_year = get_day_of_year(date_obj)
    eot = calculate_equation_of_time(day_of_year)
    
    # Solar noon in minutes from midnight UTC
    # Start with 12:00 UTC (720 minutes)
    # Adjust for Equation of Time (EoT is already in minutes)
    # Adjust for longitude: 4 minutes per degree. West longitudes (negative) mean later solar noon.
    # So, 720 - EoT - (4 * longitude) is the total minutes from midnight UTC.
    solar_noon_utc_minutes = 720 - eot - (4 * longitude)
    
    # Convert total minutes to hours, minutes, and seconds, ensuring it's within a 24-hour cycle.
    total_seconds = round(solar_noon_utc_minutes * 60) # Round to nearest second
    total_seconds %= (24 * 3600)
    if total_seconds < 0:
        total_seconds += (24 * 3600)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return datetime.time(hours, minutes, seconds)

def main():
    parser = argparse.ArgumentParser(
        description="Calculate the precise moment of solar noon for a given date and geographic location."
    )
    parser.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        required=True,
        help="Date in YYYY-MM-DD format (e.g., 2024-07-20)."
    )
    parser.add_argument(
        "--lat",
        type=float,
        required=True,
        help="Latitude of the location (degrees, e.g., 34.0522)."
    )
    parser.add_argument(
        "--lon",
        type=float,
        required=True,
        help="Longitude of the location (degrees, West is negative, e.g., -118.2437)."
    )
    parser.add_argument(
        "--tz",
        type=float,
        default=0.0,
        help="Timezone offset from UTC in hours (e.g., -7 for PDT, +2 for CET). Default is 0 (UTC)."
    )

    args = parser.parse_args()

    solar_noon_utc = calculate_solar_noon_utc(args.date, args.lon)
    
    # Convert UTC solar noon to local time based on provided timezone offset
    # Create a dummy datetime object for the date and UTC solar noon time
    dt_utc = datetime.datetime.combine(args.date, solar_noon_utc)
    
    # Apply timezone offset
    dt_local = dt_utc + datetime.timedelta(hours=args.tz)
    
    print(f"Solar Noon for {args.date} at Lat {args.lat}, Lon {args.lon}:")
    print(f"  UTC: {solar_noon_utc.strftime('%H:%M:%S')}")
    print(f"  Local Time (TZ offset {args.tz:+.1f}h): {dt_local.time().strftime('%H:%M:%S')}")
    print("\nGuidance:")
    print("  At Solar Noon, the sun is at its highest point in the sky.")
    if args.lat >= 0:
        print("  In the Northern Hemisphere, the sun will be due South. North is directly behind you.")
    else:
        print("  In the Southern Hemisphere, the sun will be due North. South is directly behind you.")
    print("  Use this moment to orient yourself and find true North/South.")

if __name__ == "__main__":
    main()
