# contains everything needed for the CLI
import sys 
import ssl 
import json 
import requests

base_url = "https://a677fgt74e.execute-api.us-east-2.amazonaws.com/first/operations?"

erroneous_message = {"message": "Internal server error"} # just to check 

add_string_filler = delete_string_filler = prefix_string_filler = search_string_filler = "nonsense"

def main() : 
    arguments = sys.argv[1:] # exclude the first argument because that's just "tricli"
    
    if not len(arguments) : 
        # they just typed "tricli"
        
        print("Invalid command. tricli's Command Line Interface is only for adding/deleting words, \n searching for words,getting autocomplete suggestions or displaying the trie.")

        quit()
        
    
    action = arguments[0] # whatever's first is the action 
    
    # now go case by case 

    if action.upper() == "CLEAR" : 
        # send GET request 
        url = base_url + "action=CLEAR" + "&add_string=" + add_string_filler + "&delete_string=" + delete_string_filler \
            + "&prefix_string=" + prefix_string_filler + "&search_string=" + search_string_filler
        response = json.loads(requests.request("GET", url).text) # get response
        # used snippets for JSON loading and requests from here : https://rowelldionicio.com/parsing-json-with-python/

        if response == erroneous_message : 
            print("Unable to perform this operation.")
    
    elif action.upper() == "SEARCH" : 
        if len(arguments) < 2 : 
            print("Didn't receive the string you want to search for in the trie.")
        else : 
            search_string = arguments[1]
            url = base_url + "action=SEARCH" + "&add_string=" + add_string_filler + "&delete_string=" + delete_string_filler \
            + "&prefix_string=" + prefix_string_filler + "&search_string=" + search_string

            response = json.loads(requests.request("GET", url).text)

            if response == erroneous_message : print("Unable to perform this operation.")

            else : 
                print(response["in"])
    
    elif action.upper() == "DELETE" : 
        if len(arguments) < 2 : 
            print("Didn't receive the string you want to delete in the trie.")
        else : 
            delete_string = arguments[1]
            url = base_url + "action=DELETE" + "&add_string=" + add_string_filler + "&delete_string=" + delete_string \
            + "&prefix_string=" + prefix_string_filler + "&search_string=" + search_string_filler

            response = json.loads(requests.request("GET", url).text)

            if response == erroneous_message : print("Unable to perform this operation.")
            
            else : 
                if not response['works'] :
                    # not working 
                    print("Failed - deleting a string not in the trie.")
    
    elif action.upper() == "ADD" : 
        if len(arguments) < 2 : 
            print("Didn't receive the string you want to add into the trie.")
        
        else : 
            add_string = arguments[1]
            url = base_url + "action=ADD" + "&add_string=" + add_string + "&delete_string=" + delete_string_filler \
            + "&prefix_string=" + prefix_string_filler + "&search_string=" + search_string_filler

            response = json.loads(requests.request("GET", url).text)
            
            if response == erroneous_message : print("Unable to perform this operation.")
            
            # otherwise, successful 
    
    elif action.upper() == "DISPLAY" : 
        url = base_url + "action=DISPLAY" + "&add_string=" + add_string_filler + "&delete_string=" + delete_string_filler \
            + "&prefix_string=" + prefix_string_filler + "&search_string=" + search_string_filler

        response = json.loads(requests.request("GET", url).text)

        if response == erroneous_message : print("Unable to perform this operation.")

        else : 
            words = response['words']

            if not words : 
                print("No words in the trie.")

            for word in words : 
                print(word)
    
    elif action.upper() == "AUTOCOMPLETE" :
        if len(arguments) < 2 : 
            print("Didn't receive the prefix you want to find suggestions for.")
        
        else : 
            prefix_string = arguments[1]
            url = base_url + "action=AUTOCOMPLETE" + "&add_string=" + add_string_filler + "&delete_string=" + delete_string_filler \
                + "&prefix_string=" + prefix_string + "&search_string=" + search_string_filler
            
            response = json.loads(requests.request("GET", url).text)

            if response == erroneous_message : print("Unable to perform this operation.")
            else : 

                if not response['suggestions'] : 
                    print("No suggestions for this prefix.")
                    
                print(response['suggestions'])

    else : 
        print(f"No known action : {action}")

if __name__ == "__main__" :
    main() 
