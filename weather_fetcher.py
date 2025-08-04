import requests
import datetime
import os
import sys
import json
import time
import subprocess

# =============================================================================
# WEATHER API SCRIPT FOR POWER BI DASHBOARD
# =============================================================================
# This script fetches 14-day weather forecasts with AQI for all 9 cities
# and saves them as separate JSON files for Power BI dashboard integration
# UPDATED: Handles "No moonrise/moonset" cases gracefully
# =============================================================================

# Configuration
API_KEY = "7640f2c8ad6141b08fa170506250408"
BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

# Your 9 cities for the dashboard
CITIES = [
    "Bengaluru",
    "Mumbai", 
    "Mysuru",
    "New Delhi",
    "Mandya",
    "Madikeri",
    "Hassan",
    "Bhagamandala",
    "Ghaziabad"
]

# Directory to save weather data files
SAVE_DIR = "weather_data"

def setup_directory():
    """Create the weather_data directory if it doesn't exist"""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"📁 Created directory: {SAVE_DIR}")
    else:
        print(f"📁 Using existing directory: {SAVE_DIR}")

def clean_astronomical_data(astro_data):
    """
    Clean astronomical data to handle 'No moonrise' and 'No moonset' cases
    
    Args:
        astro_data (dict): Astronomical data from API
    
    Returns:
        dict: Cleaned astronomical data with null values for missing times
    """
    cleaned_astro = {}
    
    # List of time fields that might have "No [field]" values
    time_fields = ['moonrise', 'moonset', 'sunrise', 'sunset']
    
    for field in time_fields:
        value = astro_data.get(field, '')
        
        # Check if the value indicates no data
        if (not value or 
            value.lower().startswith('no ') or 
            value.lower() in ['no moonrise', 'no moonset', 'no sunrise', 'no sunset', 'null', 'none']):
            cleaned_astro[field] = None  # Set to null for Power BI
        else:
            cleaned_astro[field] = value  # Keep the original time string
    
    # Copy other astronomical fields as-is
    for key, value in astro_data.items():
        if key not in time_fields:
            cleaned_astro[key] = value
    
    return cleaned_astro

def process_weather_data(raw_data):
    """
    Process raw weather data to handle problematic fields
    
    Args:
        raw_data (dict): Raw weather data from API
    
    Returns:
        dict: Processed weather data safe for Power BI
    """
    processed_data = raw_data.copy()
    
    # Process forecast days to clean astronomical data
    if 'forecast' in processed_data and 'forecastday' in processed_data['forecast']:
        for day in processed_data['forecast']['forecastday']:
            if 'astro' in day:
                day['astro'] = clean_astronomical_data(day['astro'])
    
    return processed_data

def fetch_weather_for_city(city_name, city_number):
    """
    Fetch 14-day weather forecast with AQI for a specific city
    
    Args:
        city_name (str): Name of the city
        city_number (int): City number for logging (1-9)
    
    Returns:
        bool: True if successful, False if failed
    """
    
    # Build the complete API URL
    params = {
        "key": API_KEY,
        "q": city_name,
        "days": 14,
        "aqi": "yes",
        "alerts": "no"
    }
    
    # Create the full URL
    url = f"{BASE_URL}?key={params['key']}&q={params['q']}&days={params['days']}&aqi={params['aqi']}&alerts={params['alerts']}"
    
    print(f"\n[{city_number}/9] 🌤️  Fetching data for: {city_name}")
    print(f"🔗 API URL: {url}")
    
    try:
        # Make the API call
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse JSON to validate it's correct
        raw_weather_data = response.json()
        
        # Verify the response has expected structure
        if 'location' not in raw_weather_data or 'current' not in raw_weather_data or 'forecast' not in raw_weather_data:
            print(f"❌ Invalid API response structure for {city_name}")
            return False
        
        # Process the data to handle problematic fields
        weather_data = process_weather_data(raw_weather_data)
        
        # Check for and log any cleaned astronomical data
        forecast_days = weather_data['forecast']['forecastday']
        cleaned_days = 0
        for day in forecast_days:
            if day['astro'].get('moonrise') is None or day['astro'].get('moonset') is None:
                cleaned_days += 1
        
        if cleaned_days > 0:
            print(f"🌙 Cleaned {cleaned_days} days with missing moon data for {city_name}")
        
        # Get today's date for filename
        today = datetime.date.today().isoformat()
        
        # Create filename that updates daily (overwrites previous)
        # This ensures Power BI always gets fresh data
        safe_city_name = city_name.replace(' ', '_').replace('-', '_')
        filename = f"{safe_city_name}_latest.json"  # Always "latest" - overwrites daily
        filepath = os.path.join(SAVE_DIR, filename)
        
        # Save the processed JSON response with proper formatting
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(weather_data, file, indent=2, ensure_ascii=False)
        
        # Get some basic info for confirmation
        location_name = weather_data['location']['name']
        current_temp = weather_data['current']['temp_c']
        forecast_days_count = len(weather_data['forecast']['forecastday'])
        
        print(f"✅ SUCCESS: {city_name}")
        print(f"   📍 Location: {location_name}")
        print(f"   🌡️  Current Temp: {current_temp}°C")
        print(f"   📅 Forecast Days: {forecast_days_count}")
        print(f"   💾 Saved as: {filename}")
        
        return True
        
    except requests.HTTPError as e:
        print(f"❌ HTTP Error for {city_name}: {e}")
        print(f"   Status Code: {e.response.status_code if e.response else 'Unknown'}")
        return False
        
    except requests.ConnectionError as e:
        print(f"❌ Connection Error for {city_name}: {e}")
        return False
        
    except requests.Timeout as e:
        print(f"❌ Timeout Error for {city_name}: {e}")
        return False
        
    except requests.RequestException as e:
        print(f"❌ Request Error for {city_name}: {e}")
        return False
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error for {city_name}: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error for {city_name}: {e}")
        return False

