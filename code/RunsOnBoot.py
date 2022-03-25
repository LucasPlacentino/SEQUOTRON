#crontab not working becasue needs Raspbian GUI running

# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
#and add (before @xscreensaver ...):
# @lxterminal -e /home/pi/Desktop/start.sh
#and in start.sh put:
# python3 /home/pi/TRANH201INFO3-Sequencer/code/SequencerMain.py


#import subprocess

print("RPi succesful boot.")

# then launch program : subprocess.run(args...) (only since python 3.5)   OR   Popen(...)     # (?)
