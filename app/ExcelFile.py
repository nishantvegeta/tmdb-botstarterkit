import os
import pandas as pd

from app.Constants import Constants
from qrlib.QRComponent import QRComponent
from qrlib.QREnv import QREnv
from qrlib.QRRunItem import QRRunItem
from openpyxl import Workbook

class ExcelFile(QRComponent):

    def __init__(self) -> None:
        super().__init__()

        self.excel_file_path = Constants.excel_file_path
        self.excel_worksheet_name = Constants.excel_worksheet_name
        self.excel_data_col_name = Constants.excel_data_col_name

        # self.run_item = QRRunItem(logger_name="TMDB Bot")
        # self.notify(self.run_item)
        self.logger = self.run_item.logger
        self.excel_data = None

        self.load_vault()

    def load_vault(self):
        pass

    def open_excel(self):
        try:
            self.logger.info(f"Opening workbook: {self.excel_file_path}...")
            self.excel_data = pd.read_excel(self.excel_file_path, sheet_name=self.excel_worksheet_name)
            self.logger.info(f"Successfully loaded worksheet: {self.excel_worksheet_name}")
        except Exception as e:
            # Use 'warning' instead of 'error' to avoid the AttributeError
            self.run_item.logger.warning(f"Failed to open workbook or worksheet: {self.excel_file_path}, {self.excel_worksheet_name}")
            raise e

    
    def get_column(self):
        try:
            self.logger.info(f"Getting data from column: {self.excel_data_col_name}")
            data_list = self.excel_data[self.excel_data_col_name].dropna().tolist()
            return data_list
        except Exception as e:
            # Use 'warning' instead of 'error'
            self.run_item.logger.warning(f"Failed to get data from column: {self.excel_data_col_name}")
            raise e

    # def create_excel_file(self, data, file_path, worksheet_name):
    #     try:
    #         # Convert list of dictionaries to pandas DataFrame
    #         df = pd.DataFrame(data)

    #         # Check if the file exists
    #         if os.path.exists(file_path):
    #             self.logger.info(f"File already exists at {file_path}. Appending data to the existing file.")
    #             with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    #                 df.to_excel(writer, sheet_name=worksheet_name, index=False)
    #         else:
    #             self.logger.info(f"Creating a new Excel workbook at: {file_path}")
    #             df.to_excel(file_path, sheet_name=worksheet_name, index=False)

    #         self.logger.info(f"Excel file saved successfully at: {file_path}")
    #     except Exception as e:
    #         # Use 'warning' instead of 'error'
    #         self.run_item.logger.warning(f"Failed to create or write to Excel file at: {file_path}")
    #         raise e
        
    def close_excel(self):
        # With pandas, explicit closing is not necessary.
        self.logger.info("No need to close Excel file with pandas.")



    # def create_excel_file(self, data, file_name):
    #     # Convert the dictionary to a DataFrame
    # # Filter out any None entries
    #     filtered_data = [entry for entry in data if entry is not None]
    #     self.logger.info("-----------------",filtered_data)
        
    #     # Convert the list of dictionaries to a DataFrame
    #     df = pd.DataFrame(filtered_data)
        
    #     # Save the DataFrame to an Excel file
    #     df.to_excel(file_name, index=False)

    def create_excel_file(self, data, file_name):        # Filter out any None entries
        
        # filtered_data = [entry for entry in data if entry is not None]

        print("------------------------------------------",data)
        df = pd.DataFrame(data)
        # Create a DataFrame from the list of dictionaries
        # columns_order = ['movie_name', 'user_score', 'storyline', 'genres', 'review_1', 'review_2', 'review_3', 'review_4', 'review_5', 'status']
        # df = pd.DataFrame(columns=columns_order)

        # # Reorder the columns as needed (you can add/remove columns as per your requirement)
        # df = df.from_dict(data=data)

        # Save the DataFrame to an Excel file with headers
        df.to_excel(file_name, index=False)

            

