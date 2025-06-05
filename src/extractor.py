
import zipfile
import os
import logging

logging.basicConfig(level=logging.INFO, format=\"%(asctime)s - %(levelname)s - %(message)s\")

def extract_pbix(pbix_file_path: str, output_dir: str):
    \"\"\"Extracts the contents of a PBIX file to a specified directory.

    Args:
        pbix_file_path: The path to the .pbix file.
        output_dir: The directory where the contents should be extracted.
    \"\"\"
    if not os.path.exists(pbix_file_path):
        logging.error(f\"PBIX file not found: {pbix_file_path}\")
        raise FileNotFoundError(f\"PBIX file not found: {pbix_file_path}\")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f\"Created output directory: {output_dir}\")

    try:
        with zipfile.ZipFile(pbix_file_path, \'r\') as zip_ref:
            zip_ref.extractall(output_dir)
            logging.info(f\"Successfully extracted \\\"{pbix_file_path}\\\" to \\\"{output_dir}\\\"\")
            # List extracted files for confirmation
            extracted_files = zip_ref.namelist()
            logging.info(f\"Extracted files: {extracted_files}\")
            return extracted_files
    except zipfile.BadZipFile:
        logging.error(f\"Error: The file \\\"{pbix_file_path}\\\" is not a valid zip file or is corrupted.\")
        raise
    except Exception as e:
        logging.error(f\"An unexpected error occurred during extraction: {e}\")
        raise

# Example usage (can be run as a script)
if __name__ == \"__main__\":
    import argparse

    parser = argparse.ArgumentParser(description=\"Extract a PBIX file.\")
    parser.add_argument(\"--input\", required=True, help=\"Path to the input PBIX file.\")
    parser.add_argument(\"--output\", required=True, help=\"Directory to extract the contents to.\")

    args = parser.parse_args()

    try:
        extract_pbix(args.input, args.output)
    except Exception as e:
        logging.error(f\"Extraction failed: {e}\")
        exit(1)

