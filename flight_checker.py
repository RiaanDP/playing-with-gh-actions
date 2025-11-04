#!/usr/bin/env python3
"""
Simple Flight Departure Time Checker
Uses AviationStack API (Free tier: 100 requests/month)

Setup:
1. Sign up at https://aviationstack.com/ (free, no credit card needed)
2. Get your API key from the dashboard
3. Run: python flight_checker.py <flight_number> <api_key>

Example: python flight_checker.py AA100 your_api_key_here
"""

# Change on main

import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

# Change 1
# Change 2
# Change 3
# Change 4
# Change 7
# Change 8
# Change 9
# Change 10
# Change 11
# Change 12
# Change 13
# Change Here is another one! 
# Change 15

# Change this is a breaking change! 
# Change B

def check_flight_status(flight_number, api_key):
    """
    Check the departure time and status of a flight

    Args:
        flight_number: Flight number (e.g., 'AA100', 'BA123')
        api_key: AviationStack API key
    """
    # Build API URL
    base_url = "http://api.aviationstack.com/v1/flights"
    params = {
        'access_key': api_key,
        'flight_iata': flight_number
    }

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        print(f"Checking flight {flight_number}...\n")

        # Make API request
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        # Check if we got results
        if 'data' not in data or len(data['data']) == 0:
            print(f"No flight found with number: {flight_number}")
            print("Make sure to use IATA flight code (e.g., AA100, BA456)")
            return

        # Get the first (most recent) flight
        flight = data['data'][0]

        # Extract relevant information
        airline = flight['airline']['name']
        flight_status = flight['flight_status']

        # Departure information
        dep_airport = flight['departure']['airport']
        dep_iata = flight['departure']['iata']
        dep_scheduled = flight['departure']['scheduled']
        dep_estimated = flight['departure'].get('estimated')
        dep_actual = flight['departure'].get('actual')

        # Arrival information
        arr_airport = flight['arrival']['airport']
        arr_iata = flight['arrival']['iata']
        arr_scheduled = flight['arrival']['scheduled']

        # Display results
        print("=" * 60)
        print(f"FLIGHT: {flight_number} - {airline}")
        print(f"STATUS: {flight_status.upper()}")
        print("=" * 60)

        print(f"\n📍 DEPARTURE: {dep_airport} ({dep_iata})")
        print(f"   Scheduled: {format_datetime(dep_scheduled)}")
        if dep_estimated:
            print(f"   Estimated: {format_datetime(dep_estimated)}")
        if dep_actual:
            print(f"   Actual:    {format_datetime(dep_actual)}")

        print(f"\n📍 ARRIVAL: {arr_airport} ({arr_iata})")
        print(f"   Scheduled: {format_datetime(arr_scheduled)}")

        # Show delay information if applicable
        if dep_actual and dep_scheduled:
            delay = calculate_delay(dep_scheduled, dep_actual)
            if delay > 0:
                print(f"\n⚠️  DELAY: {delay} minutes")

        print("\n" + "=" * 60)

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
        if e.code == 401:
            print("Authentication failed. Please check your API key.")
        elif e.code == 429:
            print("Rate limit exceeded. Free tier allows 100 requests/month.")
        else:
            print(f"Error details: {e.read().decode()}")
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}")
    except Exception as e:
        print(f"Error: {e}")


def format_datetime(dt_string):
    """Format ISO datetime string to readable format"""
    if not dt_string:
        return "N/A"
    try:
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M %Z")
    except:
        return dt_string


def calculate_delay(scheduled, actual):
    """Calculate delay in minutes between scheduled and actual times"""
    try:
        sched_dt = datetime.fromisoformat(scheduled.replace('Z', '+00:00'))
        actual_dt = datetime.fromisoformat(actual.replace('Z', '+00:00'))
        delay = (actual_dt - sched_dt).total_seconds() / 60
        return int(delay)
    except:
        return 0


def main():
    """Main function to handle command-line arguments"""
    if len(sys.argv) < 3:
        print("Usage: python flight_checker.py <flight_number> <api_key>")
        print("\nExample: python flight_checker.py AA100 your_api_key_here")
        print("\nTo get a free API key:")
        print("1. Visit https://aviationstack.com/")
        print("2. Sign up for free (100 requests/month, no credit card)")
        print("3. Copy your API key from the dashboard")
        sys.exit(1)

    flight_number = sys.argv[1].upper()
    api_key = sys.argv[2]

    check_flight_status(flight_number, api_key)


if __name__ == "__main__":
    main()
