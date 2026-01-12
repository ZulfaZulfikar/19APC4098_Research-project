# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR: venv\Scripts\activate  # On Windows

# Install required packages
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python main.py
```

### Step 3: Position Yourself

- Sit in front of your webcam
- Ensure good lighting
- The system will automatically start monitoring

---

## 📋 What to Expect

1. **Dashboard Opens**: Real-time metrics displayed
2. **Distance Detection**: Face should be detected within 5-10 seconds
3. **Monitoring Starts**: Metrics update every 5 seconds
4. **Alerts**: Popup notifications if risk is HIGH

---

## 🔧 Troubleshooting

### "No face detected"
- Ensure adequate lighting
- Position face clearly in front of camera
- Remove glasses/masks if possible

### "Brightness not available"
- Normal on some systems (macOS may need permissions)
- System will still work with distance and duration metrics

### "Camera access denied"
- Grant camera permissions in system settings
- Close other applications using the camera

---

## 📊 Understanding the Metrics

- **Distance**: Optimal range is 50-70 cm
- **Blue Light Score**: 
  - LOW (0-30): Safe
  - MODERATE (31-70): Consider breaks
  - HIGH (71+): Take action immediately
- **Thermal Score**: Same risk zones as blue light

---

## 💡 Tips for Best Results

1. **Consistent Setup**: Use the same workspace position
2. **Regular Breaks**: System alerts you, but follow 20-20-20 rule (every 20 minutes, look 20 feet away for 20 seconds)
3. **Review History**: Click "View History" to see trends
4. **Adjust Settings**: Use "Settings" button to customize monitoring

---

## 📝 Data Collection

All data is logged to `data/exposure_log.csv` automatically. This can be used for:
- Research validation
- Personal tracking
- Correlation analysis

---

## ❓ Need Help?

Refer to the main README.md for detailed documentation and research information.

