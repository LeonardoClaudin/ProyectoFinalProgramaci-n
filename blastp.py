#usr/bin/env python3
# -*- coding: UTF-8 -*-
# MODULO 3: BLASTP y filtro por identity y coverage

import sys
import os
import subprocess
import shutil

def funcion_blast(file):

    position = file.find(".")
    name = file[:position]

    blastp = subprocess.run(["blastp", "-query", file, "-db", "multifasta.fa", "-evalue", "0.00001", "-outfmt", "6 sseqid sseq qseqid qseq pident qcovs evalue", "-out", str(name)+"_result.fasta"])

    os.remove(file)

    return()

def seleccion_blastp(file, identity, coverage, path):

    position = file.find("_blastp")
    name = file[:position]
    new_name = name+"_filtrado.fasta"

    with open(new_name, "a") as outfile:
        with open(file, "r") as f:
            lineas = f.readlines()
            for linea in lineas:
                b = linea.split("\t")
                ident = b[4]
                cov = b[5]
                if ident > identity and cov > coverage:
                    outfile.write(">"+b[0]+"\n"+b[1]+"\n")

    f.close()
    outfile.close()
    os.remove(file)

    cwd = os.getcwd()
    ini_path = os.path.join(cwd, new_name)
    shutil.copy(ini_path, path)

    return()




