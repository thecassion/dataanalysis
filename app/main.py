from fastapi import FastAPI, File,UploadFile,HTTPException
from starlette.responses import StreamingResponse
import pandas as pd
from .core.commcare_api import CommCareAPI
import os
import io
from datetime import datetime
app = FastAPI()

@app.get("/")
def root():
    return {"docs_entry_point":"/docs"}


### This function  give you the possibility to download

@app.get("/duplicated/beneficiary")
def duplicated_beneficiary_get():
    cc_domain = os.environ["CC_DOMAIN"]
    cc_api = CommCareAPI(cc_domain,'0.5')
    cc_ben = cc_api.get_cases("beneficiaire",5000)
    return cc_ben

@app.post("/duplicated/benefiary/xlsx")
async def duplicated_beneficiary_xlsx(file:UploadFile=File(...)):
    try:
        df = pd.read_excel(file.file.read())

        ## Take only cases that are not closed
        df_case_open = df.query('closed==False')
        df_case_open["duplicated_national_id"] =df.duplicated(subset=["numero_id"], keep=False)
        df_case_open["duplicated_phone"] =df.duplicated(subset=["numero_telephone"], keep=False)
        df_case_open["duplicated_info"] =df.duplicated(subset=["name","indices.projet","sexe"], keep=False)
        ## Writing an excel file in the RAM memory or buffer
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            df_case_open.to_excel(writer,sheet_name="dupli", index=False)
            writer.save()
        buffer.seek(0)
        # Download the file
        headers = {"Content-Disposition": "attachment; filename=beneficiaire_dup"+"_"+str(datetime.now())+".xlsx"}
        return StreamingResponse(buffer,headers=headers)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))