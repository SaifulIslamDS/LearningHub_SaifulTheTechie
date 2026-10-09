#!/usr/bin/env bash
# Run the CSV cleaner every day and keep a log. Used in the cron lesson.
set -euo pipefail                      # stop on errors, unset variables and failed pipes

cd "$HOME/practice"                    # always start from a known folder
echo "$(date '+%F %T') starting daily clean" >> logs/cron.log
uv run --project "$HOME/csv-cleaner" csv-clean data/orders_raw.csv \
    -c "$HOME/csv-cleaner/config.toml" \
    -o "reports/orders_$(date +%F).csv" >> logs/cron.log 2>&1
