# ereceipt-network

A receipt inbox for Kenyan small businesses and their accountants. Staff send eTIMS
receipts by WhatsApp or a web page, we read the QR code, check the invoice against
KRA's public verification, flag anything invalid or missing the buyer's PIN, and the
owner or accountant downloads a monthly spreadsheet of valid expenses for filing.

Why it matters: since 1 January 2026, an expense without a valid eTIMS invoice can't
be deducted. A lost or invalid receipt costs the business real money.

This is v1 of a larger receipt routing network. See [docs/ROADMAP.md](docs/ROADMAP.md)
for the build steps and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the stack and
why each piece was chosen.

## Run it locally

You need [uv](https://docs.astral.sh/uv/) and Docker (for Postgres).

```bash
git clone git@github.com:rickymwethera/ereceipt-network.git
cd ereceipt-network
make setup        # installs Python 3.13 deps, creates .env from .env.example
make db           # starts Postgres in Docker
make migrate
uv run python manage.py createsuperuser
make run          # http://localhost:8000/admin
```

No Docker? Set `DATABASE_URL=sqlite:///db.sqlite3` in `.env` to get going, but switch
back to Postgres before you rely on anything (CI runs on Postgres).

Edit `.env` and set a real `SECRET_KEY`:

```bash
uv run python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

## Everyday commands

| Command     | What it does                          |
|-------------|---------------------------------------|
| `make test` | run the test suite (pytest)           |
| `make lint` | ruff lint + format check (same as CI) |
| `make fmt`  | auto-fix lint and formatting          |

## Layout

```
config/          Django settings and URLs
apps/accounts/   users, businesses, staff and accountant access
apps/receipts/   the Receipt model, statuses, monthly list
apps/intake/     WhatsApp webhook, web upload, QR decoding
apps/kra/        KRA eTIMS invoice verification (all KRA-specific code lives here)
apps/exports/    monthly xlsx/CSV export
apps/billing/    subscriptions and M-Pesa payments
templates/       shared templates
docs/            architecture, roadmap
```

## How we work

See [CONTRIBUTING.md](CONTRIBUTING.md): one branch and one pull request per roadmap
issue, CI must pass, and every PR gets a review before merge.
