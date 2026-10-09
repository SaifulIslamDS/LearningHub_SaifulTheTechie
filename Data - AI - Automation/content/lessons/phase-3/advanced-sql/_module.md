Phase 1 taught SQL for answering business questions. **Advanced SQL** is the SQL data engineers and analytics engineers write every day: multi-step queries with **CTEs**, **recursive** queries for calendars and hierarchies, and **window functions** for running totals, rankings and period-over-period growth, all without leaving the database.

!!! tip "Setup: PostgreSQL + the practice data"
    From this module on, examples run on **PostgreSQL**, the most popular open-source database. The easiest way to get it is Docker (see the Docker module):

    ```bash
    docker run --name pg -e POSTGRES_PASSWORD=practice -p 5432:5432 -d postgres:18
    ```

    Or install it from <https://www.postgresql.org/download/> (Windows/Mac installers include pgAdmin). Then, in the unzipped [data-engineering-scripts.zip](../../../downloads/phase-3/data-engineering-scripts.zip) folder:

    ```bash
    uv add "psycopg[binary]"
    export DATABASE_URL=postgresql://postgres:practice@localhost:5432/postgres   # PowerShell: $env:DATABASE_URL="..."
    uv run 03_load_postgres.py                     # loads the 2025 orders into the shop schema
    psql "$DATABASE_URL" -f 04_ctes.sql             # or open the .sql file in DBeaver, pgAdmin or VS Code
    ```

    *The outputs in these lessons come from PostgreSQL 16; everything shown works the same on 16, 17 and 18.*

**By the end of this module you can:** structure long queries with CTEs, generate calendars and walk hierarchies with recursive CTEs, and use window functions (`OVER`, `PARTITION BY`, `RANK`, `LAG`, `LEAD`, frames) for rankings, running totals and growth rates.
