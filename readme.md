# Local LLM Task Specialists

Three specialized language models for different professional tasks, optimized for local CPU execution.

## Repository Structure

── codingHelper/  
│ ├── DeepSeek-R1-Distill-Qwen-7B/ # Coding assistant model  
│ ├── codingHelper.py # Main script  
│ ├── codingHelper.txt # Prompt template  
│ └── codingHelper.yaml # Configuration  
├── lectureNotes/  
│ ├── DeepSeek-R1-Distill-Qwen-1.5B/ # Summarization model  
│ ├── lectureNotes.py # Main script  
│ ├── lectureNotes.txt # Prompt template  
│ └── lectureNotes.yaml # Configuration  
├── resumeBuilder/  
│ ├── DeepSeek-R1-Distill-Qwen-7B/ # Resume builder model  
│ ├── resumeBuilder.py # Main script  
│ ├── resumeBuilder.txt # Prompt template  
│ └── resumeBuilder.yaml # Configuration  
├── .gitignore  
└── README.md  


## Model Selection Rationale

| Task                 | Model                        | Key Strengths                        |
|----------------------|------------------------------|---------------------------------------|
| Resume Building      | DeepSeek-R1-Distill-Qwen-7B   | Professional tone, structured output  |
| Coding Assistance    | DeepSeek-R1-Distill-Qwen-7B   | Technical reasoning, problem solving  |
| Lecture Summarization| DeepSeek-R1-Distill-Qwen-1.5B | Efficient text condensation           |



🎯 Design Decisions
CPU-First Architecture

    Optimized for local execution without GPU requirements
    8-bit quantization support for memory efficiency

Task-Specific Optimization

    Separate models for different cognitive workloads
    Balance between model size and task requirements

Privacy Focus

    No data leaves local machine
    Complete control over sensitive information

Modular Design

    Easy swapping of models/prompts
    Independent task components

💻 Hardware Requirements
Component	Minimum	Recommended
RAM	8GB (1.5B model)	16GB (7B models)
Storage	15GB	30GB
Processor	x86-64 CPU	Modern multi-core CPU

⚠️ Limitations
Performance Constraints

    Slower than GPU-accelerated systems
    Complex tasks may require multiple iterations

Memory Management

    7B models require ~15GB RAM
    Very long inputs may need chunking

Model Initialization

    First run takes longer to load models
    Requires manual model downloads

📝 Customization

    Edit the .txt files to modify prompts
    Adjust max_length in scripts for different output sizes
    Modify temperature in generation parameters (0.1-1.0 range)
