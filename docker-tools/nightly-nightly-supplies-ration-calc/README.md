Nightly Supplies Ration Calculator

Overview: This Dockerized utility helps post-apocalypse survivors plan daily food rations from a stockpile. Provide a JSON file describing items and total days, and the tool outputs per-day allocation.

Usage:

1. Build the image:
   docker build -t ration-calc .

2. Prepare input.json:
   {
     "days": 5,
     "items": [
       {"name": "canned beans", "quantity": 20},
       {"name": "water bottles", "quantity": 15}
     ]
   }

3. Run:
   docker run --rm -v $(pwd):/data ration-calc /data/input.json

The output will be JSON with daily amounts.
