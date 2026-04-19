# Use Python 3.13 as the base image (slim = smaller size, no extra tools)
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files first (this helps Docker cache layers, 
# dependencies won't be reinstalled unless these files change)
COPY pyproject.toml uv.lock ./

# Install the exact packages pinned in uv.lock
# --frozen: don't update the lockfile, just install what's in it
# --no-dev: skip development-only dependencies
RUN uv sync --frozen --no-dev

# Copy the entire project into the container
COPY . .

# Tell Docker this container will listen on port 8000
EXPOSE 8000



COPY entrypoint.sh /entrypoint.sh

# This command removes the Windows carriage returns (\r)
RUN sed -i 's/\r$//' /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
