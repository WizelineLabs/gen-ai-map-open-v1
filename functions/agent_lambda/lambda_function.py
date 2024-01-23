import asyncio
from src.secrets_manager import load_secrets
from src.main_process import main_process


def handler(event, context):
    try:
        load_secrets()
        asyncio.run(main_process(event))
        return {"statusCode": 200, "body": "Success"}
    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": "Error"}


if __name__ == "__main__":
    event = {"Records": [{"body": '{"value": "GPTNeo"}'}]}
    handler(event, None)
