# Angle Calculation from XML Data
This Python script calculates angles and lengths from XML data and updates an Excel file with the results. The script utilizes libraries such as BeautifulSoup for XML parsing, NumPy for numerical operations, and Pandas for handling Excel data.

# Requirements
Make sure you have the following Python libraries installed. You can install them using pip install -r requirements.txt.

# Usage
1) Install the required libraries using the provided requirements.txt.

2) Adjust the input paths in the script according to your file locations:

```python
excelData = pd.read_excel('/path/to/your/Project1/PB_Angle.xlsx')
path = r"/path/to/your/Project1/*.xml"
```

3) Run the script to process XML files, calculate angles, and update the Excel file.

# Description
The script reads angle data from XML files, processes it using a custom function (stringConvert), and updates the specified Excel file with calculated angles, lengths, and relevant information.

# Note
Ensure that your Excel file (PB_Angle.xlsx) is structured correctly with the necessary columns (pixelSpacing, etc.).
Make sure that the XML files contain the required data structure for successful parsing.
