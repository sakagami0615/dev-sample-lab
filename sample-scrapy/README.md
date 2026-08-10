# Scrapyサンプル

Scrapyの基本的なプロジェクト構成とSpiderの定義を確認するためのサンプルです。モンスターハンターワイルズ公式サイトを対象URLに設定しています。

## 前提条件

- Python 3.12以上、4.0未満
- Poetry

以降のセットアップは、このREADMEがあるプロジェクトルートで実行してください。

## セットアップ

```bash
poetry install
```

## 動作確認

`scrapy.cfg` は `app` にあるため、Scrapyコマンドは `app` に移動してから実行します。

```bash
cd app
poetry run scrapy list
poetry run scrapy check
```

`scrapy list` に `scrapy_mh_spider` が表示され、`scrapy check` が `OK` になれば構成を読み込めています。

## 実行

```bash
poetry run scrapy crawl scrapy_mh_spider
```

このコマンドはモンスターハンターワイルズ公式サイトへ実際にアクセスします。対象サイトの利用条件を確認したうえで実行してください。

## 現在の動作とクロール設定

現状の `parse()` は取得処理が未実装です。Spiderは対象ページへアクセスしますが、アイテムは出力しません。コメントアウトされたコードはCSSセレクターとページング処理の参考例です。

主な設定は次のとおりです。

- `ROBOTSTXT_OBEY = True`: 対象サイトの `robots.txt` に従う
- `DOWNLOAD_DELAY = 3`: 同一サイトへのリクエスト間隔を3秒にする
- `HTTPCACHE_ENABLED = True`: HTTPレスポンスをキャッシュする

HTTPキャッシュは `.scrapy/` に生成され、Git管理対象外です。
