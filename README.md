# ProyectoFinal
This script was built to contrast query protein sequences to protein sequences in a GenBank file. It is capable of creating a tree based on domains highly conserved in the orthologe proteins. In order to do so, it runs several operations that require a very specific input. 
### Those operations are: 
  BlastP: query with all sequences in the Genbank Files. 
  Muscle: based on the protein orthologes, builds a tree saved in a file (.nw) and an aligment document (.fasta). 
  Domain search: based on Prosite database given by the user. It searchs for domains in the genbank for every given query.
USAGE: python
