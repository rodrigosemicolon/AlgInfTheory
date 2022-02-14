import os

def songs_folder():
    """
    Create the songs folder and its genre folders.
    """
    prefix="songs/"
    genres=["rock/","metal/","edm/","classical/","hip hop/", "jazz/","pop/", "other/"]
    if not os.path.isdir(prefix):
        os.mkdir(prefix)

    for genre in genres:
        if not os.path.isdir(prefix + genre):
            os.mkdir(prefix + genre)

if __name__=="__main__":
    songs_folder()