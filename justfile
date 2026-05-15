default:
    @just --list

# Run the Hugo development server with drafts enabled
serve:
    hugo server -D -s site

# Build the Hugo site
build:
    hugo -s site
