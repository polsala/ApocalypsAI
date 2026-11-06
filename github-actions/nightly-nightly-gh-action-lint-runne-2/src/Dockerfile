# Use a lightweight base image
FROM alpine:latest

# Install necessary tools: curl for downloading, jq for JSON processing, and git for checkout
RUN apk update && apk add --no-cache curl jq git

# Install the GitHub Actions workflow linter (actionlint)
# We'll download the latest release and make it executable.

# Get the latest release version of actionlint
ARG ACTIONLINT_VERSION=1.6.10

RUN curl -fsSL https://github.com/rhysd/actionlint/releases/download/v${ACTIONLINT_VERSION}/actionlint_${ACTIONLINT_VERSION}_linux_amd64.tar.gz | tar xz -C /usr/local/bin/

# Set the entrypoint to run actionlint
ENTRYPOINT ["actionlint"]

# The action.yml will specify the command to run, which will be passed as arguments to this entrypoint.
