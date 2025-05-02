import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Configuration
PROMPTS_FILE = "prompts.txt"
RESULTS_DIR = "results"
RESULTS_FILE = os.path.join(RESULTS_DIR, "moderation_results.json")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("Missing OPENAI_API_KEY in environment variables or .env file.")

client = OpenAI(api_key=api_key)

def setup():
    """Create results directory if it doesn't exist."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

def load_prompts(filepath):
    """
    Load prompts from file, separated by '---'.
    Extracts any #LABEL: tags without including them in the prompt.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        blocks = f.read().split('---')
        
    results = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        # Extract label and content
        lines = block.split('\n', 1)
        label = None
        content = block
        
        # Check if first line contains a label
        if lines[0].startswith('#LABEL:'):
            label = lines[0].replace('#LABEL:', '').strip()
            content = lines[1].strip() if len(lines) > 1 else ""
            
        results.append({"label": label, "content": content})
    
    return results

def moderate_prompt(prompt_text):
    """Send prompt to OpenAI moderation API."""
    return client.moderations.create(
        model="omni-moderation-latest",
        input=prompt_text
    )

def save_result(entry, filepath):
    """Save result to JSON file."""
    # If file doesn't exist, create it with an empty list
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([], f)
    
    # Read existing data
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Add new entry and write back
    data.append(entry)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    """Process all prompts and save moderation results."""
    setup()
    prompts = load_prompts(PROMPTS_FILE)
    
    for idx, prompt_data in enumerate(prompts, 1):
        prompt_id = f"prompt-{idx:03}"
        timestamp = datetime.now().isoformat()
        
        # Get moderation result - only send the content without the label
        response = moderate_prompt(prompt_data["content"])
        
        # Prepare entry - include label in results
        entry = {
            "id": prompt_id,
            "timestamp": timestamp,
            "label": prompt_data["label"],
            "input": prompt_data["content"],
            "response": response.model_dump()
        }
        
        save_result(entry, RESULTS_FILE)
        label_info = f" (Label: {prompt_data['label']})" if prompt_data["label"] else ""
        print(f"✓ Moderated {prompt_id}{label_info}")
    
    print(f"Completed moderation of {len(prompts)} prompts")

if __name__ == "__main__":
    main()