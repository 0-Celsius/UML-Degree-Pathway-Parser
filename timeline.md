# timeline.md 
my personal file to remember what i need to fix and add etc, feel free to look through my thoughts

# 08/19/2024 
## main 
    - added in a obsidian formatted file, allows for me to grab the data.
    

# 07/25/2024
## main 
    - started making a pre req checker
    - kinda weird that in find_all_major, we do a save into undergrad_major class?
        - should make a new class but idrc

## additions 
    - added a pre-req finder
    - added a total time function

## problems
    - add timers, which arent need
        - defineitly slows the program down
        - program is rpetty slow itself
        - takes around what 6 >> 30 for big majors
        - probably would be a great idea to asynchronous request for half of the urls when looking for pre reqs 
        - 30 fucking seconds for a big major like EECS 
            - do I care enough to reduce this time to probably like 1 to 5 seconds? 
                - no :/
            - it takes the old version 40 seconds
                - it was also opening tabs...
                - 38 seconds for no open tabs...


# 07/24/2024 
## main
    - finished alot of things 
    - now I need to make a pre req checker under about


    - final finished the project
    - did not check for errors 
    - currently everything seems fine? 

# notable things
    - credits parsing:
        - when encounter N-N (i.e: 0-1)
            - it will take the right hand value
        - if it encounters a N/N (should never happen.)
            - will take the right hand value
        
        - this allows me to keep a integer value 

# 07/23/2024
## main
    - !!! [implement]
    - need to create this


# 07/22/2024
## main
    - Started to actually think about what to do for this
    - I want to do an auto search for all the classes
    
## search_api.py
    - created the search file "search_api.py" 
    - allows for me to search for all the current uml degrees offer


# 07/04/2024
## main
    - Started today to remake this program
    - looked at UML discord bot and got inspired to not use selenium
    - ive always wanted to use a browserless page viewer to scrap data
    - so it should be about the same