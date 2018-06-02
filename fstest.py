#import fluidsynth   
#import time
import sys
from mingus.midi import fluidsynth   
fluidsynth.init('/usr/share/sounds/sf2/FluidR3_GM.sf2',"alsa")
fluidsynth.play_Note(64,1,10)
sys.exit(0)
fs = fluidsynth.Synth()
fs.start()

sfid = fs.sfload("example.sf2")
fs.program_select(0, sfid, 0, 0)

fs.noteon(0, 60, 30)
fs.noteon(0, 67, 30)
fs.noteon(0, 76, 30)

time.sleep(1.0)

fs.noteoff(0, 60)
fs.noteoff(0, 67)
fs.noteoff(0, 76)

time.sleep(1.0)

fs.delete()
