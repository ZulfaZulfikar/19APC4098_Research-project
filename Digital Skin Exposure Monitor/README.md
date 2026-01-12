# Digital Skin Exposure Monitor

**AI-Driven Approach to Track Blue Light and Thermal Exposure Effects on Skin Health of Remote Working Professionals to Mitigate Digital Aging**

---

## 📋 Project Information

- **Research Project**: IS 8101 Research Project in Information Systems
- **Student**: M.Z.F.Zulfa (19APC4098)
- **Supervisor**: H.M.K.T.Gunewardhana
- **Institution**: Sabaragamuwa University of Sri Lanka, Faculty of Computing

---

## 🎯 Research Objective

This system monitors and tracks blue light and thermal exposure from digital devices to help remote working professionals mitigate digital aging effects on skin health. The system uses AI-driven computer vision and rule-based modeling to estimate exposure levels in real-time.

---

## 🔬 Research Methodology

### AI-Driven Components:
1. **Computer Vision**: MediaPipe Face Mesh for distance estimation
2. **Rule-Based Modeling**: Literature-based formulas for exposure scoring
3. **Real-Time Monitoring**: Continuous data collection and risk assessment

### Exposure Models:
- **Blue Light Exposure**: Based on screen brightness, duration, and distance (inverse square law)
- **Thermal Exposure**: Based on proximity and duration (erythema ab igne research)

---

## 📁 Project Structure

```
digital_skin_exposure_monitor/
│
├── inputs/
│   ├── distance.py          # Webcam-based distance detection
│   └── brightness.py        # Cross-platform brightness detection
│
├── exposure/
│   ├── blue_light.py        # Blue light exposure scoring
│   └── thermal.py           # Thermal exposure scoring
│
├── core/
│   └── controller.py        # Main monitoring controller
│
├── data/
│   └── exposure_log.csv     # Historical exposure data
│
├── ui/
│   ├── dashboard.py         # Main dashboard GUI
│   ├── alert_popup.py       # Alert notifications
│   ├── history.py           # Historical data viewer
│   └── settings.py          # Settings configuration
│
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Webcam (for distance detection)
- Operating System: Windows, macOS, or Linux

### Installation Steps

1. **Clone or download this repository**

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure webcam permissions**
   - Grant camera access when prompted
   - Position yourself in front of the camera for accurate distance measurement

---

## 💻 Usage

### Running the Application

```bash
python main.py
```

### Features

1. **Real-Time Monitoring**
   - Distance from screen (cm)
   - Screen brightness (%)
   - Session duration (minutes)
   - Blue light exposure score
   - Thermal exposure score

2. **Risk Assessment**
   - **LOW**: Safe exposure levels
   - **MODERATE**: Consider taking breaks or adjusting settings
   - **HIGH**: Immediate action recommended (alerts displayed)

3. **Data Logging**
   - All metrics automatically logged to CSV
   - Historical data accessible via "View History" button

4. **Alerts**
   - Popup notifications when risk is HIGH
   - Cooldown period to prevent alert spam

---

## 📊 Research Validation

### Metrics Tracked:
- Distance from screen (validated using MediaPipe face landmarks)
- Screen brightness (OS-level detection)
- Exposure duration (session tracking)
- Risk scores (formula-based, literature-validated)

### Data Collection:
- CSV logging for correlation analysis
- Suitable for survey-based validation studies
- No image storage (privacy-preserving)

---

## 🔬 Technical Details

### Distance Detection
- **Method**: MediaPipe Face Mesh
- **Principle**: Inter-pupillary distance (IPD) estimation
- **Formula**: `distance = (real_IPD × focal_length) / pixel_distance`

### Blue Light Score
- **Formula**: `Score = (Brightness × Duration) / (Distance²) × K`
- **Constants**: Calibrated based on research literature
- **Risk Zones**: LOW (≤30), MODERATE (31-70), HIGH (>70)

### Thermal Score
- **Formula**: `Score = (Duration / Distance) × M`
- **Based on**: Erythema ab igne research (toasted skin syndrome)
- **Risk Zones**: LOW (≤30), MODERATE (31-70), HIGH (>70)

---

## ⚠️ Important Notes

### Research Disclaimer
- This system provides **behavioral exposure monitoring**, not medical diagnosis
- Scores are **estimates** based on computer vision and formula-based modeling
- For medical concerns, consult healthcare professionals

### Limitations
- Distance detection requires clear face visibility
- Brightness detection may vary by OS and hardware
- Exposure models are research-based approximations

### Ethics & Privacy
- **No image storage**: Only numerical metrics are logged
- **Local processing**: All data stays on your device
- **Opt-in monitoring**: User initiates all sessions

---

## 📚 References

This project is based on research literature on:
- Blue light effects on skin health (Coats et al., 2021)
- Erythema ab igne from digital devices (Salvio et al., 2016)
- Digital aging and screen exposure
- Computer vision for distance estimation

See the research proposal document for full references.

---

## 🔧 Troubleshooting

### Webcam Issues
- Ensure camera is not being used by another application
- Check camera permissions in system settings
- Try restarting the application

### Brightness Detection
- **macOS**: May require additional permissions or external tools
- **Linux**: Ensure backlight control is available
- **Windows**: Should work with standard WMI access

### No Face Detected
- Ensure adequate lighting
- Position face clearly in front of camera
- Remove obstructions (glasses, masks, etc.)

---

## 📝 License & Academic Use

This project is developed for academic research purposes as part of the BSc Honours Degree Programme in Computing and Information Systems at Sabaragamuwa University of Sri Lanka.

---

## 👤 Contact

- **Student**: M.Z.F.Zulfa (19APC4098)
- **Supervisor**: H.M.K.T.Gunewardhana

---

## 🙏 Acknowledgments

- MediaPipe team for face mesh detection
- Research community for blue light and thermal exposure studies
- Sabaragamuwa University of Sri Lanka, Faculty of Computing

---

**Version**: 1.0  
**Last Updated**: 2025  
**Status**: Research Project Implementation

