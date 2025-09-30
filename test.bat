@echo off
python emulator.py test_vfs test_script.txt
pause

python emulator.py test_vfs test_env.txt
pause

python emulator.py test_vfs test_error.txt
pause

python emulator.py
pause

python emulator.py test_vfs missing_script.txt
pause