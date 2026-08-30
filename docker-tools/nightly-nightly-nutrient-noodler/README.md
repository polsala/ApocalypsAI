# Nightly Nutrient Noodler

A whimsical-yet-vital containerized service for the discerning post-apocalyptic survivor, the Nightly Nutrient Noodler helps you make the most of your scavenged supplies. It analyzes your available pantry items, suggests balanced meal recipes, and provides "nutrient nudges" to highlight any potential dietary deficiencies. Because even after the end, a balanced diet is key to survival (and good mood!).

## Features

*   **Pantry Analysis**: Input your current inventory of ingredients.
*   **Recipe Suggestions**: Get a list of meals you can prepare with what you have.
*   **Nutrient Nudges**: Receive a summary of your current nutrient intake and warnings about potential deficiencies based on simplified daily recommended intakes.
*   **Containerized**: Easy to deploy and run anywhere Docker thrives.

## Classifier

`docker-tools`

## How to Run

1.  **Ensure Docker is installed**: If not, follow the official Docker installation guide.
2.  **Build the Docker image**: Navigate to the root of this utility's directory and run:
    ```bash
    docker build -t nightly-nutrient-noodler .
    ```
3.  **Run the container**: You can run it directly or use Docker Compose.

    **Option A: Direct Docker Run**
    ```bash
    docker run -p 5000:5000 --name nutrient-noodler-instance nightly-nutrient-noodler
    ```
    The service will be accessible at `http://localhost:5000`.

    **Option B: Using Docker Compose (Recommended)**
    ```bash
    # From the root of this utility's directory
    docker-compose up --build -d
    ```
    This will build the image (if not already built) and start the container in detached mode. The service will be accessible at `http://localhost:5000`.

## API Endpoint

The Noodler exposes a single, simple API endpoint:

### `POST /plan_meal`

Analyzes your ingredients and provides meal suggestions and nutrient insights.

*   **Request Body (JSON)**:
    ```json
    {
      "ingredients": ["canned beans", "rice", "dried fruit", "water", "spices"]
    }
    ```
    `ingredients`: An array of strings representing the items currently in your pantry.

*   **Response Body (JSON)**:
    ```json
    {
      "message": "Nutrient Noodler's Daily Digest:",
      "available_ingredients": ["canned beans", "rice", "dried fruit", "water", "spices"],
      "suggested_recipes": ["Hearty Bean Stew", "Rice & Dried Fruit Medley"],
      "nutrient_summary_from_pantry": {
        "protein": 12,
        "carbs": 55,
        "fats": 0,
        "vitamins": 10,
        "fiber": 10,
        "iron": 3
      },
      "nutrient_nudges": {
        "protein": 38,
        "carbs": 145,
        "fats": 60,
        "vitamins": 90,
        "fiber": 20,
        "iron": 7
      }
    }
    ```
    *   `suggested_recipes`: Names of recipes that can be made with your available ingredients.
    *   `nutrient_summary_from_pantry`: Total estimated nutrients from your *available* ingredients.
    *   `nutrient_nudges`: A list of nutrients you might be deficient in, along with the estimated amount needed to reach the daily recommended intake.

## Example Usage (with `curl`)

Once the Docker container is running:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"ingredients": ["canned beans", "rice", "dried fruit", "water", "spices", "root vegetables"]}' \
     http://localhost:5000/plan_meal | python3 -m json.tool
```

## Development & Testing

To run tests locally (outside Docker):

1.  **Install dependencies**: Ensure Python 3.9+ is installed, then:
    ```bash
    pip install -r src/requirements.txt pytest
    ```
2.  **Run tests**: From the root of this utility's directory:
    ```bash
    pytest tests/
    ```

The tests are designed to be deterministic and do not require a running Docker container or external network access. They use Flask's built-in test client and hardcoded data for recipes and nutrient profiles.
