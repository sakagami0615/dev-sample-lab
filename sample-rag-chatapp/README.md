# RAGチャットアプリ サンプル

Streamlit、OpenAI、LangChain、Chromaを使用したRAGチャットアプリです。登録済み文書に近い質問はRAGで回答し、それ以外は検索ツールを利用するエージェントへ渡します。

## 前提条件

- Python 3.12以上、4.0未満
- Poetry
- OpenAI APIキー
- 文書取得、OpenAI API、検索ツールを利用できるインターネット接続

以降のコマンドは、このREADMEがあるプロジェクトルートで実行してください。

## セットアップ

```bash
poetry install
cp .env.example .env
```

`.env` にOpenAIのAPIキー、モデル名、temperatureを設定します。APIキーには実際に利用する秘密情報を設定し、Gitへコミットしないでください。

```dotenv
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_MODEL=gpt-4.1-mini
OPENAI_API_TEMPERATURE=0
```

3つの環境変数はすべて必須です。未設定の場合や、`OPENAI_API_TEMPERATURE` が数値でない場合はアプリを起動できません。

## ベクトルDBの作成

```bash
poetry run python app/create_vectorstore.py
```

このコマンドは `app/create_vectorstore.py` に定義されたサンプルURLから文書を取得し、OpenAI Embeddingsでベクトル化します。外部サイトとOpenAI APIへアクセスするため、通信状況やサイト側の変更によって失敗する場合があり、OpenAI APIの利用料金が発生する可能性があります。

生成される `chroma_db/` はプロジェクトルートに保存され、Git管理対象外です。

## 起動

```bash
poetry run streamlit run app/main.py
```

`make` を利用できる環境では、ポート8080で起動できます。

```bash
make run
```

## 回答方法

現在は `app/setting.py` の `MODE` が `Mode.AUTO` に設定されています。

- 登録済み文書との関連度がしきい値以上の場合は、Chromaから取得した文書を根拠にRAGで回答する
- 関連度がしきい値未満の場合は、DuckDuckGo検索とWikipediaを利用できる検索エージェントで回答する

`MODE` を `Mode.RAG` に変更すると常にRAGを利用し、`Mode.AGENT` に変更すると常に検索エージェントを利用します。RAG回答、検索エージェントの回答ともにOpenAI APIを使用するため、利用料金が発生する可能性があります。

画面内の会話履歴はStreamlitセッション中保持されます。検索エージェントの履歴もセッションごとのthread IDで分離されます。

## テスト

外部APIへアクセスせず、アプリとサンプルスクリプトをプロジェクトルートからimportできることを確認します。

```bash
poetry run python -m unittest discover -s tests -v
```
