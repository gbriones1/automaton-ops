# automaton-ops

Generate an automaton based on automaton operations: union, intersection, concatenation and kleene star.

**Note: to se this documentation in spanish, go the [Spanish version](README_spa.md)**

## Installation

This project runs on Python3, and was developed using version 3.8.5, in case you don't have Python3 installed you can follow the python's installation instructions from the official python page: https://www.python.org/downloads/.

### Download source code

Download the source code at: https://github.com/gbriones1/automaton-ops/archive/main.zip

This file as a compressed `.zip` archive, this means you will need to uncompress the contents of this archive by right-clicking the file to open the menu, then selection the correct option to extract the file contents.

Or you can clone this repository by executing in a terminal:

```bash
git clone https://github.com/gbriones1/automaton-ops.git
```

If you already have the source code, then continue to the next step.

### Open a terminal

To verify you have Python3 installed, you need to open a terminal and execute the following command:

```bash
python3 --version
```

A terminal can be opened in different ways depending on your Operating System:

#### MacOS

On your Mac, do one of the following:

 * Click the Launchpad icon in the Dock, type Terminal in the search field, then click Terminal.
 * In the Finder, open the /Applications/Utilities folder, then double-click Terminal.

#### Windows

 1. Click the Windows icon on the bottom-left corner of your desktop or press the Win key on your keyboard
 2. Type cmd or Command Prompt. After opening the Start menu, type this on your keyboard to search the menu items. Command Prompt will show up as the top result.
 3. Click the Command Prompt app on the menu. This will open the Command Prompt terminal in a new window.

#### Linux

 * Press Ctrl+Alt+T in Ubuntu, or press Alt+F2, type in gnome-terminal, and press enter.

### Navigate to source code location

With the terminal open use the command `cd` followed by a directory structure separated by slashes (`/`) to navigate into the source code location.

```bash
cd <path>/<to>/<source>/<code>
```

**Note: If you are using windows, separate directories using backslashes: `\`**

## Usage

The automatons we use are compatible with the online tool: http://ivanzuzak.info/noam/webapps/fsm_simulator/. This is a tool used to draw and simulate finite automatons using regular expresions and automaton definitions.

### Define automatons

A valid FSM definition contains a list of states, symbols and transitions, the initial state and the accepting states. States and symbols are alphanumeric character strings and can not overlap. Transitions have the format: `stateA:symbol>stateB,stateC`. The `$` character is used to represent the empty string symbol (epsilon) but should not be listed in the alphabet.

We have provided a list of automaton definitions in the folder `samples` of this project. Otherwise you can go to http://ivanzuzak.info/noam/webapps/fsm_simulator/ then in the section `① Create automaton` navigate to `Input automaton` tab and then click on the `Generate random DFA`, `Generate random NFA`, or `Generate random eNFA` buttons to generate a random definition which will be displayed in the text box bellow.

The automatons should be text files in order to the program to be able to read them.

### Run the program

To execute the program on your terminal, type `./main.py` followed by the arguments `--automaton1 <path>/<to>/<automaton>/<definition>`, `--automaton2 <path>/<to>/<automaton>/<definition>` and `--operation <operation_name>`

The supported operation names are:

 * `union`
 * `intersect`
 * `concat`
 * `kleene_star`

**Note: `kleene_star` is a single automaton operation, for such case, the argument `--automaton2` is not required.**

You can also get the execution help by running:

```bash
./main.py --help
```

#### Examples

If you would like to execute a union between the automatons defined in files: `samples/DFA_1.txt` and `samples/DFA_2.txt`, execute the following command:

```bash
./main.py --automaton1 samples/DFA_1.txt --automaton2 samples/DFA_2.txt --operation union
```

This will generate the following output:

```
#states
AP
AR
BQ
CP
CQ
CR
#initial
AP
#accepting
AP
AR
BQ
CR
#alphabet
0
1
#transitions
AP:0>BQ
CP:0>CQ
CQ:1>CR
CR:0>CQ
CP:1>CP
CQ:0>CQ
AR:0>BQ
AR:1>AP
BQ:1>AR
AP:1>AP
CR:1>CP
BQ:0>CQ
```

### Draw automaton graph

The output of the execution will be the automaton definition resulting from the operation, this text can be copied and pasted into the text box in http://ivanzuzak.info/noam/webapps/fsm_simulator/ in the section `① Create automaton` under the tab `Input automaton`, then create the graph by clicking the `Create automaton` button.

The generated graph will appear in the section: `③ Transition graph` of the same page.
