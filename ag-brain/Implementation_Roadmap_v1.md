# [Implementation Plan] SmartDTI & DANOVO Prototyping

## 1. Phase 1: Environment & Data Baseline
Establish a working environment with the necessary DL/Cheminformatics stack and pre-process initial benchmarking datasets.

### Tasks:
- [ ] Verify `torch`, `rdkit`, `dgl` or `torch_geometric` installation.
- [ ] Create `AITFT\data\` directory for benchmarking sets.
- [ ] Script to download and sanitize **DAVIS** (Affinity) and **BioSNAP** (Bipartite) datasets.

## 2. Phase 2: SmartDTI Prototype (Affinity Prediction)
Build the "Fast Filter" layer using 2D Graph Neural Networks.

### Tasks:
- [ ] Implement **GraphDTA** (GCN/GAT/GIN) baseline in PyTorch.
- [ ] Training script for DAVIS dataset to establish initial RMSE/CI performance.
- [ ] Uni-Mol integration: Script to extract 3D descriptors for ligands.

## 3. Phase 3: DANOVO x Gatekeeper Loop
Demonstrate the initial design-and-triage cycle.

### Tasks:
- [ ] Implementation of a simple SMILES-RNN generator (REINVENT-style).
- [ ] SmartGatekeeper Triage Hook: Logic to feed generated SMILES into the Phase 2 DTI model.
- [ ] Performance report: Reduction in candidate space (e.g., $10,000$ generated -> $100$ top binders).
