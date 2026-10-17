# BizCFO — Django-first Virtual CFO platform

A Django server-rendered starter application for client organization management, basic double-entry journal drafts/posting, invoice registers, compliance tasks, banking data models, reporting snapshots, client portal screens, practice tasks and document metadata. Includes fictional demo records and responsive UI.

> **Important:** This is a functional MVP scaffold, not a certified or production-ready accounting product. Do not use it for live client books, tax filing or sensitive financial documents until the security, accounting, tenancy, upload and deployment checklist below is completed. Several screens are read-only foundations, not fully implemented workflows.

## Stack
- Python 3.12+
- Django 5.1/5.2
- SQLite for local evaluation; PostgreSQL through `DATABASE_URL` for deployment
- Django Templates, custom CSS and lightweight JavaScript
- Gunicorn + WhiteNoise for containerized serving

Django Ledger is **not installed in this starter**. Integrate it only after a license review and compatibility/accounting tests. The included ledger models are a minimal application-owned demonstration ledger, not a substitute for a mature accounting engine.

## Local setup (Windows CMD)
```bat
cd BizCFO
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
copy .env.example .env
python manage.py makemigrations organizations accounting sales banking compliance practice documents audit
python manage.py migrate
python manage.py seed_demo
python manage.py check
python manage.py runserver
```
Open `http://127.0.0.1:8000/`.

## Local setup (PowerShell)
```powershell
cd BizCFO
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
Copy-Item .env.example .env
python manage.py makemigrations organizations accounting sales banking compliance practice documents audit
python manage.py migrate
python manage.py seed_demo
python manage.py check
python manage.py runserver
```

## Demo logins
| Role | Username | Password |
|---|---|---|
| Demo platform admin | `demo-admin` | `DemoAdmin-ChangeMe123!` |
| Demo business owner | `demo-owner` | `DemoOwner-ChangeMe123!` |
| Demo accountant | `demo-accountant` | `DemoAccountant-ChangeMe123!` |

These credentials are intentionally public for local demo only. **Never deploy with these accounts/passwords.** Delete demo users and seed data before any real deployment, and create individual named accounts with strong unique passwords.

## Docker Compose
1. Copy `.env.example` to `.env`.
2. Set a strong `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS` and secure cookie/HTTPS settings in `.env`.
3. Set a strong `POSTGRES_PASSWORD` in your shell or compose environment.
4. Run:
```bash
docker compose up --build
```
The compose command migrates and seeds demo data for evaluation. Remove `seed_demo` from the startup command for a real environment. Configure TLS at a trusted reverse proxy/load balancer and confirm health checks, backups and restoration.

## Main screens
- Overview dashboard
- Organizations
- Accounting / chart of accounts / journal register / journal draft form / post action
- Sales and invoices
- Banking and transaction register
- Compliance calendar
- Financial report snapshot
- Client portal
- Practice task queue
- Document register
- Django admin

## Database / model notes
- `Organization` and `Membership` provide the tenant membership foundation.
- `Account`, `JournalEntry`, `JournalLine` store simple accounting demo data.
- `Customer`, `Invoice`, `InvoiceLine` store invoice register data.
- `BankAccount`, `BankTransaction` are banking/reconciliation foundations.
- `ComplianceTask`, `WorkTask`, `Document`, `AuditEvent` provide supporting workflows.
- All demo records are fictional and use obviously fake tax identifiers.

## Test and quality commands
```bash
python manage.py check
python manage.py test
pytest
```

## Required before production
1. **Accounting correctness:** implement immutable posted journals at the database/service layer; safe reversal workflows; period controls; currency/rounding policy; tax logic; opening-balance controls; validated P&L, balance sheet and cash flow; comprehensive property-based accounting tests.
2. **Tenant isolation:** test every view, object lookup, admin action, background task, document download and export using two unrelated organizations. Add object-level permissions and deny-by-default access. The current membership filtering is a foundation only.
3. **Permissions:** define granular role permissions, enforce server-side on each action, protect admin and exports, add MFA for privileged accounts, login throttling and session revocation.
4. **Documents:** implement private object storage and permission-checked streaming downloads. Never expose `MEDIA_ROOT` publicly. Add file-type and content validation, malware scanning, size limits and retention policies.
5. **Banking and compliance:** implement tested CSV parsing, duplicate detection, reconciliation locking, evidence retention and authorized filing integrations. Do not infer that a statutory filing is complete from an internal task status alone.
6. **Security:** rotate secrets, set DEBUG=False, configure HTTPS, secure cookies, trusted hosts/origins, database least privilege, dependency scanning, logging and alerting.
7. **Operations:** managed PostgreSQL, encrypted backups, tested restore drills, monitoring, error reporting, migrations strategy, incident response and a documented recovery objective.
8. **Privacy/legal:** retention and deletion policy, data processing agreements, consent and access logs as applicable. Review accounting/tax professional obligations and all third-party licenses.
9. **Deployment review:** run `python manage.py check --deploy`, test migrations against a production-like database, and commission an independent security review.

## Known limitations
- No GST portal or MCA live integration.
- No production invoice PDF, payment gateway, email delivery, CSV bank import or automated reconciliation.
- The reports page is a management snapshot, not a statutory financial statement.
- Client portal is a read-only foundation; approvals and client document upload are not implemented.
- The simple ledger is not yet integrated with Django Ledger and should not be relied on for statutory accounting.
- The document screen is metadata-only; private downloads are not implemented.
- `seed_demo` is for local demo environments only.
