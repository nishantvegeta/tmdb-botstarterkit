from RPA.Browser.Selenium import Selenium
import time
from app.Constants import Constants
from qrlib.QREnv import QREnv
from qrlib.QRComponent import QRComponent
from robot.libraries.BuiltIn import BuiltIn

class BrowserComponent(QRComponent):
    def __init__(self):
        super().__init__()
        self.logger = self.run_item.logger
        self.browser = Selenium()

        self.tmdb_url = None

    def open_browser(self):
        try: 
            self.tmdb_url = Constants.TMDB_URL
            self.browser.open_available_browser(
                browser_selection='firefox', 
                headless=False
            )
            self.browser.maximize_browser_window()

        except Exception as e:
            print(f"Error initializing browser: {e}")


    def search_movie(self, movie_name):
        try:
            url = self.tmdb_url + movie_name
            time.sleep(3)
            self.browser.go_to(url)
        except Exception as e:
            print(f"Error opening movie search page for '{movie_name}': {e}")

    def handle_overlays(self):
        """Dismiss any overlays or popups (e.g., cookie banners)."""
        try:
            if self.browser.is_element_visible(Constants.consent_button_xpath):
                print("Dismissing cookie consent overlay...")
                self.browser.click_element(Constants.consent_button_xpath)
                time.sleep(3)  # Wait for the banner to disappear
        except Exception as e:
            print(f"Error dismissing overlay: {e}")

    def click_and_extract_movie_details(self, movie_name):
        """Click on the movie with the latest release year and exact name match, then extract its details."""
        print("movie name : ", movie_name)
        self.handle_overlays()  # Dismiss any overlays before clicking

        # movie_titles_xpath = "//div[@class='title']//a/h2"
        movie_titles_elements = self.browser.get_webelements(Constants.movie_titles_xpath.format(movie_name))

        # movie_years_xpath = "//div[@class='wrapper']//span[@class='release_date']"
        movie_years_elements = self.browser.get_webelements(Constants.movie_released_years_xpath.format(movie_name))

        movie_data = []
        
        print(movie_years_elements)
        for index, element in enumerate(movie_years_elements):
            year_text = element.text.strip()[-4:]
            try:
                year = int(year_text)
                title = movie_titles_elements[index].text.strip()  # Use .strip() to remove whitespace
                
                # Check for exact match with the movie name (ignoring case)
                if title == movie_name:
                    movie_data.append((title, year, index))  # Store the index for later use

                # print(f"found movie: '{title}' with year: {year}")
            except ValueError:
                continue

        movie_data.sort(key=lambda x: x[1], reverse=True)

        print(f"Matching movies found: {movie_data}")
        self.logger.info(f'--****---{movie_data}')
        if not movie_data:
            print(f"No matching movies found for {movie_name}\n")
            return

        # Find the movie with the latest year among the exact matches
        latest_movie = max(movie_data, key=lambda x: x[1])
        latest_index = latest_movie[2]
        print("------------------------->", latest_index)
        print(f"Clicking on the latest movie: {latest_movie[0]} ({latest_movie[1]})")

        # Dismiss overlays again before clicking, if necessary
        # self.handle_overlays()

        # Click on the movie with the latest year
        # self.browser.wait_until_element_is_visible(movie_titles_xpath)
        # self.browser.scroll_element_into_view(movie_titles_elements[latest_index])
        # self.scroll_to_load_movies()
        self.browser.click_element(movie_titles_elements[latest_index])
        time.sleep(2)

        # Extract movie details
        return self.extract_movie_details(movie_name)

    def scroll_to_load_movies(self):
        """Scrolls down the page slowly using 'PAGE_DOWN' to load more movie results, then scrolls back up using 'PAGE_UP'."""
        try:
            scroll_pause_time = 1  # Adjust the pause time as needed

            for _ in range(2):  # You can increase or decrease the number of scrolls
                # Scroll down
                self.browser.press_keys(None, "PAGE_DOWN")
                time.sleep(scroll_pause_time)

            for _ in range(2):
                self.browser.press_keys(None, "PAGE_UP")
                time.sleep(scroll_pause_time)
        except Exception as e:
            print(f"Error scrolling the movie results page: {e}")

    def extract_movie_data(self, movie_name):
        try:
            self.search_movie(movie_name)
            self.scroll_to_load_movies()
            return self.click_and_extract_movie_details(movie_name)  # Return the movie details here
        except Exception as e:
            print(f"Error processing {movie_name}: {e}")
            return {
            'movie_name': movie_name,
            'status': 'No Movie Found'
        }  # Return None if an error occurs

    def extract_movie_details(self, movie_name):
        """Extract TMDB score, Storyline, Genres, and Reviews."""
        # try:
        # Wait for the user score element to be visible, if not raise an exception
        self.browser.wait_until_element_is_visible(Constants.user_score_xpath, timeout=10)

        user_score = self.browser.get_element_attribute(Constants.user_score_xpath, "data-percent")
        storyline = self.browser.get_text(Constants.storyline_xpath)
        genres = self.browser.get_text(Constants.genres_xpath)

        # self.scroll_to_load_movies()

        # # Step 2: Scroll to and click on "Read All Reviews"
        # self.click_read_all_reviews()

        # Step 3: Extract reviews
        # reviews = self.extract_reviews()

        self.browser.go_to(f'{self.browser.get_location()}/reviews')

        reviews_elements = self.browser.find_elements(Constants.reviews_xpath)
        self.logger.info(f'****{reviews_elements}****')
        reviews = [review.text for review in reviews_elements[:5]]
        self.logger.info(f'****{reviews}****')
        if len(reviews) < 5:
            for _ in range(5-len(reviews)):
                reviews.append(None)


        # Return a dictionary with all extracted data
        movie_data = {
            'movie_name': movie_name,
            'user_score': user_score,
            'storyline': storyline,
            'genres': genres,
            'review_1': reviews[0],
            'review_2': reviews[1],
            'review_3': reviews[2],
            'review_4': reviews[3],
            'review_5': reviews[4],
            'status': 'Success'
        }
        # self.logger.info(f'\n\nfinal:\n{movie_data}\n\n')
        self.logger.info(f'\n\nfinal:\n{movie_name}, {user_score}, {storyline}, {genres}, {reviews[0]}, {len(reviews)}\n\n')

        return movie_data
        
        # except Exception as e:
        #     print(f"Error while extracting details for '{movie_name}': {e}")
        #     return None  # Return None if an error occurs

    def extract_reviews(self):
        """Extracts the reviews from the movie page."""
        # try:
        self.scroll_to_load_movies()
        self.click_read_all_reviews()
        reviews_elements = self.browser.find_elements(Constants.reviews_xpath)
        self.logger.info(f'****{reviews_elements}****')
        reviews = [review.text.strip() for review in reviews_elements[:5]]
        self.logger.info(f'****{reviews}****')
        if len(reviews) < 5:
            for _ in 5-len(reviews):
                reviews.append(None)

        return reviews  
        # except Exception as e:
        #     print(f"Error extracting reviews: {e}")
        #     return []  


    def click_read_all_reviews(self):
        """Click on 'Read All Reviews' link if available."""
        try:
            self.handle_overlays()
            # if self.browser.is_element_visible(Constants.read_reviews_xpath):
            #     print("Clicking on 'Read All Reviews'")
            #     self.browser.click_element(Constants.read_reviews_xpath)
            #     time.sleep(3)
            # else:
            #     print("No reviews found.")
            self.click_element_when_clickable(Constants.read_reviews_xpath)
            time.sleep(3)
        except Exception as e:
            print(f"Error clicking on 'Read All Reviews': {e}")

    def close_browser(self):
        """Close the browser safely."""
        try:
            self.browser.close_browser()
        except Exception as e:
            print(f"Error closing the browser: {e}")
