*** Settings ***
Library  RoboBurp2  http://localhost:5050/
Library  REST  http://localhost:5050  proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

# you can run this app by pulling the docker image: abhaybhargav/vul_flask
# command: docker run -d -p 5050:5050 abhaybhargav/vul_flask

*** Variables ***
${BURP_EXEC}  /Applications/Burp_Suite_Professional.app/Contents/Resources/app/burpsuite_pro.jar

*** Test Cases ***
Burp Start
    start burpsuite  ${BURP_EXEC}
    sleep  20

Authenticate to Web Service
    &{res}=  POST  /login  {"username": "admin", "password": "admin123"}
    Integer  response status  200
    set suite variable  ${TOKEN}  ${res.headers["Authorization"]}

Get Customer by ID
    [Setup]  Set Headers  { "Authorization": "${TOKEN}" }
    GET  /get/2
    Integer  response status  200

Post Fetch Customer
    [Setup]  Set Headers  { "Authorization": "${TOKEN}" }
    POST  /fetch/customer  { "id": 3 }
    Integer  response status  200

Search Customer by Username
    [Setup]  Set Headers  { "Authorization": "${TOKEN}" }
    POST  /search  { "search": "dleon" }
    Integer  response status  200

Burp Authenticated Scan Only
    ${auth}=  create dictionary  username=bruce.banner@we45.com  password=secdevops
    ${id}=  initiate scan against target  config_name=Audit checks - medium active
    set suite variable  ${SCAN_ID}  ${id}

Burp Scan Status
    sleep  3
    get burp scan status for id  ${SCAN_ID}

Burp Write Results to File
    get burp scan results for id  ${SCAN_ID}