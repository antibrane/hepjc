# hepjc
Updating tool for *High-Energy Physics Journal Club (HEP-JC)* website at the University of Arizona.

## Installation

* The script uses **python 3**, with no further dependencies (although web browser and internet connection necessary).
* Run the python script by entering `./hepjc.py` in the terminal.
* If running for the first time, you will be prompted to enter some information:
  * *full* web address of page
  * username and domain for server hosting **hepjc** webpage.
  
## Using the Script

The updating of the HEP-JC web page can be completely handled by using this script.  Run the script either with `./hepjc.py` and follow the prompts, or run with one of the following options:

* `-c` **checks** the structure of the website and ensures the color coding of the schedule is properly set based on the current date (this command should be run *at least once a week* to keep up-to-date).
* `-l` **lists** schedule showing all past and future slots.
* `-d` **delete** a slot from the schedule.
* `-n` add a **new** slot to the scheudle.
* `-DS` **delete semester** completely from the schedule.
* `-NS` add a **new semester** with one empty slot to the scheudle.
* `-dc` **delete changes** to the web page that have been locally stored.
* `-db` **delete backup** files for any changes that have been made that are locally stored.
* `-p` **preview** the current locally stored changes.
* `-u` **upload** any locally stored changes and rewrite the web page.
