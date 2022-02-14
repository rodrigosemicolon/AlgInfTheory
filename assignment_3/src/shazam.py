from builder import WS, DS, NF, SH
from audio import convert_to_format, concatenate_audio
import re
import sox
import subprocess
import os
import sys

###Compressors
import gzip
import lzma
import bz2
import zlib


def get_ncd(src_file, db_file):    
    x = open(src_file, 'rb').read()  # file 1 of any type
    y = open(db_file, 'rb').read()  # file 2 of the same type as file 1
    
    x_y = x + y  # the concatenation of files
    
    if compressor == "bz2":
        cmp_x = bz2.compress(x)  # compress file 1
        cmp_y = bz2.compress(y)  # compress file 2
        cmp_x_y = bz2.compress(x_y)
    elif compressor=="lzma":
        cmp_x = lzma.compress(x)  # compress file 1
        cmp_y = lzma.compress(y)  # compress file 2
        cmp_x_y = lzma.compress(x_y)
    elif compressor=="zlib":       
        cmp_x = zlib.compress(x)  # compress file 1
        cmp_y = zlib.compress(y)  # compress file 2
        cmp_x_y = zlib.compress(x_y)  # compress file concatenated
    elif compressor=="gzip":
        cmp_x = gzip.compress(x)  # compress file 1
        cmp_y = gzip.compress(y)  # compress file 2
        cmp_x_y = gzip.compress(x_y)
    elif compressor == "lzma_legacy":
        cmp_x = lzma.compress(x,format=lzma.FORMAT_ALONE)  # compress file 1
        cmp_y = lzma.compress(y,format=lzma.FORMAT_ALONE)  # compress file 2
        cmp_x_y = lzma.compress(x_y, format=lzma.FORMAT_ALONE)
    
    return (len(cmp_x_y) - min(len(cmp_x), len(cmp_y))) / max(len(cmp_x), len(cmp_y))
    

      
def get_target_freq(filepath:str)->str:
    """Convert target file to freqs

    Args:
        path (str): path to the target file

    Returns:
        str: path to converted target file
    """
    filename = re.split("/",filepath)[-1]
    path = "target/" + filename
    final_path = re.split(".wav",path,flags=re.IGNORECASE)[0]
    sample_rate = sox.file_info.sample_rate(path)
    if sample_rate != 44100:
        print("invalid sample rate of " + str(sample_rate) + " on " + path + "\nConverting...\n")
        convert_to_format(path,"target/temp_" + filename , True)
        os.rename("target/temp_" + filename, path)
    
    cmd = '"./GetMaxFreqs/bin/GetMaxFreqs"  -ws '+str(WS)+' -nf '+str(NF)  +' -ds '+str(DS)+' -sh '+str(SH) + ' -w "' +final_path + '.freqs"' + ' "' +final_path+ ".wav"+'"' 
    
    subprocess.run(cmd, shell=True)
    
    return final_path + ".freqs"


def check_db(freqtargetpath:str)->(dict,dict):
    """Compares a target freqs file to all the freqs files in the freqs folder

    Args:
        freqtargetpath (str): path to target freqs file

    Returns:
        dict: dictionary containing the score of each file in freqs folder and dictionary containing the scores per folder(genre)
    """
    scores={}
    freqspath="freqs/"
    score_genres={}
    for d in os.listdir(freqspath):
        
        path = freqspath + d + "/"
        if os.path.isdir(path):
           
            score_genres[d]=[]
            
            for file in os.listdir(path):
                scores[file] = get_ncd(freqtargetpath,path+file)
                score_genres[d].append(scores[file])
    for genre in score_genres:
        if len(score_genres[genre])>0:
            score_genres[genre] = sum(score_genres[genre])/len(score_genres[genre])

    score_genres = {t[0]:t[1] for t in score_genres.items() if t[1]!=[]}       
    return scores,score_genres

def shazam(filePath:str)->(dict,dict):
    """
    Get the path to a file, get its signatures and compute the ncd of it with every song in the database

    Args:
        filePath (str): path to the target file.

    Returns:
        tuple: containing the scores of each song and each folder in 2 dictionaries.
    """
    freqpath=get_target_freq(filePath)
    results=check_db(freqpath)
    return results



def get_shazam(target:str)->None:
    """
    Main function that calls all the others required to guess a song.

    Args:
        target (str): path to the target audio file.
    """
    results = shazam(target)
    print("\nThe target was " + target)
    song_guesses = sorted(results[0].items(), key=lambda item: item[1])[:10]
    print("\nThe top 5 song guesses where:")
    i=1
    for song in song_guesses:
        print(str(i)+" " + str(song[0].split(".freqs")[0]) + ": " + str(song[1]))
        i+=1
    genre_guesses = sorted(results[1].items(), key=lambda item: item[1])
    print("\nThe target fits the following genres in order:")
    i=1
    for genre in genre_guesses:
        print(str(i)+" " + str(genre[0]) + ": " + str(genre[1]))
        i+=1







if __name__ == "__main__":
    t_def = False
    target=""
    compressor="bz2"
    args = sys.argv
    for i in range(len(args)):
        if i % 2 == 0:
            if args[i - 1] == "-WS":
                n = int(args[i])
                if n > 0:
                    WS=n
            elif args[i - 1] == "-SH":
                n = int(args[i])
                if n>0:
                    SH=n
            elif args[i - 1] == "-NF":
                n = int(args[i])
                if n>0:
                    NF=n
            elif args[i - 1] == "-DS":
                n = float(args[i])
                if n>=0:
                    DS=n
            elif args[i - 1] == "-TRG":
                n = args[i]
                if os.path.isfile(n):
                    target=n
                    t_def=True
            elif args[i - 1] == "-CMP":
                n = args[i]
                if n=="lzma" or n=="gzip" or n=="bz2" or n=="zlib" or n=="lzma_legacy":
                    compressor=n
            
    if len(args) == 2 and args[len(args) - 1] == "-h":
        print("Use:\n\n"
            "TRG: Name of the file to use as target(MANDATORY, must be in target folder);\n"
            "CMP: Name of the compressor to be used (gzip,lzma,lzma_legacy,bz2,zlib);\n"
            "WS: Window size to use collecting freqs;\n"
            "SH: Shift to use collecting freqs;\n"
            "NF: Number of frequencies per window when collecting freqs;\n"
            "DS: Downsampling to be applied collecting freqs;\n"
              )
        sys.exit()
    if t_def:    
        get_shazam(target)
    