FROM registry.access.redhat.com/ubi8/python-311

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

RUN chgrp -R 0 /app && \
    chmod -R g+rwX /app

EXPOSE 8080

# Switch to non-root user (UBI images come with a default user)
USER 1001

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
