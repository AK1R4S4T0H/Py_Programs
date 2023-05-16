# VLADIMIR
import tkinter as tk
from transformers import GPT2Tokenizer, TFGPT2LMHeadModel
from transformers import AdamW
import numpy as np
import tensorflow as tf

# Load tokenizer from disk if it exists, otherwise download it
if 'tokenizer' in locals():
    tokenizer = tokenizer.from_pretrained('./tokenizer')
else:
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    tokenizer.save_pretrained('./tokenizer')

# Load model from disk if it exists, otherwise download it
if 'model' in locals():
    model = model.from_pretrained('./model', pad_token_id=tokenizer.eos_token_id)
else:
    model = TFGPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id)
    model.save_pretrained('./model')


def generate_text(prompt):
    input_ids = tokenizer.encode(prompt, return_tensors='tf')
    generated_ids = model.generate(input_ids=input_ids, max_length=50, do_sample=True)[0]
    output = tokenizer.decode(generated_ids.numpy(), skip_special_tokens=True)
    return output

def get_response():
    
    user_input = input_box.get()
    
    response = generate_text(user_input)

    text_box.insert(tk.END, f"\nVladimir:   {response}\n____________________________________________________________________________________")


root = tk.Tk()
root.title("Text Generation Bot")
root.config(bg='violet')

# Create the text box for displaying conversation
text_box = tk.Text(root, pady=10,  height=20, width=100)
text_box.pack()

input_box = tk.Entry(root, width=120)
input_box.pack()


submit_button = tk.Button(root, text="Submit", command=get_response)
submit_button.pack()

root.mainloop()

