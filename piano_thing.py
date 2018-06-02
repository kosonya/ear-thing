#!/usr/bin/env python2.7

import os

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

class PianoThing(object):
	def __init__(self):
		pass

	def load_samples(self):
		octaves = [1, 2, 3, 4, 5, 6, 7]
		all_notes = [n + str(o) for n in NOTES for o in octaves]
		print all_notes


def main():
	pt = PianoThing()
	pt.load_samples()

if __name__ == "__main__":
	main()
