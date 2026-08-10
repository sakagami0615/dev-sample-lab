import scrapy
from sample_scrapy.items import SampleScrapyItem


class ScrapyMhSpiderSpider(scrapy.Spider):
    name = "scrapy_mh_spider"
    allowed_domains = ["www.monsterhunter.com"]
    start_urls = ["https://www.monsterhunter.com/wilds/ja-jp/"]

    def parse(self, response):
        """
        レスポンスに対するパース処理
        """
        pass

        # TODO: 参考記事のままだとHMページで欲しい情報取れないので加工が必要
        # (参考ページ：https://qiita.com/Chanmoro/items/f4df85eb73b18d902739)

        """
        # response.css で scrapy デフォルトの css セレクタを利用できる
        for post in response.css('.post-listing .post-item'):
            # items に定義した Post のオブジェクトを生成して次の処理へ渡す
            yield SampleScrapyItem(
                url=post.css('div.post-header a::attr(href)').extract_first().strip(),
                title=post.css('div.post-header a::text').extract_first().strip(),
                date=post.css('div.post-header span.date a::text').extract_first().strip(),
            )

        # 再帰的にページングを辿るための処理
        older_post_link = response.css('.blog-pagination a.next-posts-link::attr(href)').extract_first()
        if older_post_link is None:
            # リンクが取得できなかった場合は最後のページなので処理を終了
            return

        # URLが相対パスだった場合に絶対パスに変換する
        older_post_link = response.urljoin(older_post_link)
        # 次のページをのリクエストを実行する
        yield scrapy.Request(older_post_link, callback=self.parse)
        """
