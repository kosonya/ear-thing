#!/usr/bin/env python2.7

import os
import pygame
import sys

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

class PianoThing(object):
	def __init__(self, sample_path="my_samples"):
		self.sample_path = sample_path

	def load_samples(self):
		octaves = [1, 2, 3, 4, 5, 6, 7]
		all_notes = [n + str(o) for n in NOTES for o in octaves]
		all_notes = ["A0", "A#0", "B"] + all_notes + ["C8"]
		self.samples = dict()
		for note in all_notes:
			path = os.path.join(self.sample_path, note + ".wav")
			sample = pygame.mixer.Sound(path)
			self.samples[note] = sample
	



def main():
	size = (800, 600)
	pygame.init()
	pygame.mixer.init(frequency=22050, size=-16, channels=12, buffer=512)
	screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)
	pygame.display.set_caption(u"Piano thing")
	pt = PianoThing()
	pt.load_samples()
	key_mapping = {pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C",
			pygame.K_d: "D", pygame.K_e: "E", pygame.K_f: "F",
			pygame.K_g: "G"}
	inverse_key_mapping = {key_mapping[n]: n for n in key_mapping}
	channels = {key_mapping.items()[i][1]: pygame.mixer.Channel(i) for i in xrange(7)}
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			elif event.type == pygame.KEYDOWN:
				if event.key in key_mapping:
					channels[key_mapping[event.key]].play(pt.samples[key_mapping[event.key]+"4"], loops=0, maxtime=0, fade_ms=0)
			elif event.type == pygame.KEYUP:
				if event.key in key_mapping:
					channels[key_mapping[event.key]].stop()
		pygame.display.flip()
	

if __name__ == "__main__":
	main()
