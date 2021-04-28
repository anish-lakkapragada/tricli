# Server README

This is the readme containing the information about the server side to host and manage the trie data structure. 

## Overview

When the user wants to do an operation to the trie data structure, they simply use a command defined by the CLI. Then that command is processed and received to the trie data structure on the server side using a REST API. The way this works is that a web page (the client) is opened up with the given parameters on what operation the user wants to do and any other parameters (what string to they want to add/delete/search/autocomplete for.) The client sends this information in JSON using HTTP protocol to the server. The server then receives it, processes it, and sends back to the client any information they may need (e.x. did the delete work). Let’s take a look at the tools I used to develop the REST API, client, and server. 

## The Tools

To build the REST API, I used AWS API Gateway to setup a client. When the command is processed by the CLI, the JSON data is created and sent to the client. The client sends this JSON data to the server using a GET HTTP operation, where the operation is done on the trie. I created an AWS Lambda function on the server-side to process this JSON data, and perform the operation on the trie data structure. The AWS Lambda Function is called "lambda_function.py" and is called whenever the client performs the GET operation. Once the operation is performed, any information is sent back to the client using JSON data. This information could be whether the delete operation worked, what are the autocomplete suggestions, etc. The CLI then scrapes this JSON from the client, and passes information to the user (e.x. telling the user the delete operation didn't work.) I'll go over how the global state is managed next, talk about how to test it with curl, and then go every operation and its involvement in the REST API in more detail. 

## Global State Management

The data structure is represented with a Node() class I created (defined in lambda_function.py). The Node() class stores for a given node its children (essentially representing the trie as a tree), and so to store the entire trie I just need to store the root node (which contains the children nodes, each of which contains their children, etc.). Because the AWS Lambda function is not constantly running, the trie data structure is serialized into a (pickle) file. This file is stored in an AWS S3 Bucket. Every time the server is called, the root node is accessed from the pickle file (in the S3 bucket) and then used. If the operation is changing the trie (ADD/DELETE), the pickle file in the S3 Bucket is rewritten with the new root node (that contains the changes). In order to perform S3 operations inside of AWS Lambda I had to use boto3, AWS's SDK. I included the stack posts I used in lambda_function.py. 


## Testing

You can test the REST API using curl. All CAPITALIZED names in the url below are parameters, I will explain what they mean below. Make sure to enter all parameters or else you will incur an "Internal Server Error".

```curl
curl "https://a677fgt74e.execute-api.us-east-2.amazonaws.com/first/operations?action=ACTION&add_string=ADD_STRING&delete_string=DELETE_STRING&prefix_string=PREFIX_STRING&search_string=SEARCH_STRING"
```

Use bash when doing this. Wait a few seconds, and you will get the JSON response (from the server) back in the terminal.

### Parameters : 

Note if you are doing a different action (say ADD) than the parameter (say DELETE_STRING) you can put something random for that parameter, because it will be ignored. 
- ACTION : this can be "ADD" or "DELETE" or "CLEAR" or "AUTOCOMPLETE" or "SEARCH" or "DISPLAY". Notice how "CLEAR" and "DISPLAY" don't nead any more (meaningful) parameters. 
- ADD_STRING : this is the string you want to add into the trie. 
- DELETE_STRING : this is the string (or prefix) you want to delete from the trie. 
- PREFIX_STRING : prefix you want to receive autocomplete suggestions for. If you want to receive completions for "YE" in a trie containing "YES" and "YEW", put PREFIX_STRING = "YE". 
- SEARCH_STRING : string you want to see if is in the trie 



A few examples. 

First you may want to clear the trie's words completely. 

```curl
curl "https://a677fgt74e.execute-api.us-east-2.amazonaws.com/first/operations?action=CLEAR&add_string=nonsense&delete_string=nonsense&prefix_string=nonsense&search_string=nonsense"
```

If you want to add the string "string" you can do : 

```curl
curl "https://a677fgt74e.execute-api.us-east-2.amazonaws.com/first/operations?action=ADD&add_string=string&delete_string=nonsense&prefix_string=nonsense&search_string=nonsense"
```

Then you may want to search whether the string "string" exists : 

```curl
curl "https://a677fgt74e.execute-api.us-east-2.amazonaws.com/first/operations?action=SEARCH&add_string=nonsense&delete_string=nonsense&&prefix_string=nonsense&search_string=string"
```

## Each operation, in more detail 

# Add

The ADD operation is used for adding a string to the trie. Here in the client URL action=ADD and add_string is the string you want to add to the trie. This data is sent to the lambda function, and returns back just {} (really nothing). 

# Clear

The CLEAR operation deletes all words from the trie. Here you just set action=CLEAR and all else can be meaningless. It returns back {} (nothing). 

# Delete

The DELETE operation deletes a word from the trie. Here you set action=DELETE and delete_string is the string you want to delete. This returns back {"works" : true} if it worked or null if it didn't. This information is needed because the CLI will take this information passed back to the client and alert the 
user that there DELETE operation didn't work if needed. The DELETE operation wouldn't work if the user
is trying to delete a string that isn't in the trie. 

# Display

The DISPLAY operation returns the list of words (in a recursive ordering) inside the trie to the client, and then the CLI processes this information and prints it out. Here set action=DISPLAY.

# Autocomplete

The AUTOCOMPLETE operation takes in a given prefix and returns what other words have that prefix and are in the trie. Make sure to set action=AUTOCOMPLETE and prefix_string = to whatever prefix you want suggestions for. 

# Search
 
The SEARCH operation takes in a given word and tells you (True/False) whether that word is in the trie. Set
action=SEARCH and search_string = to the string you want to search for. 

It is worth noting that none of these action=ACTION or the add_string, delete_string, prefix_string, and search_string ever will be touched by the user. They are described here to make it easier for you test this REST API.