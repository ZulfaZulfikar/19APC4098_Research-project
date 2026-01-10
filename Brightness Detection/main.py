import subprocess
import platform
import os
import re


def get_manual_brightness():
    """Fallback manual brightness input"""
    while True:
        try:
            value = int(input("Enter screen brightness (0–100): "))
            if 0 <= value <= 100:
                return value
            else:
                print("⚠ Value must be between 0 and 100")
        except ValueError:
            print("⚠ Please enter a valid number")


def get_brightness():
    os_name = platform.system()

    try:
        # ===================== WINDOWS =====================
        if os_name == "Windows":
            cmd = (
                "powershell "
                "(Get-WmiObject -Namespace root/WMI "
                "-Class WmiMonitorBrightness).CurrentBrightness"
            )
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            brightness = result.stdout.strip()
            return int(brightness)

        # ===================== macOS =====================
        elif os_name == "Darwin":
            cmd = "ioreg -c AppleBacklightDisplay"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            # Extract ALL brightness values
            matches = re.findall(r'brightness.*?value=(\d+)', result.stdout)

            if not matches:
                raise ValueError("Brightness data not found")

            # Take last reported value
            raw_value = int(matches[-1])

            # macOS internal max varies → approximate normalization
            MAX_BRIGHTNESS = 1891
            brightness_percent = int((raw_value / MAX_BRIGHTNESS) * 100)

            return max(0, min(brightness_percent, 100))

        # ===================== LINUX =====================
        elif os_name == "Linux":
            base_path = "/sys/class/backlight/"
            if not os.path.exists(base_path):
                raise FileNotFoundError("Backlight path not found")

            device = os.listdir(base_path)[0]
            path = os.path.join(base_path, device)

            with open(os.path.join(path, "brightness")) as f:
                current = int(f.read())
            with open(os.path.join(path, "max_brightness")) as f:
                maximum = int(f.read())

            return int((current / maximum) * 100)

        else:
            raise OSError("Unsupported OS")

    except Exception as e:
        print(f"⚠ Automatic brightness failed: {e}")
        return None


def main():
    print("🔆 Screen Brightness Detection")
    print(f"Operating System: {platform.system()}\n")

    brightness = get_brightness()

    if brightness is None:
        print("➡ Switching to manual brightness input\n")
        brightness = get_manual_brightness()

    print(f"\n✅ Final Brightness Value Used: {brightness}%")
    return brightness


if __name__ == "__main__":
    main()
