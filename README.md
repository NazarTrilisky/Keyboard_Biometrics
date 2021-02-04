## Keyboard_Biometrics
Identify users by their keyboard dynamics (how they type).


## Steps to Launch
1. Update "your_certificate_name_here" with your certificate.
2. Start the server: `sudo python server.py`
3. Browse to either https://127.0.0.1 or to https://your_domain_name.tld


## Folder Structure
* certificate (folder): contains .csr, .key, and .crt files for HTTPS to work
* allowed_uuids.json (file): lists accepted UUIDs (which are access tokens for using this web service)
* keystroke_patterns (folder): stores the keystroke pattern arrays for each UUID
  These keystroke pattern arrays are what is used to identify a user by her typing pattern.
* src (folder):
    - keyboard_dynamics.py: logic for managing typing pattern arrays
    - requirements.txt: python dependencies (Note: this project was tested with Python 3.8)
    - responses.py: list of HTTP responses to API calls
    - web (folder): contains server.py, which starts the web server and the web page files.

## Approach
The high level approach is to store time differences for all key-down and key-up events and
to use these time differences to identify users.
