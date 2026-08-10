# FastAPI SQLiteチャット履歴サンプル

FastAPIとSQLiteを使い、セッションごとの会話履歴を保存・取得・削除するAPIサンプルです。LLMには接続せず、APIと永続化の構成に焦点を当てています。

## 前提条件

- Python 3.12以上、4.0未満
- Poetry

以降のコマンドは、このREADMEがあるプロジェクトルートで実行してください。

## セットアップ

```bash
poetry install --no-root
```

データベースの保存先は、`CHAT_DB_PATH` 環境変数で変更できます。未設定の場合は、プロジェクトルートの `chat.db` を使用します。

```bash
export CHAT_DB_PATH=./data/chat.db
```

保存先の親ディレクトリは、起動前に作成してください。

## 起動

```bash
poetry run uvicorn app.main:app --reload
```

Swagger UIは <http://127.0.0.1:8000/docs> で確認できます。

## エンドポイント

- `POST /sessions`: セッションを作成
- `POST /sessions/{session_id}/messages`: ユーザー発言と簡単な応答を保存
- `GET /sessions/{session_id}/messages`: 会話履歴を時系列で取得
- `DELETE /sessions/{session_id}`: セッションと履歴を削除

### API操作例

セッションを作成します。

```bash
curl -X POST http://127.0.0.1:8000/sessions
```

レスポンスの `session_id` を環境変数へ設定し、メッセージの追加、履歴の取得、セッションの削除を試せます。

```bash
export SESSION_ID="取得したsession_id"

curl -X POST "http://127.0.0.1:8000/sessions/${SESSION_ID}/messages" \
  -H "Content-Type: application/json" \
  -d '{"message":"こんにちは"}'

curl "http://127.0.0.1:8000/sessions/${SESSION_ID}/messages"

curl -X DELETE "http://127.0.0.1:8000/sessions/${SESSION_ID}"
```

このサンプルの応答はLLMが生成するものではなく、受信件数と入力内容を含む固定形式のメッセージです。

## 生成ファイル

実行時に生成される `chat.db` とSQLiteの補助ファイルはGit管理対象外です。`CHAT_DB_PATH` を設定した場合は、そのパスにデータベースが生成されます。

## テスト

```bash
poetry run pytest
```
