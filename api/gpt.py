import os
from typing import Dict, List, Optional, Union, Any
import openai
from openai import OpenAI

def call_gpt41(
    prompt: str,
    system_message: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    stream: bool = False,
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_choice: Optional[Union[str, Dict[str, str]]] = None,
) -> Union[str, Any]:
    """
    Call the GPT-4.1 model with the given prompt and parameters.
    
    Args:
        prompt: The user's input prompt
        system_message: Optional system message to set context
        temperature: Controls randomness (0-2, lower is more deterministic)
        max_tokens: Maximum number of tokens to generate
        top_p: Controls diversity via nucleus sampling
        frequency_penalty: Penalizes frequent tokens
        presence_penalty: Penalizes repeated tokens
        stream: Whether to stream the response
        tools: Optional list of tools/functions the model can use
        tool_choice: Optional specification for tool selection
        
    Returns:
        The model's response text or the full response object if streaming
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stream=stream,
        tools=tools,
        tool_choice=tool_choice,
    )
    
    if stream:
        return response
    else:
        return response.choices[0].message.content

def main():
    """
    Main function for testing the GPT-4.1 API call functionality.
    """
    # Example usage
    test_prompt = "Explain the concept of machine learning in simple terms."
    test_system_message = "You are a helpful AI assistant that explains complex topics simply."
    
    print("Testing GPT-4.1 API call...")
    response = call_gpt41(
        prompt=test_prompt,
        system_message=test_system_message,
        max_tokens=500,
        temperature=0.7
    )
    
    print("\nResponse:")
    print(response)


if __name__ == "__main__":
    main()

