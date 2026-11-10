import os
import shlex
import shutil
import subprocess
import sys

from datetime import datetime
from zoneinfo import ZoneInfo

""" 
Each run of this file takes the earliest remaining thesis- folder,
mirrors it into the thesis folder, while also staging the changes
and moving the snapshot to the processed folder. Then it prints
the commit command with the backdated datetime for the commit.
"""

ROOT = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(ROOT, 'thesis')
PROCESSED = os.path.join(ROOT, 'processed')
TIMEZONE = ZoneInfo('America/Vancouver')


def git(*args):
    result = subprocess.run(['git', *args], cwd=ROOT, check=True, capture_output=True, text=True)
    return result.stdout


def get_snapshots():
    snapshots = []
    for item in os.listdir(ROOT):
        item_path = os.path.join(ROOT, item)
        if not os.path.isdir(item_path):
            continue
        if not item.startswith('thesis-'):
            continue
        snapshots.append(item)
    snapshots.sort()
    return snapshots


def process_snapshot(snapshots: list[str]):
    next_snapshot = snapshots[0]
    shutil.rmtree(TARGET, ignore_errors=True)
    shutil.copytree(os.path.join(ROOT, next_snapshot), TARGET)
    git('add', '-A', '--', 'thesis')

    os.makedirs(PROCESSED, exist_ok=True)
    shutil.move(os.path.join(ROOT, next_snapshot), os.path.join(PROCESSED, next_snapshot))

    print(f'Snapshot: {next_snapshot}  ({len(snapshots) - 1} remaining)')


def get_commit_datetime():
    # Date the commit by the newest file that will actually be in the repo
    tracked = git('ls-files', '-z', '--', 'thesis').split('\0')
    newest = max(os.path.getmtime(os.path.join(ROOT, path)) for path in tracked if path)
    date = datetime.fromtimestamp(newest, TIMEZONE).isoformat()

    # Catch timing mismatch, just in case
    if git('rev-list', '--all', '-n', '1'):
        previous = git('log', '-1', '--format=%aI').strip()
        if datetime.fromisoformat(previous) > datetime.fromisoformat(date):
            print(f'Warning: this is older than the previous commit ({previous}).')

    return date


def main():
    print()
    if git('status', '--porcelain', '--', 'thesis'):
        sys.exit('Folder thesis/ has uncommitted changes. Commit the previous snapshot first.')

    snapshots = get_snapshots()
    if not snapshots:
        sys.exit('No snapshots left. All done!')

    process_snapshot(snapshots)
    if not git('diff', '--cached', '--name-only'):
        sys.exit('No changes compared to the previous snapshot, nothing to commit.')

    date = get_commit_datetime()
    print(f'Date: {date}\n')
    date = shlex.quote(date)
    print(f'GIT_AUTHOR_DATE={date} GIT_COMMITTER_DATE={date} git commit -m ""')


if __name__ == '__main__':
    main()
