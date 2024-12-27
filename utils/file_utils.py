import csv
import io

class FileUtils:
    @staticmethod
    def parse_csv(file):
        """Parse csv file and return rows as dictionaries"""
        try:
            file_data = file.read().decode("utf-8")
            csv_reader = csv.DictReader(io.StringIO(file_data))
            return [row for row in csv_reader], None
        except Exception as e:
            return None, f"Error parsing csv file: {str(e)}"