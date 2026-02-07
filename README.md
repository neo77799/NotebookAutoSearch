# NotebookLM 自動検索

このスクリプトは、Playwrightを利用してNotebookLMの検索を自動化します。

## 前提

- Python 3.10+ 推奨（動作実績: 3.14）
- Google Chrome がインストール済みであること（Playwrightを `channel="chrome"` で起動します）

## プロジェクト構造

プロジェクトは以下のファイルに分割されています。

- `main.py`: メインの実行スクリプト。他のモジュールをインポートして処理を調整します。
- `config.py`: 設定情報（パス、URL、セレクタ、タイムアウトなど）を定義します。
- `auth.py`: Googleアカウントへのログイン処理を担当します。
- `project_manager.py`: NotebookLMのプロジェクト一覧の取得を担当します。
- `search_automation.py`: 検索の実行と結果の保存を担当します。
- `requirements.txt`: 必要なPythonライブラリをリストします。
- `.gitignore`: Gitで無視するファイルを指定します。

## 使い方

### 0. 仮想環境の構築（venv推奨）

以下の手順で仮想環境を構築し、アクティベートしてください。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 1. 依存関係のインストール

まず、必要なライブラリをインストールします。

```powershell
python -m pip install -r requirements.txt
python -m playwright install
```

### 2. 初回セットアップ

以下のコマンドを実行して、ブラウザでGoogleアカウントにログインします。認証情報が `.secure/user_data` ディレクトリに保存されます。

```powershell
python main.py setup
```

実行するとブラウザが起動するので、手動でログインしてください。ログインが完了すると、このスクリプトは自動で終了します。

### 3. プロジェクト一覧の表示

以下のコマンドで、利用可能なプロジェクトの一覧を表示できます。

```powershell
python main.py list
```

### 4. 検索の実行

プロジェクト名と検索したい言葉を指定して、検索を実行します。

```powershell
python main.py search "プロジェクト名" "検索したい言葉"
```

複数の言葉で検索することも可能です。

```powershell
python main.py search "プロジェクト名" "言葉1" "言葉2"
```

検索結果は、`output` ディレクトリにMarkdownファイルとして保存されます。

## Headless / Headful

- デフォルトは headful（画面あり）で起動します（NotebookLM側の挙動で headless が不安定になることがあるため）
- headless を明示したい場合は環境変数を設定します

```powershell
$env:NOTEBOOKAUTOSEARCH_HEADLESS="1"
python main.py search "プロジェクト名" "検索語"
```

## トラブルシュート

### 文字化け/UnicodeEncodeError（Windowsのcp932）

必要に応じて、PowerShell側をUTF-8出力にします。

```powershell
$env:PYTHONIOENCODING="utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```

### Chromeプロファイル競合（TargetClosedError等）

`.secure/user_data` を使っているChromeプロセスが残っていると失敗することがあります。
その場合はいったんChromeを終了してから再実行してください。

## Codex向け

Codex運用手順は `CODEX.md` を参照してください。
