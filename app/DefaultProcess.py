
import time
from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item
from qrlib.QRRunItem import QRRunItem

from app.Constants import Constants
from app.ExcelFile import ExcelFile
from app.PostgreSQL import PostgreSQL
from app.DefaultComponent import DefaultComponent
from app.EmailComponent import EmailComponent
from app.BrowserComponent import BrowserComponent

from DefaultComponent import DefaultComponent
class DefaultProcess(QRProcess):
    def __init__(self):
        super().__init__()

        self.run_item = QRRunItem(logger_name="TMDB Bot")
        self.notify(self.run_item)
        self.logger = self.run_item.logger

        self.default_component = DefaultComponent()
        self.excel_component = ExcelFile()
        self.postgresql_component = PostgreSQL()
        self.email_component = EmailComponent()
        self.browser_component = BrowserComponent()

        self.register(self.default_component)
        self.register(self.excel_component)
        self.register(self.postgresql_component)
        self.register(self.email_component)
        self.register(self.browser_component)

        self.movie_name = []
        self.movies_data = []

    @run_item(is_ticket=False)
    def before_run(self, *args, **kwargs):
        try:
            self.run_item.logger.info("")
            self.excel_component.open_excel()
            self.movies_names = self.excel_component.get_column()
            self.postgresql_component.establish_connection()
            self.postgresql_component.create_table()
            self.browser_component.open_browser()
            self.email_component.authorize()
            return "Initialization completed successfully."
        except Exception as e:
            self.run_item.logger.info(f"Failed : {e}")
            return f"Initialization failed: {e}"

    @run_item(is_ticket=False, post_success=False)
    def before_run_item(self, *args, **kwargs):
        pass

    @run_item(is_ticket=True)
    def execute_run_item(self, *args, **kwargs) -> dict:
        movie_name = kwargs["movie_name"]

        final_movie_data = {
            'movie_name': movie_name,
            'user_score': None, 
            'storyline': None,
            'genres': None,
            'review_1': None,
            'review_2': None,
            'review_3': None,
            'review_4': None,
            'review_5': None,
            'status': "Not Found"
        }

        # Scrape the movie data
        scrapped_movie_data_dict = self.browser_component.extract_movie_data(movie_name)
        self.run_item.logger.info(f'\n\n\n\n{scrapped_movie_data_dict}\n\n\n\n')

        if scrapped_movie_data_dict is None:
            self.logger.info(f"Failed to extract details for movie: {movie_name}")
        else:
            # Check and safely access the keys, setting default values if keys are missing
            final_movie_data['movie_name'] = scrapped_movie_data_dict.get('movie_name', movie_name)
            final_movie_data['user_score'] = scrapped_movie_data_dict.get('user_score', '0')
            final_movie_data['storyline'] = scrapped_movie_data_dict.get('storyline', 'No storyline available')
            final_movie_data['genres'] = scrapped_movie_data_dict.get('genres', 'Unknown')
            final_movie_data['review_1'] = scrapped_movie_data_dict.get('review_1', None)
            final_movie_data['review_2'] = scrapped_movie_data_dict.get('review_2', None)
            final_movie_data['review_3'] = scrapped_movie_data_dict.get('review_3', None)
            final_movie_data['review_4'] = scrapped_movie_data_dict.get('review_4', None)
            final_movie_data['review_5'] = scrapped_movie_data_dict.get('review_5', None)
            final_movie_data['status'] = scrapped_movie_data_dict.get('status', 'Success')

            # Insert movie data into the database
            self.postgresql_component.insert_into_table(
                movie_name=final_movie_data['movie_name'],
                user_score=final_movie_data['user_score'],
                storyline=final_movie_data['storyline'],
                genres=final_movie_data['genres'],
                review_1=final_movie_data['review_1'],
                review_2=final_movie_data['review_2'],
                review_3=final_movie_data['review_3'],
                review_4=final_movie_data['review_4'],
                review_5=final_movie_data['review_5'],
                status=final_movie_data['status']
            )
            self.logger.info(scrapped_movie_data_dict)

        return final_movie_data
    
    @run_item(is_ticket=False, post_success=False)
    def after_run_item(self, *args, **kwargs):
        movie_data = kwargs["movie_data"]
        self.movies_data.append(movie_data)

    @run_item(is_ticket=False, post_success=False)
    def after_run(self, *args, **kwargs):
        try:
            self.postgresql_component.close_connection()
            self.excel_component.close_excel()
            self.browser_component.close_browser()
            return "Run completed successfully. Connections closed."
        except Exception as e:
            return f"Run completion failed: {e}"

    def execute_run(self):
        for movie in self.movies_names:
            self.before_run_item()
            movie_data_dict = self.execute_run_item(movie_name=movie)
            self.after_run_item(movie_data=movie_data_dict)

        self.excel_component.create_excel_file(
            data=self.movies_data,
            file_name=Constants.excel_output_file_path, 
            # worksheet_name='Movies'
        )

        self.email_component.send_mail()
        return "Process executed and email sent successfully."
