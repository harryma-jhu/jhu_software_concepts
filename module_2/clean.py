from llm_hosting.app import standardize 
import json
# Constants for input and output file names
INPUT_FILE = ".applicant_data.json"
OUTPUT_FILE = "out.json"
# Function to load data from a JSON file
def load_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
# Main function to process and write standardized data
def main(data):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
        for row in data:
            cleaned = standardize()
            row.update(cleaned)
            output_file.write(json.dumps(row, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    data = load_data()
    main(data)