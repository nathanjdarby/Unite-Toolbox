# Unite Toolbox - Standalone Executable

## 🚀 Quick Start

### Option 1: Using the Launcher Script (Recommended)

```bash
./launch_unite_toolbox.sh
```

### Option 2: Manual Launch

```bash
./UniteToolbox
```

Then open your browser to: http://localhost:5000

### Option 3: Double-click the App Bundle

Double-click `UniteToolbox.app` in Finder

## 📋 System Requirements

- **macOS 10.14+** (Mojave or later)
- **No Python installation required** - everything is included!

## 🛠️ Features Included

- ✅ CSV to UWP Converter
- ✅ CSV to SMS List Extractor
- ✅ CSV Divide by Workplace
- ✅ HTML Processor (MSO removal + CSS inlining)
- ✅ URL Builder with parameters
- ✅ CSV Compare tool
- ✅ JotForm Templates access

## 📁 File Structure

```
dist/
├── UniteToolbox              # Main executable (59MB)
├── UniteToolbox.app/         # macOS app bundle
├── launch_unite_toolbox.sh   # Easy launcher script
└── README_DISTRIBUTION.md    # This file
```

## 🔧 Troubleshooting

### If the app doesn't start:

1. Check if port 5000 is already in use
2. Try running: `lsof -i :5000` to see what's using the port
3. Kill any existing processes: `pkill -f UniteToolbox`

### If you get a security warning:

1. Go to System Preferences > Security & Privacy
2. Click "Allow Anyway" for UniteToolbox
3. Try running again

### If the browser doesn't open automatically:

1. Manually open: http://localhost:5000
2. The app should be running in the background

## 📦 Distribution

To share with your team:

1. **Zip the entire `dist/` folder**
2. **Send the zip file**
3. **Team members extract and run the launcher script**

## 🎯 Usage Tips

- The app runs locally on your machine
- All processing happens on your computer (no data sent to servers)
- Files are processed in memory and downloaded directly
- The app automatically creates `uploads/` and `results/` folders as needed

## 🔄 Updates

To update the executable:

1. Rebuild using PyInstaller: `pyinstaller unite_toolbox.spec`
2. Replace the old executable with the new one
3. Update the launcher script if needed

---

**Unite Toolbox v1.0** - Modern Web Edition
