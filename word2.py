import hashlib
import itertools
flag = 'wgmy{h3r3_1s_y0ur_XXXXXX_br0!}'

character = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

for i in itertools.product(character,repeat=6):
	if(hashlib.sha256(flag.replace("XXXXXX",''.join(i))).hexdigest() == "86775fe0718f57c5bcc3c32c198ece3e6a732406e3f32e3aa285059247da6652"):
		print "Found : " + flag.replace("XXXXXX",''.join(i))
		exit(0)
	else:
		print flag.replace("XXXXXX",''.join(i))
