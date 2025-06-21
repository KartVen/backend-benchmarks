#!/bin/bash

#LOG_DIR=/mnt/HC_Volume_102802706/spec/logs
LOG_DIR=/media/kartven/Backup\ Drive/spec/logs
POSITIONAL=()

COUNT_MODE=false
COUNT_ONLY_MODE=false
MODE=""
USAGE="check [steps|logs] [<endpoint>] [--count] [--count-only]"

help() {
  cat <<EOF
Usage:
  $USAGE

  --count           show number of error/warn lines per log file
  --count-only      show only number of error/warn lines per log file

Log files: $LOG_DIR/screenlog.*.<lang>.<endpoint>.0*
EOF
  exit 0
}

show_steps() {
  FOUND=$(grep -E '^\s*(script:|output:)' "$1" | tail -n 2)
  if [ -z "$FOUND" ]; then
    echo "Not found lines"
  else
    echo "$FOUND"
  fi
}

show_errors() {
  FOUND=$(grep -Ei 'error|warn' "$1" \
    | grep -vEi '0 errors|0 warnings|^\s*script:|^\s*output:')

  if [ -z "$FOUND" ]; then
    COUNT=0
  else
    COUNT=$(echo "$FOUND" | grep -c '^')
  fi

  if [ "$COUNT_ONLY_MODE" = true ]; then
    echo "[count: $COUNT]"
    return
  fi

  if [ -z "$FOUND" ]; then
    echo "No errors or warnings"
  else
    CLEANED=$(echo "$FOUND" \
      | sed -r 's/\x1B\[[0-9;]*[A-HJKf]//g' \
      | sed -E 's/WARN/\x1B[31mWARN\x1B[0m/g')
    echo "$CLEANED"
    $COUNT_MODE && echo "[count: $COUNT]"
  fi
}

show_logs() {
  for LOGFILE in "$LOG_DIR"/screenlog.*.*.0; do
    BASENAME=$(basename "$LOGFILE")
    LANG=$(echo "$BASENAME" | cut -d '.' -f 3)

    [ -f "$LOGFILE" ] && echo "$BASENAME"
  done
}

[[ "$1" == "--help" || "$1" == "-h" ]] && help

case "$1" in
  steps)
    MODE="steps"
    shift
    ;;
  logs)
    MODE="logs"
    shift
    ;;
  *)
    MODE="errors"
esac

while [[ $# -gt 0 ]]; do
  case "$1" in
    --count) COUNT_MODE=true; shift ;;
    --count-only) COUNT_ONLY_MODE=true; shift ;;
    -*)
      echo "Unknown option: $1"
      echo "Usage: $USAGE"
      exit 1
      ;;
    *) POSITIONAL+=("$1"); shift ;;
  esac
done

if [ "$MODE" == "logs" ]; then
  show_logs
  exit 0
else
  ENDPOINT="${POSITIONAL[0]}"
  if [ -z "$ENDPOINT" ]; then
    echo "Missing endpoint."
    echo "Usage: $USAGE"
    exit 1
  fi
fi

for LOGFILE in "$LOG_DIR"/screenlog.*."$ENDPOINT".0*; do
  BASENAME=$(basename "$LOGFILE")
  LANG=$(echo "$BASENAME" | cut -d '.' -f 3)

  [ ! -f "$LOGFILE" ] && {
    echo "Log file not found: $LOGFILE"
    continue
  }

  echo ">> $LOGFILE"
  case "$MODE" in
    steps) show_steps "$LOGFILE" ;;
    *)     show_errors "$LOGFILE" ;;
  esac
  echo
done
