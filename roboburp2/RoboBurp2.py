import requests
from robot.api import logger
from time import sleep
import json
import os
import subprocess

class RoboBurp2(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, target, api_url = 'http://127.0.0.1:1337/v0.1/'):
        '''
        :param target: Target may be the target URL you are planning on scanning with BurpSuite Pro. Must have trailing
        slash
        :param api_url: The URL that is used to access Burp's API. Must have trailing slash after the "v0.1"
        '''
        self.api_url = api_url
        self.target = target
        self.scan_id = 0
        if not str(self.target).endswith('/'):
            logger.error("Target must end with a slash for Burp to use it")
            raise Exception("Target must end with a slash for Burp to use it")

    def start_burpsuite(self, burp_path):
        '''
        starts burp in GUI Mode. You will still need to click through the options once it starts.
        :param burp_path: Absolute path of burpsuite_pro.jar file
        '''
        cmd = "java -jar {} --user-config-file=user_options.json".format(burp_path)
        subprocess.Popen(cmd.split(' '), stdout=open(os.devnull, 'w'))

    def start_headless_burpsuite(self, burp_path):
        '''
        starts burp in HEADLESS Mode.
        :param burp_path: Absolute path of burpsuite_pro.jar file
        '''
        cmd = "java -Djava.awt.headless=true -jar {} --user-config-file=user_options.json".format(burp_path)
        subprocess.Popen(cmd.split(' '), stdout=open(os.devnull, 'w'))        

    def initiate_crawl_and_scan_against_target(self, auth_logins = None, config_name = None):
        '''

        | initiate crawl and scan against target | auth_logins(dict)  | config_name |

        As the name suggests, this is the default scan for BurpSuite Pro.

        :param auth_logins: dictionary with username and password to perform an authenticated crawl of the app.
        Currently supports a single user
        :param config_name: configuration name for BurpSuite's "NamedConfiguration" object (Audit/Crawl).
        Will be default if not set
        :return:
        '''
        request_data = {}
        if auth_logins and isinstance(auth_logins, dict):
            if 'username' in auth_logins and 'password' in auth_logins:
                request_data['application_logins'] = [auth_logins]

        if config_name and isinstance(config_name,str):
            request_data['scan_configurations'] = [{'name': config_name}]

        request_data['urls'] = [self.target]

        scan_request = requests.post(self.api_url + "/scan", json=request_data)
        if scan_request.status_code == 201:
            scan_id = scan_request.headers.get('Location')
            self.scan_id = scan_id
            logger.info("Scan ID for the current task has been set to: {}".format(scan_id))
            return self.scan_id
        else:
            logger.error(scan_request.content)
            raise Exception(scan_request.content)

    def initiate_scan_against_target(self, config_name = None):
        '''
        This is very similar to crawl and scan, except that this mode assumes that you have already crawled the app
        Consider only using "Audit" based NamedConfigurations to scan (audit) only

        :param config_name: optional, where NamedConfiguration for Audit should be provided
        :return:
        '''
        request_data = {}
        if config_name and isinstance(config_name,str):
            request_data['scan_configurations'] = [{'name': config_name}]

        request_data['urls'] = [self.target]
        scan_request = requests.post(self.api_url + "scan", json=request_data)
        if scan_request.status_code == 201:
            scan_id = scan_request.headers.get('Location')
            self.scan_id = scan_id
            logger.info("Scan ID for the current task has been set to: {}".format(scan_id))
            return self.scan_id
        else:
            logger.error(scan_request.content)
            raise Exception(scan_request.content)

    def make_status_request(self, id):
        '''
        This is not a Robot Framework Keyword. Don't use it
        '''
        url = "{}scan/{}".format(self.api_url, id)
        logger.info(url)
        status_req = requests.get(url)
        if status_req.status_code == 200:
            return status_req.json()
        else:
            raise Exception("Unable to get scan status for the scan requested, {}".format(status_req.content))


    def get_burp_scan_status_for_id(self, scan_id, status_interval = 10):
        '''
        This keyword can be used to get a running status of the scan based on the scan_id. ]
        ID is a mandatory paramater
        :param status_interval: you can set a status interval that it needs to log of. Defaults to 10 seconds
        '''
        logger.info("Scan ID: {}".format(scan_id))
        while self.make_status_request(id = scan_id)['scan_status'] != "succeeded":
            logger.info(self.make_status_request(scan_id))
            sleep(status_interval)

    def get_burp_scan_results_for_id(self, id, filename = "burp_scan_results.json"):
        '''
        Get results of Burp Scan by id and write to file
        :param filename: provide a custom file path (absolute). must end with json
        :return:
        '''
        scan_results = self.make_status_request(id)
        with open(filename, 'w') as resultsfile:
            resultsfile.write(json.dumps(scan_results['issue_events']))
        logger.info("Successfully written results to file")

    def stop_burpsuite(self):
        '''
        stops burp process
        '''
        cmd = "pkill -f burp"
        subprocess.Popen(cmd.split(' '), stdout=open(os.devnull, 'w'))        




