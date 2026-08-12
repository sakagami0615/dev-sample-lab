# Streamlit サンプル集

## セットアップ

プロジェクトルートで依存関係をインストールします。

```bash
poetry install
```

## サンプル一覧

### basic_widgets — 基本ウィジェット一覧

Streamlit の主要なウィジェットを1ページにまとめたサンプルです。

```bash
poetry run streamlit run samples/basic_widgets/app/app.py
```

### multipage_app — マルチページアプリ

`st.navigation` + `st.Page` による3ページ構成(Home / Data View / Form)のサンプルです。

```bash
poetry run streamlit run samples/multipage_app/app/app.py
```

### dashboard — データ分析ダッシュボード

同梱のサンプル売上データ(`samples/dashboard/app/data/sales_sample.csv`)を使ったダッシュボードです。
サイドバーで期間・カテゴリ・地域を絞り込めます。

```bash
poetry run streamlit run samples/dashboard/app/app.py
```

サンプルデータを作り直す場合は以下を実行してください。

```bash
poetry run python samples/dashboard/app/generate_data.py
```

### chat_support — RAGチャットサポートUI

サポートポータルを模したチャットUIのサンプルです。ユーザー向けの初期メッセージ・関連情報を表示した後、
チャットで商品・サービスについて問い合わせると、ダミーのナレッジベースを検索して回答します。
AIだけでは回答できない質問には、問い合わせ窓口への案内を表示します。

UI(`app.py`)とロジック(`services/` の `user_service.py` / `rag_service.py` / `chat_service.py`)を分離しており、
Service層はStreamlitに依存しないため、将来的にFastAPI等へ置き換えやすい構成になっています。

本来ログイン認証から取得する想定のユーザーIDは、デモでは環境変数 `CHAT_SUPPORT_USER_ID` から取得します。
未設定の場合はデフォルト値にフォールバックせず、画面上にその旨を明示してエラー表示します。

ダミーデータ(`app/data/*.json`)はDWH(データウェアハウス)のディメンション/ファクトテーブルを模し、
`users` / `user_related_info` / `kb_documents` / `kb_document_keywords` に分割・正規化しています。
`updated_at` や `source_system` といったメタ列を持ち、Service層(`user_service.py` / `rag_service.py`)が
外部キー(`user_id` / `document_id`)で結合してドメインモデルを組み立てます。

```bash
CHAT_SUPPORT_USER_ID=user-001 poetry run streamlit run samples/chat_support/app/app.py
```
