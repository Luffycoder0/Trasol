@echo off
echo ============================================
echo  HCL Notes Downloader - Build Script
echo  Publisher: Djed Tech.ink
echo ============================================
echo.

cd /d "%~dp0"

echo [1/3] Converting icon image to .ico ...
python -c "
from PIL import Image
import os, sys
img_path = None
for ext in ['icon.png', 'icon.jpg', 'icon.jpeg', 'icon.bmp']:
    if os.path.exists(ext):
        img_path = ext
        break
if img_path is None:
    print('WARNING: No source icon image found (icon.png expected). Skipping icon conversion.')
    sys.exit(0)
img = Image.open(img_path).convert('RGBA')
sizes = [(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)]
icons = [img.resize(s, Image.LANCZOS) for s in sizes]
icons[0].save('icon.ico', format='ICO', sizes=[(s[0],s[1]) for s in sizes], append_images=icons[1:])
print('icon.ico created successfully.')
"

echo.
echo [2/3] Installing / verifying dependencies ...
pip install pyinstaller pillow pywin32 --quiet

echo.
echo [3/3] Building EXE with PyInstaller ...
pyinstaller --clean build.spec

echo.
echo ============================================
if exist "dist\HCL Notes Downloader.exe" (
    echo  BUILD SUCCESSFUL!
    echo  Output: dist\HCL Notes Downloader.exe
) else (
    echo  BUILD MAY HAVE FAILED - check output above.
)
echo ============================================
pause
