import scrapy


class LetterboxSpider(scrapy.Spider):
    name = "letterbox"
    allowed_domains = ["letterboxd.com"]
    start_urls = [
        "https://letterboxd.com/film/harakiri/",
        "https://letterboxd.com/film/come-and-see/",
        "https://letterboxd.com/film/12-angry-men/",
        "https://letterboxd.com/film/seven-samurai/",
        "https://letterboxd.com/film/the-godfather-part-ii/",
        "https://letterboxd.com/film/high-and-low/",
        "https://letterboxd.com/film/parasite-2019/",
        "https://letterboxd.com/film/the-human-condition-iii-a-soldiers-prayer/",
        "https://letterboxd.com/film/the-godfather/",
        "https://letterboxd.com/film/the-shawshank-redemption/"
    ]

    def parse(self, response):
        movie = {}
        film_header = response.css(".film-header-group")
        movie["movieName"] = film_header.css(".headline-1.filmtitle .name::text").get().strip()
        movie["releaseYear"] = film_header.css(".releaseyear a::text").get()
        movie["directorName"] = film_header.css(".directorlist a span::text").get()

        rating_header = response.css(".average-rating")
        movie["rating"] = rating_header.css("a::text").get()

        stats_header = response.css(".film-stats")
        statsList = stats_header.css(".stat .filmstat-watches")

        movie["watched"] = response.css('a.has-icon.tooltip::text').get()

        movie_info_html = response.css('.review.body-text .truncate p')
        if movie_info_html:
            movie_info = movie_info_html.css('::text').get()
            movie["info"] = movie_info.strip() if movie_info else None
        else:
            movie["info"] = None

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

        yield movie