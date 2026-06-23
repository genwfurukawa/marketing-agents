#!/usr/bin/env python3
"""
notion_setup_client.py

Scaffold a new client marketing hub in Notion under NOTION_HQ_PAGE_ID.

Usage:
    python scripts/notion_setup_client.py "Client Name"

Creates:
    [Client Name] - Marketing Hub            (page, standalone under HQ)
      |-- 📅 Content Calendar                (database, standalone)
      |-- 📦 Deliverables                    (database, standalone)
      |-- 📊 Reports                         (page)
      |-- 🧭 Strategy                        (page)
            |-- 🎯 Positioning & ICP
            |-- 🗣️ Brand Voice
            |-- ⚔️ Competitive Landscape

The hub page body is populated with link_to_page blocks so each child is
discoverable with its emoji icon.

Requires: notion-client, python-dotenv
    pip install notion-client python-dotenv
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    sys.exit("Missing dependency: python-dotenv. Install with: pip install python-dotenv")

try:
    from notion_client import Client
    from notion_client.errors import APIResponseError
except ImportError:
    sys.exit("Missing dependency: notion-client. Install with: pip install notion-client")


REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = REPO_ROOT / ".env"


def title_payload(text: str) -> list[dict]:
    return [{"type": "text", "text": {"content": text}}]


def select_options(values: list[str]) -> dict:
    return {"select": {"options": [{"name": v} for v in values]}}


def create_page(
    notion: Client,
    parent_page_id: str,
    title: str,
    emoji: str | None = None,
) -> str:
    kwargs = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "properties": {"title": {"title": title_payload(title)}},
    }
    if emoji:
        kwargs["icon"] = {"type": "emoji", "emoji": emoji}
    page = notion.pages.create(**kwargs)
    return page["id"]


def create_database(
    notion: Client,
    parent_page_id: str,
    title: str,
    properties: dict,
    emoji: str | None = None,
) -> str:
    kwargs = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": title_payload(title),
        "is_inline": False,
        "properties": properties,
    }
    if emoji:
        kwargs["icon"] = {"type": "emoji", "emoji": emoji}
    db = notion.databases.create(**kwargs)
    return db["id"]


def append_hub_links(
    notion: Client,
    hub_page_id: str,
    content_calendar_db_id: str,
    deliverables_db_id: str,
    reports_page_id: str,
    strategy_page_id: str,
) -> None:
    """Add structured link blocks to the hub page body."""
    children = [
        {
            "type": "heading_2",
            "heading_2": {"rich_text": title_payload("Databases")},
        },
        {
            "type": "link_to_page",
            "link_to_page": {"type": "database_id", "database_id": content_calendar_db_id},
        },
        {
            "type": "link_to_page",
            "link_to_page": {"type": "database_id", "database_id": deliverables_db_id},
        },
        {
            "type": "heading_2",
            "heading_2": {"rich_text": title_payload("Pages")},
        },
        {
            "type": "link_to_page",
            "link_to_page": {"type": "page_id", "page_id": reports_page_id},
        },
        {
            "type": "link_to_page",
            "link_to_page": {"type": "page_id", "page_id": strategy_page_id},
        },
    ]
    notion.blocks.children.append(block_id=hub_page_id, children=children)


def print_env_block(client_name: str, ids: dict[str, str]) -> None:
    slug = (
        client_name.lower()
        .replace("&", "and")
        .replace("/", "-")
        .replace(" ", "_")
    )
    header = f"# --- Notion IDs for {client_name} ---"
    print()
    print(header)
    print(f"NOTION_CLIENT_SLUG={slug}")
    print(f"NOTION_CLIENT_HUB_PAGE_ID={ids['hub']}")
    print(f"NOTION_CONTENT_CALENDAR_DB_ID={ids['content_calendar']}")
    print(f"NOTION_DELIVERABLES_DB_ID={ids['deliverables']}")
    print(f"NOTION_REPORTS_PAGE_ID={ids['reports']}")
    print(f"NOTION_STRATEGY_PAGE_ID={ids['strategy']}")
    print(f"NOTION_STRATEGY_POSITIONING_ICP_PAGE_ID={ids['positioning_icp']}")
    print(f"NOTION_STRATEGY_BRAND_VOICE_PAGE_ID={ids['brand_voice']}")
    print(f"NOTION_STRATEGY_COMPETITIVE_PAGE_ID={ids['competitive']}")
    print("# " + "-" * (len(header) - 2))


def fail(step: str, err: Exception, created: dict[str, str]) -> None:
    print(f"\nERROR during: {step}", file=sys.stderr)
    print(f"  {type(err).__name__}: {err}", file=sys.stderr)
    if created:
        print("\nPartial progress (resources already created):", file=sys.stderr)
        for k, v in created.items():
            print(f"  {k}: {v}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        sys.exit('Usage: python scripts/notion_setup_client.py "Client Name"')

    client_name = sys.argv[1].strip()
    hub_title = f"{client_name} - Marketing Hub"

    load_dotenv(ENV_PATH)
    notion_token = os.getenv("NOTION_TOKEN")
    hq_page_id = os.getenv("NOTION_HQ_PAGE_ID")

    if not notion_token:
        sys.exit("NOTION_TOKEN not set in .env")
    if not hq_page_id:
        sys.exit("NOTION_HQ_PAGE_ID not set in .env")

    notion = Client(auth=notion_token)
    created: dict[str, str] = {}

    print(f"Setting up Notion workspace for: {client_name}")
    print(f"Parent HQ page: {hq_page_id}")

    # 1. Hub page
    try:
        print(f"  -> Creating hub page: {hub_title}")
        hub_id = create_page(notion, hq_page_id, hub_title, emoji="🚀")
        created["hub"] = hub_id
    except APIResponseError as e:
        fail("create hub page", e, created)

    # 2. Content Calendar database
    try:
        print("  -> Creating Content Calendar database")
        content_calendar_props = {
            "Title": {"title": {}},
            "Type": select_options(["Blog", "LinkedIn", "Email", "Other"]),
            "Status": select_options(
                ["Brief", "Draft", "Review", "Approved", "Published"]
            ),
            "Publish Date": {"date": {}},
            "Notes": {"rich_text": {}},
        }
        cc_id = create_database(
            notion,
            hub_id,
            "Content Calendar",
            content_calendar_props,
            emoji="📅",
        )
        created["content_calendar"] = cc_id
    except APIResponseError as e:
        fail("create Content Calendar database", e, created)

    # 3. Deliverables database
    try:
        print("  -> Creating Deliverables database")
        deliverables_props = {
            "Name": {"title": {}},
            "Type": select_options(
                ["Audit", "Strategy", "Campaign", "Report", "Other"]
            ),
            "Status": select_options(
                ["Not Started", "In Progress", "Review", "Delivered"]
            ),
            "Due Date": {"date": {}},
            "Link": {"url": {}},
        }
        deliverables_id = create_database(
            notion,
            hub_id,
            "Deliverables",
            deliverables_props,
            emoji="📦",
        )
        created["deliverables"] = deliverables_id
    except APIResponseError as e:
        fail("create Deliverables database", e, created)

    # 4. Reports page
    try:
        print("  -> Creating Reports page")
        reports_id = create_page(notion, hub_id, "Reports", emoji="📊")
        created["reports"] = reports_id
    except APIResponseError as e:
        fail("create Reports page", e, created)

    # 5. Strategy page + sub-pages
    try:
        print("  -> Creating Strategy page")
        strategy_id = create_page(notion, hub_id, "Strategy", emoji="🧭")
        created["strategy"] = strategy_id
    except APIResponseError as e:
        fail("create Strategy page", e, created)

    sub_pages = [
        ("Positioning & ICP", "🎯", "positioning_icp"),
        ("Brand Voice", "🗣️", "brand_voice"),
        ("Competitive Landscape", "⚔️", "competitive"),
    ]
    for title, emoji, key in sub_pages:
        try:
            print(f"     -> Creating sub-page: {title}")
            sub_id = create_page(notion, strategy_id, title, emoji=emoji)
            created[key] = sub_id
        except APIResponseError as e:
            fail(f"create Strategy sub-page: {title}", e, created)

    # 6. Link children into hub page body
    try:
        print("  -> Linking children in hub page body")
        append_hub_links(
            notion,
            hub_page_id=hub_id,
            content_calendar_db_id=created["content_calendar"],
            deliverables_db_id=created["deliverables"],
            reports_page_id=created["reports"],
            strategy_page_id=created["strategy"],
        )
    except APIResponseError as e:
        fail("append link blocks to hub page", e, created)

    print("\nDone. All resources created successfully.")
    print_env_block(client_name, created)


if __name__ == "__main__":
    main()
