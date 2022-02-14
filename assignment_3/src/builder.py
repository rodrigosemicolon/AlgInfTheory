import lzma
import gzip
import bz2
import zlib
import os
import subprocess
import sox
import sys
import re
from audio import convert_to_format


WS=4096
NF=4
SH=128
DS=4

def get_freqs(pathname):
    """Convert all songs in musics folder to freqs files in freqs folder

    Args:
        pathname (str): path to the musics folder
    """
    for d in os.listdir(pathname):
        directory  = pathname+d +"/"
        if os.path.isdir(directory):
            print("getting " + directory +" freqs..." )
            check_sample_rates(directory)
            for file in os.listdir(directory):
                final_path = d + "/" + re.split(".wav", file, flags=re.IGNORECASE)[0]
                
                
               
                cmd = '"./GetMaxFreqs/bin/GetMaxFreqs"  -ws ' +str(WS) +' -nf '+str(NF)+' -ds '+str(DS)+ ' -sh ' +str(SH) + ' -w "freqs/'+ final_path + '.freqs"' + ' "' + directory + file+'"'             
                
                
                
                subprocess.run(cmd,shell=True)
                
                os.remove(directory + file)


def check_sample_rates(pathname:str):
    """
    Check for every song in the folder if its sample rate is compatible with getmaxfreqs and convert it if necessary

    Args:
        pathname (str): path to the folder containing the songs
    """

    for file in os.listdir(pathname):
        sample_rate = sox.file_info.sample_rate(pathname + file)
        if sample_rate != 44100:
            print("invalid sample rate of " + str(sample_rate) + " on " + file + "\nConverting...\n")
            convert_to_format(pathname + file,pathname+"temp_" + file , True)
            os.rename(pathname + "temp_" + file, pathname + file)



def freq_folders(): 
    """
    Creates any folder missing in freqs/ to match the songs/ folder structure
    """
    for d in os.listdir("songs/"):
        freqs_prefix="freqs/"
        if not os.path.isdir(freqs_prefix+d):
            os.mkdir(freqs_prefix+d)

if __name__ == "__main__":
   

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
           
    if len(args) == 2 and args[len(args) - 1] == "-h":
        print("Use:\n\n"
            
              "WS: Window size to use collecting freqs;\n"
              "SH: Shift to use collecting freqs;\n"
              "NF: Number of frequencies per window when collecting freqs;\n"
              "DS: Downsampling to be applied collecting freqs;\n"
              )
        sys.exit()
    
    freq_folders()
    get_freqs("songs/")
