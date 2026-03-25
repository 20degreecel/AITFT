import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from smartdti_model import SmartDTI_Baseline
import os

# Helper to encode SMILES/Sequences (Simplistic for baseline)
def label_smiles(smiles, max_len=100):
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()[]#%@+=-/\\."
    char_to_int = {c: i+1 for i, c in enumerate(chars)}
    res = [char_to_int.get(c, 0) for c in smiles[:max_len]]
    return res + [0] * (max_len - len(res))

def label_sequence(seq, max_len=1000):
    chars = "ACDEFGHIKLMNPQRSTVWY"
    char_to_int = {c: i+1 for i, c in enumerate(chars)}
    res = [char_to_int.get(c, 0) for c in seq[:max_len]]
    return res + [0] * (max_len - len(res))

class DavisDataset(Dataset):
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        smiles = label_smiles(self.df.iloc[idx]['SMILES'])
        seq = label_sequence(self.df.iloc[idx]['Target_Sequence'])
        affinity = self.df.iloc[idx]['pKd']
        return torch.LongTensor(smiles), torch.LongTensor(seq), torch.FloatTensor([affinity])

def train():
    data_path = r"c:\Users\teoyo\Downloads\VSCODE\AITFT\data\davis_processed.csv"
    if not os.path.exists(data_path):
        print("Error: Preprocessed data not found.")
        return

    dataset = DavisDataset(data_path)
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    model = SmartDTI_Baseline()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    
    print("Starting Training Loop (Sample 5 Epochs for Pilot)...")
    for epoch in range(5):
        model.train()
        total_loss = 0
        for smiles, seq, target in train_loader:
            optimizer.zero_grad()
            output = model(smiles, seq)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        print(f"Epoch {epoch+1}, Loss: {total_loss/len(train_loader):.4f}")
    
    # Save Model
    save_path = r"c:\Users\teoyo\Downloads\VSCODE\AITFT\smartdti_baseline.pth"
    torch.save(model.state_dict(), save_path)
    print(f"Model saved to {save_path}")

if __name__ == "__main__":
    train()
