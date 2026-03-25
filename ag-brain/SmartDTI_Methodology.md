# [Methodology] SmartDTI: Gigascale Chemical Space Screening

## 1. Overview
SmartDTI is designed to perform large-scale virtual screening against massive external libraries (e.g., **Enamine REAL**, ZINC-22). It employs a hierarchical fusion of 2D and 3D deep learning models to identify high-affinity hits among billions of compounds.

## 2. Algorithmic Fusion Architecture

### Phase 1: Rapid 2D Screening (Lightweight GNNs)
- **Model**: **GIN** (Graph Isomorphism Network) or **GraphDTA**.
- **Goal**: High-speed filtering of the $10^9$ chemical space down to $10^6$.
- **Feature Extraction**: Capturing local chemical environments and topological features.

### Phase 2: Hierarchical Heterogeneous Modeling
- **Model**: **H2GnnDTI** (Jing et al., 2025).
- **Logic**: Utilizing a two-level hierarchical heterogeneous graph learning approach to capture both local component interactions and global network relationships.

### Phase 3: Multi-View Interaction Mapping
- **Model**: **MVGCN** (Fu et al., 2022) / **MolTrans** (Huang et al., 2021).
- **Logic**: Fusing topological structure with biomedical bipartite networks (e.g., previous target similarity) and transformer-based interaction mapping.

### Phase 4: 3D Structural Refinement
- **Model**: **Uni-Mol** (Zhou et al., 2023) / **Uni-Mol+** (Lu et al., 2024).
- **Logic**: Using SE(3)-equivariant representations to assess the spatial fit of the top $10^5$ candidates in the protein pocket.

## 3. Deployment Strategy: Deep Docking Style
Following **Deep Docking** (Gentile et al., 2020):
- **Iterative Loop**: Use a QSAR-style deep learning surrogate to predict docking scores for the entire library.
- **Active Learning**: Dock a small high-confidence subset, retrain the surrogate, and repeat to efficiently navigate the billion-scale space without docking every compound.

## 4. External Data Sources
- **Standard Benchmarks**: DAVIS, KIBA, PDBbind, BindingDB, ChEMBL, BioSNAP, Luo et al. (2017).
- **Massive Screening Library**: Enamine REAL, ZINC-20/22.

## 5. Outcome
SmartDTI generates a curated list of top-tier candidates for **Wet-Lab** synthesis and testing.
