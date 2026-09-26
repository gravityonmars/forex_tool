# Forex Converter with Groq Tool Calling

A simple Python forex converter that uses the **ExchangeRate API** to fetch current exchange rates and **Groq's LLM** to demonstrate AI tool/function calling.

## Features

* Convert between different currencies
* Fetch live exchange rates
* Uses Groq's `openai/gpt-oss-120b` model
* Demonstrates LLM tool calling
* Uses environment variables for API keys

## How It Works

```text
User Input
    ↓
Groq AI
    ↓
get_forex() Tool
    ↓
ExchangeRate API
    ↓
Currency Conversion
    ↓
Groq AI
    ↓
Final Response
```

## Requirements

* Python 3.9+
* Groq API key
* Internet connection

## Installation

Clone the project and install the dependencies:

```bash
pip install requests groq python-dotenv
```

## Environment Variables

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

**Never commit your `.env` file to GitHub.**

Add this to `.gitignore`:

```gitignore
.env
```

## Run the Project

```bash
python main.py
```

You will be asked:

```text
Enter the currency code to convert from (e.g., USD): USD
Enter the currency code to convert to (e.g., EUR): EUR
Enter the amount to convert (default is 1.0): 100
```

The program will then fetch the exchange rate and return the conversion.

## Example

```text
Enter the currency code to convert from (e.g., USD): USD
Enter the currency code to convert to (e.g., EUR): EUR
Enter the amount to convert (default is 1.0): 100

100 USD is approximately 85 EUR.
```

*Exchange rates change over time, so the actual result may be different.*

## Technologies Used

* **Python**
* **Groq API**
* **ExchangeRate API**
* **Requests**
* **python-dotenv**

## What This Project Demonstrates

This project is mainly built to understand **AI tool/function calling**.

The LLM decides when to use the `get_forex` function, while the Python function handles the actual API request and currency conversion.

## Project Structure

```text
forex-converter/
├── main.py
├── .env
├── .gitignore
└── README.md
```


