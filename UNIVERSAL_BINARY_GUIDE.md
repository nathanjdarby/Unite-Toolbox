# Universal Binary Guide for Flask App

## Current Solution: Apple Silicon Build (Works on Both)

The Flask app is built for **Apple Silicon (arm64)** architecture. This build will work on:

✅ **Apple Silicon Macs** - Runs natively (fastest)
✅ **Intel Macs** - Runs via Rosetta 2 (works, but slightly slower)

This is the **simplest and most practical solution** because:

- No need for Universal2 Python installation
- No need for Universal2 versions of all dependencies
- Works on both architectures out of the box
- Rosetta 2 performance is excellent for most applications

## To Build (Current Method)

Simply run:

```bash
./build_flask_executable.sh
```

This creates `dist/UniteToolboxWeb.app` that works on both Intel and Apple Silicon Macs.

## True Universal Binary (Advanced)

If you need a **true universal binary** (native performance on both architectures), you would need:

### Requirements:

1. **Universal2 Python** - Download from [python.org](https://www.python.org/downloads/)
2. **Universal2 Dependencies** - All packages must be universal binaries
   - Use `universalPip` to create universal wheels
   - Or manually build universal versions of problematic packages

### Steps:

1. Install Universal2 Python
2. Create virtual environment with Universal2 Python
3. Install dependencies (may need to build universal wheels)
4. Build with `target_arch='universal2'` in spec file

### Known Issues:

- **numpy**: Often not universal - may need to build from source
- **PIL/Pillow**: Some extensions not universal
- **pandas**: Depends on numpy, inherits issues

## Recommendation

**Use the current arm64 build** - it works perfectly on both Intel and Apple Silicon Macs. The performance difference via Rosetta 2 is minimal for a Flask web application.

## Testing on Intel Mac

To test on an Intel Mac:

1. Transfer `UniteToolboxWeb.app` to the Intel Mac
2. Double-click to run
3. It will automatically use Rosetta 2
4. Performance should be excellent

## Alternative: Build Separate Versions

If you need native performance on both:

1. Build arm64 version on Apple Silicon Mac
2. Build x86_64 version on Intel Mac (or via Rosetta 2)
3. Distribute both versions separately
