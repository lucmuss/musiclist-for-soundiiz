#!/usr/bin/env python3
"""
Web interface entry point for MusicList for Soundiiz
Starts the Django development server or production server
"""

import argparse
import os
import sys
from pathlib import Path


def main():
    """Main entry point for web interface"""
    parser = argparse.ArgumentParser(
        description="MusicList for Soundiiz - Web Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  musiclist-for-soundiiz-web              # Start development server on port 8000
  musiclist-for-soundiiz-web --port 8080  # Start on custom port
  musiclist-for-soundiiz-web --production # Start production server with gunicorn
        """,
    )

    parser.add_argument(
        "--port", "-p", type=int, default=8000, help="Port to run the server on (default: 8000)"
    )

    parser.add_argument(
        "--host", "-H", type=str, default="127.0.0.1", help="Host to bind to (default: 127.0.0.1)"
    )

    parser.add_argument(
        "--production", "--prod", action="store_true", help="Run in production mode with gunicorn"
    )

    parser.add_argument("--migrate", action="store_true", help="Run migrations before starting")

    parser.add_argument(
        "--collect-static", action="store_true", help="Collect static files before starting"
    )

    args = parser.parse_args()

    # Add src to path
    src_dir = Path(__file__).parent.parent
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    # Set Django settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "musiclist_project.settings.development")

    if args.production:
        os.environ["DJANGO_SETTINGS_MODULE"] = "musiclist_project.settings.production"

    import django

    django.setup()

    # Run migrations if requested
    if args.migrate:
        print("Running migrations...")
        from django.core.management import call_command

        call_command("migrate", verbosity=1)
        print("Migrations complete.\n")

    # Collect static files if requested
    if args.collect_static:
        print("Collecting static files...")
        from django.core.management import call_command

        call_command("collectstatic", verbosity=1, interactive=False)
        print("Static files collected.\n")

    if args.production:
        # Run with gunicorn in production
        try:
            import gunicorn.app.wsgiapp as wsgi

            print(f"Starting production server on {args.host}:{args.port}...")
            sys.argv = [
                "gunicorn",
                "--bind",
                f"{args.host}:{args.port}",
                "--workers",
                "4",
                "--threads",
                "4",
                "--worker-class",
                "uvicorn.workers.UvicornWorker",
                "--access-logfile",
                "-",
                "--error-logfile",
                "-",
                "--capture-output",
                "--enable-stdio-inheritance",
                "musiclist_project.wsgi:application",
            ]
            wsgi.run()
        except ImportError:
            print("Error: gunicorn not installed. Install with: uv pip install gunicorn uvicorn")
            sys.exit(1)
    else:
        # Run with Django development server
        from django.core.management import execute_from_command_line

        print(f"Starting development server on http://{args.host}:{args.port}/")
        print("Press Ctrl+C to stop.\n")
        execute_from_command_line([sys.argv[0], "runserver", f"{args.host}:{args.port}"])


if __name__ == "__main__":
    main()
