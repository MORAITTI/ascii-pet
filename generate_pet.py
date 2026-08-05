import subprocess
import json
import os

user = os.getenv('GITHUB_REPOSITORY').split('/')[0] # login
cmd = f"gh api user/repos --jq '.[].name'"
repos = subprocess.check_output(cmd, shell=True, text=True).strip().split('\n')

total_weekly = 0

for repo in repos:
  
