import glob
import os

read_files = glob.glob("text*.txt")

with open("result.txt", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())
	    os.remove(f)
