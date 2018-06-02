#!/usr/bin/env python

import pygame

def main():
	pygame.init()
	pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
	#Initialize the mixer module for Sound loading and playback. The default arguments can be overridden to provide specific audio mixing. Keyword arguments are accepted. For backward compatibility where an argument is set zero the default value is used (possible changed by a pre_init call).
	#The size argument represents how many bits are used for each audio sample. If the value is negative then signed sample values will be used. Positive values mean unsigned audio samples will be used. An invalid value raises an exception.
	#The channels argument is used to specify whether to use mono or stereo. 1 for mono and 2 for stereo. No other values are supported (negative values are treated as 1, values greater than 2 as 2).
	#The buffer argument controls the number of internal samples used in the sound mixer. The default value should work for most cases. It can be lowered to reduce latency, but sound dropout may occur. It can be raised to larger values to ensure playback never skips, but it will impose latency on sound playback. The buffer size must be a power of two (if not it is rounded up to the next nearest power of 2).
	#Some platforms require the pygame.mixerpygame module for loading and playing sounds module to be initialized after the display modules have initialized. The top level pygame.init() takes care of this automatically, but cannot pass any arguments to the mixer init. To solve this, mixer has a function pygame.mixer.pre_init() to set the proper defaults before the toplevel init is used.
	#It is safe to call this more than once, but after the mixer is initialized you cannot change the playback arguments without first calling pygame.mixer.quit().



	effect = pygame.mixer.Sound('pysynth_anthem.wav')
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
		effect.play()

if __name__ == "__main__":
	main()
