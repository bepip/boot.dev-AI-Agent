import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

def main():
    try:
        client = init()
    except Exception as e:
        print(e)
        exit(1)

    args = parser()

    run_prompt(client, args)

if __name__ == "__main__":
    main()

def get_api_key() -> str:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("Failed to get api key")
    return api_key

def init() -> OpenAI:
    api_key = get_api_key()
    return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key = api_key
            )

def run_prompt(client: OpenAI, args: argparse.Namespace) -> None:
    prompt :str  = args.user_prompt
    verbose: bool = args.verbose
    msgs: list[ChatCompletionMessageParam]=[
            {
                "role": "user",
                "content": prompt
                }
            ]

    response =  client.chat.completions.create(
            model="openrouter/free",
            messages= msgs
            )
    print_response(response, prompt, verbose)



def print_response(response: ChatCompletion, prompt: str, verbose: bool):
    if response.usage is None:
        raise RuntimeError("Did not receive a response")
    prompt_tokens  = response.usage.prompt_tokens
    response_tokens = response.usage.completion_tokens
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")    
        print(f"Response tokens: {response_tokens}")    
    print(response.choices[0].message.content)

def parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    return parser.parse_args()
