@echo off
echo ====================================
echo VFS Emulator Testing
echo ====================================
echo Current folder: %CD%
echo.

echo Test 1: Launch with correct parameters
python emulator.py test_vfs test_script.txt
pause

echo.
echo Test 2: Launch without parameters (should show error)
python emulator.py
pause

echo.
echo Test 3: Launch with missing script
python emulator.py test_vfs missing_script.txt
pause

echo.
echo All tests completed!
pause