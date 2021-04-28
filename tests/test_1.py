import requests
import json 
import subprocess
import os
import requests

def run_command(command) : 
    # getting the output of a command 
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()

# first let's clear the current trie
run_command("tricli clear")

# then let's add some words 
WORDS = ["git", "github", "sling", "slingshot", "slingshots"]

for word in WORDS : 
    run_command(f"tricli add {word}")

# check below. 
assert run_command("tricli display") == b' git\n  github\n sling\n  slingshot\n   slingshots\n'

# let's try to delete "githubs"

assert run_command("tricli delete githubs") != None
 
# above we are making sure that trying to delete "githubs" doesn't work, if it did execute the command
# would have returned nothing, but clearly it returned something so the operation isn't working

# time to test whether the trie has a global state by calling the rest endpoint now 
# and seeing if it got these updates made by the CLI

url = "https://a677fgt74e.execute-api.us-east-2.amazonaws.com/first/operations?action=AUTOCOMPLETE&add_string=nonsense&delete_string=nonsense&search_string=nonsense&prefix_string=sl"

# checking with a prefix = 'sl'

suggestions = json.loads(requests.request("GET", url).text)['suggestions']

assert suggestions == ['sling', 'slingshot', 'slingshots']

# also check to see that deleting the word git by calling the client
# is reflected in the CLI as well 

url = "https://a677fgt74e.execute-api.us-east-2.amazonaws.com/first/operations?action=DELETE&add_string=nonsense&delete_string=git&search_string=nonsense&prefix_string=nonsense"

worked = json.loads(requests.request("GET", url).text)['works'] # server sends back to client whether delete operation worked

assert worked # make sure it worked

assert run_command("tricli search git") == b'False\n'

# make sure git is deleted in the CLI too, to test for the global state. 