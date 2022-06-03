import json
import requests
import pandas as pd


class HttpUtil:

    def http_post(urlParams, filename):
        with open('headers.json') as f:
            requestParams = json.load(f)
        baseDir = requestParams['baseDir']
        if("analysisprocesses" in urlParams or "orgs" in urlParams):
            headers = requestParams['suSecurityInfo']
        else:
            headers = requestParams['OrgAdminSecurityInfo']
        baseUrl = requestParams['baseUrl']
        url = baseUrl + urlParams 
        body = baseDir + filename
        with open(body) as f:
            request_data = json.load(f)
        request_data = json.dumps(request_data)
        #info = json.loads(data_from_api)
        #print (headers)
        #print(url,request_data)
        response = requests.post(url, headers=headers, data=request_data)
        #print(response)
        return response

    def http_post_withoutbody(urlParams):
        with open('headers.json') as f:
            requestParams = json.load(f)
        if("analysisprocesses" in urlParams or "orgs" in urlParams):
            headers = requestParams['suSecurityInfo']
        else:
            headers = requestParams['OrgAdminSecurityInfo']
        baseUrl = requestParams['baseUrl']
        url = baseUrl + urlParams 
        response = requests.post(url, headers=headers)
        return response


    def http_post_withfile(urlParams, filename):
        with open('headers.json') as f:
            requestParams = json.load(f)
        baseDir = requestParams['baseDir']
        if("analysisprocesses" in urlParams or "orgs" in urlParams):
            headers = requestParams['suSecurityInfo']["Authorization"]
        else:
            headers = requestParams['OrgAdminSecurityInfoforfile']
        baseUrl = requestParams['baseUrl']
        url = baseUrl + urlParams
        body = baseDir + filename
        test_file = open(body, "rb")
        response = requests.post(url, headers=headers, data={"mysubmit":"Go"}, files={"archive": (filename, test_file)})
        return response
        

    def http_get(urlParams):
        with open('headers.json') as f:
            requestParams = json.load(f)
            headers = requestParams['securityInfo']
        
        baseUrl = requestParams['baseUrl']
        url = baseUrl + urlParams 
        #print (url)

        response = requests.get(url, headers=headers)
        return response

    def http_get_security(urlParams):
        with open('headers.json') as f:
            requestParams = json.load(f)
        if("admin" in urlParams or "realms" in urlParams):
            headers = requestParams['suSecurityInfo']
        else:
            headers = requestParams['OrgAdminSecurityInfo']
        baseUrl = requestParams['securityBaseUrl']
        url = baseUrl + urlParams 
        response = requests.get(url, headers=headers)
        return response

   



    def http_get_with_params(urlParams,queryParams):
        with open('headers.json') as f:
            requestParams = json.load(f)
        if("analysisprocesses" in urlParams or "orgs" in urlParams):
            headers = requestParams['suSecurityInfo']
        else:
            headers = requestParams['OrgAdminSecurityInfo']
        baseUrl = requestParams['baseUrl']
        url = baseUrl + urlParams 
        #print (url)

        response = requests.get(url,params=queryParams, headers=headers)
        return response

    def http_delete(urlParams):
        with open('headers.json') as f:
            requestParams = json.load(f)
        if("analysisprocesses" in urlParams or "orgs" in urlParams or "testorg" in urlParams):
            headers = requestParams['suSecurityInfo']
        else:
            headers = requestParams['OrgAdminSecurityInfo']
        baseUrl = requestParams['baseUrl']
        url = baseUrl + urlParams 
        
        response = requests.delete(url, headers=headers)
        return response

    def http_put_for_delete(urlParams,filename):
        with open('headers.json') as f:
            requestParams = json.load(f)
        baseDir = requestParams['baseDir']
        headers = requestParams['OrgAdminSecurityInfo']
        baseUrl = requestParams['baseUrl']
        url = baseUrl + urlParams 
        body = baseDir + filename
        with open(body) as f:
            request_data = json.load(f)
        request_data = json.dumps(request_data) 
        print(url,request_data)
        response = requests.put(url, headers=headers, data=request_data)
        return response

    def http_put_for_tasks(urlParams):
        with open('headers.json') as f:
            requestParams = json.load(f)
       
        if("analysisprocesses" in urlParams or "orgs" in urlParams):
            headers = requestParams['suSecurityInfo']
        else:
            headers = requestParams['OrgAdminSecurityInfo']

        if("tasks" in urlParams ):
            baseUrl = requestParams['baseUrl']
            url = baseUrl + urlParams 
            taskurl = baseUrl + "tasks"
            response = requests.get(taskurl, headers=headers)
            # print(response.text)
            json_response = response.text
            print(json_response)
            df = pd.read_json(json_response)
            max_id = df['reveloTaskId'].max()
            a_file = open("deleteTask.json", "r")
            json_object = json.load(a_file)
            a_file.close()
            # print(json_object)
            json_object["taskIds"] = [(max_id)]
            a_file = open("deleteTask.json", "w")
            json.dump(json_object, a_file)
            a_file.close()
            response = requests.put(url, headers=headers, json=json_object)
            return response

    def http_delete_for_delete(urlParams,filename):
        with open('headers.json') as f:
            requestParams = json.load(f)
        baseDir = requestParams['baseDir']
        if("analysisprocesses" in urlParams or "orgs" in urlParams or "users" in urlParams):
            headers = requestParams['suSecurityInfo']
        else:
            headers = requestParams['OrgAdminSecurityInfo']
        baseUrl = requestParams['baseUrl']
        url = baseUrl + urlParams 
        body = baseDir + filename
        with open(body) as f:
            request_data = json.load(f)
        request_data = json.dumps(request_data) 
        print(url,request_data)
        response = requests.delete(url, headers=headers, data=request_data)
        return response


    

    def http_post_su_runtime(urlParams, filename):
        with open('headers.json') as f:
            requestParams = json.load(f)
        baseDir = requestParams['baseDir']
        headers = requestParams['suSecurityInfo']
        baseUrl = requestParams['baseUrl']
        url = baseUrl + urlParams 
        body = baseDir + filename
        with open(body) as f:
            request_data = json.load(f)
        request_data = json.dumps(request_data)
        response = requests.post(url, headers=headers, data=request_data)
        return response


    def http_get_su_runtime(urlParams):
        with open('headers.json') as f:
            requestParams = json.load(f)
        headers = requestParams['suSecurityInfo']
        baseUrl = requestParams['baseUrl']
        url = baseUrl + urlParams 
        response = requests.get(url, headers=headers)
        return response
    
    # def http_get_by_id(urlParams):
    #     with open('headers.json') as f:
    #         requestParams = json.load(f)
    #     headers = requestParams['suSecurityInfo']
    #     baseUrl = requestParams['baseUrl']
    #     url = baseUrl + urlParams
    #     response = requests.request("GET", url, headers=headers)
    #     output = response.text
    #     df = pd.read_json(output)
    #     max_id = df['toolId'].max()
    #     params = { 'toolId': max_id }
    #     # url = baseUrl + urlParams + max_id
    #     url += max_id
    #     response = requests.get(url, params=params)
    #     return response

    def http_get_by_id(urlParams):
        with open('headers.json') as f:
            requestParams = json.load(f)
        if("analysisprocesses" in urlParams or "tools" in urlParams ):
            headers = requestParams['suSecurityInfo']
        else:
            headers = requestParams['OrgAdminSecurityInfo']
        baseUrl = requestParams['baseUrl']
        url = baseUrl + urlParams 
        response = requests.get(url, headers=headers)
       
        return response

    def http_post_su(urlParams):
        with open('headers.json') as f:
            requestParams = json.load(f)
        
        baseUrl = requestParams['securityBaseUrl']
        url =  baseUrl + urlParams 
        payload='username=su&password=pass123&client_id=reveloadmin&grant_type=password'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
         }
        response = requests.post(url, headers=headers, data=payload)
        return response


    def http_post_org(urlParams):
        with open('headers.json') as f:
            requestParams = json.load(f)
        
        baseUrl = requestParams['securityBaseUrl']
        url =  baseUrl + urlParams 
        payload='username=orgadmin&password=pass123&client_id=reveloadmin&grant_type=password'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
         }
        response = requests.post(url, headers=headers, data=payload)
        return response


    def http_post_user(urlParams):
        with open('headers.json') as f:
            requestParams = json.load(f)
        
        baseUrl = requestParams['securityBaseUrl']
        url =  baseUrl + urlParams 
        payload='username=testuser&password=pass123&client_id=reveloadmin&grant_type=password'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
         }
        response = requests.post(url, headers=headers, data=payload)
        return response



    def http_post_with_id(urlParams):
        with open('headers.json') as f:
            requestParams = json.load(f)
        baseDir = requestParams['baseDir']
       
        if("analysisprocesses" in urlParams or "orgs" in urlParams):
            headers = requestParams['suSecurityInfo']
        else:
            headers = requestParams['OrgAdminSecurityInfo']

        if("links" in urlParams ):
            baseUrl = requestParams['baseUrl']
            url = baseUrl + urlParams 
            toolurl = baseUrl + "analysismodels/testmodel/tools/"
            response = requests.get(toolurl, headers=headers)
            #print(response.text)
            json_response = response.text
            #print(json_response)
            df = pd.read_json(json_response)
            #print(df)
            max_id = df['toolId'].max()
            #print(max_id)
            url = baseUrl + urlParams
            a_file = open("createLink.json", "r")
            #print(a_file)
            json_object = json.load(a_file)
            a_file.close()
            #print(json_object)
            json_object["fromToolId"] = int(max_id)
            json_object["toToolId"] = int(max_id-1)
            #print(json_object)
            # a_file = open("createLink.json", "w")
            # print(a_file)
            # json.dump(json_object, a_file)
            #a_file.close()
            #print(url)
            #print(headers)
            json_object = json.dumps(json_object)
            print(json_object)
            response = requests.post(url, headers=headers, data=json_object)
            print(response)
            return response
        if("tools" in urlParams ):
            baseUrl = requestParams['baseUrl']
            url = baseUrl + urlParams
            response = requests.get(url, headers=headers)
            output = response.text
            df = pd.read_json(output)
            max_id = df['toolId'].max()
            url1 = url+str(max_id)
            a_file = open("modifyTool.json", "r")
            json_object = json.load(a_file)
            a_file.close()
            json_object["toolId"] = int(max_id)
            # a_file = open("modifyTool.json", "w")
            # json.dump(json_object, a_file)
            # a_file.close()
            url1 = url+str(max_id)
            response2 = requests.request("POST", url1, headers=headers, json=json_object)
            return response2

    def http_refresh(urlParams):
        with open('headers.json') as f:
            requestParams = json.load(f)
        baseDir = requestParams['baseDir']
        if("analysisprocesses" in urlParams or "orgs" in urlParams):
            headers = requestParams['suSecurityInfo']
        else:
            headers = requestParams['OrgAdminSecurityInfo']
        baseUrl = requestParams['baseUrl']
        url = baseUrl + urlParams 
        
        # with open(body) as f:
        #     request_data = json.load(f)
        # request_data = json.dumps(request_data)
        #info = json.loads(data_from_api)
        #print (headers)
        #print(url,request_data)
        response = requests.post(url, headers=headers)
        #print(response)
        return response
    