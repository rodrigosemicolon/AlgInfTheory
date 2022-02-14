Assignment done by: Diogo Almeida, Rodrigo Ferreira
The program was made and tested with python 3.9, it was implemented and tested on windows throughout the whole process and later tested on linux, it should work on both.
Some problems were found on linux which were solved by giving getmaxfreqs execution permissions. 
If any other problems with GetMaxFreqs are found, the user can substitute the executable by his own as long as they have the same exact name and path (inserted in the GetMaxFreqs/bin/ folder).
It's important that all code is executed having the terminal in the same folder as this readme file.
First, right after downloading everything, the user should run the structure_songs.py like so:

	python src/structure_songs.py

this builds the songs folder to allow the user to add new songs to the database

to add songs to the database, simply add them to the songs folder, in the respective genre folder or "other" if you're not sure.
after adding the files run the builder.py, without parameters it will run with the best combination we found, though the parameters can be specified

(our combination) python src/builder.py
(user combination) python src/builder.py -WS [value] -SH [value] -NF [value] -DS [value]
parameters:
		-WS window size (default 4096);
		-SH shift size (default 128);
		-DS downsampling (default 4);
		-NF number of frequencies (default 4);

####################################################################################################################################################

our audio.py allows for some audio file manipulation:
the order of the parameters is important here
cut a section of a song with -trim:
	python src/audio.py -trim [targetpath] [finalfilename] [seconds to start cutting from] [seconds to end cutting]

convert a files sample rate to be compatible with getmaxfreqs (this is done automatically both in builder and shazam, no need to run manually):
	python src/audio.py -convert [targetpath] [finalfilename] [1-delete original,0-keep original]

concatenate several audio files:
	python src/audio.py -cat [finalfilename] [file to be concatenated] [other file to be concatenated] [other file to be concatenated]...

add noise to an audio file:
	python src/audio.py -noise [targetpath] [finalfilename] [float 0 to 1 determining level of noise to be added]

self concatenate a song to match the average length of a song in the database:
	python src/audio.py -selfcat [targetpath]

####################################################################################################################################################
once you have built your database, you can start querying samples of songs.

we recommend that you always insert your target in the target folder to avoid possible errors (the corresponding freqs file will always be in /target/).
then run:

(in case you built the database with our parameters)	python src/shazam.py -TRG [targetpath] -CMP [compressor to be used]
(if you used your own parameters, use the same here)	python src/shazam.py -WS [value] -SH [value] -NF [value] -DS [value] -TRG [targetpath] -CMP [compressor to be used]
the CMP parameter accepts: "lzma","lzma_legacy","bz2","zlib","gzip"


####################################################################################################################################################

the freqs folder comes with the freqs built from our songs using our best combination of parameters.
there are some wav files in the target folder that can be used for testing.
after building the database it deletes the songs that were used to build the freqs to prevent them from being built each time