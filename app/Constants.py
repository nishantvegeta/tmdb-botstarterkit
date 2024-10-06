import os

class Constants:
    script_path = os.path.abspath(__file__)
    excel_file_path = os.path.join(os.path.dirname(script_path), 'Movies.xlsx')
    excel_worksheet_name = 'Sheet1'
    excel_data_col_name = 'Movie'

    excel_output_file_path = 'output/movies_data.xlsx'

    TMDB_URL = 'https://www.themoviedb.org/search/movie?query='
    movie_titles_xpath = "//div[@class='title']//a[@data-media-type='movie']/h2[text()='{}']"
    movie_released_years_xpath = "//div[@class='title']//h2[text()='{}']//ancestor::div[@class='title']//span"
    user_score_xpath = "//div[@class='user_score_chart' and @data-percent]"
    storyline_xpath = '//div[@class="overview"]//p'
    genres_xpath = '//span[@class="genres"]'
    reviews_xpath = '//section[@class="panel review"]//div[@class="review_container"]//div[@class="teaser"]'
    read_reviews_xpath = '//a[contains(text(),"Read All Reviews")]'
    # reviews_xpath = '//section[@class="panel review"]//div[@class="review_container"]//div[@class="content"]//p'
                
    consent_button_xpath = '//*[@id="onetrust-accept-btn-handler"]'  # Replace with the correct button XPath