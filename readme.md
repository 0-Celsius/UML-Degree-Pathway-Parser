# UML Degree Parser

## Description
A small project for me to look my university([Umass Lowell](https://www.uml.edu/))'s pathways & check their pre-reqs for when I need to help friends plan out their lives. 
\* (please check if an course might need a pre-req, I cannot guaranteed I didn't miss a parse)
\* (if there is an error, good luck.)
## how to use
1. Follow Installation guide
2. go to file: `search_api.py` 
3. run `search_api.py` 
4. Click on `pathway.txt` or `obs_pathway.md`

#### This program does have options
> under `if __name__ == '__main__':`: change things under the options comments
> \* <ctrl + f> paste: ` #Tag: Options `

--- 
## Options:

### Program
`program = True`
> walks you throughout everything:
> 1. choose a major
> 2. a concentration

`program = False`
> drop a url like: `https://www.uml.edu/catalog/undergraduate/engineering/departments/electrical-computer-engineering/degree-pathways/dp-ece-eecs-2023.aspx` 
> then it will grab your class requirements and spit it back out 

### return_txt_file
`return_txt_file = True`
> spits out a text file called `pathway.txt` 

`return_txt_file = False`
> doesnt create a text file 


### return_md_file
`return_md_file = True`
> spits out a text filed called `obs_pathway.md`
> `ctrl + c` + `ctrl + shift + v` into Obsidian to view a cleaner version of the pathway
> you could view the `obs_pathway.md` as well, it just not as clean

`return_md_file = True`
> doesnt create a md file
---
## Installation 
1. Clone Repo: `git clone https://github.com/0-Celsius/UML-Degree-Pathway-Parser.git`
* make sure you have pip and python 3+ installed 
2. Navigate to the project directory 
3. install depencencies by opening terminal in folder `pip install -r requirement.txt`

---
## Licenses 
This project is licensed under the MIT License - see the LICENSE.md file for details.

Thanks for reading this and good luck! :D