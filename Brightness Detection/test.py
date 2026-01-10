import subprocess
import platform
import os


def get_brightness():
    os_name = platform.system()

    try:
        # --- macOS ---
        if os_name == "Darwin":
            # Uses AppleScript to query the Display Services
            cmd = "osascript -e 'tell application \"System Events\" to get brightness of first display group of system preferences'"
            # If the above fails on newer macOS versions, use ioreg:
            alt_cmd = 'ioreg -c AppleBacklightDisplay | grep -Eo "\"brightness\"[^}]+" | cut -d ":" -f2'

            result = subprocess.run(alt_cmd, shell=True, capture_output=True, text=True)
            print("============")
            print(result)
            print("============")

            val = result.stdout.strip().replace('"', '').replace('{', '')
            # Returns a raw value, typically needs normalization to 100
            return int(float(val) / 65535 * 100) if val else "Error"

        # --- Windows ---
        elif os_name == "Windows":
            cmd = "powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness"
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            return int(result.stdout.strip())

        # --- Linux ---
        elif os_name == "Linux":
            # Common path for laptop backlights
            path = "/sys/class/backlight/intel_backlight/"
            if not os.path.exists(path):
                # Fallback for different hardware
                path = "/sys/class/backlight/acpi_video0/"

            with open(os.path.join(path, "brightness"), "r") as f:
                current = int(f.read())
            with open(os.path.join(path, "max_brightness"), "r") as f:
                maximum = int(f.read())
            return int((current / maximum) * 100)

    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    current_brightness = get_brightness()
    print(f"Current {platform.system()} Brightness: {current_brightness}%")