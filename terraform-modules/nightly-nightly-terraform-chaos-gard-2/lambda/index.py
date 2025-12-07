import json
import os

def lambda_handler(event, context):
    """
    Chaos Lambda function that responds to API Gateway and EventBridge triggers.
    """
    chaos_level = os.environ.get('CHAOS_LEVEL', 'medium')
    environment = os.environ.get('ENVIRONMENT', 'test')
    
    # Simulate chaos by introducing random delays
    import time
    import random
    
    if chaos_level == "high":
        time.sleep(random.uniform(0.5, 2.0))
    elif chaos_level == "medium":
        time.sleep(random.uniform(0.1, 0.5))
    
    # Log the chaos
    print(f"Chaos Lambda executed in {environment} environment with chaos level: {chaos_level}")
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Welcome to the Chaos Garden Lambda!',
            'chaos_level': chaos_level,
            'environment': environment,
            'request_id': context.aws_request_id,
            'chaos_fact': get_chaos_fact(chaos_level)
        })
    }

def get_chaos_fact(level):
    """
    Return a whimsical chaos fact based on the chaos level.
    """
    facts = {
        'low': [
            "Chaos theory suggests that small changes can lead to big differences!",
            "The butterfly effect is a classic example of chaos in action.",
            "Even in chaos, there's often underlying order."
        ],
        'medium': [
            "Chaos can actually help systems become more resilient!",
            "Some of the most beautiful patterns emerge from chaotic systems.",
            "Chaos engineering helps us build better, more robust systems."
        ],
        'high': [
            "In the realm of chaos, even the most careful plans can go wonderfully wrong!",
            "Chaos is not randomness; it's complex, deterministic behavior.",
            "Embrace the chaos - it's where innovation happens!"
        ]
    }
    
    import random
    return random.choice(facts.get(level, facts['medium']))

# Example of how this Lambda could be used in chaos testing:
# 1. API Gateway trigger: Test API response times under chaos
# 2. EventBridge trigger: Simulate periodic chaos events
# 3. SQS trigger: Process messages with intentional delays
# 4. CloudWatch Events: Monitor chaos metrics and logs
