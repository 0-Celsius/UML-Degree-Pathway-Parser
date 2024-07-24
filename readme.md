# UML Degree Parser

## Description
A small project for me to look my university([Umass Lowell](https://www.uml.edu/))'s pathways when I need to help friends plan out their lives. 


## how to use
1. Follow Installation guide
2. go to file: `search_api.py` 
3. under `if __name__ == '__main__':`: change things under the options comments
* <ctrl + f> paste: ` #Tag: Options `

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


## Installation 
1. Clone Repo: `git clone https://github.com/0-Celsius/UML-Degree-Pathway-Parser.git`
2. Navigate to the project directory 
3. install depencencies `pip install -r requirement.txt`
* make sure you have pip and python 3+ installed 

## Licenses 
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Contact me 
Kelvin - [kelvinlee227greenwood@gmail.com](mailto:kelvinlee227greenwood@gmail.com)

