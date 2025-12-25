import streamlit as st
import joblib
import pandas as pd
import numpy as np
from scipy.sparse import hstack

numeric_feature_names = joblib.load("models/numeric_feature_names.pkl")
tfidf = joblib.load("models/tfidf_vectorizer.pkl")
clf = joblib.load("models/classification_model.pkl")
reg = joblib.load("models/regression_model.pkl")
df= pd.read_csv("data/processed/processed.csv")
numeric_df = pd.DataFrame(columns=numeric_feature_names)
numeric_df.loc[0] = 0
st.set_page_config(
    page_title="AutoJudge – Problem Difficulty Predictor",
    layout="centered"
)

st.title("AutoJudge")
st.write("Predict programming problem difficulty using its problem description,input description and output description.")

title=st.text_area("Title")
description = st.text_area("Problem Description", placeholder="Enter the problem dedscription here")
input_desc = st.text_area("Input Description", placeholder="Describe the input format ")
output_desc = st.text_area("Output Description",placeholder="Describe the output format")

if st.button("Predict Difficulty"):

    if description.strip()=="":
        st.warning("Please enter a problem description")
    else:
        full_text=" ".join([description, input_desc, output_desc]).lower()
        temp_df=pd.DataFrame({"clean_text":[full_text]})
        X_tfidf=tfidf.transform(temp_df["clean_text"])
        # text_length = len(full_text)
        # word_count = len(full_text.split())
        numeric_features = np.zeros((1, len(numeric_feature_names)))
        numeric_df.loc[0, 'text_length'] = len(full_text)
        numeric_df.loc[0, 'word_count'] = len(full_text.split())

        numeric_df.loc[0, 'kw_graph'] = int('graph' in full_text)
        numeric_df.loc[0, 'kw_tree'] = int('tree' in full_text)
        numeric_df.loc[0, 'kw_dp'] = int(' dp ' in f' {full_text} ')
        numeric_df.loc[0, 'kw_dynamic_programming'] = int('dynamic programming' in full_text)
        numeric_df.loc[0, 'kw_recursion'] = int('recursion' in full_text)
        numeric_df.loc[0, 'kw_bfs'] = int('bfs' in full_text)
        numeric_df.loc[0, 'kw_dfs'] = int('dfs' in full_text)
        numeric_df.loc[0, 'kw_greedy'] = int('greedy' in full_text)
        numeric_df.loc[0, 'kw_binary_search'] = int('binary search' in full_text)
        numeric_df.loc[0, 'kw_segment_tree'] = int('segment tree' in full_text)
        numeric_df.loc[0, 'kw_modulo'] = int('modulo' in full_text or '%' in full_text)

        numeric_features = numeric_df.values
        X_final = hstack([X_tfidf, numeric_features])
        class_pred = clf.predict(X_final)[0]
        score_pred = reg.predict(X_final)[0]
        class_map = {0: "Easy", 1: "Medium", 2: "Hard"}
        class_name = class_map[class_pred]
        st.success("✅ Prediction Complete")

        colA, colB = st.columns(2)

        with colA:
            st.metric(
                label="📊 Difficulty Class",
                value=class_name
            )

        with colB:
            st.metric(
                label="🔢 Difficulty Score",
                value=f"{score_pred:.2f} / 10"
            )
