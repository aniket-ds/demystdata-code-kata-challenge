import csv
import json
import os

class FixedWidthFileParser:

    def __init__(self, spec_file):
        """
        Initialize the FixedWidthFileParser with a specification file.

        :param spec_file: Path to the JSON specification file.
        """
        self.spec_file = spec_file
        self.load_spec()

    def load_spec(self):
        """
        Load the specification from the JSON file.
        """
        if not os.path.isfile(self.spec_file):
            raise FileNotFoundError(f"Specification file '{self.spec_file}' not found.")

        with open(self.spec_file, 'r') as file:
            try:
                spec = json.load(file)
            except json.JSONDecodeError:
                raise ValueError(f"Error decoding JSON from the specification file '{self.spec_file}'.")

        self.field_lengths = list(map(int, spec["Offsets"]))
        self.column_names = spec["ColumnNames"]
        self.fixed_width_encoding = spec["FixedWidthEncoding"]
        self.include_header = spec["IncludeHeader"]
        self.delimited_encoding = spec["DelimitedEncoding"]

    def generate_fixed_width_file(self, output_file):
        """
        Generate a fixed-width file with dummy data.

        This method creates a fixed-width text file with dummy data based on the
        field lengths specified in the spec file. Each field in the file is filled
        with repeated characters ('A', 'B', etc.).

        :param 
        output_file: Path to the fixed-width output file.
        """
        try:
            with open(output_file, 'w', encoding=self.fixed_width_encoding) as file:
                for i in range(7):
                    line = ""
                    for length in self.field_lengths:
                        field = chr(65 + (i % 26)) * length
                        line += field
                    file.write(line + "\n")
            print("Successfully generated a fixed-width file.")
        except IOError as e:
            raise IOError(f"Failed to write to '{output_file}': {e}")

    def parse_fixed_width_file(self, fixed_width_file):
        """
        Parse the fixed-width file based on the field lengths.

        This method reads a fixed-width file and extracts records based on the
        field lengths specified in the spec file.

        :param 
        fixed_width_file: Path to the fixed-width input file.

        :return: 
        A list of records, where each record is a list of field values.
        """
        if not os.path.isfile(fixed_width_file):
            raise FileNotFoundError(f"Fixed-width file '{fixed_width_file}' not found.")

        records = []
        try:
            print('Parsing the fixed-width file')
            with open(fixed_width_file, 'r', encoding=self.fixed_width_encoding) as file:
                for line in file:
                    record = []
                    position = 0
                    for length in self.field_lengths:
                        field = line[position:position+length].strip()
                        record.append(field)
                        position += length
                    records.append(record)
        except IOError as e:
            raise IOError(f"Failed to read from '{fixed_width_file}': {e}")

        print("Parsing completed.")
        return records

    def write_csv_file(self, csv_file, records):
        """
        Write the parsed records into a CSV file.

        This method writes the parsed records to a CSV file, including a header row
        if specified in the spec file.

        :params 
        csv_file: Path to the output CSV file.
        records: A list of records, where each record is a list of field values.
        """
        try:
            print('Generating a CSV file..')
            with open(csv_file, 'w', newline='', encoding=self.delimited_encoding) as file:
                writer = csv.writer(file)
                if self.include_header:
                    writer.writerow(self.column_names)
                writer.writerows(records)
            print(f"Successfully generated a CSV file: '{csv_file}'")
        except IOError as e:
            raise IOError(f"Failed to write to '{csv_file}': {e}")

    def process_files(self, fixed_width_file, csv_file):
        """
        Generate, parse, and convert fixed-width file to CSV.

        This method orchestrates the entire process of generating a fixed-width file,
        parsing it, and converting it to a CSV file.

        :params 
        fixed_width_file: Path to the fixed-width input file.
        csv_file: Path to the output CSV file.
        """
        try:
            self.generate_fixed_width_file(fixed_width_file)
            records = self.parse_fixed_width_file(fixed_width_file)
            self.write_csv_file(csv_file, records)
            print("Fixed-width file processing completed successfully.")
        except Exception as e:
            print(f"An error occurred during file processing: {e}")