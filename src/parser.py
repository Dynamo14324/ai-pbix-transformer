
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format=\"%(asctime)s - %(levelname)s - %(message)s\")

LAYOUT_FILE_PATH = \"Report/Layout\"

def find_layout_file(extracted_dir: str) -> str | None:
    \"\"\"Finds the report layout file within the extracted PBIX directory.\"\"\"
    # Check common variations of the layout file name/path
    possible_paths = [
        os.path.join(extracted_dir, LAYOUT_FILE_PATH),
        os.path.join(extracted_dir, \"Report\", \"layout.json\") # Older PBIX versions might use this
    ]
    for path in possible_paths:
        if os.path.isfile(path):
            logging.info(f\"Found layout file at: {path}\")
            return path

    # Fallback: Search recursively for a file named \"Layout\" or \"layout.json\" within \"Report\"
    report_dir = os.path.join(extracted_dir, \"Report\")
    if os.path.isdir(report_dir):
        for root, _, files in os.walk(report_dir):
            for file in files:
                if file.lower() == \"layout\" or file.lower() == \"layout.json\":
                    found_path = os.path.join(root, file)
                    logging.info(f\"Found layout file via search: {found_path}\")
                    return found_path

    logging.warning(f\"Layout file not found in expected locations within {extracted_dir}\")
    return None

def parse_report_layout(extracted_dir: str) -> dict | None:
    \"\"\"Parses the Report/Layout JSON file from an extracted PBIX directory.

    Args:
        extracted_dir: The directory containing the extracted PBIX contents.

    Returns:
        A dictionary representing the parsed JSON layout, or None if the file
        cannot be found or parsed.
    \"\"\"
    layout_file = find_layout_file(extracted_dir)

    if not layout_file:
        return None

    try:
        # PBIX layout often uses UTF-16 LE encoding
        with open(layout_file, \"r\", encoding=\"utf-16-le\") as f:
            layout_data = json.load(f)
            logging.info(f\"Successfully parsed layout file: {layout_file}\")
            return layout_data
    except FileNotFoundError:
        logging.error(f\"Layout file path found but file not accessible: {layout_file}\")
        return None
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logging.warning(f\"Failed to parse {layout_file} with utf-16-le ({e}), trying utf-8...\")
        # Try reading with different encoding as fallback
        try:
            with open(layout_file, \"r\", encoding=\"utf-8\") as f_utf8:
                layout_data = json.load(f_utf8)
                logging.info(f\"Successfully parsed layout file with UTF-8 fallback: {layout_file}\")
                return layout_data
        except Exception as fallback_e:
            logging.error(f\"Fallback UTF-8 parsing also failed for {layout_file}: {fallback_e}\")
            return None
    except Exception as e:
        logging.error(f\"An unexpected error occurred while parsing {layout_file}: {e}\")
        return None

def save_report_layout(extracted_dir: str, layout_data: dict):
    \"\"\"Saves the modified layout data back to the Report/Layout file.

    Args:
        extracted_dir: The directory containing the extracted PBIX contents.
        layout_data: The dictionary representing the layout to be saved.

    Raises:
        FileNotFoundError: If the original layout file cannot be found.
        IOError: If there is an error writing the file.
    \"\"\"
    layout_file = find_layout_file(extracted_dir)

    if not layout_file:
        logging.error(f\"Cannot save layout: Original layout file not found in {extracted_dir}\")
        raise FileNotFoundError(f\"Original layout file not found in {extracted_dir}\")

    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(layout_file), exist_ok=True)

        # Write the file using UTF-16 LE encoding, which is common for PBIX layouts
        with open(layout_file, \"w\", encoding=\"utf-16-le\") as f:
            json.dump(layout_data, f, ensure_ascii=False, indent=2) # Use indent for readability
            logging.info(f\"Successfully saved modified layout to: {layout_file}\")
    except IOError as e:
        logging.error(f\"Failed to write layout file {layout_file}: {e}\")
        raise
    except Exception as e:
        logging.error(f\"An unexpected error occurred while saving {layout_file}: {e}\")
        raise

# --- Example Modification Function (Conceptual) ---
# This is where specific editing logic would go.
# For now, it just demonstrates reading, making a trivial change, and saving.

def modify_and_save_layout(extracted_dir: str):
    \"\"\"Example function to parse, modify, and save the layout.\"\"\"
    logging.info(\"Attempting to modify layout...\")
    layout = parse_report_layout(extracted_dir)
    if not layout:
        logging.error(\"Cannot modify layout, parsing failed.\")
        return

    # --- Placeholder Modification --- 
    # Example: Add a comment or metadata to the layout root
    layout[\"_modification_comment\"] = \"Layout modified by AI PBIX Transformer\"
    logging.info(\"Applied placeholder modification to layout data.\")
    # --- End Placeholder Modification ---

    try:
        save_report_layout(extracted_dir, layout)
        logging.info(\"Layout modification saved successfully.\")
    except Exception as e:
        logging.error(f\"Failed to save layout modification: {e}\")

# --- Main execution block for testing --- 
if __name__ == \"__main__\":
    import argparse
    from extractor import extract_pbix
    import shutil

    parser = argparse.ArgumentParser(description=\"Parse, optionally modify, and save the Report/Layout file from a PBIX.\")
    parser.add_argument(\"--input\", required=True, help=\"Path to the input PBIX file.\")
    parser.add_argument(\"--temp_dir\", default=\"./temp_extracted\", help=\"Temporary directory to extract PBIX contents.\")
    parser.add_argument(\"--modify\", action=\"store_true\", help=\"Apply a placeholder modification before saving.\")

    args = parser.parse_args()
    cleanup_temp = True

    try:
        # Clean up previous temp dir if it exists
        if os.path.exists(args.temp_dir):
            logging.warning(f\"Removing existing temporary directory: {args.temp_dir}\")
            shutil.rmtree(args.temp_dir)

        logging.info(f\"Extracting {args.input} to {args.temp_dir}...\")
        extract_pbix(args.input, args.temp_dir)

        if args.modify:
            modify_and_save_layout(args.temp_dir)
        else:
            logging.info(f\"Parsing layout from {args.temp_dir}...\")
            layout = parse_report_layout(args.temp_dir)
            if layout:
                print(\"Layout parsed successfully.\")
                if \"sections\" in layout:
                    print(f\"Number of report sections: {len(layout[\"sections\"])}\")
            else:
                print(\"Failed to parse report layout.\")

    except Exception as e:
        logging.error(f\"An error occurred in the main execution: {e}\")
        cleanup_temp = False # Keep temp dir for debugging if error occurs
        exit(1)
    finally:
        # Clean up the temporary directory if successful and cleanup is enabled
        if cleanup_temp and os.path.exists(args.temp_dir):
            logging.info(f\"Cleaning up temporary directory: {args.temp_dir}\")
            # shutil.rmtree(args.temp_dir) # Uncomment to enable cleanup
            pass

