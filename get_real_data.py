from Bio.PDB import PDBList
import os

def download_pdb(pdb_id: str, output_dir: str):
    pdbl = PDBList()
    os.makedirs(output_dir, exist_ok=True)
    # This downloads in .ent format or .pdb
    path = pdbl.retrieve_pdb_file(pdb_id, pdir=output_dir, file_format="pdb")
    print(f"Downloaded {pdb_id} to {path}")
    return path

if __name__ == "__main__":
    # CRM197 PDB ID
    download_pdb("4AEI", "data/structures")
