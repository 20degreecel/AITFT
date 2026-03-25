import os
import pandas as pd
import numpy as np
import json

data_dir = r"c:\Users\teoyo\Downloads\VSCODE\AITFT\data"

def preprocess_davis():
    print("=== Preprocessing DAVIS Dataset (JSON + Binary Matrix) ===")
    
    # Load raw files
    ligands_file = os.path.join(data_dir, "davis_ligands.txt")
    proteins_file = os.path.join(data_dir, "davis_proteins.txt")
    affinity_file = os.path.join(data_dir, "davis_affinity.txt")
    
    # Load JSON data
    with open(ligands_file, 'r', encoding='utf-8') as f:
        ligands_dict = json.load(f)
    
    with open(proteins_file, 'r', encoding='utf-8') as f:
        proteins_dict = json.load(f)
        
    ligands_list = list(ligands_dict.values())
    proteins_list = list(proteins_dict.values())
    
    # Load binary matrix
    try:
        y = np.load(affinity_file, allow_pickle=True, encoding='latin1')
    except Exception as e:
        print(f"Error loading binary matrix: {e}")
        return

    print(f"Num Ligands (JSON): {len(ligands_list)}")
    print(f"Num Proteins (JSON): {len(proteins_list)}")
    print(f"Affinity Matrix Shape: {y.shape}")
    
    # Standard DeepDTA format: Matrix is (Proteins, Drugs) or (Drugs, Proteins)?
    # In davis/Y, it's (442 proteins, 68 drugs) usually.
    # Matrix Shape in output was (68, 442) in the previous failed run log.
    # So (Drugs, Proteins).
    
    if y.shape == (len(ligands_list), len(proteins_list)):
        # (Drugs, Proteins)
        rows = []
        for i in range(len(ligands_list)):
            for j in range(len(proteins_list)):
                rows.append({
                    "SMILES": ligands_list[i],
                    "Target_Sequence": proteins_list[j],
                    "Affinity": y[i, j]
                })
    elif y.shape == (len(proteins_list), len(ligands_list)):
        # (Proteins, Drugs)
        rows = []
        for i in range(len(proteins_list)):
            for j in range(len(ligands_list)):
                rows.append({
                    "SMILES": ligands_list[j],
                    "Target_Sequence": proteins_list[i],
                    "Affinity": y[i, j]
                })
    else:
        print("Error: Matrix dimensions do not match JSON counts.")
        return
            
    df = pd.DataFrame(rows)
    # Log transformation: pKd = -log10(kd / 1e9)
    df['pKd'] = -np.log10(df['Affinity'] / 10**9)
    
    out_file = os.path.join(data_dir, "davis_processed.csv")
    df.to_csv(out_file, index=False)
    print(f"Saved processed data to {out_file} ({len(df)} records)")

if __name__ == "__main__":
    preprocess_davis()
