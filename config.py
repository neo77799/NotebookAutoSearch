from pathlib import Path

# Define the project root
project_root = Path(__file__).parent

CONFIG = {
    "paths": {
        "project_root": project_root,
        "user_data_dir": project_root / ".secure" / "user_data",
        "output_dir": project_root / "output",
        "error_screenshot": "error.png",
    },
    "urls": {
        "notebooklm": "https://notebooklm.google.com/",
    },
    "selectors": {
        "project_button": "project-button",
        # Click the actual action button inside the project tile to avoid click interception.
        "project_title": lambda project_name: (
            f'project-button:has(span.project-button-title:has-text("{project_name}")) '
            f'button.primary-action-button'
        ),
        "search_box": 'textarea[aria-label="クエリボックス"]',
        # NotebookLM renders multiple send buttons; prefer an enabled one.
        "send_button": 'button[aria-label="送信"]:not([disabled])',
        "result_message_card": "mat-card.to-user-message-card-content",
        "message_text_content": "div.message-text-content",
        "response_actions": "response-actions",
    },
    "timeouts": {
        "login": 300000,  # 5 minutes for manual login
        "default": 90000,
        "stabilization": 90000,
        "stabilization_interval": 1000,
        "wait_for_visible": 60000,
    },
    "stability": {
        "required_stable_iterations": 5,
    },
    "messages": {
        "info": {
            "profile_creation": "Google Chromeのプロファイルを '{}' に作成・使用します。",
            "launching_browser": "Google Chromeを起動します。",
            "manual_login_prompt": "手動でGoogleアカウントにログインしてください。",
            "script_auto_termination": "ログインが完了すると、このスクリプトは自動で終了します。",
            "waiting_for_login": "ログインが成功し、プロジェクト一覧が表示されるのを待っています...",
            "login_detected": "ログインを検知しました。セットアップを完了します。",
            "moving_to_notebooklm": "NotebookLMに移動しています...",
            "entering_project": "プロジェクト「{}」に入っています...",
            "project_page_loaded": "プロジェクトページに遷移しました。",
            "listing_projects": "プロジェクト一覧を取得しています...",
            "available_projects": """
--- 利用可能なプロジェクト ---
""",
            "re_run_hint": """
検索したいプロジェクト名を指定して、再度コマンドを実行してください。
例: python main.py "プロジェクト名" "検索語"
""",
            "no_projects_found": "プロジェクトが見つかりませんでした。",
            "starting_search": """
-----------------------------------
「{}」で検索を開始します...
""",
            "wait_for_search_box": "検索ボックスが表示されるのを待っています...",
            "filling_search_box": "「{}」と入力します...",
            "clicking_send": "検索実行ボタンをクリックします...",
            "wait_for_response": "AIの応答テキストが安定するまで待機します...",
            "text_stabilized": "テキストが安定しました。",
            "search_result_header": "--- 検索結果 ---",
            "search_result_footer": "----------------",
            "file_saved": "✅ 検索結果を {} に保存しました。",
            "browser_closed": "ブラウザを閉じました。",
            "separator": "--------------------------------------------------",
        },
        "error": {
            "login_missing": """
エラー: ログイン情報が見つかりません。
先に 'python main.py setup' を実行して、ログインを完了させてください。
""",
            "search_terms_missing": """
エラー: プロジェクト名に加えて、1つ以上の検索したい言葉を指定してください。
例: python main.py "プロジェクト名" "検索語1" "検索語2" ...
""",
            "generic_error": """
エラーが発生しました: {}
""",
            "screenshot_notice": """
デバッグのため、スクリーンショットを {} に保存します。
""",
            "timeout_suggestion": """
タイムアウトした場合は、再度コマンドを実行してください。
""",
        },
        "warn": {
            "text_not_stable": "警告: テキストが安定しませんでした。結果が不完全な可能性があります。",
        },
    },
}
