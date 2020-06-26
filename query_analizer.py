#usr/bin/env python3
# -*- coding: UTF-8 -*-
# MODULO 2: Separa los querys del multifasta en fastas independientes
# y comprueba su formato

import os
import sys
import shutil

def multifasta_fasta(query, file):
    cwd = os.getcwd()
    current_path = os.path.join(cwd, query, file)
    with open(current_path, "r") as f: # Abrir el multifasta
        lineas = f.read()
        b = lineas.split(">") # Separar query
        for i in range(1, len(b)):
            new_filename = "Query_"+b[i][:4]+".fasta"
            with open(new_filename, "w") as outfile:
                outfile.write(">"+b[i])
            my_path = os.path.join(cwd, new_filename)
            output_path = os.path.join(cwd, query, new_filename)
            shutil.move(my_path, output_path) # Los muevo a la carpeta de querys
    return()

def comprobar_query(query, filename):
        direccion = os.path.join(query, filename)
        cwd = os.getcwd()
        pos = filename.find(".")
        name = filename[:pos]
        new_filename = name+"_blastp.fasta"
        new_dir = os.path.join(cwd, new_filename)
        file = open(direccion, "r")
        file2 = file.read()
        file.close()
        fasta = file2.count(">")
        if fasta == 0:
            print("ERROR: El archivo no es de formato FASTA")
            exit()
        else:
            shutil.copy(direccion, new_dir)

        return()

