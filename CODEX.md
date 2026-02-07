# Codex向け: NotebookLM 自動検索フロー

このドキュメントは、このリポジトリ内の `NotebookAutoSearch/` を使って、NotebookLM から検索結果を取得し、`output/` に保存された Markdown を根拠として引用・要約するための運用手順です。

対象:
- Codex (この作業環境でのエージェント運用)
- Windows + PowerShell

## 前提
- `NotebookAutoSearch/.secure/user_data` に NotebookLM へログイン済みの永続プロファイルがあること
  - ない場合は `python main.py setup` をユーザーが手動で実行して作成する
- `NotebookAutoSearch/.venv` があること（なければ作る）

## セットアップ（初回のみ）

```powershell
cd d:\Flash_dev\fl_shape_app\NotebookAutoSearch
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install
```

## 実行コマンド

### プロジェクト一覧

```powershell
cd d:\Flash_dev\fl_shape_app\NotebookAutoSearch
.\.venv\Scripts\python.exe main.py list
```

### 検索（1つ以上のキーワード）

```powershell
cd d:\Flash_dev\fl_shape_app\NotebookAutoSearch
.\.venv\Scripts\python.exe main.py search "プロジェクト名" "検索語1" "検索語2"
```

プロジェクトID（UUID）が分かっている場合は、`id:` プレフィックス（またはUUID単体）で指定できます。

```powershell
.\.venv\Scripts\python.exe main.py search "id:<notebook_uuid>" "検索語"
.\.venv\Scripts\python.exe main.py search "<notebook_uuid>" "検索語"
```

検索結果は `NotebookAutoSearch/output/` に `YYYYMMDD_プロジェクト名_検索語.md` のようなファイル名で保存されます。

## Headless / Headful

NotebookLM 側の挙動により headless で不安定になる場合があります。

- デフォルト: headful（画面あり）
- headless を明示する場合:

```powershell
$env:NOTEBOOKAUTOSEARCH_HEADLESS="1"
.\.venv\Scripts\python.exe main.py search "プロジェクト名" "検索語"
```

## 出力（引用）の扱い方

1. `main.py search ...` で `output/*.md` を生成する
2. 引用・要約は `output/*.md` のテキストを根拠に行う
3. ユーザーへの回答では、参照元ファイルパスを併記する
   - 例: `NotebookAutoSearch/output/20260207_..._ShapeRecords.md`

## よくあるトラブル

### 文字化け/UnicodeEncodeError（cp932）
- PowerShell 側で UTF-8 出力を使う（必要に応じて）

```powershell
$env:PYTHONIOENCODING="utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```

### `TargetClosedError` / Chrome プロファイル競合
- `user_data_dir` を使っている Chrome プロセスが残っていると失敗することがあります。
- `--user-data-dir=...NotebookAutoSearch\.secure\user_data` を含む Chrome を終了してから再実行します。

## 推奨の使い分け
- 構造体名/タグ名など「固有名詞で引ける」もの: そのまま検索語にする（例: `ShapeRecords`, `DefineShape4`）
- 「説明を引き出したい」もの: 質問文で検索する（例: `StraightEdgeRecord は水平/垂直/一般線をどう符号化する？`）
