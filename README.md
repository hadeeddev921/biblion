# Biblion

Biblion is an open source integrated library system (ILS) for heritage, public and school libraries and their networks, built on the Invenio framework.

## What This Project Does

Running a library network means keeping one shared catalogue, many libraries with their own rules, and thousands of patrons and loans in sync. Biblion is the backend that does that: it stores the bibliographic records, holdings and items of every library in a network, runs circulation and acquisitions, and exposes everything through a REST API and a public catalogue. It is meant for library networks (consortia) and for single libraries that need a full, multilingual ILS.

Main features:

- **Multi-organisation catalogue**: organisations, libraries and locations share one catalogue, with a global view and one view per organisation.
- **Cataloguing**: documents, holdings (including serial patterns and issues), items, local fields, collections and templates, validated with JSON Schemas.
- **Imports and conversion**: MARC21, UNIMARC and MARCXML converters (DNB, KUL, LoC, SLSP, UGent, BnF and others), external import services, Dublin Core and MARC21 export.
- **Authority entities**: links documents to persons, organisations, subjects and places from a MEF authority server, plus locally catalogued entities.
- **Circulation**: requests, checkouts, renewals, transits and returns, driven by circulation policies, item types and patron types, with library opening hours and exceptions.
- **Patrons**: patron accounts, subscriptions, fees and payments (patron transactions), and a public patron profile.
- **Notifications**: availability, due-soon, overdue, recall and transit notifications by email, with per-library templates.
- **Acquisitions**: vendors, budgets, accounts, orders, order lines and receipts.
- **Interlibrary loan (ILL)** requests from the public interface.
- **Statistics**: billing, librarian and configurable report statistics.
- **Interoperability**: SRU search, OAI-PMH server, OAuth2 tokens, a SIP2 self-check interface and API harvesting of e-books.
- **Operations**: operation logs, record deduplication, data migration tools, monitoring endpoints and scheduled tasks.
- **Translations**: English, French, German, Italian, Spanish and Dutch.

## How It Works

Biblion is an Invenio instance. Each resource (document, item, loan, patron, …) is a module with the same building blocks: a JSON Schema, an Elasticsearch mapping, a record API class, permissions, serializers and REST/UI views. Records are stored as JSON in PostgreSQL and indexed in Elasticsearch, which serves every search. Long or periodic work (indexing, notifications, harvesting, statistics) runs in Celery workers through RabbitMQ, with Redis as cache and session store.

The professional interface and the public search pages are an Angular application (the `@rero/rero-ils-ui` npm package) that `scripts/bootstrap` installs into the static folder. It talks to the REST API; Jinja templates in this repository render the page shells, the public detail views and the patron pages.

```mermaid
flowchart LR
    U[Browser / Angular UI] -->|HTTPS| V[Flask views & REST endpoints]
    V --> P[Permissions & policies]
    P --> A[Record API classes<br/>documents, items, loans …]
    A -->|JSON records| DB[(PostgreSQL)]
    A -->|index| ES[(Elasticsearch)]
    V -->|search| ES
    A -->|tasks| MQ[[RabbitMQ]]
    MQ --> W[Celery worker & beat<br/>notifications, indexing, harvesting]
    W --> DB
    W --> ES
    V <--> R[(Redis<br/>cache & sessions)]
    A -->|authorities| MEF[MEF server]
```

A typical request, for example a checkout from the professional interface, goes: Angular UI → `POST /api/item/checkout` → item view → permission check against the circulation policy → `Item`/`Loan` API (Invenio Circulation state machine) → PostgreSQL commit → Elasticsearch reindex → Celery task that sends the notification.

## Project Structure

