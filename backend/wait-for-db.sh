#!/bin/sh


    set -e

    host="$1"
    shift
    cmd="$@"


    db_user="${POSTGRES_USER:-user}"
    db_name="${POSTGRES_DB:-hackdb}"

    # wait for the database to be ready
    until PGPASSWORD=$POSTGRES_PASSWORD pg_isready -h "$host" -p "5432" -U "$db_user" -d "$db_name" -q; do
      >&2 echo "Postgres is unavailable - sleeping"
      sleep 1
    done

    >&2 echo "Postgres is up - executing command"
    exec $cmd
    