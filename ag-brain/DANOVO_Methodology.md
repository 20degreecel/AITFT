# [Methodology] DANOVO: Generative Molecular Design

## 1. Overview
DANOVO is the generative engine of the pipeline, responsible for *de novo* design of small molecules. It aims to explore the chemical space to find potential ligands that meet predefined multi-objective criteria.

## 2. Core Engine: REINVENT 4
As per the recent literature (Loeffler et al., 2024), DANOVO adopts the **REINVENT 4** framework.
- **Generative Models**:
    - **SMILES-based RNN**: Leveraging GRU/LSTM for sequence generation.
    - **Transformer-based Generator**: For capturing long-range dependencies in molecular structures.
- **Learning Mechanisms**:
    - **Reinforcement Learning (RL)**: Using policy gradients (e.g., REINVENT algorithm) to optimize agent behavior based on external scoring functions.
    - **Curriculum Learning**: Gradually increasing the complexity of the objectives (e.g., starting with drug-likeness, then moving to specific target affinity).
    - **Transfer Learning**: Pre-training on massive datasets (e.g., ChEMBL) before target-specific fine-tuning.

## 3. Multi-Objective Scoring (The Reward Function)
The generative process is guided by a composite reward function:
1. **Bioactivity (SmartDTI/Gatekeeper)**: Predicted binding affinity for the target protein.
2. **Drug-likeness (QED)**: Based on the "Chemical Beauty" metrics (Bickerton et al., 2012).
3. **Synthesizability (SAscore)**: Estimated ease of chemical synthesis.
4. **Physicochemical Properties**: LogP, Molecular Weight, TPSA, etc.

## 4. Iterative Optimization Loop
- **Sample**: The generator produces a batch of novelty SMILES.
- **Score**: The scoring head (Gatekeeper) evaluates the batch.
- **Update**: The agent's policy is updated to prioritize high-scoring regions of the chemical space.
