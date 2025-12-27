from Bio.PDB import PDBParser
import warnings

warnings.filterwarnings('ignore')

def inspect():
    parser = PDBParser()
    structure = parser.get_structure("debug", "data/structures/pdb4ae1.ent")
    model = structure[0]
    
    print("Chains found:")
    for chain in model:
        residues = list(chain.get_residues())
        if not residues:
            print(f"  Chain {chain.id}: Empty")
            continue
            
        first = residues[0].id[1]
        last = residues[-1].id[1]
        print(f"  Chain {chain.id}: {len(residues)} residues. Range: {first} - {last}")
        
        # Check specific ranges
        count_in_zone = 0
        ppz_ranges = [range(271, 291), range(321, 341), range(411, 431)]
        
        for res in residues:
            if any(res.id[1] in r for r in ppz_ranges):
                count_in_zone += 1
        print(f"    Residues in PPZ zones: {count_in_zone}")

if __name__ == "__main__":
    inspect()
