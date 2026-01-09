import screen_brightness_control as sbc
import platform
import time

def get_screen_brightness():
    try:
        brightness = sbc.get_brightness()
        if isinstance(brightness, list):
            return brightness[0]
        return brightness
    except Exception as e:
        print("⚠ Brightness read failed:", e)
        return None


def main():
    print("🔆 Screen Brightness Detector")
    print(f"OS: {platform.system()}")
    print("Press Ctrl+C to stop\n")

    while True:
        brightness = get_screen_brightness()

        if brightness is not None:
            print(f"Brightness Level: {brightness}%")
        else:
            print("❌ Brightness unavailable (use manual input)")

        time.sleep(2)


if __name__ == "__main__":
    main()