```
biblion/
├── biblion/                     # The Python package
│   ├── config.py                # All Invenio and Biblion settings (BIBLION_* keys)
│   ├── modules/                 # One sub-package per resource
│   │   ├── documents/           # Bibliographic records, MARC/UNIMARC/DC converters
│   │   ├── holdings/  items/    # Holdings, serial patterns and physical items
│   │   ├── loans/  circ_policies/  item_types/  patron_types/   # Circulation
│   │   ├── patrons/  patron_transactions/  patron_transaction_events/
│   │   ├── organisations/  libraries/  locations/   # Network structure
│   │   ├── acquisition/  vendors/   # Orders, budgets, receipts
│   │   ├── entities/            # Remote (MEF) and local authority entities
│   │   ├── ill_requests/  notifications/  collections/  templates/
│   │   ├── stats/  stats_cfg/   # Statistics and configurable reports
│   │   ├── sru/  imports/  api_harvester/  selfcheck/   # Interoperability
│   │   ├── operation_logs/  migrations/  deduplications/  monitoring/
│   │   └── cli/                 # `invenio biblion …` management commands
│   ├── dojson/                  # Shared DoJSON (MARC) conversion helpers
│   ├── jsonschemas/  es_templates/   # Common schemas and search templates
│   ├── theme/                   # Jinja templates, SCSS/JS assets, menus, theme views
│   ├── translations/            # gettext catalogues (de, en, es, fr, it, nl)
│   ├── alembic/                 # Database migrations
│   └── oauth/                   # OAuth2 scopes
├── data/                        # Demo fixtures loaded by scripts/setup, help wiki pages
├── tests/                       # unit, api, ui, e2e (Playwright) and scheduler tests
├── scripts/                     # bootstrap, setup, server, test, gen-certs, update …
├── docker/                      # Dockerfiles/config for Elasticsearch, nginx, haproxy, uwsgi
├── docker-compose.yml           # Development services (PostgreSQL, Redis, RabbitMQ, ES)
├── docker-compose.full.yml      # Full stack example (web UI, API, worker, beat, lb)
├── Dockerfile.base  Dockerfile  # Base image and application image
├── pyproject.toml  uv.lock      # Dependencies, entry points and poe tasks
└── .env.example                 # Environment variables template
```

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.14 | Backend code (`requires-python >=3.14,<3.15`) |
| Framework | Invenio (invenio-app ≥ 3.0, invenio-records ≥ 4.0, invenio-records-rest ≥ 6.0.2) on Flask | Records, REST API, accounts, OAI-PMH, assets |
| Circulation | invenio-circulation ≥ 4.0 | Loan state machine |
| Database | PostgreSQL 17 (SQLAlchemy, Alembic) | Record storage |
| Search | Elasticsearch OSS 7.10.2 with ICU (invenio-search[elasticsearch7] ≥ 3.0) | Search and facets |
| Tasks | Celery (invenio-celery ≥ 2.0.2), RabbitMQ 4.2, sqlalchemy-celery-beat ≥ 0.8.3 | Background and scheduled jobs |
| Cache | Redis | Cache, sessions, rate limiting |
| Conversion | DoJSON ≥ 1.4, dcxml, isbnlib | MARC21/UNIMARC/Dublin Core conversion |
| Frontend | Jinja2, Bootstrap-Flask ≥ 2.5, Angular UI (`@rero/rero-ils-ui` 21.3.1, Node 24) | Public and professional interfaces |
| Auth | invenio-accounts ≥ 6.0, invenio-oauth2server ≥ 6.1, invenio-oauthclient ≥ 5.0 | Login, API tokens |
| Self-check | invenio-sip2 ≥ 0.6.25 | SIP2 self-check machines |
| Testing | pytest-invenio ≥ 3.0, pytest-playwright ≥ 0.8, freezegun, ruff ≥ 0.12.8 | Unit/API/UI/E2E tests and linting |
| Tooling | uv, poethepoet | Dependency management and task runner |
| Deployment | Docker, uWSGI ≥ 2.0.30, nginx, haproxy | Container images and serving |

## How to Run This Project

