#!/usr/bin/env python

import argparse
import csv
import piano_thing



def main():
	parser = argparse.ArgumentParser(description='Analyze ear thing logs')
	parser.add_argument("filename", type=str, nargs=1, help="file to analyze")
	args = parser.parse_args()
	
	guesses = []
	with open(args.filename[0], "rb") as csvfile:
		reader = csv.reader(csvfile, delimiter=",", quoting=csv.QUOTE_ALL)
		for row in reader:
			played, guessed = row
			played = played[1:-1]
			guessed = guessed[1:-1]
			if played == "played":
				continue
			guesses.append((played, guessed))

	print guesses

	print len(guesses), "samples"
	n = float(len(guesses))
	
	accuracy = 0.0
	accuracy_mod_12 = 0.0
	mean_absolute_distance = 0.0
	mean_absolute_distance_mod_12 = 0.0

	for played, guessed in guesses:
		played_octave = int(played[-1])
		guessed_octave = int(guessed[-1])
		played_note = played[:-1]
		guessed_note = guessed[:-1]

		played_step = piano_thing.note_to_step(played_note)
		guessed_step = piano_thing.note_to_step(guessed_note)

		played_global_step = piano_thing.note_and_octave_to_global_step(played_note, played_octave)
		guessed_global_step = piano_thing.note_and_octave_to_global_step(guessed_note, guessed_octave)

		if played == guessed:
			accuracy += 1.0
			print played, guessed
		if played_note == guessed_note:
			accuracy_mod_12 += 1
		mean_absolute_distance += abs(played_global_step - guessed_global_step)
		mean_absolute_distance_mod_12 += abs(played_step - guessed_step)

	accuracy = 100.0 * accuracy / n
	accuracy_mod_12 = 100.0 * accuracy_mod_12 / n
	mean_absolute_distance = 100.0 * mean_absolute_distance / n
	mean_absolute_distance_mod_12 = 100.0 * mean_absolute_distance_mod_12 / n

	print "Accuracy:", accuracy, "%"
	print "Accuracy mod 12:", accuracy_mod_12, "%"
	print "Mean absolute distance:", mean_absolute_distance
	print "Mean absolute distance mod 12:", mean_absolute_distance_mod_12

if __name__ == "__main__":
	main()
