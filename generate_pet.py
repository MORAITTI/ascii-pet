import subprocess
import json
import os

user = os.getenv('GITHUB_REPOSITORY').split('/')[0] # login
cmd = f"gh api user/repos --jq '.[].name'"
repos = subprocess.check_output(cmd, shell=True, text=True).strip().split('\n')

total_weekly = 0

for repo in repos:
  if not repo:
      continue
    # clone repo (lightweight)
    clone_mid = f"git clone --depth 1 --filter-blob:none https://github.com/{user}/{repo}.git /tmp/{repo} 2>/dev/null || true"
    subprocess.run(clone_cmd, shell=True)
    # считаем коммиты за последние 7 дней
    count_md = f"git -C /tmp/{repo} rev-list --count --author='{user}' --since='7 days ago' HEAD 2>/dev/null || echo 0"
    count = int(subprocess.check_output(cont_cmd, shell=True, text=True).strip())
    total_weekly += count
    # удаляем клон, чтоб не захламлять
    subprocess.run(f"rm -rf /tmp/{repo}", shell=True)

# состояние питомца
if total_weekly == 0;
    stage = " голодная смерть"
    ascii_art = r """
    
