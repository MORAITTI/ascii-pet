import subprocess
import json
import os

# Получаем список всех репозиториев пользователя через GitHub CLI
user = os.getenv('GITHUB_REPOSITORY').split('/')[0]  # ваш логин
cmd = f"gh api user/repos --jq '.[].name'"
repos = subprocess.check_output(cmd, shell=True, text=True).strip().split('\n')

total_weekly = 0

for repo in repos:
    if not repo:
        continue
    # Клонируем каждый репозиторий (глубоко не нужно, достаточно lightweight)
    clone_cmd = f"git clone --depth 1 --filter=blob:none https://github.com/{user}/{repo}.git /tmp/{repo} 2>/dev/null || true"
    subprocess.run(clone_cmd, shell=True)
    # Считаем коммиты автора за последние 7 дней
    count_cmd = f"git -C /tmp/{repo} rev-list --count --author='{user}' --since='7 days ago' HEAD 2>/dev/null || echo 0"
    count = int(subprocess.check_output(count_cmd, shell=True, text=True).strip())
    total_weekly += count
    # Удаляем клон, чтобы не захламлять
    subprocess.run(f"rm -rf /tmp/{repo}", shell=True)

# Определяем состояние питомца
if total_weekly == 0:
    stage = "💀 Голодная смерть"
    ascii_art = r"""
     .-.
    (x.x)
     |=|
    /|_|\
    """
elif total_weekly < 5:
    stage = "😵 Ослаблен"
    ascii_art = r"""
     .-.
    (o.o)
     |=|
    /|_|\
    """
elif total_weekly < 15:
    stage = "😐 В норме"
    ascii_art = r"""
     .-.
    (^_^)
     |=|
    /|_|\
    """
else:
    stage = "⚡ Энергичный зверь"
    ascii_art = r"""
     .-.
    (>_<)
     |=|
    /|_|\
    """

# Общее число коммитов за всё время (опционально) — можно тоже посчитать, но оставим для красоты
total_all = subprocess.check_output(
    f"gh api users/{user}/events --jq '[.[] | select(.type==\"PushEvent\")] | length'",
    shell=True, text=True
).strip()
if not total_all:
    total_all = "?"

# Генерируем SVG
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="340">
  <rect width="100%" height="100%" fill="#0d1117" rx="10"/>
  <text x="20" y="40" font-family="Courier New, monospace" fill="#58a6ff" font-size="18">
    📅 Коммитов за неделю (все репозитории): {total_weekly}
  </text>
  <text x="20" y="80" font-family="Courier New, monospace" fill="#f0883e" font-size="18">
    🏆 Всего коммитов (приблизительно): {total_all}
  </text>
  <text x="20" y="120" font-family="Courier New, monospace" fill="#c9d1d9" font-size="16">
    Статус: {stage}
  </text>
  <text x="20" y="190" font-family="Courier New, monospace" fill="#c9d1d9" font-size="14" xml:space="preserve">
{ascii_art}
  </text>
</svg>'''

with open('pet.svg', 'w') as f:
    f.write(svg_content)

print(f"✅ Питомец обновлён! Недельных коммитов: {total_weekly}")