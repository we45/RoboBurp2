*** Settings ***
Library  RoboBurp2  http://localhost:6070/

# you can run this app by pulling the docker image: we45/wecare
# command: docker run -d -p 6070:80 we45/wecare

*** Variables ***
${BURP_EXEC}  burpsuite_pro.jar
${CONFIG_JSON}  user_options.json
${SCAN_CONFIG}  Audit checks - light active

*** Test Cases ***
Burp Start
    start burpsuite  ${BURP_EXEC}  ${CONFIG_JSON}
    sleep  40

Burp Default Scan
    ${auth}=  create dictionary  username=bruce.banner@we45.com  password=secdevops
    ${id}=  initiate crawl and scan against target  auth_logins=${auth}  config_name=${SCAN_CONFIG}
    set suite variable  ${SCAN_ID}  ${id}

Burp Scan Status
    sleep  3
    get burp scan status for id  ${SCAN_ID}

Burp Write Results to File
    get burp scan results for id  ${SCAN_ID}

