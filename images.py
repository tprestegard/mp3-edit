import subprocess, pdb

def set_album_art(song, img_filename):
	
	# Check img_filename for correct endings.
	# jpg/jpeg, png, gif (upper or lower is OK).
	if True:
		pass
	else:
		raise TypeError("Image should be a jpg, png, or gif.")

	# Command to run lame.
	lame_cmd = "lame --ti %s %s" % (img_filename, song.filename)


	subprocess.check_output(
