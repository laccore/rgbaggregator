# rgbaggregator
Gather data from individual core sections' RGB data files in CSV format and combine
them into a single CSV file with an additional column indicating the source
section for each row of data.

Can be run as a command-line utility (main.py) or Qt-based GUI application (qtmain.py).


### RGB Formats
Two RGB formats are supported. For each aggregation process, all input files must use the same format.

#### Raw CIS/Geotek Format
Depth, R, G, and B values are in a single column, separated by tabs.
After seven metadata rows (ignored), data starts at row 9.

|Column 1|
|--------|
|Image Aperture: 5.6|
|Calibration Aperture: 5.6|
|Left Position: 3.700|
|Width: 3.100|
|Top: 0.0000|
|Height: 110.000|
|Interval: 0.010|
|Data:|
|0.000	36.497	35.519	33.224|
|0.010	37.082	36.007	33.630...etc|

#### ImageJ Format
Depth, R, G, and B values are in separate columns. They may be preceded
by a measurement sequence value in its own column. This is ignored if present.
Row 1 is a header row. Data starts at row 2.

| sequence (ignored if present)  | depth | r         | g         | b         |
| - | ----- | --------- | --------- | --------- |
| 1 | 0     | 27487.316 | 24817.115 | 19938.307 |
| 2 | 0.005 | 27339.631 | 24842.467 | 20003.578 |
| 3 | 0.01  | 27444.188 | 24829.719 | 19999.551..etc |



### Developer Notes
rgbaggregator expects Python 3.

Clone repo and install dependencies: `pip install -r requirements.txt`

Launch with `python qtmain.py` for GUI, `python main.py` for command-line.