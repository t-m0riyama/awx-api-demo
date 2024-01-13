import json
import requests
import jmespath
from requests.auth import HTTPBasicAuth


class AWXApiHelper:

    # const
    JOB_TEMPLATE_ID_NOT_FOUND = -1
    JOB_TEMPLATE_ID_CONNECTION_FAILED = -2
    JOB_LAUNCH_FAILED = -3
    JOB_LAUNCH_CONNECTION_FAILED = -4
    JOB_STATUS_FAILED = -5
    JOB_STATUS_CONNECTION_FAILED = -6

    @staticmethod
    def login(uri_base, loginid, password):
        reqest_url = uri_base + '/api/v2/me/'
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(reqest_url, headers=headers, auth=HTTPBasicAuth(
                loginid, password), verify=False)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    @staticmethod
    def set_vm_cpu_memory(uri_base, loginid, password, job_template_name, parameter_dict):
        headers = {'Content-Type': 'application/json'}
        vars_json = AWXApiHelper.generate_vars(parameter_dict)
        try:
            job_template_id = AWXApiHelper.get_job_template_id(
                uri_base, loginid, password, job_template_name)
            launch_url = uri_base + \
                '/api/v2/job_templates/{}/launch/'.format(job_template_id)
            print(launch_url)
            print(vars_json)
            response = requests.post(launch_url, headers=headers, auth=HTTPBasicAuth(
                loginid, password), verify=False, data=vars_json)
            if response.status_code == 201:
                response_results = jmespath.search('job', response.json())
                print("job_id: " + str(response_results))
                return response_results
            else:
                return AWXApiHelper.JOB_LAUNCH_FAILED
        except Exception as e:
            return AWXApiHelper.JOB_LAUNCH_CONNECTION_FAILED

    @staticmethod
    def generate_vars(parameter_dict):
        return json.dumps({"extra_vars": parameter_dict})

    @staticmethod
    def get_job_template_id(uri_base, loginid, password, job_template_name):
        job_templates_url = uri_base + '/api/v2/job_templates/'
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(job_templates_url, headers=headers, auth=HTTPBasicAuth(
                loginid, password), verify=False)
            if response.status_code == 200:
                response_results = jmespath.search(
                    'results[?name == `{}`].id'.format(job_template_name), response.json())
                return response_results[0]
            else:
                return AWXApiHelper.JOB_TEMPLATE_ID_NOT_FOUND
        except Exception as e:
            return AWXApiHelper.JOB_TEMPLATE_ID_CONNECTION_FAILED

    @staticmethod
    def get_job_status(uri_base, loginid, password, job_id):
        job_status_url = uri_base + '/api/v2/jobs/{}/'.format(job_id)
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(job_status_url, headers=headers, auth=HTTPBasicAuth(
                loginid, password), verify=False)
            print(response.status_code)
            print(response.json())
            print(jmespath.search('status', response.json()))
            if response.status_code == 200:
                response_results = jmespath.search('status', response.json())
                print("job_status: " + str(response_results))
                return response_results
            else:
                return str(AWXApiHelper.JOB_STATUS_FAILED)
        except Exception as e:
            return str(AWXApiHelper.JOB_STATUS_CONNECTION_FAILED)
