import os
import requests
class CommCareAPI:
    def __init__(self,domain,version) -> None:
        self.domain = domain
        self.version = version
        self.base_url = f"https://www.commcarehq.org/a/{domain}/api/v{version}/"
        self.bbase_url = f"https://www.commcarehq.org/a/{domain}/"
        self.auth = (os.environ["COMMCARE_USERNAME"], os.environ["COMMCARE_PASSWORD"])
    def get_cases(self,type,limit,closed=False):
        url = self.base_url + "case/"
        parameters = {"type": type, "limit": limit}
        response = requests.get(url, auth = self.auth, params= parameters).json()
        objects = response["objects"]

        while response["meta"]["next"]:
            response = requests.get(url+response["meta"]["next"], auth=self.auth).json()
            objects += response["objects"]
            print(response["meta"]["next"])
        return objects
    def get_case(self,case_id):
        url = self.base_url + f"case/{case_id}"
        response = requests.get(url, auth = self.auth).json()
        return response
    def get_case_properties(self,case_id):
        url = self.base_url + f"case/{case_id}"
        response = requests.get(url, auth = self.auth).json()
        return response
    def get_forms(self,xmlns,limit):
        url = self.base_url + "form/"
        parameters = {"xmlns": xmlns, "limit": limit}
        response = requests.get(url, auth = self.auth, params= parameters).json()
        objects = response["objects"]

        while response["meta"]["next"]:
            response = requests.get(url+response["meta"]["next"], auth=self.auth).json()
            objects += response["objects"]
        return objects
    def get_form(self,form_id):
        url = self.base_url + f"form/{form_id}"
        response = requests.get(url, auth = self.auth).json()
        return response

    def bulkupload(self,data):
        url = self.bbase_url + "importer/excel/bulk_upload_api/"
        print(url)
        response = requests.post(url, auth = self.auth,data={"case_type":data["case_type"]},files={"file":data["file"]})
        return response