default:
    @just --list

# Generate meeting pages from the Pike13 calendar in .env
meetings:
    python3 scripts/gen_meetings.py

# Run the Hugo development server with drafts enabled
serve: meetings
    hugo server -D -s site

# Build the Hugo site
build: meetings
    hugo -s site --cleanDestinationDir
