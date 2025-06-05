# Extractor Module Usage

This document describes how to use the `extractor.py` module to extract the contents of a Power BI PBIX file.

## Overview

PBIX files are essentially zip archives containing various components that make up a Power BI report, such as the data model, report layout, and connection settings. The `extractor.py` script uses Python\\'s built-in `zipfile` library to unpack these components into a specified directory, allowing for inspection and programmatic modification.

## Prerequisites

*   Python 3.6 or higher

## How it Works

The script defines a function `extract_pbix(pbix_file_path, output_dir)`:

1.  It checks if the input PBIX file exists.
2.  It creates the output directory if it doesn\\'t exist.
3.  It opens the PBIX file as a zip archive.
4.  It extracts all contents of the archive into the specified output directory.
5.  It logs the process, including success messages or errors.

## Usage (Command Line)

The script can be run directly from the command line.

```bash
python src/extractor.py --input /path/to/your/report.pbix --output /path/to/extracted_files_directory
```

**Arguments:**

*   `--input` (Required): The full path to the input `.pbix` file.
*   `--output` (Required): The full path to the directory where the extracted files should be saved. The directory will be created if it does not exist.

**Example:**

```bash
python src/extractor.py --input "C:\\Reports\\Sales_Report.pbix" --output "C:\\Extracted\\Sales_Report_Contents"
```

Upon successful execution, the contents of `Sales_Report.pbix` will be placed inside the `C:\\Extracted\\Sales_Report_Contents` directory.

## Usage (Python Module)

You can also import and use the `extract_pbix` function within other Python scripts:

```python
from src.extractor import extract_pbix
import logging

pbix_path = \"/path/to/your/report.pbix\"
extract_to_dir = \"/path/to/extracted_files\"

try:
    extracted_file_list = extract_pbix(pbix_path, extract_to_dir)
    logging.info(f\"Extraction complete. Files: {extracted_file_list}\")
except FileNotFoundError as e:
    logging.error(e)
except Exception as e:
    logging.error(f\"An error occurred: {e}\")
```

## Extracted Components

After extraction, you will typically find files and folders such as:

*   `DataModel`: Contains the data model schema (often in TMDL format if saved with enhanced metadata).
*   `Report/Layout`: JSON file describing the report\\'s visual layout.
*   `Connections`: Information about data source connections.
*   `StaticResources`: Images and themes used in the report.
*   `Metadata`: Various metadata files.
*   `[Content_Types].xml`, `SecurityBindings`, etc.

Understanding these components is crucial for the next steps involving parsing and modification.

