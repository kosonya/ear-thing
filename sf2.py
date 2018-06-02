#!/usr/bin/env python

import numpy
import pygame
import tempfile



from sf2utils.sf2parse import Sf2File
with open('Kawai Grand Piano.sf2', 'rb') as sf2_file:
	sf2 = Sf2File(sf2_file)
	print sf2.pretty_print()
	for s in sf2.samples:
		print s
	rsl = sf2.samples[0].raw_sample_data
	rsr = sf2.samples[1].raw_sample_data
	temp = tempfile.TemporaryFile()
	temp.write(rsl)
	raw_sample_l = numpy.fromfile(temp, dtype=numpy.uint16)
	temp.close()
	temp = tempfile.TemporaryFile()
	temp.write(rsr)
	raw_sample_r = numpy.fromfile(temp, dtype=numpy.uint16)
	temp.close()


	raw_sample = numpy.column_stack((raw_sample_l, raw_sample_r))
	print raw_sample
	pygame.init()
	pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
	sound = pygame.sndarray.make_sound(raw_sample)
	sound.play()
	sound.play()
	effect = pygame.mixer.Sound('pysynth_anthem.wav')

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
		sound.play()

	
