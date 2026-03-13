#!/usr/bin/env python3
"""
Search for vcpkg-configuration.json and vcpkg-run-configuration.json files
across specified GitHub organizations and summarize findings in a CSV file.

Organizations searched:
  - Arm-Examples
  - Arm-Software
  - Open-CMSIS-Pack
  - MDK-packs

Usage:
  python3 search_vcpkg_configs.py [--output OUTPUT] [--token TOKEN]

Options:
  --output  Path to the output CSV file (default: vcpkg_configurations.csv)
  --token   GitHub personal access token (or set GITHUB_TOKEN env variable)
"""

import argparse
import base64
import csv
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error


ORGANIZATIONS = [
    "Arm-Examples",
    "Arm-Software",
    "Open-CMSIS-Pack",
    "MDK-packs",
]

FILENAMES = [
    "vcpkg-configuration.json",
    "vcpkg-run-configuration.json",
]

GITHUB_API_URL = "https://api.github.com"


def github_request(path, token, params=None):
    """Make an authenticated request to the GitHub API and return parsed JSON."""
    url = f"{GITHUB_API_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        print(f"  HTTP {exc.code} for {url}: {exc.reason}", file=sys.stderr)
        return None


def search_code(query, token):
    """Search GitHub code and return all matching items (handles pagination)."""
    items = []
    page = 1
    per_page = 100

    while True:
        params = {"q": query, "per_page": per_page, "page": page}
        data = github_request("/search/code", token, params)

        if data is None:
            break

        page_items = data.get("items", [])
        items.extend(page_items)

        # Check if there are more pages
        total_count = data.get("total_count", 0)
        if len(items) >= total_count or len(page_items) < per_page:
            break

        page += 1
        # Respect GitHub search API rate limit (10 req/min unauthenticated,
        # 30 req/min authenticated)
        time.sleep(2)

    return items


def get_file_content(repo_full_name, file_path, token):
    """Retrieve and decode the content of a file from a GitHub repository."""
    path = f"/repos/{repo_full_name}/contents/{urllib.parse.quote(file_path)}"
    data = github_request(path, token)

    if data is None:
        return None

    encoding = data.get("encoding")
    content = data.get("content", "")

    if encoding == "base64":
        try:
            return base64.b64decode(content).decode("utf-8")
        except Exception as exc:
            print(f"  Failed to decode content for {repo_full_name}/{file_path}: {exc}",
                  file=sys.stderr)
            return None

    return content


def main():
    parser = argparse.ArgumentParser(
        description="Search for vcpkg configuration files across GitHub organizations."
    )
    parser.add_argument(
        "--output",
        default="vcpkg_configurations.csv",
        help="Output CSV file path (default: vcpkg_configurations.csv)",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN", ""),
        help="GitHub personal access token (or set GITHUB_TOKEN env variable)",
    )
    args = parser.parse_args()

    if not args.token:
        print(
            "Warning: No GitHub token provided. Unauthenticated requests are heavily "
            "rate-limited. Set --token or GITHUB_TOKEN.",
            file=sys.stderr,
        )

    # Collect all findings: keyed by (repo_html_url, filename) so that each
    # repository has at most one entry per configuration file type.
    # Structure: { repo_html_url: { "repo": repo_html_url, "vcpkg-configuration.json": content, "vcpkg-run-configuration.json": content } }
    findings = {}

    for org in ORGANIZATIONS:
        for filename in FILENAMES:
            query = f"filename:{filename} org:{org}"
            print(f"Searching: {query}")

            items = search_code(query, args.token)
            print(f"  Found {len(items)} result(s)")

            for item in items:
                repo = item.get("repository", {})
                repo_full_name = repo.get("full_name", "")
                repo_html_url = repo.get("html_url", f"https://github.com/{repo_full_name}")
                file_path = item.get("path", "")

                print(f"  Fetching {repo_full_name}/{file_path} ...")
                content = get_file_content(repo_full_name, file_path, args.token)

                if repo_html_url not in findings:
                    findings[repo_html_url] = {
                        "repository_url": repo_html_url,
                        "vcpkg-configuration.json": "",
                        "vcpkg-run-configuration.json": "",
                    }

                file_block = f"--- {file_path} ---\n{content or ''}"
                if findings[repo_html_url][filename]:
                    # Append subsequent instances separated by a blank line
                    findings[repo_html_url][filename] += f"\n\n{file_block}"
                else:
                    findings[repo_html_url][filename] = file_block

                # Avoid hitting secondary rate limits
                time.sleep(1)

            # Pause between searches to respect search rate limits
            time.sleep(3)

    # Write the CSV output
    output_path = args.output
    fieldnames = [
        "repository_url",
        "vcpkg-configuration.json",
        "vcpkg-run-configuration.json",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_ALL,
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in sorted(findings.values(), key=lambda r: r["repository_url"]):
            writer.writerow(row)

    print(f"\nResults written to {output_path} ({len(findings)} repositories found).")


if __name__ == "__main__":
    main()
