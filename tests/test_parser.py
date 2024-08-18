import pytest
import json
import os
from src.parser import FixedWidthFileParser

@pytest.fixture
def setup_test_environment():
    """
    Set up test environment.
    """
    spec_file = 'tests/test_spec.json'
    fixed_width_file = 'tests/test_fixed_width.txt'
    csv_file = 'tests/test_output.csv'
    
    # Sample spec file data
    spec_data = {
        "ColumnNames": ["Field1", "Field2"],
        "Offsets": [7, 2],
        "FixedWidthEncoding": "windows-1252",
        "IncludeHeader": "True",
        "DelimitedEncoding": "utf-8"
    }
    
    with open(spec_file, 'w') as f:
        json.dump(spec_data, f)
    
    parser = FixedWidthFileParser(spec_file)

    yield {
        'parser': parser,
        'spec_file': spec_file,
        'fixed_width_file': fixed_width_file,
        'csv_file': csv_file
    }

    # Clean up test environment
    for file in [spec_file, fixed_width_file, csv_file]:
        if os.path.exists(file):
            os.remove(file)

def test_load_spec(setup_test_environment):
    """
    Test loading of the specification file.
    """
    parser = setup_test_environment['parser']
    assert parser.field_lengths == [7, 2]
    assert parser.column_names == ["Field1", "Field2"]
    assert parser.fixed_width_encoding == "windows-1252"
    assert parser.include_header
    assert parser.delimited_encoding == "utf-8"

def test_generate_fixed_width_file(setup_test_environment):
    """
    Test generation of a fixed-width file with dummy data.
    """
    parser = setup_test_environment['parser']
    fixed_width_file = setup_test_environment['fixed_width_file']
    parser.generate_fixed_width_file(fixed_width_file)
    assert os.path.isfile(fixed_width_file)
    with open(fixed_width_file, 'r') as file:
        content = file.readlines()
    assert len(content) == 7  # 7 lines generated

def test_parse_fixed_width_file(setup_test_environment):
    """
    Test parsing of a fixed-width file.
    """
    parser = setup_test_environment['parser']
    fixed_width_file = setup_test_environment['fixed_width_file']
    parser.generate_fixed_width_file(fixed_width_file)
    records = parser.parse_fixed_width_file(fixed_width_file)
    assert len(records) == 7  # 7 lines
    assert records[0] == ['AAAAAAA', 'AA']  # First record

def test_write_csv_file(setup_test_environment):
    """
    Test writing of records to a CSV file.
    """
    parser = setup_test_environment['parser']
    fixed_width_file = setup_test_environment['fixed_width_file']
    csv_file = setup_test_environment['csv_file']
    parser.generate_fixed_width_file(fixed_width_file)
    records = parser.parse_fixed_width_file(fixed_width_file)
    parser.write_csv_file(csv_file, records)
    assert os.path.isfile(csv_file)
    with open(csv_file, 'r') as file:
        content = file.readlines()
    assert content[0].strip() == "Field1,Field2"  # Header
    assert content[1].strip() == "AAAAAAA,AA"  # First record

def test_process_files(setup_test_environment):
    """
    Test the complete processing of files.
    """
    parser = setup_test_environment['parser']
    fixed_width_file = setup_test_environment['fixed_width_file']
    csv_file = setup_test_environment['csv_file']
    parser.process_files(fixed_width_file, csv_file)
    assert os.path.isfile(csv_file)
    with open(csv_file, 'r') as file:
        content = file.readlines()
    assert content[0].strip() == "Field1,Field2"  # Header
    assert content[1].strip() == "AAAAAAA,AA"  # First record
