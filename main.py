import asyncio
import sys
import os
import re
from playwright.async_api import async_playwright, Page
from typing import Callable, Awaitable

from config import CONFIG
from auth import setup_auth
from project_manager import list_projects
from search_automation import search_and_save

def _ensure_utf8_stdio() -> None:
    """Avoid UnicodeEncodeError on Windows consoles (cp932) when printing Japanese text."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def _headless_default() -> bool:
    """NotebookLM may block automation in headless mode; default to headful unless explicitly enabled."""
    v = os.environ.get("NOTEBOOKAUTOSEARCH_HEADLESS", "").strip().lower()
    return v in ("1", "true", "yes", "on")

async def with_playwright(func: Callable[[Page], Awaitable[None]]):
    """Initializes Playwright, creates a context and page, and handles errors."""
    if not CONFIG["paths"]["user_data_dir"].exists():
        print(CONFIG["messages"]["error"]["login_missing"])
        return

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            CONFIG["paths"]["user_data_dir"],
            headless=_headless_default(),
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = await context.new_page()
        page.set_default_timeout(CONFIG["timeouts"]["default"])
        try:
            await func(page)
        except Exception as e:
            print(CONFIG["messages"]["error"]["generic_error"].format(e))
            screenshot_path = CONFIG["paths"]["error_screenshot"]
            print(CONFIG["messages"]["error"]["screenshot_notice"].format(screenshot_path))
            await page.screenshot(path=screenshot_path, full_page=True)
        finally:
            await context.close()
            print(CONFIG["messages"]["info"]["browser_closed"])

async def list_command(page: Page):
    """Lists all available projects."""
    print(CONFIG["messages"]["info"]["moving_to_notebooklm"])
    await page.goto(CONFIG["urls"]["notebooklm"])
    await list_projects(page)

async def search_command(page: Page, project_name: str, search_terms: list[str]):
    """Performs a search in a project."""
    print(CONFIG["messages"]["info"]["moving_to_notebooklm"])
    await page.goto(CONFIG["urls"]["notebooklm"])

    raw = project_name.strip()
    m = re.fullmatch(r"id:([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})", raw)
    if m:
        project_id = m.group(1)
        label = f"id:{project_id}"
        project_selector = CONFIG["selectors"]["project_id"](project_id)
    elif re.fullmatch(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", raw):
        # Convenience: if user passes just the UUID, treat it as project id.
        project_id = raw
        label = f"id:{project_id}"
        project_selector = CONFIG["selectors"]["project_id"](project_id)
    else:
        label = raw
        project_selector = CONFIG["selectors"]["project_title"](raw)

    print(CONFIG["messages"]["info"]["entering_project"].format(label))
    await page.locator(project_selector).click()
    print(CONFIG["messages"]["info"]["project_page_loaded"])

    for term in search_terms:
        await search_and_save(page, label, term)

async def main():
    """Main function to orchestrate the automation."""
    _ensure_utf8_stdio()
    args = sys.argv[1:]
    
    if not args:
        print("Usage: python main.py <command> [options]")
        print("Commands:")
        print("  setup: Run the initial setup to log in to Google.")
        print("  list: List available projects.")
        print("  search <project_name> <search_term1> <search_term2> ...: Search for terms in a project.")
        return

    command = args[0]

    if command == "setup":
        await setup_auth()
    elif command == "list":
        await with_playwright(list_command)
    elif command == "search":
        if len(args) < 3:
            print(CONFIG["messages"]["error"]["search_terms_missing"])
            return
        project_name = args[1]
        search_terms = args[2:]
        await with_playwright(lambda page: search_command(page, project_name, search_terms))
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    asyncio.run(main())
