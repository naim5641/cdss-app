# mappings/symptom_to_test.py

# ডেটাসেটের ১৫০টি টেস্ট থেকে বেছে নেওয়া কিছু কমন ম্যাপিং
SYMPTOM_TO_TEST = {
    "Fever": ["CBC", "Dengue NS1 Antigen", "Malaria Parasite (MP)", "Typhidot / Widal Test", "CRP (C-Reactive Protein)"],
    "Cough": ["Chest X-ray (PA View)", "Sputum for AFB", "CBC"],
    "Chest pain": ["ECG", "Troponin I/T", "Chest X-ray (PA View)"],
    "Shortness of breath": ["Chest X-ray (PA View)", "Spirometry", "Blood Gas Analysis (ABG)"],
    "Burning urination": ["Urine R/E", "Urine C/S"],
    "Frequent urination": ["Blood Sugar (Fasting)", "Urine R/E", "Serum Creatinine"],
    "Abdominal pain": ["Ultrasound (Whole Abdomen)", "CBC", "Urine R/E"],
    "Headache": ["CBC", "CT Scan (Brain)", "Blood Sugar (Fasting)"],
    "Dizziness": ["CBC", "Blood Sugar (Fasting)", "ECG"],
    "Diarrhea": ["Stool R/E", "Stool C/S", "CBC"],
    "Vomiting": ["CBC", "Electrolytes (Na, K, Cl)", "Serum Creatinine"],
    "Joint pain": ["Rheumatoid Factor (RF)", "Anti-CCP", "ESR", "Uric Acid"],
    "Back pain": ["Spine X-ray", "MRI Spine", "CBC"],
    "Weight loss": ["CBC", "Blood Sugar (Fasting)", "Thyroid Profile (TSH, T3, T4)", "Chest X-ray (PA View)"],
    "Palpitation": ["ECG", "Echocardiogram (ECHO)", "Thyroid Profile (TSH, T3, T4)"],
    "Swelling of legs": ["Serum Creatinine", "Echocardiogram (ECHO)", "Urine R/E"],
    "Jaundice": ["Liver Function Test (LFT)", "Serum Bilirubin (Total/Direct)", "Hepatitis B", "Hepatitis C"],
    "Rash": ["CBC", "Dengue NS1 Antigen", "ESR"],
    "Ear pain": ["Otoscopy (Clinical)", "CBC"], # Dataset e direct nai, clinical
    "Toothache": ["X-ray (Dental)", "CBC"], 
    "Eye redness": ["Eye Refraction Test", "CBC"],
    "Irregular menstruation": ["USG Pelvis", "Thyroid Profile (TSH, T3, T4)", "Pregnancy Test (Urine for HCG)"],
}

# ডিপার্টমেন্ট অনুযায়ী কমন টেস্ট (যদি স্পেসিফিক সিম্পটম ম্যাপিং না থাকে)
DEPT_TO_TEST = {
    "Cardiology": ["ECG", "Echocardiogram (ECHO)", "Lipid Profile"],
    "Cardio": ["ECG", "Echocardiogram (ECHO)", "Lipid Profile"],
    "Chest": ["Chest X-ray (PA View)", "Spirometry", "Sputum for AFB"],
    "Urology": ["Urine R/E", "Urine C/S", "USG KUB"],
    "Gynae": ["USG Pelvis", "Pap Smear", "Pregnancy Test (Urine for HCG)"],
    "Hepatology": ["Liver Function Test (LFT)", "USG Whole Abdomen"],
    "Neuro": ["CT Scan (Brain)", "MRI Brain", "EEG"],
    "ENT": ["Audiometry", "PNS X-ray"],
    "Dental": ["X-ray (Dental)", "CBC"],
    "Ortho": ["X-ray (Bone)", "Serum Calcium", "Uric Acid"],
    "Orthopedic": ["X-ray (Bone)", "Serum Calcium", "Uric Acid"],
}