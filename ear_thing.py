#!/usr/bin/env python

import pygame
import piano_thing
import sys
import random
import csv
import datetime
import os.path

EAR_OCTAVES = [2, 3, 4, 5, 6]

class NoteGuesser(object):
	def __init__(self, pianothing):
		self.pianothing = pianothing
		self.chosen_n_o = self.choose_note()
		self.rounds = 0
		self.guesses = []
		self.filename = os.path.join("logs", datetime.date.today().strftime("%Y-%m-%d") + ".csv")


	def choose_note(self):
		note = random.choice(piano_thing.NOTES)
		octave = random.choice(EAR_OCTAVES)
		n_o = str(note) + str(octave)
		return n_o

	def check_guess(self, note):
		only_note = note[:-1]
		octave = int(note[-1])
		self.pianothing.remove_all_from_playing()
		if note == self.chosen_n_o:
			self.pianothing.add_to_playing(only_note, octave, color=(1,255,1))
		else:
			self.pianothing.add_to_playing(only_note, octave, color=(255,0,0))
			self.pianothing.highlight_note(self.chosen_n_o, color=(1,255,1))
		print "Played", self.chosen_n_o, "guessed", note
		self.guesses.append((self.chosen_n_o, note))
		self.write_csv()
		self.rounds += 1
		self.chosen_n_o = self.choose_note()

	def process_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				note = self.chosen_n_o[:-1]
				octave = int(self.chosen_n_o[-1])
				self.pianothing.play_note(note, octave, maxtime=1000)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			note = self.pianothing.check_mouse_click_key(event.pos)
			if note:
				self.check_guess(note)
		elif event.type == pygame.MOUSEBUTTONUP:
			self.pianothing.remove_all_from_playing()
			self.pianothing.unhighlight_all()

	def write_csv(self):
		with open(self.filename, "wb") as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar="'", quoting=csv.QUOTE_ALL)
    			writer.writerow(["played", "guessed"])
    			for p, g in self.guesses:
				writer.writerow([p, g])

	


def main():
	size = (1700, 1200)
	pygame.init()
	
	screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)
	pygame.display.set_caption(u"Ear thing")
	pt = piano_thing.PianoThing(screen_size = size)
	ng = NoteGuesser(pt)

	screen.fill((255,255,255))
	screen.set_colorkey((0,0,255))


	while True:
		screen.fill((255,255,255))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			ng.process_event(event)
		if ng.rounds > 50:
			sys.exit(0)

		pt.render(screen)
		pygame.display.flip()
	

if __name__ == "__main__":
	main()
