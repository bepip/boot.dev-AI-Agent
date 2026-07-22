import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv
from openai.types.chat import ChatCompletion
from config import MAX_ITERS
from prompts import system_prompt
from functions.call_functions import available_functions, call_function

def main():
     try:
         client = init()
     except Exception as e:
         print(e)
         exit(1)
     args = parser()
     run_prompt(client, args)

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
    messages: list=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
            ]
    for _ in range(MAX_ITERS):
        response =  call_agent(client, messages)
        if response_handler(response, prompt, verbose, messages):
            return
    print(f'Something went wrong: Max_iteration {MAX_ITERS} reached')
    exit(1)

def call_agent(client: OpenAI, messages: list) -> ChatCompletion:
    return  client.chat.completions.create(
            model = "openrouter/free",
            messages = messages,
            tools = available_functions
            )

def response_handler(response: ChatCompletion, prompt: str, verbose: bool, messages: list) -> bool:
    if response.usage is None:
        raise RuntimeError("Did not receive a response")
    prompt_tokens  = response.usage.prompt_tokens
    response_tokens = response.usage.completion_tokens
    message = response.choices[0].message
    messages.append(message)
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")    
        print(f"Response tokens: {response_tokens}")
    if not message.tool_calls:
        print("Final response:")
        print(message.content)
        return True
    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        result_message = call_function(tool_call, verbose)
        messages.append(result_message)
        if not result_message.get("content"):
            raise RuntimeError(f"content missing from response for {tool_call.function.name}")
        if verbose:
            print(f'-> {result_message["content"]}')
    return False

def parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    return parser.parse_args()

if __name__ == "__main__":
    main()

