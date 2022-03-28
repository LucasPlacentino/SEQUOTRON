#crontab not working because needs Raspbian GUI running

# $ sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
#and add (before @xscreensaver ...):
# @lxterminal -e /path/to/SEQUOTRON/code/start.sh

echo '=====Launching Sequencer====='
#python3 RunsOnBoot.py
python3 SequencerMain.py
