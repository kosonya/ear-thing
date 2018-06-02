#!/usr/bin/env python2.7

import os
import pygame
import sys

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
OCTAVES = [1, 2, 3, 4, 5, 6, 7]
ALL_NOTES = [n + str(o) for n in NOTES for o in OCTAVES]
ALL_NOTES = ["A0", "A#0", "B"] + ALL_NOTES + ["C8"]

class PianoThing(object):
	def __init__(self, sample_path="my_samples", init_mixer=True, standalone=True):
		self.sample_path = sample_path
		self.load_samples()
		self.standalone = standalone
		if self.standalone:
			self.init_standalone()
		if init_mixer:
			pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
			pygame.mixer.set_num_channels(88)
		self.channels = {ALL_NOTES[i]: pygame.mixer.Channel(i) for i in xrange(88)}

	def init_standalone(self):
		self.standalone_key_mapping = {pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C",
			pygame.K_d: "D", pygame.K_e: "E", pygame.K_f: "F",
			pygame.K_g: "G"}
		self.standalone_inverse_key_mapping = {self.standalone_key_mapping[n]: n for n in self.standalone_key_mapping}

	def load_samples(self):
		self.samples = dict()
		for note in ALL_NOTES:
			path = os.path.join(self.sample_path, note + ".wav")
			sample = pygame.mixer.Sound(path)
			self.samples[note] = sample

	def play_note(self, note, octave):
		n_o = str(note) + str(octave)
		self.channels[n_o].play(self.samples[n_o], loops=0, maxtime=0, fade_ms=0)

	def stop_note(self, note, octave):
		n_o = str(note) + str(octave)
		self.channels[n_o].stop()

	def stop_all_notes(self):
		for channel in self.channels.values():
			channel.stop()
	
	def stop_all_notes_not_held(self):
		keys = pygame.key.get_pressed()
		for note in ALL_NOTES:
			if "4" in note and "#" not in note:
				only_note = note[:-1]
				key = self.standalone_inverse_key_mapping[only_note]
				if keys[key]:
					pass
				else:
					self.channels[note].stop()
			else:
				self.channels[note].stop()


	def process_event_standalone(self, event):	
		if event.type == pygame.KEYDOWN:
			if event.key in self.standalone_key_mapping:
				self.play_note(self.standalone_key_mapping[event.key], 4)
		elif event.type == pygame.KEYUP:
			keys = pygame.key.get_pressed()
			if not keys[pygame.K_SPACE]:
				if event.key in self.standalone_key_mapping:
					self.stop_note(self.standalone_key_mapping[event.key], 4)
			if event.key == pygame.K_SPACE:
				self.stop_all_notes_not_held()



def step_to_note(step):
	return NOTES[step]

def note_to_step(note):
	for i in xrange(12):
		if NOTES[i] == note:
			return i

def note_and_octave_to_global_step(note, octave):
	n_o = str(note) + str(octave)
	for i in xrange(88):
		if ALL_NOTES[i] == n_o:
			return i

def global_step_to_note_and_octave(global_step):
	n_o = ALL_NOTES[global_step]
	note = n_o[:-1]
	octave = int(n_o[-1])
	return note, octave
	
	



def main():
	size = (800, 600)
	pygame.init()
	
	screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)
	pygame.display.set_caption(u"Piano thing")
	pt = PianoThing()


	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			pt.process_event_standalone(event)

		pygame.display.flip()
	

if __name__ == "__main__":
	main()
