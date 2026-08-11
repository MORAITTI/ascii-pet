import subprocess
import os
import sys
import json
import urllib.request

repo_full = os.getenv('GITHUB_REPOSITORY', '')
if not repo_full:
    print("GITHUB_REPOSITORY not set")
    sys.exit(1)
user = repo_full.split('/')[0]

url = f"https://api.github.com/users/{user}/repos?type=public&per_page=100"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        repos = [repo['name'] for repo in data]
except Exception as e:
    print(f"Failed to fetch public repos: {e}")
    sys.exit(1)

total_weekly = 0

for repo in repos:
    clone_url = f"https://github.com/{user}/{repo}.git"
    clone_cmd = f"git clone --depth 1 --filter=blob:none {clone_url} /tmp/{repo} 2>/dev/null || true"
    subprocess.run(clone_cmd, shell=True)

    count_cmd = f"git -C /tmp/{repo} rev-list --count --author='{user}' --since='7 days ago' HEAD 2>/dev/null || echo 0"
    try:
        count = int(subprocess.check_output(count_cmd, shell=True, text=True).strip())
    except:
        count = 0
    total_weekly += count
    subprocess.run(f"rm -rf /tmp/{repo}", shell=True)

MAX_COMMITS = 20
satiety = min(100, int((total_weekly / MAX_COMMITS) * 100))

if satiety < 30:
    bar_color = "#e74c3c"
    status = "Hungry"
    ascii_art = r"""
     .-.
    (x.x)
     |=|
    /|_|\
    """
elif satiety < 70:
    bar_color = "#f1c40f"
    status = "Normal"
    ascii_art = r"""
     .-.
    (o.o)
     |=|
    /|_|\
    """
else:
    bar_color = "#2ecc71"
    status = "Energetic"
    ascii_art = r"""
     .-.
    (>_<)
     |=|
    /|_|\
    """

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="540" height="380">
  <rect width="100%" height="100%" fill="#0d1117" rx="10"/>
  <text x="20" y="40" font-family="Courier New, monospace" fill="#58a6ff" font-size="18">
    Commits last week (public repos): {total_weekly}
  </text>
  <text x="20" y="75" font-family="Courier New, monospace" fill="#f0883e" font-size="16">
    Status: {status}
  </text>
  <text x="20" y="115" font-family="Courier New, monospace" fill="#c9d1d9" font-size="14">
    Satiety: {satiety}%
  </text>
  <rect x="20" y="130" width="480" height="20" rx="10" fill="#2d2d2d" />
  <rect x="20" y="130" width="{int(480 * satiety / 100)}" height="20" rx="10" fill="{bar_color}" />
  <text x="20" y="190" font-family="Courier New, monospace" fill="#c9d1d9" font-size="14" xml:space="preserve">
{ascii_art}
  </text>
</svg>'''

with open('pet.svg', 'w') as f:
    f.write(svg_content)

print(f"Pet updated. Weekly commits: {total_weekly}, Satiety: {satiety}%")