#!/usr/bin/env python
import os
import sys
from crew import mycrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
import logging
# configure logging
logging.basicConfig(level=os.getenv("APP_LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

required_env = ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT"]
missing = [v for v in required_env if not os.getenv(v)]
if missing:
    logger.warning("Missing required Azure env vars: %s. Running locally may fail.", missing)

# Debug: Print Azure config (hide actual key values)
logger.info("=== Azure Configuration ===")
logger.info(f"AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
logger.info(f"AZURE_OPENAI_DEPLOYMENT: {os.getenv('AZURE_OPENAI_DEPLOYMENT')}")
logger.info(f"AZURE_OPENAI_API_KEY present: {bool(os.getenv('AZURE_OPENAI_API_KEY'))}")
logger.info(f"OPENAI_API_VERSION: {os.getenv('OPENAI_API_VERSION', 'Not set')}")
logger.info("===========================")

os.environ["AZURE_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["AZURE_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
os.environ["AZURE_API_VERSION"] = os.getenv("OPENAI_API_VERSION")
os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
os.environ["AZURE_DEPLOYMENT_NAME"] = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def run():
    """
    Run the crew.
    """
    inputs = {
        'initial_message': 'sample_value'
    }
    mycrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'initial_message': 'sample_value'
    }
    try:
        mycrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        mycrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'initial_message': 'sample_value'
    }
    try:
        mycrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
