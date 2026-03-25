from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski
import pandas as pd

class SmartGatekeeper:
    def __init__(self):
        # Basic drug-likeness rules
        self.rules = {
            "MW": 500.0,
            "LogP": 5.0,
            "HBD": 5,
            "HBA": 10
        }

    def check_lipinski(self, sm):
        mol = Chem.MolFromSmiles(sm)
        if mol is None:
            return False, "Invalid SMILES"
        
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        hbd = Lipinski.NumHDonors(mol)
        hba = Lipinski.NumHAcceptors(mol)
        
        reasons = []
        if mw > self.rules["MW"]: reasons.append(f"MW ({mw:.1f}) > 500")
        if logp > self.rules["LogP"]: reasons.append(f"LogP ({logp:.1f}) > 5")
        if hbd > self.rules["HBD"]: reasons.append(f"HBD ({hbd}) > 5")
        if hba > self.rules["HBA"]: reasons.append(f"HBA ({hba}) > 10")
        
        if not reasons:
            return True, "Pass"
        else:
            return False, ", ".join(reasons)

    def filter_molecules(self, smiles_list):
        passed = []
        info = []
        for sm in smiles_list:
            is_ok, msg = self.check_lipinski(sm)
            if is_ok:
                passed.append(sm)
            info.append({"SMILES": sm, "Gatekeeper_Status": msg})
        return passed, pd.DataFrame(info)

if __name__ == "__main__":
    gatekeeper = SmartGatekeeper()
    test_smiles = ["C", "CC(=O)OC1=CC=CC=C1C(=O)O", "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"]
    passed, report = gatekeeper.filter_molecules(test_smiles)
    print(report)
