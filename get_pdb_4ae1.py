from Bio.PDB import PDBList
import os

pdbl = PDBList()
# CRM197 crystal structure
pdbl.retrieve_pdb_file('4AE1', pdir='data/structures', file_format='pdb')
print("Downloaded 4AE1")
