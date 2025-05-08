# onr

## Overview
The onr project is a Python application designed to determine the best actions to take to maintain an oil pipeline network. This project was developed as part of a funded Office of Naval Research research initiative led by Dr. Thomas Seager.

## Result
![Tab Save Our System](report/images/tabsaveoursystem.png)


## Usage
To run the project, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Download `chromedriver` and place it in the project directory. Update the `config/breakitbad.py` and `config/saveoursystem1.py` files with the path to the `chromedriver`.
4. Install the required dependencies using:
    ```bash
    pip install -r requirements.txt
    ```
5. Modify the configuration files in the `config` folder as needed. The configuration files are:
    - `break_it_bad.py`: Configuration file for the `BreakItBad` game.
    - `save_our_system.py`: Configuration file for the `SaveOurSystem` game.
6. Run the bot for the desired game:
    ```bash
    python3 bot.py
    ```
    or
    ```bash
    python3 bot-saveoursystem.py
    ```

## Directory Structure
```
onr/
├── config/
│   ├── breakitbad.py       # Configuration file for the BreakItBad game
│   ├── saveoursystem1.py   # Configuration file for the SaveOurSystem game
├── src/
│   ├── game.py             # Main game logic
│   ├── utils/
│   │   ├── const.py        # Constants used across the project
│   │   ├── Edge.py         # Edge-related utilities
│   │   ├── metrics.py      # Metrics calculation utilities
│   │   └── Node.py         # Node-related utilities
├── bot.py                  # Bot script for BreakItBad
├── bot-saveoursystem.py    # Bot script for SaveOurSystem
├── requirements.txt        # List of dependencies
```