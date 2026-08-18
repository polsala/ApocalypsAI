FROM python:3.11-alpine
WORKDIR /app
COPY src/cryptid_generator.py .
ENTRYPOINT ["python", "-c", "import cryptid_generator, sys; sys.stdout.write(cryptid_generator.generate() + '\\n')"]
