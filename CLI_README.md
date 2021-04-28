# tricli

tricli is a python library that allows everybody to perform operations on my trie data structure. Note that the trie data structure is global and the same at any given moment for everyone. 

tricli (given by the last three letters of its name) is meant to be used inside of the
terminal as a command-line interface (CLI) and NOT inside of your code files. 

Also note that the trie in tricli is case-sensitive, meaning that "Hello" and "hello" are considered
to be two different words!

## How to install

To install, go into your terminal and do : 

```shell 
pip install tricli
```

Make sure you are using Python 3 and pip3 if needed.  

## tricli operations

With tricli, you can add a word to trie, delete a word from the trie, clear the trie by removing all of its words, have the trie displayed to you, and get autocomplete suggestions for a given prefix string. 

Avoid stopping a command while it is running (should only take a few seconds), because that may lead to your requested operation not being processed by the server. 

With that in mind, let's take a closer look at each of these operations. 

## Add

Self-explanatory -  the add operation adds a word to the trie. 

Here's how you do that from your terminal : 

```shell 
tricli add WORD
```

where WORD is the word you want to add. If WORD is already inside the trie, nothing will happen. 

## Delete

The delete operation removes a word from the trie. 

From terminal :

```shell 
tricli delete WORD
```

where WORD is the word you want to delete. If WORD is not in the trie, then you will get a message saying that the operation failed. Note that if WORD is a prefix of other words in the trie, those other words will NOT get deleted.

## Search 

The search operation lets you know whether a word is inside of the trie or not. 

Like such : 

```shell 
tricli search WORD
```

where WORD is the string you want to search for. If WORD is in the trie, you will get back True otherwise you will get False. 

## Clear

The clear operation removes all words inside of the trie. Just do (no parameters) : 

```shell 
tricli clear
```

## Display 

The display operation shows you the trie (more specifically, the words in a trie) in an indentational format to make it easy for you to understand. 

As an example, say you have added the words "she", "sheet", "sheets", and "shot" (in that order) inside of your trie. Perform display by : 

```shell 
tricli display 
```

and you can expect to see back : 

```shell 
she
  sheet
   sheets
shot
```

This indentation style becomes clear and intuitive with this example. Essentially the display method prints out the words in the trie based on their prefix, and indents on a word to show that this word can be made by adding characters at the end of above words.

## Autocomplete

Lastly, the autocomplete function gives you the ability to type in a prefix string (regardless of whether its an actual word), and see if any words in the trie have that prefix. 

Let's see this with the same example we used in display. First run : 

```shell 
tricli autocomplete sh 
```

where "sh" can be replaced with any prefix string. Here we are looking for all of the words in the trie with the prefix "sh". You can then expect to get back : 

```shell 
['shot', 'she', 'sheet', 'sheets']
```

## Final Remarks

That's it for the CLI. Hope you enjoy it. Feel free to email questions to anish.lakkapragada@gmail.com!