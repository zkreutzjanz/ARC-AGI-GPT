import os
import json
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Replace with your actual API key
model = "o3-mini-2024-12-17"

# Emoji map
emojis = ['⬛️', '🟦', '🟥', '🟩', '🟨', '⬜️', '🟪', '🟧', '🔷', '🟫']

if not os.path.exists("printed"):
    os.makedirs("printed")

# Function to load the generated task
def load_task(file_path):
    with open(file_path, "r") as f:
        return f.read()

# Function to load ground-truth outputs and convert to emojis
def load_ground_truth(task_file):
    task_path = os.path.join("data/training", task_file.replace("_task3.txt", ".json"))
    with open(task_path, "r") as f:
        data = json.load(f)
    ground_truth = data["test"][0]["output"]  # Assuming one test case per task
    return [[emojis[num] for num in row] for row in ground_truth]

# Function to parse GPT response into a comparable format
def parse_gpt_output(response, expected_dimensions=None):
    try:
        print("\nDEBUG - Raw response:")
        print(response[:200] + "..." if len(response) > 200 else response)
        
        # Find content between [[ and ]] that looks like a grid
        import re
        grid_pattern = r'\[\[(.*?)\]\]'
        match = re.search(grid_pattern, response, re.DOTALL)
        
        if not match:
            print("DEBUG - No grid pattern found in response")
            return []
            
        # Split into rows and clean up
        content = match.group(1)
        # Split by '], [' to separate rows and clean up brackets
        rows = [row.strip().strip('[').strip(']') for row in content.split('],')]
        
        # Parse each row into emojis
        grid = []
        for row in rows:
            # Split by commas and clean up whitespace
            cells = [cell.strip() for cell in row.split(',') if cell.strip()]
            # Keep only valid emojis
            emoji_row = []
            for cell in cells:
                for emoji in emojis:
                    if emoji in cell:
                        emoji_row.append(emoji)
                        break
            if emoji_row:
                grid.append(emoji_row)
        
        # Validate dimensions
        if not grid:
            print("DEBUG - No valid grid constructed")
            return []
            
        row_length = len(grid[0])
        if not all(len(row) == row_length for row in grid):
            print("DEBUG - Inconsistent row lengths")
            print("Row lengths:", [len(row) for row in grid])
            return []
        
        if expected_dimensions:
            expected_rows, expected_cols = expected_dimensions
            if len(grid) != expected_rows or row_length != expected_cols:
                print(f"DEBUG - Grid dimension mismatch. Expected {expected_rows}x{expected_cols}, got {len(grid)}x{row_length}")
                return []
        
        print("\nDEBUG - Successfully parsed grid:")
        print(grid)
        return grid
        
    except Exception as e:
        print(f"DEBUG - Error parsing grid: {str(e)}")
        print(f"Response type: {type(response)}")
        return []

# Update the system prompt to be more explicit about format
def get_system_prompt():
    return """You are an expert in solving ARC puzzles. When providing solutions:
1. Present your solution as a Python list of lists containing emojis
2. Each inner list represents one row of the grid
3. Format EXACTLY like this (including brackets, commas, and spaces):
[[⬛️, 🟦, 🟦],
 [🟥, 🟥, ⬛️],
 [⬛️, 🟦, 🟦]]

4. Start your response with [[ and end with ]]
5. Include commas between emojis and between rows
6. Do not include any explanation text in your response"""

def format_task_with_dimensions(task_content, expected_dimensions):
    return (
        task_content + 
        f"\n\nIMPORTANT: Your solution must be a grid with exactly {expected_dimensions[0]} rows and {expected_dimensions[1]} columns.\n" +
        "Format your solution EXACTLY like this example (including all brackets, commas, and spaces):\n" +
        "[[⬛️, 🟦, 🟦],\n" +
        " [🟥, 🟥, ⬛️],\n" +
        " [⬛️, 🟦, 🟦]]\n\n" +
        "Your solution (start with [[ and end with ]]):"
    )

# Path to the directory with tasks
printed_dir = "printed"
output_file = "gpt_responses_with_validation.txt"  # Output file for all responses with validation

# Prepare output file
with open(output_file, "w") as out:
    out.write("GPT API Responses for ARC Tasks (With Validation)\n")
    out.write("=" * 50 + "\n\n")

# Function to load input grid
def load_input_grid(task_file):
    task_path = os.path.join("data/training", task_file.replace("_task3.txt", ".json"))
    with open(task_path, "r") as f:
        data = json.load(f)
    input_grid = data["test"][0]["input"]  # Assuming one test case per task
    return [[emojis[num] for num in row] for row in input_grid]

# Process each task file and validate results
print(f"Model: {model}")
print(f"Processing {len(os.listdir(printed_dir))} tasks")
for task_file in os.listdir(printed_dir):
    if task_file.endswith("_task3.txt"):  # Only process relevant task files
        task_path = os.path.join(printed_dir, task_file)
        task_content = load_task(task_path)
        print(f"Processing: {task_file}")
        
        try:
            # Load ground truth first to get expected dimensions
            ground_truth = load_ground_truth(task_file)
            expected_dimensions = (len(ground_truth), len(ground_truth[0]))
            
            # Use the new formatting function
            task_with_dimensions = format_task_with_dimensions(task_content, expected_dimensions)
            
            if(model == "o3-mini-2024-12-17"):
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": get_system_prompt()},
                        {"role": "user", "content": task_with_dimensions},
                    ]
                    # no temperature allowed
                )
            else:
                response = client.chat.completions.create(
                    model=model,  # or "gpt-3.5-turbo"
                    messages=[
                        {"role": "system", "content": "You are an expert in solving ARC puzzles."},
                        {"role": "user", "content": task_with_dimensions},
                    ],
                    temperature=0  # Lower temperature for deterministic results
                )
            gpt_response = response.choices[0].message.content
            print("\nDEBUG - Processing response for", task_file)
            print("Response length:", len(gpt_response))
            
            # Parse GPT output with dimension validation
            gpt_output = parse_gpt_output(gpt_response, expected_dimensions)
            
            if not gpt_output:
                print("DEBUG - Failed to parse response into valid grid")
            
            # Validate the result
            is_correct = gpt_output == ground_truth
            validation_result = "CORRECT" if is_correct else "INCORRECT"
        except Exception as e:
            gpt_response = f"Error occurred: {e}"
            gpt_output = []  # Empty output on error
            validation_result = "FAILED TO PROCESS"

        # Write the task, response, and validation result to the output file
        with open(output_file, "a") as out:
            out.write(f"Task: {task_file}\n")
            out.write("-" * 50 + "\n")
            out.write(f"{task_content}\n")
            
            # Add input grid
            input_grid = load_input_grid(task_file)
            out.write("\nInput Grid:\n")
            out.write("\n".join(["".join(row) for row in input_grid]) + "\n")
            
            out.write("\nGPT Response (Array):\n")
            out.write(f"{gpt_output}\n")
            if validation_result == "FAILED TO PROCESS":
                out.write(f"Error: {gpt_response}\n")
            out.write("\nGPT Response (Formatted Grid):\n")
            if gpt_output:
                out.write("\n".join(["".join(row) for row in gpt_output]) + "\n")
            else:
                out.write("No output generated.\n")
            out.write(f"\nValidation Result: {validation_result}\n")
            if validation_result != "FAILED TO PROCESS":
                out.write(f"\nGround Truth (Emoji):\n")
                out.write("\n".join(["".join(row) for row in ground_truth]) + "\n")
            out.write("\n" + "=" * 50 + "\n\n")
        print(f"Validation Result: {validation_result}")

print(f"All responses with validation saved to {output_file}")
