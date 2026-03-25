# [Methodology] SmartGatekeeper: Multi-Stage Filtering & Triage

## 1. Overview
SmartGatekeeper acts as a high-throughput triage module situated between **DANOVO** (Generation) and **DAPRE** (Validation). Its primary role is to reduce the computational load on the expensive MD/Schrödinger simulations by filtering out low-probability candidates.

## 2. Filtering Hierarchy

### Level 1: Hard Constraint Filters (Rule-based)
- **Molecular Weight / Lipophilicity**: Filtering based on Lipinski's Rule of Five or project-specific ADMET requirements.
- **Substructure Alerts**: Removal of PAINS (Pan-Assay Interference Compounds) and reactive functional groups.

### Level 2: Property Prediction (Neural Filters)
- **QED (Chemical Beauty)**: Incorporating the Quantitative Estimate of Drug-likeness (Bickerton et al., 2012) to ensure the generated leads have drug-like profiles.
- **LogP / Solubility**: Real-time prediction using GNN-based property models.

### Level 3: Fast Affinity Triage (SmartDTI Lightweight)
- **Mechanism**: Using rapid 1D/2D DTI models (e.g., **GraphDTA** or **MolTrans**) to get a "ballpark" affinity score.
- **Multi-View Integration**: Utilizing **MVGCN** (Multi-View Graph Convolutional Network) logic to integrate data from disparate views (e.g., topological, physicochemical, and interaction-based) for more robust triage.

## 3. Triage Logic (The "WHAT/HOW" Framework)
Inspired by the **Multi-View Talent Recommendation** research (Kim & Kim, 2025):
- **"WHAT" Dimension**: Direct binding interaction patterns (3D pocket alignment).
- **"HOW" Dimension**: Chemical stability and interaction networks (GCN-based).
- **Gating Mechanism**: An adaptive fusion layer that weights the importance of direct affinity vs. general drug-likeness depending on the target class.

## 4. Integration with DAPRE
Only the top ~100-500 compounds that pass the SmartGatekeeper threshold are forwarded to the DAPRE module for rigorous physical validation.
