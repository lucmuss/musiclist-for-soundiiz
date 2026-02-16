#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

print_usage() {
    cat <<'EOF'
Usage:
  ./scripts/bootstrap.sh run [CLI_ARGS...]
  ./scripts/bootstrap.sh env
  ./scripts/bootstrap.sh help

Commands:
  run   Load environment and run the CLI entrypoint (default command).
  env   Load environment and print bootstrap/runtime info.
  help  Show this help.
EOF
}

log_debug() {
    local debug_flag="${BOOTSTRAP_DEBUG:-false}"
    case "${debug_flag,,}" in
        "1"|"true"|"yes"|"on")
            echo "[bootstrap] $*"
            ;;
        *)
            ;;
    esac
}

load_env() {
    local env_file="$REPO_ROOT/.env"
    if [[ -f "$env_file" ]]; then
        log_debug "Lade Umgebungsvariablen aus $env_file"
        set -a
        # shellcheck disable=SC1090
        source "$env_file"
        set +a
    else
        log_debug "Keine .env gefunden, nutze bestehende System-Umgebung"
    fi
}

show_dev_info() {
    local output_dir="${OUTPUT_DIR:-./output}"
    log_debug "Repo Root: $REPO_ROOT"
    log_debug "OUTPUT_DIR: $output_dir"
}

print_env_summary() {
    local output_dir="${OUTPUT_DIR:-./output}"
    echo "BOOTSTRAP_DEBUG=${BOOTSTRAP_DEBUG:-false}"
    echo "OUTPUT_DIR=$output_dir"
}

run_cli() {
    if [[ $# -eq 0 ]]; then
        set -- --help
    fi
    exec uv run python -m musiclist_for_soundiiz.cli "$@"
}

main() {
    cd "$REPO_ROOT"

    local command="${1:-run}"
    case "$command" in
        run)
            shift || true
            load_env
            show_dev_info
            run_cli "$@"
            ;;
        env)
            load_env
            print_env_summary
            ;;
        help|-h|--help)
            print_usage
            ;;
        *)
            load_env
            show_dev_info
            run_cli "$@"
            ;;
    esac
}

main "$@"
