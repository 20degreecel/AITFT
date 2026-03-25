# DAPRE: Substance Validation Workflow

## 1. Overview
DAPRE (Deep Affinity Prediction & Rigorous Evaluation) is the validation engine for SmartDTI's generative outputs. It ensures that every proposed lead compound undergoes a "Gold Standard" verification before wet-lab synthesis.

## 2. Integrated Validation Pipeline

### Step 1: High-Precision Docking (Schrödinger Suite)
- **Tool**: Glide (XP - Extra Precision).
- **Process**: Generate multiple binding poses for the target protein pocket. Use induced-fit docking (IFD) if the pocket is known to be flexible.
- **Output**: Optimized binding poses with initial docking scores.

### Step 2: Dynamic Stability Assessment (Molecular Dynamics)
- **Tool**: Desmond / Gromacs.
- **Process**: Run a 100ns-1µs MD simulation of the protein-ligand complex in an explicit water box.
- **Metrics**: Root Mean Square Deviation (RMSD) and Root Mean Square Fluctuation (RMSF) to ensure the ligand stays in the pocket.
- **Analysis**: Check for stable hydrogen bonds and π-π stacking interactions over time.

### Step 3: Neural Affinity Scoring (Boltz-2)
- **Tool**: Boltz-2 neural engine.
- **Process**: Feed the MD-stable frame into Boltz-2 for a final affinity prediction.
- **Validation**: Compare Boltz-2 scores with Schrödinger's MM-GBSA (Molecular Mechanics Generalized Born Surface Area) scores.
- **Criteria**: Leads must show high confidence in both physics-based (MD/GBSA) and neural-based (Boltz-2) scoring.

## 3. Decision Logic
- **Green Light**: Stable MD trajectory + High Boltz-2 Affinity + Low GBSA score.
- **Yellow Light**: Minor instability or lower affinity; requires human review by Ph.D. teammate.
- **Red Light**: Ligand exits pocket during MD or low neural affinity; discard.
