FROM python:3.8

# Install rclone
RUN apt-get update && apt-get install -y rclone

# Print the location of the rclone executable
RUN which rclone

WORKDIR /function

# Add requirements.txt and install Python dependencies
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rclone configuration file
COPY rclone.conf /.rclone.conf

# Print contents of the root directory
RUN ls -la /

# Copy func.py
COPY func.py /function/

ENV PYTHONPATH="$PYTHONPATH:/function"

ENTRYPOINT ["fdk", "/function/func.py", "handler"]