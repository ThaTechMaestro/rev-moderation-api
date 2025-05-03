# Rev Moderation API

A Python-based tool for testing OpenAI's content moderation API. This project provides a framework for evaluating the effectiveness of OpenAI's moderation system by processing predefined prompts and analyzing the results.

## Features

- Processes multiple prompts with optional labels
- Uses OpenAI's latest moderation model
- Saves results in JSON format with timestamps
- Supports environment-based API key configuration

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Add test prompts to `test_usage/prompts.txt` using the format:
```
#LABEL: LABEL_NAME
Your prompt text here
---
```

2. Run the moderation test:
```bash
python test_usage/sandbox.py
```

3. View results in `test_usage/results/moderation_results.json`

## Project Structure

- `test_usage/`: Contains test scripts and results
  - `sandbox.py`: Main script for running moderation tests
  - `prompts.txt`: Test prompts with optional labels
  - `results/`: Directory for storing moderation results
