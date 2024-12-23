import os, json
from os import listdir
from os.path import isfile, join

emojis = ['⬛️', '🟦', '🟥', '🟩', '🟨', '⬜️', '🟪', '🟧', '🔷', '🟫']

if not os.path.exists("printed"):
    os.makedirs("printed")


def strize(nums, trans=True):
    ret = ""
    if trans == True:
        for item in nums:
            ret += emojis[item]
    else:
        for item in nums:
            ret += str(item) + " "
    return ret

def emojize(ilist, trans=True):
    ret = str(ilist)
    if trans == True:
        for i, e in enumerate(emojis):
            ret = ret.replace(str(i), e)
    return ret

def print_task(fn, trans=True):
    fname = "data/training/"+fn+".json"
    data = None
    with open(fname, "r") as f:
        data = json.loads(f.read())

    outstr = ""
    outstr += "We are going to do a challenge wherein I give you a set of input/output "
    outstr += "examples, and you have to present the correct output from a new input.\n"
    outstr += "The input to each puzzle is a 2D grid. The solution to the "
    outstr += "puzzle is also a 2D grid. Across different inputs, the sizes of the grids "
    outstr += "may vary. The correct output grid may or may not have a different size "
    outstr += "to the input grid.\n"
    outstr += "As an example, consider the following input/output examples for a simple task:\n"
    for item in data['train']:
        it = item['input']
        gridx = len(it[0])
        gridy = len(it)
        outstr += "input:\n"
        for ind in range(gridy):
            ix = strize(it[ind], trans)
            outstr += ix + "\n"
        it = item['output']
        gridx = len(it[0])
        gridy = len(it)
        outstr += "\n"
        outstr += "output:\n"
        for ind in range(gridy):
            ix = strize(it[ind], trans)
            outstr += ix + "\n"
        outstr += "\n"
    outstr += "As you can see, each example depicts a visual transformation between the "
    outstr += "original and final grid.\n"
    outstr += "Can you see the pattern yet?\n"
    outstr += "For each example, list the rules that were applied to go from input to output.\n"
    outstr += "Rules should include adjectives such as identify, count, extend, fill, "
    outstr += "copy, move, rotate, and delete."
    outstr += "Here is the unsolved problem:\n"
    for item in data['test']:
        it = item['input']
        gridx = len(it[0])
        gridy = len(it)
        outstr += "input:\n"
        for ind in range(gridy):
            ix = strize(it[ind], trans)
            outstr += ix + "\n"
        outstr += "\n"
    outstr += "Apply the rules you found in the examples to the unsolved problem. "
    outstr += "Please present a depiction of the resulting solution."
    of = "printed/" + fn + "_task.txt"
    with open(of, "w") as f:
        f.write(outstr)

def print_task2(fn, trans=True):
    fname = "data/training/"+fn+".json"
    data = None
    with open(fname, "r") as f:
        data = json.loads(f.read())

    outstr = ""
    outstr += "We are going to do a challenge wherein I give you a set of input/output "
    outstr += "examples, and you have to solve for the correct output from a new input.\n"
    outstr += "The input to each puzzle is a 2D grid, represented as a Python list of "
    outstr += "lists. Each inner list represents one row of the grid. The solution to the "
    outstr += "puzzle is also a 2D grid. Across different inputs, the sizes of the grids "
    outstr += "may vary. The correct output grid may or may not have a different size "
    outstr += "to the input grid.\n"
    outstr += "As an example, consider the following input/output examples for a simple task:\n"
    for index, item in enumerate(data['train']):
        outstr += "input" + str(index) + " = "
        outstr += emojize(item['input'], trans) + "\n"
        outstr += "output" + str(index) + " = "
        outstr += emojize(item['output'], trans) + "\n"

    outstr += "As you can see, each example depicts a visual transformation between the "
    outstr += "original and final grid.\n"
    outstr += "Can you see the pattern yet?\n"
    outstr += "For each example, list the rules that were applied to go from input to output.\n"
    outstr += "Rules should include adjectives such as identify, count, extend, fill, "
    outstr += "copy, move, rotate, and delete."
    outstr += "Here is the unsolved problem:\n"
    for index, item in enumerate(data['test']):
        outstr += "input = "
        outstr += emojize(item['input'], trans) + "\n"
    outstr += "Apply the rules you found in the examples to the unsolved problem. "
    outstr += "Please present a depiction of the resulting solution."
    #print(outstr)
    of = "printed/" + fn + "_task2.txt"
    with open(of, "w") as f:
        f.write(outstr)
        
