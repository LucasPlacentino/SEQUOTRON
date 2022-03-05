# add this file to crontab : @reboot python3 /path/to/this/file/RunsOnBoot.py

#import subprocess

print("RPi succesful boot.")

# then launch program : subprocess.run(args...) (only since python 3.5)   OR   Popen(...)     # (?)
