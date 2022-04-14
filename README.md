# rgbaggregator
Gather data from individual core sections' RGB data files and combine
them into a single CSV file with an additional column indicating the source
section for each row of data.

Can be run as a command-line utility (main.py) or Qt-based GUI application (qtmain.py).

### Developer Notes
rgbaggregator expects Python 3.

Clone repo and install dependencies: `pip install -r requirements.txt`

Launch with `python qtmain.py` for GUI, `python main.py` for command-line.