"""Contracts and safety policy for the external Zotero MCP server.

MROS does not import Zotero MCP directly. Claude Code calls the configured server, while
records are normalized into MROS files. This module exposes the curated tool allowlist used
by validation and setup documentation.
"""

READ_ONLY_TOOLS = {
    "zotero_search_items",
    "zotero_semantic_search",
    "zotero_get_item_metadata",
    "zotero_get_item_children",
    "zotero_get_annotations",
    "zotero_read_pdf_pages",
    "zotero_get_collection_items",
    "zotero_find_related_papers",
    "zotero_export_bibliography",
    "zotero_library_coverage",
}

DENIED_BY_DEFAULT = {
    "zotero_get_item_fulltext",
    "zotero_delete_item",
    "zotero_merge_duplicates",
    "zotero_update_item",
    "zotero_create_note",
    "zotero_add_by_doi",
    "zotero_add_by_url",
    "zotero_add_by_bibtex",
    "zotero_add_by_csl_json",
    "zotero_add_from_file",
    "zotero_remove_tags",
    "zotero_add_tags",
}


def is_safe_default_tool(tool_name: str) -> bool:
    return tool_name in READ_ONLY_TOOLS and tool_name not in DENIED_BY_DEFAULT
