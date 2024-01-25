from google.cloud import bigquery
import os

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Admin\Downloads\elp-prod-c69c22187b05.json"


def get_config_details(vAR_config):
    
    # PST_DATE,PST_TIMESTAMP,LICENSE_PLATE_CONFIG,TOXIC,SEVERE_TOXIC,OBSCENE,IDENTITY_HATE,INSULT,THREAT,RECOMMENDATION,REASON,TOXIC_REASON,SEVERE_TOXIC_REASON,OBSCENE_REASON,IDENTITY_HATE_REASON,INSULT_REASON,THREAT_REASON
    print("Calling Bigquery Method")
    vAR_client = bigquery.Client()
    vAR_sql =(
        "select PST_DATE,PST_TIMESTAMP,LICENSE_PLATE_CONFIG,TOXIC,SEVERE_TOXIC,OBSCENE,IDENTITY_HATE,INSULT,THREAT,RECOMMENDATION,REASON,TOXIC_REASON,SEVERE_TOXIC_REASON,OBSCENE_REASON,IDENTITY_HATE_REASON,INSULT_REASON,THREAT_REASON from `elp-prod.DMV_ELP_WSI.DMV_ELP_MLOPS_RESPONSE` where LICENSE_PLATE_CONFIG='"+vAR_config+"'"
    )

    vAR_df = vAR_client.query(vAR_sql).to_dataframe()


    print("Data - ",vAR_df.head())

    vAR_result = f"""Here is the configuration details: 
   DATE : {vAR_df.iloc[0][0]}\n
   TIMESTAMP : {vAR_df.iloc[0][1]}\n
   LICENSE_PLATE_CONFIG : {vAR_df.iloc[0][2]}\n
   TOXIC : {vAR_df.iloc[0][3]}\n
   SEVERE_TOXIC : {vAR_df.iloc[0][4]}\n
   OBSCENE : {vAR_df.iloc[0][5]}\n
   IDENTITY_HATE : {vAR_df.iloc[0][6]}\n
   INSULT : {vAR_df.iloc[0][7]}\n
   THREAT : {vAR_df.iloc[0][8]}\n
   RECOMMENDATION : {vAR_df.iloc[0][9]}\n
   REASON : {vAR_df.iloc[0][10]}\n
   TOXIC_REASON : {vAR_df.iloc[0][11]}\n
   SEVERE_TOXIC_REASON : {vAR_df.iloc[0][12]}\n
   OBSCENE_REASON : {vAR_df.iloc[0][13]}\n
   IDENTITY_HATE_REASON : {vAR_df.iloc[0][14]}\n
   INSULT_REASON : {vAR_df.iloc[0][15]}\n
   THREAT_REASON : {vAR_df.iloc[0][16]}\n
   """

    return vAR_result