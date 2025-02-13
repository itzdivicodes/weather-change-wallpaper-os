import os
import requests
from pathlib import Path
import ctypes  # For Windows
import platform

API_KEY = "c38a4c4313956b9eec5ac2b415effe86"  # Replace with your API key
CITY = "CHENNAI"
IMAGE_PATH ="C:\\Users\\91944\\Downloads\\TRIAL\\wallpapers\\"

def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] != 200:
        print("Error fetching weather data:", data["message"])
        return None
    return data["weather"][0]["main"].lower()

def set_wallpaper(image_path):
    system = platform.system()
    if system == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
    elif system == "Linux":
        os.system(f"gsettings set org.gnome.desktop.background picture-uri file://{image_path}")
    elif system == "Darwin":  # macOS
        os.system(f'osascript -e "tell application \"Finder\" to set desktop picture to POSIX file \"{image_path}\""')
    else:
        print("Unsupported OS")

def main():

    weather_condition = get_weather(API_KEY, CITY)
    if not weather_condition:
        return
    
    wallpaper_dir = Path(IMAGE_PATH)
   ## wallpaper_dir = IMAGE_PATH
    wallpapers = {
        "clear": wallpaper_dir / "clear.jpg",
        "clouds": wallpaper_dir / "cloud.jpg",
        "rain": wallpaper_dir / "rain.jpg",
        "snow": wallpaper_dir / "snowy.jpg",
        "thunderstorm": wallpaper_dir / "storm.jpg",
        "mist": wallpaper_dir / "foggy.jpg",
    }
    
    image_path = wallpapers.get(weather_condition, wallpaper_dir / "default.jpg")
    if not image_path.exists():
        print(f"Wallpaper for '{weather_condition}' not found. Using default.")
        image_path = wallpaper_dir / "default.jpg"
    
    set_wallpaper(str(image_path))
    print(f"Wallpaper changed to {image_path}")

if __name__ == "__main__":
    main()
