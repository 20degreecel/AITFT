import torch
import torch.nn as nn
import torch.nn.functional as F

class SmartDTI_Baseline(nn.Module):
    def __init__(self, drug_vocab_size=100, protein_vocab_size=26, embed_dim=128):
        super(SmartDTI_Baseline, self).__init__()
        
        # Drug Encoder: Simple CNN for SMILES (placeholder for GNN)
        self.drug_embed = nn.Embedding(drug_vocab_size, embed_dim)
        self.drug_conv1 = nn.Conv1d(embed_dim, 32, kernel_size=4)
        self.drug_conv2 = nn.Conv1d(32, 64, kernel_size=6)
        self.drug_conv3 = nn.Conv1d(64, 96, kernel_size=8)
        self.drug_fc = nn.Linear(96, 128)
        
        # Protein Encoder: CNN for Sequences
        self.prot_embed = nn.Embedding(protein_vocab_size, embed_dim)
        self.prot_conv1 = nn.Conv1d(embed_dim, 32, kernel_size=4)
        self.prot_conv2 = nn.Conv1d(32, 64, kernel_size=8)
        self.prot_conv3 = nn.Conv1d(64, 96, kernel_size=12)
        self.prot_fc = nn.Linear(96, 128)
        
        # Combined Interaction Layers
        self.fc1 = nn.Linear(256, 1024)
        self.fc2 = nn.Linear(1024, 512)
        self.out = nn.Linear(512, 1)
        
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, drug_seq, prot_seq):
        # Drug Branch
        d = self.drug_embed(drug_seq).permute(0, 2, 1)
        d = F.relu(self.drug_conv1(d))
        d = F.relu(self.drug_conv2(d))
        d = F.relu(self.drug_conv3(d))
        d = F.adaptive_max_pool1d(d, 1).squeeze(2)
        d = self.drug_fc(d)
        
        # Protein Branch
        p = self.prot_embed(prot_seq).permute(0, 2, 1)
        p = F.relu(self.prot_conv1(p))
        p = F.relu(self.prot_conv2(p))
        p = F.relu(self.prot_conv3(p))
        p = F.adaptive_max_pool1d(p, 1).squeeze(2)
        p = self.prot_fc(p)
        
        # Fusion
        combined = torch.cat((d, p), dim=1)
        combined = self.dropout(F.relu(self.fc1(combined)))
        combined = self.dropout(F.relu(self.fc2(combined)))
        return self.out(combined)

print("SmartDTI Baseline Architecture Initialized.")
