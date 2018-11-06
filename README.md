# RoboBurp2

### Robot Framework Library for BurpSuite Pro

> Write all your BurpSuite Pentest Automations in Natural Language Syntax recipes

**NOTE: You should NOT be using this in your CI/CD environments, as it will violate the BurpSuite Licensing Policy.
Burp only allows CI/CD requirements to leverage Burp's Enterprise Product.
You can use this as a pentester on your laptop/testing environment to automate stuff**

Please refer to the test (directory) for examples of how you can use this. Video will follow

### Installation

* You need to have a BurpSuite Pro license to use this
* Install `pip install RoboBurp2` to install this and its deps. I recommend `pipenv`
* Use this lib to automate scanning, crawling of Burp with its new 2.0 API

### Limitations

* This can scan one app at a time. Haven't provided for multiple scan tasks yet.
* This library can start Burp, but Burp doesn't seem to provide an API call to shut it down. So it doesn't
* When Burp starts, you might need to click some prompts to get to an operational mode.
I advise that you give it adequate sleep time for this to happen

### Keywords

`| start burpsuite  | <PATH> |`

This starts burpsuite from the path in your system. This needs to be the absolute path of the burpsuite_pro.jar file


`| initiate crawl and scan against target  | auth_logins (dictionary)  | config_name(string)  |`

This is the "Default Scan" where you can crawl and then audit(scan).
If you need to do an authenticated crawl, you need to provide a dictionary value to
the "auth_logins" argument.

You can also specify the config_name from a list of `NamedConfigurations` that can be found
in your BurpSuite Pro's Top navbar under `Burp >> Configuration library`

This returns a `scan_id` that you can use to get status and results later


`| initiate scan against target | config_name  |`

This is pretty much the same as above, except that this should be used
when you already have test automation that has "crawled" the app and you only use
this mode to "audit". You will need to provide a config_name in this case.
Preferably only an Audit config_name, else Burp will try and crawl and audit (default)

This returns a `scan_id` that you can use to get status and results later


`| get burp scan status for id  | scan_id  |`

This fetches the scan status for the particular scan_id that you can use to continuously wait
for scan to complete. Once the `scan_status` shows up as `succeeded`, this function stops

`| get burp scan results for id  | scan_id  | filename (optional) | `

This fetches the scan results for the particular scan_id and writes the results to a JSON file
You can provide as an arg, the full path to the file you want to write it to. Else
the library writes a file called `burp_scan_results.json` in the current working directory

