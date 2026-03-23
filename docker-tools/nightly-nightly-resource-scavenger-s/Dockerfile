FROM python:3.9-slim-buster AS builder

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ . 

FROM python:3.9-slim-buster

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app/scavenger_sim.py .

ENV SIMULATION_DAYS=7
ENV ZONES="Ruined City,Abandoned Factory,Overgrown Forest"
ENV RESOURCES_PER_ZONE=5
ENV RESOURCE_TYPES="Water,Food,Scrap Metal,Medical Supplies,Fuel"

CMD ["python", "scavenger_sim.py"]
