# Mean-Meadian-Mode-And-Range-Calculator

A Python-based statistical analysis application with a graphical user interface built using Tkinter.  
This program allows users to enter numerical datasets, calculate key statistical values, visualise the data using graphs, and export a professional PDF report.

## Features

- Flexible data input
  - Single values
  - Comma-separated lists (e.g. 1,2,3,4)
  - Repeated values using multiplication syntax (e.g. 5x3)

- Statistical calculations
  - Mean
  - Median
  - Mode
  - Range
  - Quartiles (Q1, Q2, Q3)
  - Interquartile Range (IQR)
  - Outlier detection
  - Standard deviation
  - Sorted dataset

- Graph generation
  - Boxplot
  - Histogram
  - Graphs created using Matplotlib

- Graph display
  - Graphs are saved as images and displayed inside the GUI using Pillow (PIL)

- PDF report export
  - Automatically generates a PDF report
  - Includes the graph image and full statistical summary
  - Created using ReportLab

## Technologies Used

- Python 3.12
- Tkinter
- Matplotlib
- NumPy
- Statistics (Python standard library)
- Pillow (PIL)
- ReportLab

## Project Structure

MMM_R_calculator.py    Main application file  
number.txt             Stores graph numbering  
Graph_*.png            Temporary graph images  
*_report.pdf           Generated PDF reports  

## How to Run

1. Clone the repository:
   git clone https://github.com/your-username/your-repo-name.git

2. Navigate to the project directory:
   cd your-repo-name

3. Run the application:
   python MMM_R_calculator.py

Required libraries will be installed automatically if missing.

## Purpose

This project was developed to improve understanding of statistics, GUI development with Tkinter, data visualisation, and automated report generation in Python.

It is suitable for educational use and portfolio demonstration.

## Future Improvements

- CSV file import and export
- Support for multiple datasets
- Improved user interface layout
- Custom graph styling
- Data persistence between sessions

## Author

Luke Reilly (Year 9 Student Developer)
