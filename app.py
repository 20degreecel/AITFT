import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="AITFT R&D Hub", layout="wide")

st.title("🧪 AITFT: AI Drug Discovery R&D Hub")
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Project Overview", "Methodology & Docs", "Data Exploration", "Model Inference", "Research Library"])

# Paths (Refactored to relative for cloud compatibility)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRAIN_DIR = os.path.join(BASE_DIR, "ag-brain")
WORD_DIR = os.path.join(BASE_DIR, "Methodology_Word")
DATA_FILE = os.path.join(BASE_DIR, "data", "davis_processed.csv")
MODEL_PATH = os.path.join(BASE_DIR, "smartdti_baseline.pth")
RESEARCH_LOG = os.path.join(BRAIN_DIR, "research_log.md")
TASK_FILE = os.path.join(BRAIN_DIR, "task.md")

if selection == "Project Overview":
    st.header("Project Status & Roadmap")
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            st.markdown(f.read())

elif selection == "Methodology & Docs":
    st.header("Technical Methodologies")
    doc_files = [f for f in os.listdir(BRAIN_DIR) if f.endswith(".md") and "Methodology" in f or "Workflow" in f or "Proposal" in f]
    selected_doc = st.selectbox("Select a Document to View", doc_files)
    
    if selected_doc:
        with open(os.path.join(BRAIN_DIR, selected_doc), "r", encoding="utf-8") as f:
            st.markdown(f.read())
            
    st.divider()
    st.subheader("Download Word Versions (.docx)")
    if os.path.exists(WORD_DIR):
        for word_f in os.listdir(WORD_DIR):
            with open(os.path.join(WORD_DIR, word_f), "rb") as f:
                st.download_button(label=f"Download {word_f}", data=f, file_name=word_f)

elif selection == "Data Exploration":
    st.header("Benchmark Dataset: DAVIS")
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.write(f"Total Records: {len(df)}")
        st.dataframe(df.head(100))
        st.subheader("Binding Affinity (pKd) Distribution")
        st.bar_chart(df['pKd'].head(100)) 
    else:
        st.error("Processed data not found. Please run preprocessing first.")

elif selection == "Model Inference":
    st.header("Live SmartDTI Inference (Beta)")
    smiles_input = st.text_input("Enter Ligand SMILES", "CC1=C2C=C(C=CC2=NN1)C3=CC(=CN=C3)OCC(CC4=CC=CC=C4)N")
    protein_input = st.text_area("Enter Protein Sequence (FASTA)", "MKKFFDSRREQGGSGLGSGSSGGGGSTSGLGSGYIGRVFGIGRQQVTV...")
    
    if st.button("Predict Affinity"):
        from smartdti_model import SmartDTI_Baseline
        import torch
        
        # Helper encoders (Sync with train_baseline.py)
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

        model = SmartDTI_Baseline()
        
        if os.path.exists(MODEL_PATH):
            try:
                model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
                model.eval()
                
                s_idx = torch.LongTensor([label_smiles(smiles_input)])
                p_idx = torch.LongTensor([label_sequence(protein_input)])
                
                with torch.no_grad():
                    prediction = model(s_idx, p_idx).item()
                
                st.success("Inference Successful!")
                st.metric("Predicted pKd (Binding Affinity)", f"{prediction:.4f}")
                st.info("pKd = -log10(Kd). Higher values indicate stronger binding.")
            except Exception as e:
                st.error(f"Error loading model: {e}")
        else:
            st.warning("Model weights (smartdti_baseline.pth) not found. Displaying dummy result.")
            st.metric("Predicted pKd", "7.42", "± 0.2")

elif selection == "Research Library":
    st.header("Curated Research Papers")
    st.info("Log of 20+ collected papers including Boltz-2, Uni-Mol, and REINVENT 4.")
    if os.path.exists(os.path.join(BRAIN_DIR, "research_log.md")):
        with open(os.path.join(BRAIN_DIR, "research_log.md"), "r", encoding="utf-8") as f:
            st.markdown(f.read())
