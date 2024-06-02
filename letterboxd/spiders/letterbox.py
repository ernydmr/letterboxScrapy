import scrapy

class LetterboxSpider(scrapy.Spider):
    name = "letterbox"  # Name of the spider
    allowed_domains = ["letterboxd.com"]  # Allowed domain for the spider to crawl
    start_urls = [
        "https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/",
        "https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/page/2/",
        "https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/page/3/"
    ]

    def parse(self, response):
        # Extract movie links from the response
        movie_elements = response.css('div.really-lazy-load')
        for movie_element in movie_elements:
            # Get movie URL
            movie_url = movie_element.css('::attr(data-target-link)').extract_first()
            if movie_url:
                movie_url = response.urljoin(movie_url)
                # Make a request to the movie URL and call parse_movie for further processing
                yield scrapy.Request(url=movie_url, callback=self.parse_movie)

    def parse_movie(self, response):
        movie = {}  # Dictionary to store movie details

        # Extract movie header details
        film_header = response.css(".film-header-group")
        movie["movieName"] = film_header.css(".headline-1.filmtitle .name::text").get().strip()
        movie["releaseYear"] = film_header.css(".releaseyear a::text").get()
        movie["directorName"] = film_header.css(".directorlist a span::text").get()

        # Extract movie information if available
        movie_info_html = response.css('.review.body-text .truncate p')
        if movie_info_html:
            movie_info = movie_info_html.css('::text').get()
            movie["info"] = movie_info.strip() if movie_info else None
        else:
            movie["info"] = None

        # Extract average rating
        rating_label = response.xpath("//meta[@name='twitter:label2']/@content").get()
        rating_data = response.xpath("//meta[@name='twitter:data2']/@content").get()
        if rating_label == "Average rating" and rating_data:
            movie["rating"] = rating_data.strip()

        # Extract cast details
        tab_cast = response.css("#tab-cast")
        castList = tab_cast.css("p a")
        cast = []
        for castP in castList:
            cast_item = {}
            cast_item["castRealName"] = castP.css("::text").get()
            cast_item["castActorpage"] = castP.attrib.get("href", "")
            cast_item["character"] = castP.attrib.get("title", "")
            cast.append(cast_item)
        movie["Cast List"] = cast

        movie["movie_url"] = response.url  # Store movie URL

        # Create stats URL and make a request to it, passing the movie data
        movie_name = response.url.split('/')[-2]
        stats_url = f"https://letterboxd.com/csi/film/{movie_name}/stats/"
        yield scrapy.Request(url=stats_url, callback=self.parse_stats, meta={'movie': movie}) #Meta is work for Data transfer

    def parse_stats(self, response):
        movie = response.meta['movie']  # Retrieve movie data from meta

        # Extract stats details
        stats = response.css('ul.film-stats li.stat')
        movie['watches'] = self.convert_stats(stats.css('li.filmstat-watches a::text').get())
        movie['lists'] = self.convert_stats(stats.css('li.filmstat-lists a::text').get())
        movie['likes'] = self.convert_stats(stats.css('li.filmstat-likes a::text').get())
        movie['top250_rank'] = stats.css('li.filmstat-top250 a::text').get()

        yield movie  # Return the final movie data

    def convert_stats(self, text):
        # Convert stats text to a more readable format
        if text:
            text = text.strip()
            text = text.replace('.', '')  # Remove dots
            if 'K' in text:
                text = text.replace('K', '000')
            elif 'M' in text:
                text = text.replace('M', '000000')
        return text