1. **Prerequisites**
   - Python 3.14 and [uv](https://docs.astral.sh/uv/)
   - Node.js 24 and npm (to install the Angular UI)
   - Docker with Docker Compose (PostgreSQL 17, Elasticsearch 7.10.2, Redis, RabbitMQ)
   - `openssl` (for the development TLS certificate)

2. **Clone**
   ```bash
   git clone https://github.com/hadeeddev921/biblion.git
   cd biblion
   ```

3. **Install dependencies and build the assets**
   ```bash
   ./scripts/bootstrap
   ```
   This runs `uv sync --frozen`, installs the Angular UI into the static folder, collects and builds the web assets with webpack, compiles the translations, generates a self-signed certificate in `.certs/` and installs the Playwright browsers used by the E2E tests.

4. **Environment variables**
   ```bash
   cp .env.example .env
   ```
   | Variable | Description | Example |
   |---|---|---|
   | `INVENIO_SECRET_KEY` | Flask secret key | `change-me-to-a-long-random-string` |
   | `INVENIO_SQLALCHEMY_DATABASE_URI` | PostgreSQL connection | `postgresql+psycopg2://biblion:biblion@localhost/biblion` |
   | `INVENIO_SEARCH_ELASTIC_HOSTS` | Elasticsearch hosts | `['localhost:9200']` |
   | `INVENIO_CACHE_TYPE` / `INVENIO_CACHE_REDIS_URL` | Cache backend | `redis` / `redis://localhost:6379/0` |
   | `INVENIO_ACCOUNTS_SESSION_REDIS_URL` | Session store | `redis://localhost:6379/1` |
   | `INVENIO_CELERY_RESULT_BACKEND` | Celery results | `redis://localhost:6379/2` |
   | `INVENIO_RATELIMIT_STORAGE_URI` | Rate limit storage | `redis://localhost:6379/3` |
   | `INVENIO_BROKER_URL` / `INVENIO_CELERY_BROKER_URL` | RabbitMQ broker | `amqp://guest:guest@localhost:5672/` |
   | `BIBLION_MEF_REF_BASE_URL` | MEF authority server host | `mef.rero.ch` |
   | `INVENIO_BIBLION_FILES_FOLDER` | Where the setup stores document files | `data/files` |
   | `INVENIO_BIBLION_ACCESS_TOKEN_*` | Optional fixed API tokens created by the setup | *(empty)* |

   Any other setting in `biblion/config.py` can be overridden the same way with an `INVENIO_` prefix.

5. **Start the services**
   ```bash
   docker compose up -d
   ```

6. **Database, indices and demo data**
   ```bash
   uv run poe setup
   ```
   `scripts/setup` creates the database and the search indices and loads the demo fixtures from `data/` (organisations, libraries, users, documents, items, circulation, acquisitions). Use `./scripts/setup --e2e` for the minimal data set used by the end-to-end tests. The demo accounts in `data/users.json` use the password `Pw123456` (for example `biblion.demo@example.com`).

7. **Run**
   ```bash
   uv run poe server
   ```
   This starts the Flask server over HTTPS together with a Celery worker and beat scheduler. Open <https://localhost:5000> (accept the self-signed certificate). Use `./scripts/server --no-worker` to start the web server alone.

8. **Run tests**
   ```bash
   uv run poe run_tests   # pip-audit, JSON and license checks, ruff, then pytest
   uv run poe tests       # pytest only
   uv run poe e2e         # Playwright E2E tests against a running instance
   ```
   The test suite needs the services from step 5. Code style is checked with `uv run poe lint` and `uv run poe format`.

9. **Docker (full stack)**
   ```bash
   docker build -t biblion-base -f Dockerfile.base .
   docker compose -f docker-compose.full.yml up -d --build
   ```
   This builds the application image on top of `biblion-base` and starts the web UI, REST API, Celery worker and beat, nginx, haproxy and the backing services.

## License

Biblion is released under the GNU Affero General Public License v3.0 or later. See [LICENSE](LICENSE).