def upload_to_github():
    """
    Optional: Auto-upload to GitHub repository
    Uncomment and configure if you want automatic GitHub upload
    """
    try:
        # Add all files
        subprocess.run(['git', 'add', '.'], cwd=SAVE_DIR, check=True)
        
        # Commit with timestamp
        commit_message = f"Weather data update - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(['git', 'commit', '-m', commit_message], cwd=SAVE_DIR, check=True)
        
        # Push to GitHub
        subprocess.run(['git', 'push'], cwd=SAVE_DIR, check=True)
        
        print("🚀 Successfully uploaded to GitHub!")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  GitHub upload failed (optional)")
        return False

def main():
    """Main function to execute the weather data fetching process"""
    
    print("=" * 80)
    print("🌤️  WEATHER DATA FETCHER FOR POWER BI DASHBOARD")
    print("🌙 UPDATED: Handles 'No moonrise/moonset' cases gracefully")
    print("=" * 80)
    print(f"📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏙️  Total Cities: {len(CITIES)}")
    print(f"🔑 API Key: {API_KEY}")
    print(f"📊 Forecast Days: 14")
    print(f"🌬️  AQI Included: Yes")
    print(f"🛡️  Moon Data: Safe handling enabled")
    print("=" * 80)
    
    # Setup directory
    setup_directory()
    
    # Initialize counters
    successful_cities = []
    failed_cities = []
    start_time = time.time()
    
    # Process each city
    for index, city in enumerate(CITIES, 1):
        if fetch_weather_for_city(city, index):
            successful_cities.append(city)
        else:
            failed_cities.append(city)
        
        # Add a small delay between requests to be respectful to the API
        if index < len(CITIES):  # Don't sleep after the last request
            time.sleep(1)  # 1 second delay
    
    # Calculate execution time
    end_time = time.time()
    execution_time = round(end_time - start_time, 2)
    
    # Final Summary
    print("\n" + "=" * 80)
    print("📊 EXECUTION SUMMARY")
    print("=" * 80)
    print(f"✅ Successful: {len(successful_cities)}/{len(CITIES)} cities")
    print(f"❌ Failed: {len(failed_cities)}/{len(CITIES)} cities")
    print(f"⏱️  Execution Time: {execution_time} seconds")
    print(f"📁 Data Directory: {os.path.abspath(SAVE_DIR)}")
    
    if successful_cities:
        print(f"\n🎉 Successfully fetched data for:")
        for city in successful_cities:
            print(f"   ✓ {city}")
    
    if failed_cities:
        print(f"\n⚠️  Failed to fetch data for:")
        for city in failed_cities:
            print(f"   ✗ {city}")
        print(f"\n💡 Tip: Check your internet connection and API key validity")
    else:
        print(f"\n🎉 ALL CITIES PROCESSED SUCCESSFULLY!")
        print(f"🔄 Your Power BI dashboard can now refresh with the latest data")
        print(f"🌙 Moon data issues automatically resolved")
    
    print("=" * 80)
    
    # Return success status for automation scripts
    return len(failed_cities) == 0

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Script interrupted by user")
        sys.exit(2)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(3)

