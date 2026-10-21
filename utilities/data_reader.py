"""
Data reader utility for reading test data from various formats
"""
import csv
import json
from pathlib import Path
from config.config import Config
from utilities.logger_utils import get_logger

logger = get_logger(__name__)


class DataReader:
    """Utility class for reading test data"""

    @staticmethod
    def read_csv(filename):
        """Read data from CSV file"""
        try:
            filepath = Config.TEST_DATA_DIR / filename
            if not filepath.exists():
                logger.error(f"CSV file not found: {filepath}")
                return []

            data = []
            with open(filepath, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)

            logger.info(f"Read {len(data)} rows from {filename}")
            return data
        except Exception as e:
            logger.error(f"Error reading CSV file {filename}: {str(e)}")
            return []

    @staticmethod
    def read_json(filename):
        """Read data from JSON file"""
        try:
            filepath = Config.TEST_DATA_DIR / filename
            if not filepath.exists():
                logger.error(f"JSON file not found: {filepath}")
                return []

            with open(filepath, mode='r', encoding='utf-8') as file:
                data = json.load(file)

            logger.info(f"Read data from {filename}")
            return data if isinstance(data, list) else [data]
        except Exception as e:
            logger.error(f"Error reading JSON file {filename}: {str(e)}")
            return []

    @staticmethod
    def read_excel(filename, sheet_name=0):
        """Read data from Excel file"""
        try:
            import openpyxl
            filepath = Config.TEST_DATA_DIR / filename
            if not filepath.exists():
                logger.error(f"Excel file not found: {filepath}")
                return []

            workbook = openpyxl.load_workbook(filepath)
            worksheet = workbook[sheet_name] if isinstance(sheet_name, str) else workbook.worksheets[sheet_name]

            data = []
            headers = []
            for idx, row in enumerate(worksheet.iter_rows(values_only=True)):
                if idx == 0:
                    headers = row
                else:
                    data.append(dict(zip(headers, row)))

            workbook.close()
            logger.info(f"Read {len(data)} rows from {filename}")
            return data
        except ImportError:
            logger.error("openpyxl not installed. Install it to read Excel files.")
            return []
        except Exception as e:
            logger.error(f"Error reading Excel file {filename}: {str(e)}")
            return []

    @staticmethod
    def get_test_data(filename, format_type=None):
        """Get test data from file"""
        if format_type is None:
            # Detect format from file extension
            filepath = Config.TEST_DATA_DIR / filename
            if filepath.suffix.lower() == '.csv':
                return DataReader.read_csv(filename)
            elif filepath.suffix.lower() == '.json':
                return DataReader.read_json(filename)
            elif filepath.suffix.lower() in ['.xlsx', '.xls']:
                return DataReader.read_excel(filename)
            else:
                logger.error(f"Unsupported file format: {filepath.suffix}")
                return []
        elif format_type.lower() == 'csv':
            return DataReader.read_csv(filename)
        elif format_type.lower() == 'json':
            return DataReader.read_json(filename)
        elif format_type.lower() == 'excel':
            return DataReader.read_excel(filename)
        else:
            logger.error(f"Unsupported format type: {format_type}")
            return []
