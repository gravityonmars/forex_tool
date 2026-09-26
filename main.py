import requests
import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=api_key)

def get_forex(from_currency, to_currency, amount):
    try:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        url = f"https://open.er-api.com/v6/latest/{from_currency}"

        response = requests.get(url)
        data = response.json()

        if "rates" not in data or to_currency not in data["rates"]:
            return f"Error: Unable to fetch exchange rate for {from_currency} to {to_currency}."

        converted_amount = data["rates"][to_currency] * amount
        rate_per_unit = converted_amount / amount if amount > 0 else 0

        result = {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "converted_amount": converted_amount,
            "rate_per_unit": rate_per_unit
        }

        return json.dumps(result, indent=4)
    except Exception as e:
        return f"Error: An unexpected error occurred while fetching the exchange rate: {str(e)}"

def get_forex_tool_properties():
    return {
        "type": "function",
        "function": {
            "name": "get_forex",
            "description": "Get the forex information of a currency pair. it provides current exchange rates and conversion information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_currency": {
                        "type": "string",
                        "description": "The currency code to convert from"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "The currency code to convert to"
                    },
                    "amount": {
                        "type": "number",
                        "description": "The amount to convert"
                    }
                },
                "required": ["from_currency", "to_currency", "amount"]
            }
        }

    }

def run_forex_tool(from_currency, to_currency, amount):
    system_prompt = {
        "role": "system",
        "content": """You are a forex information assistant. You have access to a tool called 'get_forex' that can provide current exchange rates and conversion information for currency pairs. When a user requests forex information, you should use the 'get_forex' tool to fetch the data and return it in a structured format."""
    }

    user_prompt = {
        "role": "user",
        "content": f"Get the forex information for {amount} {from_currency} to {to_currency}."
    }

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[system_prompt, user_prompt],
        max_tokens=1500,
        temperature=0.7,
        tools = [get_forex_tool_properties()],
        tool_choice ="auto"
    )

    tool_call_decisions = response.choices[0].message.tool_calls

    if tool_call_decisions:
        for tool_call in tool_call_decisions:
            if tool_call.function.name == "get_forex":
                from_currency = json.loads(tool_call.function.arguments).get("from_currency")
                to_currency = json.loads(tool_call.function.arguments).get("to_currency")
                amount = json.loads(tool_call.function.arguments).get("amount")
                forex_result = get_forex(from_currency, to_currency, amount)

                tool_response = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": "get_forex", 
                    "content": forex_result
                }

                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[system_prompt, user_prompt, tool_response],
                    max_tokens=1500,
                    temperature=0.7,
                    tools = [get_forex_tool_properties()],
                    tool_choice ="auto"
                )

                result = response.choices[0].message.content
    else:
        result = response.choices[0].message.content

    return result
from_currency = input("Enter the currency code to convert from (e.g., USD): ")
to_currency = input("Enter the currency code to convert to (e.g., EUR): ")
amount = float(input("Enter the amount to convert (default is 1.0): "))
result = run_forex_tool(from_currency, to_currency, amount)

print(result)