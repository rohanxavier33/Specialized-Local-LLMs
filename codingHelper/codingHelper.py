from transformers import AutoModelForCausalLM, AutoTokenizer 

# Load the model and tokenizer from local directory
model = AutoModelForCausalLM.from_pretrained("codingHelper/DeepSeek-R1-Distill-Qwen-7B", device_map="cpu")
tokenizer = AutoTokenizer.from_pretrained("codingHelper/DeepSeek-R1-Distill-Qwen-7B")

# Prepare the input from local text file
with open("codingHelper/codingHelper.txt", "r") as file:
    content = file.read()
prompt = content
inputs = tokenizer(prompt, return_tensors="pt")

# Generate and print output
outputs = model.generate(**inputs, max_length=500)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))