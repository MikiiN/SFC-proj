# Fuzzy shower
This project was created for Soft computing course at FIT VUT.

Given theme was *Hybrid Genetic algoritm and fuzzy system* application. So I made fuzzy system for controlling shower valves to reach temperature and flow requested by user with fuzzy rules optimization using Genetic algorithm. For easier testing was implemented shower simulator with GUI.

## Instalation
For running this application you need to have python 3.12 (tested on) and venv installed. Following commands (in other sections too) are for linux. 

Then just run this command:
```
bash setup.sh
```
Script will create new virtual enviroment and install all dependecies to created enviroment.

## Execution
First you need to activate enviroment:
```
source venv/bin/activate
```
Then you can run application in any of these modes.

### Execution with reference rules
```
python main.py
```
### Optimization execution
```
python main.py -o
python main.py --optimize
```
### Execution with rules configuration from file
```
python main.py -l cfg.txt
python main.py --load cfg.txt
```
### Execution with random rules configuration
```
python main.py -r
python main.py --random
```
