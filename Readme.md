### **README**

# ARC Task Automation and Validation

This project automates the process of testing solutions for ARC (Abstraction and Reasoning Corpus) tasks using OpenAI's GPT API. It generates task descriptions, queries GPT for solutions, and validates the output against ground-truth data.

---

### **Directory Structure**

```
.
├── printed/            # Directory for generated task files and GPT outputs
├── data/               # Contains the training and evaluation data
│   ├── training/       # Training tasks in JSON format
│   ├── evaluation/     # Evaluation tasks for additional testing (optional)
```

---

### **Directories Explained**

#### **`printed/`**
- This directory contains all the generated files, including:
  - Task descriptions sent to GPT (e.g., `_task3.txt` files).
  - GPT's outputs and their validation results saved in a consolidated text file (`gpt_responses_with_validation.txt`).

#### **`data/`**
- The main directory for ARC dataset files.

##### **`data/training/`**
- Contains JSON files representing training tasks.
- Each JSON file includes:
  - **`train`**: A set of input/output pairs for learning patterns.
  - **`test`**: Input grids for which the output needs to be predicted.

##### **`data/evaluation/`**
- Contains evaluation tasks, if needed, for testing solutions beyond the training set.

---

### **How It Works**

1. **Generate Task Descriptions:**
   - Each task from `data/training/` is converted into a formatted textual prompt.
   - These prompts include:
     - Training examples (input/output pairs).
     - A test input for which GPT must generate the output.

2. **Query GPT:**
   - The formatted prompts are sent to OpenAI's GPT API.
   - GPT generates responses as solutions to the test inputs.

3. **Validate Outputs:**
   - GPT's output is compared against the ground-truth outputs from the JSON files.
   - Results are logged, including:
     - The raw output (as an array).
     - A visually formatted grid representation.
     - Validation status (CORRECT or INCORRECT).

4. **Log Results:**
   - All results are saved in `printed/gpt_responses_with_validation.txt`.

---

### **How to Run**

1. **Install Dependencies:**
   - Install the OpenAI Python SDK:
     ```bash
     pip install openai
     ```

2. **Set Up API Key:**
   - Export your OpenAI API key as an environment variable:
     ```bash
     export OPENAI_API_KEY="your-api-key-here"
     ```

3. **Configure the Model:**
   - The script currently uses the `o3-mini-2024-12-17` model.
   - If you want to use a different model (e.g., `gpt-3.5-turbo`), change the line in the test.py script:
     ```python
     model = "o3-mini-2024-12-17"
     ```

4. **Run the Scripts:**
   - Execute the main script:
     ```bash
     python main.py
     ```
   - Execute the test script: (this will log results to gpt_responses_with_validation.txt)
     ```bash
     python test.py
     ```

5. **Review Results:**
   - Check the `printed/` directory for generated task files and logs.
   - Open `printed/gpt_responses_with_validation.txt` for detailed results.

---

### **Output Example**

For each task, the log includes:
- **Task Content:** Description of the ARC task.
- **GPT Response (Array):** The raw output as an array of arrays.
- **GPT Response (Formatted Grid):** A human-readable 2D grid.
- **Validation Result:** Whether GPT's output matches the ground truth.
- **Ground Truth (Emoji):** The expected output in emoji format.

**Example Log:**

```plaintext
GPT API Responses for ARC Tasks (With Validation)
==================================================

Task: a85d4709_task3.txt
--------------------------------------------------
We are going to do a challenge wherein I give you a set of input/output examples, ...

GPT Response (Array):
[['🟦', '🟦', '🟦'], ['🟦', '🟥', '🟦'], ['🟦', '🟦', '🟦']]

GPT Response (Formatted Grid):
🟦🟦🟦
🟦🟥🟦
🟦🟦🟦

Validation Result: CORRECT

Ground Truth (Emoji):
🟦🟦🟦
🟦🟥🟦
🟦🟦🟦

==================================================
```

---

### **Future Enhancements**

1. **Support for Evaluation Tasks:**
   - Extend the script to handle tasks in `data/evaluation/`.

2. **Improve Parsing:**
   - Enhance the GPT output parsing to handle edge cases or non-standard formats.

3. **Visualization:**
   - Add a feature to visualize grids as images or graphical outputs.

4. **Performance Metrics:**
   - Include accuracy statistics across multiple tasks.

---

### **License**
This project is for educational and research purposes. Ensure compliance with OpenAI's terms of service when using the GPT API.

--- 

This README is now updated with clear instructions to configure the model name! Let me know if further adjustments are needed.
