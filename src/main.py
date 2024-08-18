from parser import FixedWidthFileParser

def exec():
    """
    Main function to execute the FixedWidthFileParser workflow.

    This function creates an instance of FixedWidthFileParser and processes the
    fixed-width file to generate a CSV file.
    """
    spec_file = '/app/data/spec.json'
    fixed_width_file = '/app/data/fixed_width.txt'
    csv_file = '/app/data/output.csv'

    processor = FixedWidthFileParser(spec_file)
    processor.process_files(fixed_width_file, csv_file)

if __name__ == "__main__":
    exec()