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

# we can start by adding some words

WORDS = ['boo', 'book', 'back', 'trie', 'tries']

for word in WORDS : 
    run_command(f"tricli add {word}")

# next let's try to search for some words 

assert (run_command("tricli search boo")) == b'True\n' # it is there 

# let's see if we can delete some words by sending a direct request to the client 
# to see if the above add operations were globally maintained. 

url = "https://a677fgt74e.execute-api.us-east-2.amazonaws.com/first/operations?action=DELETE&add_string=nonsense&delete_string=boo&search_string=nonsense&prefix_string=nonsense"

works = json.loads(requests.request("GET", url).text)['works']

assert works # make sure it works

# also let's check to make sure that book is still there, even if boo (shares the same prefix) was deleted

url = "https://a677fgt74e.execute-api.us-east-2.amazonaws.com/first/operations?action=SEARCH&add_string=nonsense&delete_string=nonsense&search_string=book&prefix_string=nonsense"

books_exists = json.loads(requests.request("GET", url).text)['in']

assert books_exists # make sure it is there

# finally let's add a word by sending a request to the client, and then testing with the CLI method 

url = "https://a677fgt74e.execute-api.us-east-2.amazonaws.com/first/operations?action=ADD&add_string=BAM&delete_string=nonsense&search_string=nonsense&prefix_string=nonsense"

requests.request("GET", url)

assert "BAM" in str(run_command("tricli autocomplete B")) 
# make sure it is there with the character B
# str() operation to deal with the b"string" as output

# also we can test for case sensitiveness by : 
assert run_command("tricli search bam") == b'False\n' # make sure bam isn't in there