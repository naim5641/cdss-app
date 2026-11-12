# utils/helpers.py
import pandas as pd
import streamlit as st
from collections import Counter

DATA_PATH = "data/Prescription_Industrial_DataSet.xlsx"

@st.cache_data
def load_chief_complaint():
     # skiprows=2 দিয়ে প্রথম ফাঁকা সারি এবং টাইটেল সারি বাদ দিন
    df = pd.read_excel(DATA_PATH, sheet_name="Chief Complaint", skiprows=2)
    
    # বাকি ক্লিনিং আগের মতোই থাকবে
    df = df.dropna(subset=['Chief Complaint'])
    df = df[df['Chief Complaint'] != 'Chief Complaint']
    
    for col in ['Chief Complaint', 'বাংলা অর্থ', 'Associated Symptoms', 'Department']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    return df


def get_top_departments(rows, top_n=3):
    """একাধিক row থেকে common department বের করা"""
    all_depts = []
    for d in rows['Department'].dropna():
        # "Medicine / Neuro" → ["Medicine", "Neuro"]
        all_depts.extend([x.strip() for x in str(d).split('/') if x.strip()])
    if not all_depts:
        return []
    return Counter(all_depts).most_common(top_n)


def expand_associated_symptoms(selected_symptoms, df):
    """Selected symptom-এর associated symptoms যোগ করা"""
    expanded = set(selected_symptoms)
    for s in selected_symptoms:
        row = df[df['Chief Complaint'] == s]
        if not row.empty:
            assoc = row.iloc[0]['Associated Symptoms']
            if pd.notna(assoc) and assoc.lower() != 'nan':
                for a in str(assoc).split(','):
                    a = a.strip()
                    if a:
                        expanded.add(a)
    return expanded

@st.cache_data
def load_past_history():
    """Past Medical History শীট লোড করা"""
    df = pd.read_excel(DATA_PATH, sheet_name="Past Medical History", skiprows=0)
    df = df.dropna(subset=['Medical Condition (English)'])
    return sorted(df['Medical Condition (English)'].astype(str).str.strip().unique().tolist())

@st.cache_data
def load_allergies():
    """Allergic history শীট লোড করা"""
    df = pd.read_excel(DATA_PATH, sheet_name="Allergic history", skiprows=0)
    df = df.dropna(subset=['Allergy Type / Source (English)'])
    return sorted(df['Allergy Type / Source (English)'].astype(str).str.strip().unique().tolist())