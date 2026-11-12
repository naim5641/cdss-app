import streamlit as st
from utils.helpers import (
    load_chief_complaint, get_top_departments, expand_associated_symptoms,
    load_past_history, load_allergies
)
from mappings.symptom_to_test import SYMPTOM_TO_TEST, DEPT_TO_TEST
from mappings.allergy_warnings import ALLERGY_WARNINGS, HISTORY_NOTES
from mappings.diagnosis_patterns import DIAGNOSIS_PATTERNS

# ---------- 1. Page Config ----------
st.set_page_config(page_title="CDSS App", page_icon="🩺", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 40px; color: #1E88E5; text-align: center; }
    .sub-title { text-align: center; color: gray; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🩺 Clinical Decision Support System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">রোগীর লক্ষণ বিশ্লেষণ ও চিকিৎসা সহায়িকা (বাংলা + English)</div>', unsafe_allow_html=True)

# ---------- 2. Data Load ----------
df = load_chief_complaint()
all_history = load_past_history()
all_allergies = load_allergies()
all_symptoms = sorted(df['Chief Complaint'].unique().tolist())

# ---------- 3. Sidebar Inputs ----------
st.sidebar.header("👤 রোগীর তথ্য দিন")

selected = st.sidebar.multiselect(
    "লক্ষণ (Symptoms)", 
    options=all_symptoms,
    placeholder="লক্ষণ বাছুন..."
)

show_assoc = st.sidebar.checkbox(
    "Associated symptoms-ও বিবেচনা করুন",
    value=True
)

st.sidebar.markdown("---")
st.sidebar.header("📋 মেডিকেল হিস্ট্রি")

selected_allergies = st.sidebar.multiselect(
    "অ্যালার্জি (Allergies)", 
    options=all_allergies,
    placeholder="অ্যালার্জি থাকলে বাছুন..."
)

selected_history = st.sidebar.multiselect(
    "আগের রোগ (Past History)", 
    options=all_history,
    placeholder="আগের রোগ থাকলে বাছুন..."
)

# ---------- 4. Main Logic ----------
if not selected:
    st.info("👈 শুরু করতে বাম দিকের সাইডবার থেকে রোগীর লক্ষণ বেছে নিন।")
    st.stop()

# Data processing
rows = df[df['Chief Complaint'].isin(selected)]
expanded = expand_associated_symptoms(selected, df) if show_assoc else set(selected)
top_depts = get_top_departments(rows, top_n=3)

# Create Tabs for better UI
tab1, tab2, tab3, tab4 = st.tabs([
    "🏥 Department & Tests", 
    "🔍 Differential Diagnosis", 
    "🚨 Alerts & Notes", 
    "📋 Symptom Details"
])

# ---------- Tab 1: Department & Tests ----------
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏥 Suggested Department")
        if top_depts:
            st.success(f"**সবচেয়ে সম্ভাব্য: {top_depts[0][0]}**")
            if len(top_depts) > 1:
                others = ", ".join([f"{d} ({c})" for d, c in top_depts[1:]])
                st.write(f"অন্যান্য বিভাগ: {others}")
        else:
            st.warning("ডিপার্টমেন্ট পাওয়া যায়নি।")
            
    with col2:
        st.subheader("🧪 Suggested Investigations")
        suggested_tests = set()
        for s in selected:
            if s in SYMPTOM_TO_TEST: suggested_tests.update(SYMPTOM_TO_TEST[s])
        if top_depts and top_depts[0][0] in DEPT_TO_TEST:
            suggested_tests.update(DEPT_TO_TEST[top_depts[0][0]])
            
        if suggested_tests:
            for test in sorted(list(suggested_tests)):
                st.write(f"🔬 {test}")
        else:
            st.info("এই লক্ষণের জন্য নির্দিষ্ট টেস্ট পাওয়া যায়নি।")

# ---------- Tab 2: Differential Diagnosis ----------
with tab2:
    st.subheader("🔍 সম্ভাব্য রোগ (Differential Diagnosis)")
    
    scores = {}
    for disease, pattern in DIAGNOSIS_PATTERNS.items():
        match_count = len(set(expanded) & set(pattern))
        if match_count > 0:
            score = round((match_count / len(pattern)) * 100, 1)
            scores[disease] = score
            
    if scores:
        top_diagnoses = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
        for disease, score in top_diagnoses:
            if score >= 60:
                st.error(f"**{disease}** — মিল: {score}% (উচ্চ সম্ভাবনা)")
            elif score >= 30:
                st.warning(f"**{disease}** — মিল: {score}% (মাঝারি সম্ভাবনা)")
            else:
                st.info(f"**{disease}** — মিল: {score}%")
    else:
        st.success("লক্ষণগুলো কোনো নির্দিষ্ট রোগের সাথে সরাসরি মিলছে না।")

# ---------- Tab 3: Alerts & Notes ----------
with tab3:
    if selected_allergies:
        st.subheader("🚨 Allergy Alerts")
        for allergy in selected_allergies:
            msg = ALLERGY_WARNINGS.get(allergy, f"⚠️ রোগীর {allergy} আছে। সতর্ক থাকুন।")
            st.error(msg)
            
    if selected_history:
        st.subheader("📋 Past Medical History Notes")
        for history in selected_history:
            msg = HISTORY_NOTES.get(history, f"ℹ️ রোগীর পূর্বে {history} ছিল।")
            st.info(msg)
            
    if not selected_allergies and not selected_history:
        st.success("রোগীর কোনো অ্যালার্জি বা পূর্ববর্তী রোগের তথ্য দেওয়া হয়নি।")

# ---------- Tab 4: Symptom Details ----------
with tab4:
    st.subheader("📋 দেওয়া লক্ষণগুলোর বিস্তারিত")
    st.dataframe(
        rows[['Chief Complaint', 'বাংলা অর্থ', 'Duration', 'Associated Symptoms', 'Department']],
        use_container_width=True,
        hide_index=True
    )
    if show_assoc:
        assoc_only = expanded - set(selected)
        if assoc_only:
            st.write("**অন্যান্য সংশ্লিষ্ট লক্ষণ (Auto-expanded):**", ", ".join(sorted(assoc_only)))

# ---------- Footer ----------
st.markdown("---")
st.caption("⚠️ **Disclaimer:** এটি একটি সফটওয়্যার টুল। চূড়ান্ত রোগনির্ণয় ও চিকিৎসার সিদ্ধান্ত সর্বদা একজন যোগ্য ডাক্তারের।")