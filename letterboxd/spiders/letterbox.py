import scrapy
import urllib.parse

class LetterboxSpider(scrapy.Spider):
    name = "letterbox"
    allowed_domains = ["letterboxd.com"]
    start_urls = [
        "https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/",
        "https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/page/2/",
        "https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/page/3/"
    ]

    def parse(self, response):
        movie_elements = response.css('div.really-lazy-load')
        for movie_element in movie_elements:
            movie_url = movie_element.css('::attr(data-target-link)').extract_first()
            if movie_url:
                # Make sure the URL is absolute
                movie_url = response.urljoin(movie_url)
                yield scrapy.Request(url=movie_url, callback=self.parse_movie)

    def parse_movie(self, response):
        movie = {}

        tab_cast = response.css("#tab-cast")
        castList = tab_cast.css("p a")

        cast = []

        film_header = response.css(".film-header-group")

        movie["movieName"] = film_header.css(".headline-1.filmtitle .name::text").get().strip()
        movie["releaseYear"] = film_header.css(".releaseyear a::text").get()
        movie["directorName"] = film_header.css(".directorlist a span::text").get()


        movie_info_html = response.css('.review.body-text .truncate p')
        if movie_info_html:
            movie_info = movie_info_html.css('::text').get()
            movie["info"] = movie_info.strip() if movie_info else None
        else:
            movie["info"] = None

        rating_label = response.xpath("//meta[@name='twitter:label2']/@content").get()
        rating_data = response.xpath("//meta[@name='twitter:data2']/@content").get()

        if rating_label == "Average rating" and rating_data:
            movie["rating"] = rating_data.strip()

        for castP in castList:
            cast_item = {}
            cast_item["castRealName"] = castP.css("::text").get()
            cast_item["castActorpage"] = castP.attrib.get("href", "")
            cast_item["character"] = castP.attrib.get("title", "")
            cast.append(cast_item)

        movie["Cast List"] = cast
        movie["movie_url"] = response.url

        yield movie