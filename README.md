
# NICE2ASP

NICE2ASP is a pipeline for extracting knowledge from clinical guidelines using large language models (LLMs) and converting it into Answer Set Programming (ASP) rules. The pipeline supports multiple LLM providers (Groq, OpenAI, Anthropic) and outputs both intermediate and final artifacts for downstream analysis.

## 1. Setup and Installation

### Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/installation/)
- (Recommended) [virtualenv](https://virtualenv.pypa.io/en/latest/)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd NICE2ASP
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API keys:**
   - Obtain API keys from the following providers as needed:
     - [Groq](https://console.groq.com/home)
     - [OpenAI](https://platform.openai.com/api-keys)
     - [Anthropic](https://docs.anthropic.com/en/api/admin-api/apikeys/get-api-key)
   - Create a file named `API_KEYS.py` in the project root with the following structure (replace with your actual keys):
     ```python
     API_KEYS = {
         'ANTHROPIC_API_KEY': 'your_anthropic_key_here',
         'GROQ_API_KEY': 'your_groq_key_here',
         'OPENAI_API_KEY': 'your_openai_key_here',
     }
     ```
   - **Note:** Do not commit your API keys to version control. This is sensitve information so you will want to add it in a .gitignore

5. **Configure the experiment:**
   - Edit `config.yaml` to specify:
     - Experiment name, version, and output directory
     - Input file locations (problem text, prompts, ground truth)
     - LLM parameters (model, temperature, number of iterations)
   - Example:
     ```yaml
     experiment:
       name: "pancreatic_cancer_guidelines"
       version: "1"
       output_dir: "outputs/PC/PC_D2K_Claude"

     input_files:
       problem_text: "input_files/input_guidelines/pancreatic_cancer_guidelines.txt"
       constant_prompt: "input_files/prompt_files/PC/constant_prompt.txt"
       predicate_prompt: "input_files/prompt_files/PC/predicate_prompt.txt"
       rule_generation_prompt: "input_files/prompt_files/PC/rule_generation_prompt.txt"
       ground_truth: "input_files/ground_truths/GT_PC.lp"

     llm_params:
       constant_inference_iterations: 1
       predicate_inference_iterations: 1
       rule_generation_iterations: 1
       model: "claude-3-7-sonnet-20250219"
       temperature: 0.25
     ```

## 2. Running the Pipeline

To execute the pipeline, run:

```bash
python main.py
```

This will:
- Load the configuration from `config.yaml`
- Run the LLM-based extraction and rule generation
- Perform graph-based analysis and output results to the specified directory

## 3. Input and Output

### Input

- **Problem Text:** Clinical guideline in plain text (e.g., `input_files/input_guidelines/pancreatic_cancer_guidelines.txt`)
- **Prompt Files:** Text prompts for constants, predicates, and rule generation (e.g., `input_files/prompt_files/PC/constant_prompt.txt`)
- **Ground Truth:** Reference ASP program for evaluation (e.g., `input_files/ground_truths/GT_PC.lp`)

### Output

All outputs are saved in a subdirectory under the specified `output_dir` and `version` in `config.yaml`. Example outputs include:

- `constant_raw.txt` / `constant_processed.txt`: Raw and processed constants extracted by the LLM
- `predicate_raw.txt` / `predicate_processed.txt`: Raw and processed predicates
- `rulegen_raw.lp`: Generated ASP rules
- `graph_metrics.csv`: Graph-based similarity metrics between generated and ground truth programs
- `config.yaml`: Copy of the configuration used for the run

#### Example: `graph_metrics.csv`
| experiment_name | model | wl_similarity | emd_adjusted_similarity | accuracy | ... |
|-----------------|-------|---------------|------------------------|----------|-----|
| output_files/32 | claude-3-7-sonnet-20250219 | 0.27301 | 0.87609 | 0.84091 | ... |

#### Example: `rulegen_raw.lp`
```prolog
offer("pancreatic_protocol_CT_scan") :- have("obstructive_jaundice"), suspected(cancer("pancreas")), not offered("draining_the_bile_duct").
...
```

## 4. Metadata and Artifact Characterization

- **Configuration:** Each run is characterized by its `config.yaml`, which is copied into the output directory for reproducibility.
- **Experiment Metadata:** Output files and metrics are versioned by experiment name and version.
- **API Keys:** Required for LLM access, but not included in the repository.
- **Input/Output Traceability:** All input files and generated outputs are referenced in the configuration and output directories.

## 5. Notes

- **Sensitive Information:** Do not include real API keys in any committed files.
- **Reproducibility:** Ensure all input files and configuration are preserved for each experiment.
- **Extensibility:** You can add new guidelines, prompts, or models by updating the input files and configuration.

