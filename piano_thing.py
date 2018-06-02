#!/usr/bin/env python2.7

import os
import pygame
import sys

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
OCTAVES = [1, 2, 3, 4, 5, 6, 7]
ALL_NOTES = [n + str(o) for o in OCTAVES for n in NOTES ]
ALL_NOTES = ["A0", "A#0", "B0"] + ALL_NOTES + ["C8"]

class PianoThing(object):
	def __init__(self, screen_size, sample_path="my_samples", init_mixer=True, standalone=True):
		self.sample_path = sample_path
		self.load_samples()
		self.standalone = standalone
		if self.standalone:
			self.init_standalone()
		if init_mixer:
			pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
			pygame.mixer.set_num_channels(88)
		self.channels = {ALL_NOTES[i]: pygame.mixer.Channel(i) for i in xrange(88)}
		self.screen_size = screen_size
		self.white_key_size = 30, 120
		self.black_key_size = 15, 80
		self.draw_white_notes()
		self.draw_black_notes()
		self.playing_notes = set()
		self.mouseheld = set()


	def render(self, screen):
		screen.blit(self.white_notes_surface, (0,0))
		screen.blit(self.black_notes_surface, (0,0))

	def check_mouse_click_key(self, position):
		horz, vert = position
		for note, rect in self.black_note_rects.items():
			if rect.collidepoint(position):
				return note
		for note, rect in self.white_note_rects.items():
			if rect.collidepoint(position):
				return note
		return None

	def draw_white_notes(self, top_offset = 100, left_offset = 50):
		self.white_notes_surface = pygame.Surface(self.screen_size)
		self.white_notes_surface.fill((0,255,0))
		self.white_notes_surface.set_colorkey((0,255,0))
		cur_key = 0
		self.white_note_rects = dict()
		cur_left_offset = left_offset
		for note in ALL_NOTES:
			if "#" in note:
				continue
			rect = self.draw_white_key(self.white_notes_surface, self.white_key_size, top_offset, cur_left_offset)
			cur_key += 1
			self.white_note_rects[note] = rect
			if note == "C4":
				pygame.draw.circle(self.white_notes_surface, (0,0,0), (cur_left_offset + self.white_key_size[0]/2, top_offset + int(self.white_key_size[1]*0.8))  , 3, 0)
			cur_left_offset += self.white_key_size[0]


	def draw_black_notes(self, top_offset = 100, left_offset = 50):
		self.black_notes_surface = pygame.Surface(self.screen_size)
		self.black_notes_surface.fill((0,255,0))
		self.black_notes_surface.set_colorkey((0,255,0))
		cur_note = 0
		cur_black_key = 0
		self.black_note_rects = dict()
		cur_offset = left_offset
		for note in ALL_NOTES:
			if "#" in note:
				rect = self.draw_black_key(self.black_notes_surface, self.black_key_size, top_offset, cur_offset - self.black_key_size[0]/2)
				self.black_note_rects[note] = rect
				cur_black_key += 1
			else:
				cur_offset += self.white_key_size[0]
			cur_note += 1



	def draw_black_key(self, surface, key_size, top, left):
		rect = pygame.Rect((left, top), key_size)
		pygame.draw.rect(surface, (0,0,0), rect, 0)
		return rect

	def draw_white_key(self, surface, key_size, top, left):
		rect = pygame.Rect((left, top), key_size)
		pygame.draw.rect(surface, (255,255,255), rect, 0)
		pygame.draw.rect(surface, (0,0,0), rect, 2)
		return rect

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

	def add_to_playing(self, note, octave):
		n_o = str(note) + str(octave)
		self.playing_notes.add(n_o)
		self.play_note(note, octave)

	def remove_from_playing(self, note, octave):
		n_o = str(note) + str(octave)
		if n_o in self.playing_notes:
			self.playing_notes.remove(n_o)
		self.stop_note(note, octave)
	
	def stop_all_notes_not_held(self):
		keys = pygame.key.get_pressed()
		for note in ALL_NOTES:
			if note in self.mouseheld:
				continue
			only_note = note[:-1]
			octave = int(note[-1])
			if "4" in note and "#" not in note:
				key = self.standalone_inverse_key_mapping[only_note]
				if keys[key]:
					pass
				else:
					self.remove_from_playing(only_note, octave)
			else:
				self.remove_from_playing(only_note, octave)


	def process_event_standalone(self, event):	
		if event.type == pygame.KEYDOWN:
			if event.key in self.standalone_key_mapping:
				self.add_to_playing(self.standalone_key_mapping[event.key], 4)
		elif event.type == pygame.KEYUP:
			keys = pygame.key.get_pressed()
			if not keys[pygame.K_SPACE]:
				if event.key in self.standalone_key_mapping:
					self.remove_from_playing(self.standalone_key_mapping[event.key], 4)
			if event.key == pygame.K_SPACE:
				self.stop_all_notes_not_held()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			note = self.check_mouse_click_key(event.pos)
			if note:
				self.mouseheld.add(note)
				only_note = note[:-1]
				octave = int(note[-1])
				self.add_to_playing(only_note, octave)
		elif event.type == pygame.MOUSEBUTTONUP:
			keys = pygame.key.get_pressed()
			for note in self.mouseheld:
				only_note = note[:-1]
				octave = int(note[-1])
				if not keys[pygame.K_SPACE]:
					self.remove_from_playing(only_note, octave)
			self.mouseheld = set()


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
	size = (1700, 600)
	pygame.init()
	
	screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)
	pygame.display.set_caption(u"Piano thing")
	pt = PianoThing(screen_size = size)

	screen.fill((255,255,255))
	screen.set_colorkey((0,255,0))
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			pt.process_event_standalone(event)

		pt.render(screen)
		pygame.display.flip()
	

if __name__ == "__main__":
	main()
