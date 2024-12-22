import os
import json
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key="")  # Replace with your actual API key

# Emoji map
emojis = ['⬛️', '🟦', '🟥', '🟩', '🟨', '⬜️', '🟪', '🟧', '🔷', '🟫']

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
def parse_gpt_output(response):
    grid = []
    for line in response.splitlines():
        row = [char for char in line if char in emojis]
        if row:
            grid.append(row)
    return grid

# Path to the directory with tasks
printed_dir = "printed"
output_file = "gpt_responses_with_validation.txt"  # Output file for all responses with validation

# Prepare output file
with open(output_file, "w") as out:
    out.write("GPT API Responses for ARC Tasks (With Validation)\n")
    out.write("=" * 50 + "\n\n")

# Process each task file and validate results
for task_file in os.listdir(printed_dir):
    if task_file.endswith("_task3.txt"):  # Only process relevant task files
        task_path = os.path.join(printed_dir, task_file)
        task_content = load_task(task_path)
        print(f"Processing: {task_file}")
        
        try:
            # Call GPT API
            response = client.chat.completions.create(
                model="gpt-4",  # or "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": "You are an expert in solving ARC puzzles."},
                    {"role": "user", "content": task_content},
                ],
                temperature=0  # Lower temperature for deterministic results
            )
            gpt_response = response.choices[0].message.content

            # Parse GPT output and ground truth
            gpt_output = parse_gpt_output(gpt_response)
            ground_truth = load_ground_truth(task_file)

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
            out.write("\nGPT Response (Array):\n")
            out.write(f"{gpt_output}\n")
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

print(f"All responses with validation saved to {output_file}")
