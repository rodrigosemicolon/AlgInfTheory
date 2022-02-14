# G12

Group 12

# Members

Rodrigo Ferreira, rodrigosemicolon, rodrigo.nas.aulas@gmail.com, 104737

Diogo Almeida, dioalmeida, doalmeida94@gmail.com, 104601

# Assignment 1
## How to run
Tested with python3.6 and above

Simply execute either modules on the console, like so(considering the src folder as the starting point):
```sh
#fcm.py
python fcm.py -k 2 -a 0.4 -p "../example/example.txt"

#generator.py
python generator.py -k 2 -a 0.5 -l 50 -p "../example/example.txt" -pr "as"
```
For fcm.py there are 3 arguments:
    
    k: Context size;
    a: Alpha smoothing parameter;
    p: Path to text file.
    
    or...
    h: Available options and descriptions
    
For generator.py there are 6 arguments:
    
    k: Context size;
    a: Alpha smoothing parameter;
    p: Path to text file;
    l: Length of generated text;
    pr: Starting initial context.
    f: Force hardcoded seed.(Just param is needed, no value)
    
    or...
    h: Available options and descriptions
    
If there are no arguments or missing arguments when executing the script it will be used default values, with:
    
    f= False
    k= 3;
    a= 0;
    p= "../example/example2.txt";
    l = 200;
    prior = "god".
    
# Assignment 2
## How to run
Tested with python3.6 and above

Simply execute either modules on the console, like so(considering the src folder as the starting point):
```sh
# note that its important to have the "/" at the end of the path when the argument is a folder path
# language.py will return the estimated total amount of bits needed to compress\desribe the target give a reference model.
python language.py -k 4 -a 0.001 -tp "../targets/test.txt" -mp "../models/pt.txt"

# recognizer.py will identify the language of a target text document given reference models. 
# If the references have not yet been concatenated into one document(use for newly added references)
python recognizer.py -k 3 -a 0.001 -tp "../targets/test.txt" -mp "../models/" -rp "../references/"

# If the references have already been concatenated into one document(no new references)
python recognizer.py -k 3 -a 0.001 -tp "../targets/test.txt" -mp "../models/"

# langsegments.py will detect foreignisms or variations in language on a given target. 
python langsegments.py -k 4 -a 0.001 -tp "../targets/test.txt" -mp "../models/"
```


For language.py there are 4 arguments:
    
    k: Context size.
    a: Alpha smoothing parameter.
    tp: Path to specific target text file.
    mp: Path to specific model text file.
    
    or...
    h: Available options and descriptions.

For recognizer.py there are 5 arguments:
    
    k: Context size.
    a: Alpha smoothing parameter.
    tp: Path to specific target text file.
    mp: Path to the folder containing the models.
    rp: Path to a folder containing reference folders which contain texts that will make up models (optional).
    
    or...
    h: Available options and descriptions.

For langsegments.py there are 7 arguments:
    
    k: Context size.
    a: Alpha smoothing parameter.
    tp: Path to specific target text file.
    mp: Path to the folder containing the models.
    rp: Path to a folder containing reference folders which contain texts that will make up models (optional).
    sg: Display the results visually if set to 1 (optional).
    fw: Weight used in the low pass filter (optional).
    
    or...
    h: Available options and descriptions
    
# Assignment 3


# Builder
It's important that all code is executed having the terminal in the same folder as this readme file.
First, right after downloading everything, the user should run the structure_songs.py like so:

	python src/structure_songs.py

this builds the songs folder to allow the user to add new songs to the database

to add songs to the database, simply add them to the songs folder, in the respective genre folder or "other" if you're not sure.
after adding the files run the builder.py, without parameters it will run with the best combination we found, though the parameters can be specified

    #(our combination) 
    python src/builder.py

    #(user combination) 
    python src/builder.py -WS [value] -SH [value] -NF [value] -DS [value]

parameters:

		-WS window size (default 4096);
		-SH shift size (default 128);
		-DS downsampling (default 4);
		-NF number of frequencies (default 4);


# Audio

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

# Shazam

once you have built your database, you can start querying samples of songs.

we recommend that you always insert your target in the target folder to avoid possible errors (the corresponding freqs file will always be in /target/).
then run:

    #(in case you built the database with our parameters)	
    python src/shazam.py -TRG [targetpath] -CMP [compressor to be used]
    
    #(if you used your own parameters, use the same here)	
    python src/shazam.py -WS [value] -SH [value] -NF [value] -DS [value] -TRG [targetpath] -CMP [compressor to be used]
    
    #the CMP parameter accepts: "lzma","lzma_legacy","bz2","zlib","gzip"


# Notes

the freqs folder comes with the freqs built from our songs using our best combination of parameters.
there are some wav files in the target folder that can be used for testing.
after building the database it deletes the songs that were used to build the freqs to prevent them from being built each time