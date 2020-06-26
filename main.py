#usr/bin/env python3
# -*- coding: UTF-8 -*-
#--------------------------------------------------------
#--------------------------------------------------------
import genbank_converter
import sys
import re
import shutil
import os
import re
from pathlib import Path

##1. Creación de la función de ayuda.
def help():
	print("\n"+"------------------------------------------------------------")
	print("\n"+"FIRST AID PANNEL. STAY CALM, HELP IS ON ITS WAY.")
	print("\n"+"------------------------------------------------------------")
	print("USAGE: python [PROYECTO_FINAL.py] [GENBANK] [QUERY] [IDENTITY] [COVERAGE]")
	print("\n"+"------------------------------------------------------------")
	print("USAGE GUIDE FOR EACH PLOT")
	print("[PROYECTO_FINAL.py]: folder containing every GenBanks desired to analyse")
	print("[GENBANK]: folder containing multifasta with every query sequence desired to analyse")
	print("-----------------------------------------------------------------")
	print("IMPORTANT: Each of the modules required for the Script must be in the same directory, including GenBanks and Query folder")
	print("-----------------------------------------------------------------")
	print("[IDENTITY]: numeric value")
	print("[COVERAGE]: numeric value")
	print("-----------------------------------------------------------------")
length = len(sys.argv)

##2. Comprobación del número de argumentos introducidos
if  length < 5:
	print("\n")
	print("ERROR: Invalid number of arguments")
	help()
	exit ()

##3. Asignación de las variables introducidas en los argumentos como variables del sistema.
genbank = sys.argv[1]
query = sys.argv[2]
identity = sys.argv[3]
coverage = sys.argv[4]

##4. Verificación del IDENTITY y el COVERAGE. Deben ser valores numéricos.
if (identity.isdigit() == False):
        print("\n")
        print("ERROR: IDENTITY must be a numeric value")
        help()
        exit()
elif (coverage.isdigit() == False):
        print("\n")
        print("ERROR: COVERAGE must be a numeric value")
        help()
        exit()

##5.  Seleccion de la carpeta donde estan los GenBanks
print("Analysis of given GENBANKS")

# En el caso de que ya exista un mismo archivo multifasta, se borra
# Debemos comprobar que en la carpeta del banco de genes no se haya generado o exista previamente
# una carpeta multifasta.fa
if os.path.isfile("multifasta.fa"):
    print("Multifasta.fa alredy exists. It would be rewrited")
    os.remove("multifasta.fa")

#Debemos comprobar que el directorio seleccionado sí que existe.
if os.path.isdir(genbank):
        ### MODULO 1 ###
        resultado = genbank_converter.convertidor_fasta(genbank)
else:
        print("ERROR: Selected directory do not exist")
        help()
        exit()

##6. Seleccion de la carpeta donde esta almacenado el multifasta de los query
print("Analysis of given QUERY")
# Separo el multifasta en archivos fasta independientes
import query_analizer
if os.path.isdir(query):
    for file in os.listdir(query):
        ### MODULO 2 ###
        fasta = query_analizer.multifasta_fasta(query, file)
cwd = os.getcwd()

# Debemos comprobar que el directorio seleccionado sí que existe y que tiene el formato correcto.
if os.path.isdir(query):
    for filename in os.listdir(query):
        if filename.startswith("Query"):
        ### MODULO 2 ###
            comprobacion = query_analizer.comprobar_query(query, filename)

##7.  Creación de la Base de Datos.
print("\n"+"Creating database...")
os.system("makeblastdb -in multifasta.fa -dbtype prot")
print("Done!")

##8. Comprobación de que el blastp es correcto.
import blastp
for file in os.listdir(cwd):
    if file.endswith("_blastp.fasta"):
        ### MODULO 3 ###
       resultado_blastp = blastp.funcion_blast(file)

##9. Carpeta de resultado.
print("\n"+"Creating RESULTS folder...")
path = Path("RESULTS/Blastp_results")
if not os.path.isdir("RESULTS"):
    path.mkdir(parents = True)
else:
    shutil.rmtree("RESULTS")
    path.mkdir(parents = True)

##10. Filtrado del blastp por IDENTITY Y COVERAGE. Almacenar en carpeta de resultado.
print("\n"+"Running Blastp...")
for file in os.listdir(cwd):
    if file.endswith("_blastp_result.fasta"):
        ### MODULO 3 ###
        blastp_filtro = blastp.filtro_blastp(file, identity, coverage, path)
print("\n"+"Blastp succesfully conducted."+"\n"+"The results are shown in: RESULTS/Blastp_results folder")

##11.  Incluir en  el query original los archivos que entraran como input en el MUSCLE
import muscle
print("\n"+"Preparing MUSCLE input files...")
if os.path.isdir(query):
    i = 1
    for file in os.listdir(query):
        if file.startswith("Query"+str(i)):
        ### MODULO 4 ###
            input_muscle = muscle.input_muscle(query, file, i)
            i += 1
print("\n"+"MUSCLE files correctly created.")

##12.  Alineamiento múltiple con MUSCLE de cada uno de los .fasta del query.
for file in os.listdir(cwd):
    if file.endswith("_filtrado.fasta"):
        ### MODULO 4 ###
        multiple_alignment = muscle.funcion_muscle(file)
print("\n"+"Multiple Alignment successfully conducted.")
print("\n"+"You can check alignments and trees in RESULTS/Muscle_results folder.")

#Almacenamos el muscle.
path2 = Path("RESULTS/Muscle_results")
path2.mkdir(parents = True)
for file in os.listdir(cwd):
    if file.endswith("_muscle.fa") or file.endswith("_muscle_tree.nw"):
        ini_path = os.path.join(cwd, file)
        shutil.move(ini_path, path2)

##13. MODULO PROSITE.
### MODULO 5: Busqueda de dominios en Prosite ###
import prosite
print("\n"+"Creating Prosite Database...")
if os.path.isfile("prosite_db") == False:
    domain_search = prosite.prosite_db()
    dictionary_pattern = prosite.dictionary()
else:
    os.remove("prosite_db")
    domain_search = prosite.prosite_db()
    dictionary_pattern = prosite.dictionary()

path3 = Path("RESULTS/Prosite_results")
path3.mkdir(parents = True)

shutil.move("prosite_db", path3)
print("\n"+"Database file succesfully created. Check in RESULTS/Prosite_results/prosite_db")

#Eliminación de archivos existentes.
for filename in os.listdir(path3):
    if filename.endswith("_domains"):
        os.remove(filename)
    else:
        pass

#Ejecución de la búsqueda de dominios.
print("\n"+"Searching for patterns in the input sequences...")
path = "RESULTS/Blastp_results"
for file in os.listdir(path):
    domain_search = prosite.domain_search(dictionary_pattern, file, path)
print("Research carried out as expected.Check the results in RESULTS/Prosite_results folder")

