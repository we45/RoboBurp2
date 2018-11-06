*** Settings ***
Library  RoboBurp2  http://localhost:6070/

*** Variables ***
${BURP_EXEC}  /Applications/Burp_Suite_Professional.app/Contents/Resources/app/burpsuite_pro.jar

*** Test Cases ***
Burp Start
    start burpsuite  ${BURP_EXEC}
    sleep  20

Burp Default Scan
    ${auth}=  create dictionary  username=bruce.banner@we45.com  password=secdevops
    ${id}=  initiate crawl and scan against target  auth_logins=${auth}
    set suite variable  ${SCAN_ID}  ${id}

Burp Scan Status
    sleep  3
    get burp scan status for id  ${SCAN_ID}

Burp Write Results to File
    get burp scan results for id  ${SCAN_ID}

