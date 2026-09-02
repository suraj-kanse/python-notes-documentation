#!/usr/bin/env python3
"""
Multi-Commit & Push Automation Script
Iterates through generated note files and creates individual, descriptive git commits
for each topic, maximizing GitHub contribution visibility.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MANIFEST_FILE = BASE_DIR / "generated_manifest.json"
README_FILE = BASE_DIR / "README.md"
QUEUE_FILE = BASE_DIR / "video_queue.txt"


def run_git(command: list):
    """Execute a git command in the repository directory."""
    result = subprocess.run(
        ["git"] + command,
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"[ERROR] Git command failed: git {' '.join(command)}")
        print(f"[STDERR] {result.stderr.strip()}")
    else:
        if result.stdout.strip():
            print(f"[GIT] {result.stdout.strip()}")
    return result.returncode == 0


def main():
    if not MANIFEST_FILE.exists():
        print("[INFO] No generated_manifest.json found. Nothing to commit.")
        sys.exit(0)

    try:
        manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERROR] Failed to read manifest: {e}")
        sys.exit(1)

    created_files = manifest.get("created_files", [])
    date_str = manifest.get("date", "")
    video_url = manifest.get("video_url", "")

    print(f"[INFO] Found {len(created_files)} topic notes to commit individually.")

    # 1. Commit and push each generated topic file individually
    for i, item in enumerate(created_files, 1):
        file_path = item.get("file_path")
        commit_msg = item.get("commit_message", f"docs: add educational notes on {item.get('title')}")
        rel_path = os.path.relpath(file_path, BASE_DIR).replace("\\", "/")

        print(f"\n[INFO] [{i}/{len(created_files)}] Committing: {rel_path}")
        if run_git(["add", rel_path]):
            if run_git(["commit", "-m", commit_msg]):
                print(f"[INFO] Pushing commit for {rel_path}...")
                run_git(["push", "origin", "main"])

    # 2. Commit and push README index and video_queue changes
    files_to_update = []
    if README_FILE.exists():
        files_to_update.append(str(README_FILE))
    if QUEUE_FILE.exists():
        files_to_update.append(str(QUEUE_FILE))

    if files_to_update:
        print("\n[INFO] Updating index and queue in repository...")
        for f in files_to_update:
            run_git(["add", os.path.relpath(f, BASE_DIR).replace("\\", "/")])
        
        index_msg = f"docs(index): update learning log and index for {date_str}"
        if run_git(["commit", "-m", index_msg]):
            run_git(["push", "origin", "main"])

    # Clean up manifest
    if MANIFEST_FILE.exists():
        MANIFEST_FILE.unlink()
        print("[INFO] Cleaned up manifest file.")

    print("[SUCCESS] All topic notes committed and pushed individually to GitHub!")


if __name__ == "__main__":
    main()
