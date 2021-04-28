# this is the file that is put on the server side (AWS Lambda)
import json
import pickle
import os
import boto3

class Node() : 
        def __init__(self, character, end) : 
            self.children_nodes = [] # contains children nodes
            self.character = character
            self.end = end
            

def lambda_handler(event, context):
        
        
    action = event['queryStringParameters']['action']  # what action do they want to perform

    # read trie.pickle, used this article : https://medium.com/@nrk25693/how-to-use-boto3-to-load-your-pickle-files-dcdf59cc0016
    session = boto3.session.Session(region_name = "us-west-1")
    s3client = session.client("s3")
    response = s3client.get_object(Bucket = "triebucket", Key= "trie.pickle")
    body_string = response["Body"].read()
    root = pickle.loads(body_string)
    
        
    def add(add_string) : 
        current_node = root
        for i, character in enumerate(add_string) : 
            characters = [child_node.character for child_node in current_node.children_nodes]

            if character not in characters : 
                current_node.children_nodes.append(Node(character, (i == len(add_string) - 1)))
                current_node = current_node.children_nodes[-1] # use the one just created as the child 
            
            if character in characters : 
                
                character_node, character_node_index = [(node, i) for i, node in enumerate(current_node.children_nodes) 
                            if node.character == character][0]

                if i == len(add_string) - 1 and character_node.end == False : 
                    # set end = True now
                    character_node.end = True
                    current_node.children_nodes[character_node_index] = character_node

                current_node = character_node 

    def display() :
        statements = []
        def traverse(prior_indents, prefix, node) : 
            for child_node in node.children_nodes : 
                if child_node.end : 
                    statements.append((" " * (prior_indents + 1) + prefix + child_node.character))
                    traverse(prior_indents + 1, prefix + child_node.character, child_node)
                else : 
                    traverse(prior_indents, prefix + child_node.character, child_node)
        traverse(0, "", root)
        return statements

    def delete(delete_string) : 
        
        """
        delete() method will return None if the operation has failed, and True if it has worked. 
        """

        current_node = root

        for i, character in enumerate(delete_string) : 
            character_children = [child_node.character for child_node in current_node.children_nodes]

            if character not in character_children : 
                # doesn't even exist 
                return None

            end = (i == len(delete_string) - 1) 

            character_node, character_node_index = [(node, i) for i, node in enumerate(current_node.children_nodes) 
                                if node.character == character][0]

            if end : 
                if character_node.end == True : 
                    del current_node.children_nodes [character_node_index]
                else : 
                    # this is an incomplete prefix
                    return None

            current_node = character_node # set to the character node 

        return True # completely works here


    def search(search_string) : 

        # see whether or not a string exists in the trie 

        current_node = root

        for i, character in enumerate(search_string) : 
            end = i == (len(search_string) - 1) 
            character_node = [node for node in current_node.children_nodes if node.character == character ]
            
            if not len(character_node) : return False
            
            character_node = character_node[0]
            
            # character_node is the node in the children nodes with the given character 
            if character not in [child_node.character for child_node in current_node.children_nodes] : 
                return False 
            if end :
                if character_node.end == False : 
                    return False
                else : 
                    return True
            current_node = character_node # continue with this character nod
        return True


    def autocomplete(prefix) : 
        """

        Returns None if the prefix doesn't even exist. 

        """ 

        suggestions = []

        def suggest(current_prefix, node) : 
            for child_node in node.children_nodes : 
                if child_node.end : 
                    suggestions.append(current_prefix + child_node.character)
                suggest(current_prefix + child_node.character, child_node)
        
        # find the node to start the suggest loop 
        current_node = root
        for i, character in enumerate(prefix) : 
            characters = [child_node.character for child_node in current_node.children_nodes] 
            if character not in characters : 
                return None 
        
            current_node = [node for node in current_node.children_nodes if node.character == character][0]

        suggest(prefix, current_node) 
        return suggestions

    if action == "CLEAR" : 
        # if action is clear, just create a new root node and rewrite trie.pickle
        pickle_byte_obj = pickle.dumps(Node("", False))
        s3_resource = boto3.resource("s3")
        s3_resource.Object("triebucket", 'trie.pickle').put(Body=pickle_byte_obj)
        
        http_response = {"statusCode" : 200, "headers" : {}}
        http_response["headers"]["Content-Type"] = "application/json"
        http_response['body'] = json.dumps({}) # return nothing here 

        return http_response
        
    elif action == "ADD" :
        add_string = event['queryStringParameters']['add_string'] # what string do they want to add 
        add(add_string=add_string) # add this string 
        
        # now save this to the trie.pickle file
        # used this stack post : https://stackoverflow.com/questions/49120069/writing-a-pickle-file-to-an-s3-bucket-in-aws
        pickle_byte_obj = pickle.dumps(root)
        s3_resource = boto3.resource("s3")
        s3_resource.Object("triebucket", 'trie.pickle').put(Body=pickle_byte_obj)
        
        
        # return response 
        http_response = {"statusCode" : 200, "headers" : {}}
        http_response["headers"]["Content-Type"] = "application/json"
        http_response['body'] = json.dumps({}) # return nothing here 

        return http_response
    
    elif action == "SEARCH" : 
        search_string = event['queryStringParameters']['search_string']
        result = search(search_string)

        http_response = {"statusCode" : 200, "headers" : {}}
        http_response["headers"]["Content-Type"] = "application/json"
        http_response['body'] = json.dumps({"in" : result}) # return nothing here 

        return http_response
    
    elif action == "DISPLAY" :
        # get the words in an array, send that via json, manually handle in CLI
        words = display()

        http_response = {"statusCode" : 200, "headers" : {}}
        http_response["headers"]["Content-Type"] = "application/json"
        http_response['body'] = json.dumps({"words" : words}) # return the words, that are to be printed 

        return http_response
    
    elif action == "DELETE" : 
        delete_string = event['queryStringParameters']['delete_string']     
        works = delete(delete_string) 

        # save this to the file
        pickle_byte_obj = pickle.dumps(root)
        s3_resource = boto3.resource("s3")
        s3_resource.Object("triebucket", 'trie.pickle').put(Body=pickle_byte_obj)

        # return the reposnse
        body_response = {"works" : works}
        http_response = {"statusCode" : 200, "headers" : {}}
        http_response["headers"]["Content-Type"] = "application/json"
        http_response['body'] = json.dumps(body_response) 

        return http_response

    elif action == "AUTOCOMPLETE" : 
        prefix = event['queryStringParameters']['prefix_string']
        suggestions = autocomplete(prefix) # suggestions could be None if the prefix doesn't exist. 

        http_response = {"statusCode" : 200, "headers" : {}}
        http_response["headers"]["Content-Type"] = "application/json"
        http_response['body'] = json.dumps({"suggestions" : suggestions})
        return http_response

    else : 
        http_response = {"statusCode" : 200, "headers" : {}}
        http_response["headers"]["Content-Type"] = "application/json"
        http_response["body"] = json.dumps(f"No known action : {action}") # nothing
        
        return http_response