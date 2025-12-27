import torch
import sys
import os

# Add src to path so imports work
sys.path.append(os.path.join(os.getcwd(), 'src'))

from virtual_lab.epitope_mapping import (
    Glycoconjugate, 
    CarrierProtein, 
    Glycan, 
    StructuralModeler, 
    FeatureExtractor, 
    EpitopeClassifier
)

def main():
    print("=== Starting Verification of Epitope Mapping Pipeline ===")
    
    # 1. Define Input
    print("\n1. Defining Glycoconjugate Input...")
    carrier = CarrierProtein(
        name="CRM197",
        sequence="MASRGASRGASRG" * 10
    )
    glycan = Glycan(
        name="Polysialic Acid",
        attachment_site=5,
        linkage="alpha-2,8",
        length=10
    )
    construct = Glycoconjugate(
        name="Test_Vaccine_01",
        carrier_protein=carrier,
        glycans=[glycan],
        meta={"pathogen": "TestPathogen"}
    )
    print(f"Defined construct: {construct.name}")

    # 2. Structural Modeling
    print("\n2. Running Structural Modeling (Mock)...")
    modeler = StructuralModeler(output_dir="data/structures")
    pdb_files = modeler.generate_ensemble(construct, n_models=2)
    print(f"Output files: {pdb_files}")

    # 3. Feature Extraction
    print("\n3. Running Feature Extraction (Mock)...")
    extractor = FeatureExtractor(embed_dim=64)
    features = extractor.extract_features(pdb_files)
    print(f"Features shape: {features.shape}")

    # 4. Neural Network Inference
    print("\n4. Running Model Inference...")
    model = EpitopeClassifier(embed_dim=64, hidden_dim=32)
    model.eval()
    with torch.no_grad():
        preds = model(features)
    
    print(f"Predictions shape: {preds.shape}")
    print(f"Average predicted probability: {preds.mean().item():.4f}")
    
    print("\n=== Verification Complete: SUCCESS ===")

if __name__ == "__main__":
    main()
