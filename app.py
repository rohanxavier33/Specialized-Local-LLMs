import tkinter as tk
from tkinter import ttk, scrolledtext
from transformers import AutoModelForCausalLM, AutoTokenizer
import threading

MODEL_CONFIGS = {
    'Coding Helper': {
        'model_dir': "codingHelper/DeepSeek-R1-Distill-Qwen-7B",
        'prompt_path': "codingHelper/codingHelper.txt",
        'input_labels': ["Coding Problem:"],
        'prompt_formatter': lambda content, inputs: content + inputs[0]
    },
    'Resume Builder': {
        'model_dir': "resumeBuilder/DeepSeek-R1-Distill-Qwen-7B",
        'prompt_path': "resumeBuilder/resumeBuilder.txt",
        'input_labels': ["Resume:", "Job Description:"],
        'prompt_formatter': lambda content, inputs: f"{content} Resume: '{inputs[0]}' Job Description: '{inputs[1]}'"
    },
    'Lecture Summarizer': {
        'model_dir': "lectureNotes/DeepSeek-R1-Distill-Qwen-1.5B",
        'prompt_path': "lectureNotes/lectureNotes.txt",
        'input_labels': ["Lecture Transcript:"],
        'prompt_formatter': lambda content, inputs: content + inputs[0]
    }
}

class LLMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Assistant")
        self.geometry("1000x800")
        self.configure(bg='#F0F8FF')  # Alice Blue background
        
        # Create UI elements
        self.create_widgets()
        self.current_input_fields = []
        
    def create_widgets(self):
        # Model selection
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(
            self,
            textvariable=self.model_var,
            values=list(MODEL_CONFIGS.keys()),
            state='readonly'
        )
        self.model_dropdown.bind('<<ComboboxSelected>>', self.update_input_fields)
        self.model_dropdown.pack(pady=10, padx=20, fill=tk.X)
        self.model_dropdown.current(0)
        
        # Input container
        self.input_container = ttk.Frame(self)
        self.input_container.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Generate button
        self.generate_btn = ttk.Button(
            self,
            text="Generate",
            command=self.on_generate,
            style='Accent.TButton'
        )
        self.generate_btn.pack(pady=10)
        
        # Output area
        self.output_area = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            state='disabled',
            height=15
        )
        self.output_area.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(
            self,
            textvariable=self.status_var,
            relief=tk.SUNKEN
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#F0F8FF')
        self.style.configure('Accent.TButton', 
                           background='#0096FF', 
                           foreground='white',
                           font=('Helvetica', 12, 'bold'))
        
        # Initial setup
        self.update_input_fields()

    def update_input_fields(self, event=None):
        # Clear previous inputs
        for widget in self.input_container.winfo_children():
            widget.destroy()
            
        config = MODEL_CONFIGS[self.model_var.get()]
        self.current_input_fields = []
        
        for label in config['input_labels']:
            frame = ttk.Frame(self.input_container)
            frame.pack(pady=5, fill=tk.X)
            
            lbl = ttk.Label(frame, text=label, width=15, anchor=tk.W)
            lbl.pack(side=tk.LEFT, padx=5)
            
            entry = tk.Text(frame, height=8, wrap=tk.WORD)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            self.current_input_fields.append(entry)

    def on_generate(self):
        self.generate_btn.config(state=tk.DISABLED)
        self.status_var.set("Processing...")
        
        config = MODEL_CONFIGS[self.model_var.get()]
        inputs = [entry.get("1.0", tk.END).strip() for entry in self.current_input_fields]
        
        # Run in background thread
        threading.Thread(
            target=self.run_generation,
            args=(config, inputs),
            daemon=True
        ).start()

    def run_generation(self, config, inputs):
        try:
            model = AutoModelForCausalLM.from_pretrained(config['model_dir'], device_map="cpu")
            tokenizer = AutoTokenizer.from_pretrained(config['model_dir'])
            
            with open(config['prompt_path'], "r") as f:
                content = f.read()
                
            prompt = config['prompt_formatter'](content, inputs)
            inputs = tokenizer(prompt, return_tensors="pt")
            
            outputs = model.generate(**inputs, max_length=500)
            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            self.update_output(result)
            self.status_var.set("Generation complete")
            
        except Exception as e:
            self.status_var.set("Error occurred")
            self.update_output(f"Error: {str(e)}")
            
        finally:
            self.generate_btn.config(state=tk.NORMAL)

    def update_output(self, text):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, text)
        self.output_area.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = LLMApp()
    app.mainloop()