# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 20:12:36 2020

@author: rejid4996
"""

import streamlit as st
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
import base64
from io import BytesIO

st.set_option('deprecation.showfileUploaderEncoding', False)

def main():
    """NLP App with Streamlit"""
    
    st.sidebar.title("Text Matching")
    st.sidebar.subheader("Similarity check")
    
    st.success("For more contents please subscribe to my Youtube Channel https://www.youtube.com/channel/UCgOwsx5injeaB_TKGsVD5GQ")
    
    st.info("Text Matching using Fuzzywuzzy")
    
    uploaded_file = st.sidebar.file_uploader("Your base file should have two columns which contains the text that has to be matched", type="xlsx")
    
    st.sidebar.success("Please reach out to https://www.linkedin.com/in/deepak-john-reji/ for more queries")
    
    
    
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        
        compounds1 = list(df.iloc[:, 0])
        compounds2 = list(df.iloc[:, 1])
        
        compounds1 = [x for x in compounds1 if str(x) != 'nan']
        compounds2 = [x for x in compounds2 if str(x) != 'nan']
        
        # token slider
        slider1 = st.sidebar.slider(label="choose the token sort ratio for voc",
                   min_value=50,
                   max_value=100,
                   step=5)
        
        compound1_match = []
        compound2_match = []
        for i in range(0, len(compounds1)):
            str1 = compounds1[i]
            for j in range(0, len(compounds2)):
                str2 = compounds2[j]
                Token_Sort_Ratio = fuzz.token_sort_ratio(str1,str2)
                if Token_Sort_Ratio > slider1: # <--- this can be tweaked
                    compound1_match.append(compounds1[i])
                    compound2_match.append(compounds2[j])
        
        match_df = pd.DataFrame({'compound 1':compound1_match, 'compound 2':compound2_match})
        
        st.write(match_df)
        
        def to_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            processed_data = output.getvalue()
            return processed_data

        def get_table_download_link(df):
            """Generates a link allowing the data in a given panda dataframe to be downloaded
            in:  dataframe
            out: href string
            """
            val = to_excel(df)
            b64 = base64.b64encode(val)  # val looks like b'...'
            return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download file</a>' # decode b'abc' => abc
    

        st.markdown(get_table_download_link(match_df), unsafe_allow_html=True)
               
if __name__ == "__main__":
    main()
