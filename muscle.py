#usr/bin/env python3
# -*- coding: UTF-8 -*-
# MODULO 4: MUSCLE

import sys
import os
import subprocess
import shutil

def input_muscle(query, file, i):
    cwd = os.getcwd()
    pathi = os.path.join(query, file)
    pathf = os.path.join(cwd, file)
    shutil.copy(pathi, pathf)
    with open(pathf, "r") as f:
        lines = f.read()
        for filename in os.listdir(cwd):
            if filename.endswith(str(i)+"_filtrado.fasta"):
                with open(filename, "a") as outfile:
                    outfile.write(lines)

    os.remove(pathf)
    return()

def funcion_muscle(file):
    pos = file.find("_filtrado")
    name = file[:pos]
    out_file = name+"_muscle.fa"
    print("Alignment is running...")

    try:
        alignment = subprocess.run(["muscle", "-in", file, "-out", out_file])
    except:
        print("Error: alignment error")


    output_tree = name+"_muscle_tree.nw"
    try:
        muscle_tree = subprocess.run(["muscle", "-maketree", "-in", out_file, "-out", output_tree, "-cluster", "neighborjoining"])
    except:
        print("Error in -maketree statement")

    os.remove(file)
    return(alignment, muscle_tree)






