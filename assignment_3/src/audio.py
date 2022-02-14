import sox
import sys
import re
import os
import subprocess


def trim_audio(path: str,desiredPath: str,beg: int, end: int)->None:
    """
    Trim an audio file to a smaller one

    Args:
        path (str): path of the original file.
        desiredPath (str): path of the destination file.
        beg (int): seconds to start trimming from.
        end (int): seconds to end trimming from.
    """
    tfm = sox.Transformer()
    tfm.trim(beg,end)
    tfm.build_file(path, desiredPath)

def self_cat(path: str)->None:
    """
    Self concatenates a file until its close to the average length of a song in the database (4 minutes) 

    Args:
        path (str): path to the file to be self concatenated.
    """
    final_path = re.split(".wav",path,flags=re.IGNORECASE)[0]
    file_len = sox.file_info.num_samples(path)/44100
    repeat = int((60*4)//file_len)
    cat_list = []
    for _ in range(repeat):
        cat_list.append(path)
    concatenate_audio(cat_list,final_path + "_selfcat.wav")
    

def concatenate_audio(paths_list: str, desiredPath: str)->None:
    """
    Concatenate a list of audio files together.

    Args:
        paths_list (str): list of audio files to be concatenated.
        desiredPath (str): destination path for resulting file.
    """
    if os.path.isfile(desiredPath):
        os.remove(desiredPath)
    cbn = sox.Combiner()
    cbn.convert(samplerate=44100,n_channels=2)
    file_extensions = [k.split(".")[-1] for k in paths_list]
    cbn.set_input_format(file_type=file_extensions)
    cbn.build(paths_list,desiredPath,'concatenate')
    
def convert_to_format(path: str,desiredPath: str, removeOriginal: bool)->None:
    """
    Convert an audio file to the appropriate sample rate and number of channels to be used by getmaxfreqs later

    Args:
        path (str): original file path.
        desiredPath (str): destination file path.
        removeOriginal (bool): true to remove original file, false otherwise.
    """
    tfm = sox.Transformer()
    song_format =path.split(".")[-1]
    tfm.set_input_format(song_format.lower())
    tfm.set_output_format(file_type="wav",rate=44100,channels=2)
    tfm.build_file(path,desiredPath)
    if removeOriginal:
        os.remove(path)
    
def add_whitenoise(targetPath: str,destPath: str,volume: float)->None:
    """
    Add noise to an existing file, creating a new file

    Args:
        targetPath (str): path to the original file.
        destPath (str): path of the resulting file.
        volume (float): volume of the noise to add.
    """

    cmd1 = 'sox "' + targetPath + '" target/noise.wav synth whitenoise vol ' + str(volume)
    cmd2 = 'sox -m "' + targetPath  + '" target/noise.wav "' + destPath + '"' 
    subprocess.run(cmd1,shell=True)
    subprocess.run(cmd2,shell=True)
    os.remove("target/noise.wav")

if __name__ == "__main__":
    
    args = sys.argv
    
    if (len(args)==2 and args[1]=="-h") or len(args)==1:
        print("Possible operations:\n")
        print("-trim <targetfile> <newfilename> <beginning seconds> <ending seconds>\n")
        print("-cat <newfilename> <filetocat1> <filetocat2> <...>\n")
        print("-selfcat <targetfile>\n")
        print("-convert <targetfile> <newfilename> <True to delete original, false otherwise>\n")
        print("-noise <targetfile> <newfilename> <volume float (0<n<1)>\n")
        sys.exit()
    
    if args[1] == "-trim":

        targetPath=args[2]
        desiredPath = args[3]
        beginning=int(args[4])
        ending=int(args[5])

        if ending<=beginning:
            print("invalid beginning and ending")
            sys.exit()
        else:
            trim_audio(targetPath,desiredPath,beginning,ending)
    
    if args[1] == "-convert":
    
        targetPath=args[2]
        desiredPath = args[3]
        remove_original = bool(args[4]) 
        convert_to_format(targetPath,desiredPath, remove_original)
    
    if args[1] == "-cat":
    
        desiredPath=args[2]
        path_list=args[3:] 
        concatenate_audio(path_list,desiredPath)

    if args[1] == "-noise":
        targetPath=args[2]
        desiredPath=args[3]
        vol = float(args[4])
        
        if vol<=0:
            print("invalid volume value")
            sys.exit()
        add_whitenoise(targetPath,desiredPath,vol)
    if args[1] == "-selfcat":
        desiredPath=args[2]
        self_cat(desiredPath)