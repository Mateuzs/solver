# solver

problem solver - STRIPS language.

Works in two modes:

- **normal** - solves problem instantly and gives prepared plan
- **analysis** - debug mode, allows to monitor sequences of agent solving problem. It is a step-by-step mode, every step of agent must be triggered by using **Enter** key.

It takes three arguments at the beginning from the command line:

- **filePath** - path to file with problem defined in STRIPS language
- **analysis** - flag _true_|_false_ saying if we want to solve problem in debug mode or not
- **depth** - depth of the searching tree

Examples of usage:

1. Version - normal:

```
    python main.py shopping1.txt false 10
```

2. Version - analysis:

```
    python main.py shopping1.txt true 10
```

Example of response from the agent:

```
> python main.py shopping1.txt false 10

Parsing problem...

State:
{'Byc': set([('Dom',)]), 'Sprzedaje': set([('Sklep', 'Ser'), ('Targ', 'Banany'), ('Sklep', 'Szynka')])}

Actions:
Kupic
Przejsc

Literals:
set(['Banany', 'Dom', 'Targ', 'Szynka', 'Sklep', 'Ser'])

Goal:
Miec(Szynka)
Miec(Banany)
Miec(Ser)
Byc(Dom)


Solving......

Problem solved!

Plan: Przejsc(Dom, Sklep) -> Kupic(Sklep, Szynka) -> Przejsc(Sklep, Targ) -> Kupic(Targ, Banany) -> Przejsc(Targ, Sklep) -> Kupic(Sklep, Ser) -> Przejsc(Sklep, Dom)
```
