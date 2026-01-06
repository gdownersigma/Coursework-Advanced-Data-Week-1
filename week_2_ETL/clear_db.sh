#!/bin/bash

#grep -v '^#' — ignores comment lines starting with #
#xargs — converts each line into a format bash can use
#export $(...) — makes those variables available to the script

export $(grep -v '^#' .env | xargs)

PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "TRUNCATE review, incident RESTART IDENTITY;"

echo "Database reset complete"
