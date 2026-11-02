# Volt Vortex — Appliances Scheduler

A Flask web app that helps households see what their appliances cost to run and shift heavy loads to cheaper off-peak hours.

You add the appliances you own from a built-in catalog, say how long you use them, and the app estimates their energy use and cost. It can then:

- **optimize**: pick which appliances to keep running under a daily energy cap
- **schedule**: find the cheapest hours to run each appliance inside the time window you're free

## Demo

![Volt Vortex walkthrough: login, dashboard, appliances, optimization, scheduling and analytics](docs/demo.gif)

*Walkthrough: log in → dashboard → edit an appliance → optimize under a 30 kWh cap → generate a schedule → analytics.*

## Screenshots

| Dashboard | Smart scheduling |
|---|---|
| ![Dashboard with monthly stats, today's schedule timeline and biggest energy users](docs/screenshots/dashboard.png) | ![Smart scheduling with appliance picker, time window and generated schedule](docs/screenshots/scheduling.png) |
| **Appliances** | **Edit an appliance** |
| ![Appliance list with on/off switches, load levels and daily cost](docs/screenshots/appliances.png) | ![Edit appliance dialog with usage controls and live cost preview](docs/screenshots/appliance-edit.png) |
| **Optimization** | **Analytics** |
| ![Optimized plan under a daily energy cap with estimated savings](docs/screenshots/optimization.png) | ![Analytics charts for usage by appliance, usage over time and savings](docs/screenshots/analytics.png) |
| **Login** | **Settings** |
| ![Login page with photo slideshow and electricity rates](docs/screenshots/login.png) | ![Settings page for profile, password and session](docs/screenshots/settings.png) |

<details>
<summary><strong>Mobile</strong></summary>

<p>
<img src="docs/screenshots/mobile-dashboard.png" width="300" alt="Dashboard on a phone">
&nbsp;&nbsp;
<img src="docs/screenshots/mobile-scheduling.png" width="300" alt="Smart scheduling on a phone">
</p>

</details>

## Features

| Page | What it does |
|---|---|
| **Login / Register** | Account creation and sign-in, with a photo slideshow and the current electricity rates. |
| **Dashboard** | Energy and cost for this month; savings from your saved schedule; today's schedule as a 24-hour timeline with a "now" marker; live peak/off-peak rate chip; on/off switches for your biggest energy users; a tip based on your own appliances; a getting-started checklist for new accounts. |
| **Appliances** | Add appliances from the catalog, edit nickname and usage (hours/day, days/week, weeks/month), switch them on or off, delete them. Energy, cost and load level (Light / Medium / Severe) are recalculated automatically. |
| **Optimization** | Enter a daily kWh cap; a knapsack algorithm keeps the most important appliances within it. Save the result as your optimized plan. |
| **Scheduling** | Choose your saved optimized plan or pick appliances, set the hours you're available, and generate the cheapest run time for each appliance (Dijkstra-style search over hourly rates). Save the schedule to show it on the dashboard. |
| **Analytics** | Usage charts. **Currently uses sample data**, labelled as such on the page. |
| **Settings** | Update your name and email (changing email needs your password), change your password, log out. |

Only appliances that are **switched on** count toward the dashboard totals and can be scheduled.

## Electricity rates

All rates live in one place, [`app/rates.py`](app/rates.py). Every page reads from it.

| Period | Hours | Rate |
|---|---|---|
| Peak | 8 AM – 9 PM | ₱7.48 / kWh |
| Off-peak | 9 PM – 8 AM | ₱3.55 / kWh |

- Cost estimates for usage that isn't scheduled assume the peak rate.
- "Saved by scheduling" compares a saved schedule against running the same hours at peak.
- The dashboard warns when your switched-on appliances add up to more than `DAILY_LIMIT_KWH` (35 kWh) a day.

## Tech stack

- **Backend:** Python 3.11, Flask 3, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-WTF (CSRF protection)
- **Database:** SQLite by default; MySQL through PyMySQL
- **Frontend:** Jinja2 templates with plain CSS (`app/static/theme.css` holds the design tokens and shared components). Chart.js is used on Analytics. Fonts are Manrope for the interface and Syne for the VOLT VORTEX wordmark (Google Fonts).

## Getting started

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd Appliances-Scheduler
python -m venv venv
```

Activate it:

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure `.env`

Create a `.env` file in the project root:

```env
# SQLite (stored in instance/app.db)
MYSQL_PATH=sqlite:///app.db
# or MySQL:
# MYSQL_PATH=mysql+pymysql://user:password@localhost/volt_vortex

SECRET_KEY=change-me-to-a-long-random-string
```

`SECRET_KEY` signs sessions and CSRF tokens. Use a long random value and never commit it.

### 4. Run

```bash
python run.py
```

Open <http://127.0.0.1:5001>.

On startup the app creates any missing tables and adds newer columns (such as `scheduled_appliances.selected_type`) to an existing database. No manual migration is needed.

## Project structure

```
Appliances-Scheduler/
├── run.py                     # entry point: creates tables, starts the dev server on :5001
├── database/config.py         # reads MYSQL_PATH and SECRET_KEY from .env
├── instance/app.db            # SQLite database (created on first run)
├── docs/                      # demo.gif and screenshots/ used in this README
└── app/
    ├── __init__.py            # app factory, login manager, CSRF, blueprints
    ├── models.py              # User, Appliances, OptimizedAppliances, ScheduledApplianceUsage
    ├── rates.py               # electricity rates and peak hours (single source of truth)
    ├── appliances_utils.py    # appliance catalog (types, capacities, wattages)
    ├── routes/
    │   ├── login_routes.py        # /, /register, /logout, /settings
    │   ├── home_routes.py         # /dashboard
    │   ├── appliances_routes.py   # /appliances/ (add, edit, toggle, delete)
    │   ├── optimization_routes.py # /optimize
    │   ├── daily_scheduler_routes.py # /scheduling
    │   └── analytics_routes.py    # /analytics
    ├── templates/             # base.html layout, _icons.html, _auth.html, one template per page
    └── static/                # theme.css + per-page CSS, auth/ slideshow photos
```

## Security

- **CSRF:** every form and `fetch` request carries a CSRF token (Flask-WTF).
- **Passwords:** hashed with bcrypt.
- **Sessions:**
  - Session cookies are `HttpOnly` and `SameSite=Lax`.
  - Each session is tied to a fingerprint of the password hash, so changing your password logs out every other device.
- **Data access:** each user can only read or change their own appliances and schedules.

## Known limitations

- Analytics shows sample figures; it isn't connected to your appliance data yet.
- Appliances store how many days a week they're used, not which days.
- Each saved schedule is kept. The dashboard shows the most recent one.

## Credits

Login and register photos are from [Unsplash](https://unsplash.com) and used under the Unsplash License.
