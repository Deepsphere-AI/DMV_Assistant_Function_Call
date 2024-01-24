import streamlit as vAR_st
vAR_st.set_page_config(page_title="DMV Assistant", layout="wide")

from DSAI_Utility.DSAI_Utility import All_Initialization,CSS_Property
from DSAI_SourceCode_Implementation.DSAI_Assistant_API import FunctionWithAssistant
import traceback



if __name__=='__main__':
    vAR_hide_footer = """<style>
            footer {visibility: hidden;}
            </style>
            """
    vAR_st.markdown(vAR_hide_footer, unsafe_allow_html=True)
    try:
        # Applying CSS properties for web page
        CSS_Property("DSAI_Utility/DSAI_style.css")
        # Initializing Basic Componentes of Web Page
        choice = All_Initialization()
        
        if choice=="Interact with Bigquery in NL":
        
            FunctionWithAssistant()
            
            
        else:
            pass


    except BaseException as exception:
        print('Error in main function - ', exception)
        exception = 'Something went wrong - '+str(exception)
        traceback.print_exc()
        vAR_st.error(exception)