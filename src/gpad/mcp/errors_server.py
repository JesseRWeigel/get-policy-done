"""gpad-errors MCP server — Known LLM policy analysis failure modes.

Provides access to the catalog of systematic LLM failure patterns in
policy analysis (double counting, transfer payment confusion, baseline drift,
false precision, present value errors, etc.).
"""

from __future__ import annotations

import json
import re
import asyncio
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("gpad-errors")

ERRORS_FILE = Path(__file__).resolve().parents[1] / "specs" / "references" / "verification" / "llm-policy-errors.md"


def _parse_errors() -> list[dict]:
    """Parse the error catalog markdown into structured records."""
    if not ERRORS_FILE.exists():
        return []

    content = ERRORS_FILE.read_text()
    errors = []
    current_error: dict | None = None
    current_section = ""

    for line in content.splitlines():
        err_match = re.match(r"^###\s+(E\d+):\s+(.+)", line)
        if err_match:
            if current_error:
                errors.append(current_error)
            current_error = {
                "id": err_match.group(1),
                "title": err_match.group(2).strip(),
                "severity": current_section,
                "pattern": "",
                "example": "",
                "guard": "",
            }
            continue

        if line.startswith("## Critical"):
            current_section = "critical"
        elif line.startswith("## Serious"):
            current_section = "serious"
        elif line.startswith("## Subtle"):
            current_section = "subtle"

        if current_error:
            if line.startswith("**Pattern**:"):
                current_error["pattern"] = line.replace("**Pattern**:", "").strip()
            elif line.startswith("**Example**:"):
                current_error["example"] = line.replace("**Example**:", "").strip()
            elif line.startswith("**Guard**:"):
                current_error["guard"] = line.replace("**Guard**:", "").strip()

    if current_error:
        errors.append(current_error)

    return errors


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_errors",
            description="List all known LLM policy analysis failure modes with IDs and severity.",
            inputSchema={
                "type": "object",
                "properties": {
                    "severity": {
                        "type": "string",
                        "description": "Filter by severity level",
                        "enum": ["critical", "serious", "subtle"],
                    },
                },
            },
        ),
        Tool(
            name="get_error",
            description="Get full details of a specific error pattern by ID (e.g., E001).",
            inputSchema={
                "type": "object",
                "properties": {
                    "error_id": {"type": "string", "description": "Error ID (e.g., 'E001')"},
                },
                "required": ["error_id"],
            },
        ),
        Tool(
            name="search_errors",
            description="Search error patterns by keyword. Useful for checking if a planned action might trigger a known failure mode.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search keyword (e.g., 'discount rate', 'double counting', 'baseline')"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_guards_for_task",
            description="Given a task description, return all relevant error guards that should be checked.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_description": {"type": "string", "description": "Description of the policy analysis task being performed"},
                },
                "required": ["task_description"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    errors = _parse_errors()

    if name == "list_errors":
        severity = arguments.get("severity")
        if severity:
            errors = [e for e in errors if e["severity"] == severity]
        summary = [{"id": e["id"], "title": e["title"], "severity": e["severity"]} for e in errors]
        return [TextContent(type="text", text=json.dumps(summary, indent=2))]

    elif name == "get_error":
        error_id = arguments["error_id"].upper()
        match = next((e for e in errors if e["id"] == error_id), None)
        if match is None:
            return [TextContent(type="text", text=json.dumps({
                "error": f"Error '{error_id}' not found",
                "available": [e["id"] for e in errors],
            }))]
        return [TextContent(type="text", text=json.dumps(match, indent=2))]

    elif name == "search_errors":
        query = arguments["query"].lower()
        matches = [
            e for e in errors
            if query in e["title"].lower()
            or query in e["pattern"].lower()
            or query in e["example"].lower()
            or query in e["guard"].lower()
        ]
        return [TextContent(type="text", text=json.dumps(matches, indent=2))]

    elif name == "get_guards_for_task":
        desc = arguments["task_description"].lower()
        keyword_map = {
            "double count": ["E001"],
            "benefit": ["E001"],
            "mortality": ["E001"],
            "vsl": ["E001"],
            "transfer": ["E002"],
            "tax": ["E002"],
            "subsidy": ["E002"],
            "baseline": ["E003"],
            "counterfactual": ["E003"],
            "no-action": ["E003"],
            "precision": ["E004"],
            "uncertainty": ["E004"],
            "confidence interval": ["E004"],
            "discount": ["E005"],
            "present value": ["E005"],
            "npv": ["E005"],
            "nominal": ["E005"],
            "real": ["E005"],
            "equilibrium": ["E006"],
            "market": ["E006"],
            "wage": ["E006"],
            "cost-benefit": ["E001", "E002", "E003", "E005"],
            "cba": ["E001", "E002", "E003", "E005"],
            "regulatory impact": ["E001", "E003", "E004", "E005"],
            "sensitivity": ["E004"],
        }
        relevant_ids: set[str] = set()
        for keyword, eids in keyword_map.items():
            if keyword in desc:
                relevant_ids.update(eids)
        guards = [e for e in errors if e["id"] in relevant_ids]
        return [TextContent(type="text", text=json.dumps(guards, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
