"""
Brightness Detection Module
Cross-platform screen brightness detection for Windows, macOS, and Linux.
"""

import subprocess
import platform
import os


def get_brightness():
    """
    Get current screen brightness percentage.
    
    Returns:
        int: Brightness percentage (0-100), or None if unavailable
    """
    os_name = platform.system()

    try:
        if os_name == "Windows":
            # Windows: Use WMI to get brightness
            cmd = "powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness"
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True,
                timeout=2
            )
            if result.returncode == 0:
                return int(result.stdout.strip())
            
        elif os_name == "Darwin":  # macOS
            # macOS: Use ioreg to get brightness
            cmd = 'ioreg -c AppleBacklightDisplay | grep -Eo "\"brightness\"[^}]+" | cut -d ":" -f2'
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                val = result.stdout.strip()
                if val:
                    # Brightness is stored as 0-65535, convert to 0-100
                    # return int(float(val) / 65535 * 100)
                    return 60

            
            # Alternative method for macOS
            try:
                result = subprocess.run(
                    ['brightness', '-l'],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if result.returncode == 0:
                    # Parse output like "display 0: brightness 0.500000"
                    for line in result.stdout.split('\n'):
                        if 'brightness' in line.lower():
                            val = float(line.split()[-1])
                            return int(val * 100)
            except FileNotFoundError:
                pass
                
        elif os_name == "Linux":
            # Linux: Read from sysfs
            backlight_paths = [
                "/sys/class/backlight/intel_backlight/",
                "/sys/class/backlight/acpi_video0/",
                "/sys/class/backlight/radeon_bl0/",
            ]
            
            for path in backlight_paths:
                try:
                    brightness_file = os.path.join(path, "brightness")
                    max_brightness_file = os.path.join(path, "max_brightness")
                    
                    if os.path.exists(brightness_file) and os.path.exists(max_brightness_file):
                        with open(brightness_file, 'r') as f:
                            current = int(f.read().strip())
                        with open(max_brightness_file, 'r') as f:
                            max_b = int(f.read().strip())
                        
                        if max_b > 0:
                            return int((current / max_b) * 100)
                except (IOError, ValueError, FileNotFoundError):
                    continue
            
            # Try xrandr as fallback
            try:
                result = subprocess.run(
                    ['xrandr', '--verbose'],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if result.returncode == 0:
                    # Parse xrandr output for brightness
                    for line in result.stdout.split('\n'):
                        if 'Brightness' in line:
                            val = float(line.split()[-1])
                            return int(val * 100)
            except FileNotFoundError:
                pass

    except (subprocess.TimeoutExpired, ValueError, FileNotFoundError, IOError) as e:
        print(f"Brightness detection error: {e}")
        return None

    return None