def print_task3(fn, trans=True):
    fname = "data/training/" + fn + ".json"
    data = None
    with open(fname, "r") as f:
        data = json.loads(f.read())

    outstr = ""
    # Replace the content of ARC_examples.txt with a direct explanation here
    outstr += "Example ARC Task:\n"
    outstr += "Consider the following input/output example:\n\n"
    outstr += "Input:\n⬛️⬛️⬛️\n⬛️🟦⬛️\n⬛️⬛️⬛️\n\n"
    outstr += "Output:\n⬛️⬛️⬛️\n⬛️🟥⬛️\n⬛️⬛️⬛️\n\n"
    outstr += "Explanation:\n"
    outstr += "In this task, the goal is to identify the blue square (🟦) and change it to a red square (🟥).\n"
    outstr += "Rules may include identifying specific patterns, locations, or transformations.\n"
    outstr += "Try to infer the rules and apply them to solve the new problems!\n"
    outstr += "\nTask\n"
    for index, item in enumerate(data['train']):
        outstr += "input" + str(index) + " = "
        outstr += emojize(item['input'], trans) + "\n"
        outstr += "output" + str(index) + " = "
        outstr += emojize(item['output'], trans) + "\n"
    outstr += "###\n"
    outstr += "\n"
    outstr += "Explain how to convert the above inputs into outputs.\n"
    outstr += "Here is an unsolved problem:\n"
    for index, item in enumerate(data['test']):
        outstr += "input = "
        outstr += emojize(item['input'], trans) + "\n"
    outstr += "Apply the same rules to this unsolved problem and present a depiction of the solution.\n"
    outstr += "Present your solution as a Python list of lists where:\n"
    outstr += "1. Each inner list represents one row of the grid\n"
    outstr += "2. Each element in the lists must be an emoji\n"
    outstr += "3. The grid must have exactly the same dimensions as the example outputs\n"
    outstr += "4. Format your solution exactly like this example:\n\n"
    outstr += "[[⬛️, 🟦, 🟦],\n"
    outstr += " [🟥, 🟥, ⬛️],\n"
    outstr += " [⬛️, 🟦, 🟦]]\n\n"
    
    # Add example dimensions to make it clearer
    for index, item in enumerate(data['train']):
        input_grid = item['input']
        output_grid = item['output']
        outstr += f"Note: Example {index}'s output grid is {len(output_grid)}x{len(output_grid[0])} - "
        outstr += f"your solution must also be {len(output_grid)}x{len(output_grid[0])}\n"
    
    outstr += "\nYour solution (as a Python list of lists):\n"
    
    of = "printed/" + fn + "_task3.txt"
    with open(of, "w") as f:
        f.write(outstr)



def print_answer(fn, trans=True):
    fname = "data/training/"+fn+".json"
    data = None
    with open(fname, "r") as f:
        data = json.loads(f.read())
    outstr = ""

    for item in data['test']:
        it = item['output']
        gridx = len(it[0])
        gridy = len(it)
        outstr += "output:\n"
        for ind in range(gridy):
            ix = strize(it[ind], trans)
            outstr += ix + "\n"
        outstr += "\n"

        of = "printed/" + fn + "_answer.txt"
        with open(of, "w") as f:
            f.write(outstr)

#tasks = ['de1cd16c', '29c11459', '2dc579da', '50cb2852', 'd6ad076f', 'd13f3404', 'ef135b50']
#tasks = ['de1cd16c']
mypath = "data/training"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)
tasks = []
for fn in onlyfiles:
    tasks.append(fn[:-5])
trans = True
for t in tasks:
    print_task(t, trans)
    print_task2(t, trans)
    print_task3(t, trans)
    print_answer(t, trans)