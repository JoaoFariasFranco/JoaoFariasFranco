#!/usr/bin/env python3
"""
Extrai contribuições diárias do GitHub usando a API GraphQL.
Requer um token de acesso (PAT ou GITHUB_TOKEN).
"""
import datetime
import json
import os
import sys
import requests

USERNAME = os.environ.get("GH_PROFILE_USER", "JoaoFariasFranco")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_PAT")

if not TOKEN:
    print("❌ Token não encontrado. Defina a variável GITHUB_TOKEN ou GH_PAT.", file=sys.stderr)
    sys.exit(1)

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")
GRAPHQL_URL = "https://api.github.com/graphql"

QUERY = """
query($username: String!) {
  user(login: $username) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
  }
}
"""

def fetch_days():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Python-GitHub-Contribution-Scraper"
    }
    variables = {"username": USERNAME}

    print(f"🔍 Consultando API GraphQL para {USERNAME}")
    resp = requests.post(GRAPHQL_URL, json={"query": QUERY, "variables": variables}, headers=headers, timeout=30)
    
    if resp.status_code != 200:
        print(f"❌ Erro na API: {resp.status_code}", file=sys.stderr)
        print(resp.text, file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    if "errors" in data:
        print("❌ Erro GraphQL:", file=sys.stderr)
        for err in data["errors"]:
            message = err.get("message", "unknown error")
            print(f"   - {message}", file=sys.stderr)
            if "resource is not accessible by integration" in message.lower() or "read:user" in message.lower():
                print("   → O token provavelmente não tem permissão read:user ou o perfil é privado.", file=sys.stderr)
                print("   → Configure um segredo GH_PAT com permissão read:user no repositório.", file=sys.stderr)
        sys.exit(1)

    calendar = data.get("data", {}).get("user", {}).get("contributionsCollection", {}).get("contributionCalendar", {})
    weeks = calendar.get("weeks", [])
    
    days = []
    for week in weeks:
        for day in week.get("contributionDays", []):
            days.append({
                "date": day["date"],
                "count": day["contributionCount"]
            })
    
    # Ordena e filtra (já vem ordenado, mas por segurança)
    days.sort(key=lambda d: d["date"])
    return days


def compute_current_streak(days):
    if not days:
        return 0, None, None
    idx = len(days) - 1
    if days[idx]["count"] == 0:
        idx -= 1
    streak = 0
    end_idx = idx
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1
    start_idx = idx + 1
    if streak == 0:
        return 0, None, None
    return streak, days[start_idx]["date"], days[end_idx]["date"]


def compute_longest_streak(days):
    longest = run = 0
    longest_start = longest_end = None
    run_start_idx = None
    for i, d in enumerate(days):
        if d["count"] > 0:
            if run == 0:
                run_start_idx = i
            run += 1
            if run > longest:
                longest = run
                longest_start = days[run_start_idx]["date"]
                longest_end = days[i]["date"]
        else:
            run = 0
    return longest, longest_start, longest_end


def build_data(days):
    total = sum(d["count"] for d in days)
    active_days = sum(1 for d in days if d["count"] > 0)
    best = max(days, key=lambda d: d["count"]) if days else {"date": None, "count": 0}
    cur_len, cur_start, cur_end = compute_current_streak(days)
    long_len, long_start, long_end = compute_longest_streak(days)

    monthly = {}
    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["count"]
    monthly_list = [{"month": k, "total": v} for k, v in sorted(monthly.items())]

    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active_days,
        "avg_per_active_day": round(total / active_days, 1) if active_days else 0,
        "current_streak": {"length": cur_len, "start": cur_start, "end": cur_end},
        "longest_streak": {"length": long_len, "start": long_start, "end": long_end},
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": monthly_list,
        "days": days,
    }


if __name__ == "__main__":
    print(f"🎯 GitHub Contribution Scraper (GraphQL)")
    print(f"👤 Usuário: {USERNAME}")
    print("-" * 50)

    try:
        days = fetch_days()
        print(f"📊 Total de contribuições extraídas: {sum(d['count'] for d in days)}")
        print("📅 Últimos 7 dias:")
        for d in days[-7:]:
            bar = "█" * min(d["count"], 20) if d["count"] > 0 else "·"
            print(f"  {d['date']}: {d['count']:2d} {bar}")

        data = build_data(days)
        os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
        with open(OUT_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Dados salvos em: {OUT_PATH}")
        print(f"📊 Total de contribuições: {data['total_contributions']}")
        print(f"📈 Dias ativos: {data['active_days']}")
        print(f"🔥 Streak atual: {data['current_streak']['length']} dias")
        print(f"💪 Maior streak: {data['longest_streak']['length']} dias")
        print(f"⭐ Melhor dia: {data['best_day']['date']} ({data['best_day']['count']} contribuições)")

    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)