# Nightly Metronome Madness

A playful Ansible playbook that generates randomized metronome beats and plays them through your system's audio output. Perfect for keeping your coding rhythm alive with a touch of chaos!

## Features
- Random tempo generation between 60-180 BPM
- Variety of beat patterns (straight, triplet, swing)
- Optional audio output via system speakers or headphones
- Configurable duration and intervals

## Usage
```bash
ansible-playbook metronome_madness.yml -i inventory.ini
```

## Inventory Example
Create `inventory.ini` with your local machine:
```ini
localhost ansible_connection=local
```

## Customization
Edit `vars/metronome.yml` to adjust:
- `tempo_range`: [min, max] BPM
- `beat_pattern`: "straight", "triplet", or "swing"
- `duration_minutes`: How long to run

## Dependencies
- Ansible
- Python `simpleaudio` library (installed via pip)

## License
MIT
