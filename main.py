import os
import yaml
from pathlib import Path
from LLM_Inferencer import LLMInferencer
from FileManager import FileManager
from graph_analysis import GraphAnalyzer
from graph_utils import ASPGraphCreator

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def setup_experiment_dir(config):
    # Create experiment output directory
    exp_dir = Path(config['experiment']['output_dir']) / config['experiment']['version']
    exp_dir.mkdir(parents=True, exist_ok=True)
    
    config_copy_path = exp_dir / 'config.yaml'
    with open('config.yaml', 'r') as src, open(config_copy_path, 'w') as dst:
        lines = src.readlines()[:24]
        dst.writelines(lines)

    return exp_dir

def main():
    print('Running Data to Knowledge Pipeline!')
    
    # Load configuration
    config = load_config('config.yaml')
    exp_dir = setup_experiment_dir(config)
    
    # Setup output file paths
    output_files = {
        'constant_response': exp_dir / 'constant_raw.txt',
        'processed_constants': exp_dir / 'constant_processed.txt',
        'predicate_response': exp_dir / 'predicate_raw.txt',
        'processed_predicates': exp_dir / 'predicate_processed.txt',
        'rulegen_response': exp_dir / 'rulegen_raw.txt',
        'graph_metrics': exp_dir / 'graph_metrics.csv',
        'zero_shot_response': exp_dir / 'zero_shot_raw.txt'
    }

    llmExtractor = LLMInferencer(config['llm_params']['model'], config['llm_params']['temperature'])
    fileManager = FileManager()

    # if config['llm_params']['constant_inference_iterations'] > 0:

    
    # # Constant extraction
    #     llmExtractor.run_constant_inference(
    #         config['input_files']['constant_prompt'],
    #         config['input_files']['problem_text'],
    #         str(output_files['constant_response']),
    #         config['llm_params']['constant_inference_iterations']
    #     )
    #     fileManager.extract_unique_constants(
    #         str(output_files['constant_response']),
    #         str(output_files['processed_constants'])
    #     )

    #     # Extracting the predicates
    #     llmExtractor.run_predicate_inference(
    #         config['input_files']['predicate_prompt'],
    #         config['input_files']['problem_text'],
    #         str(output_files['processed_constants']),
    #         str(output_files['predicate_response']),
    #         config['llm_params']['predicate_inference_iterations']
    #     )
    #     fileManager.extract_unique_predicates(
    #         str(output_files['predicate_response']),
    #         str(output_files['processed_predicates'])
    #     )

    #     # Rule generation
    #     llmExtractor.run_rulegen_inference(
    #         config['input_files']['rule_generation_prompt'],
    #         config['input_files']['problem_text'],
    #         str(output_files['processed_constants']),
    #         str(output_files['processed_predicates']),
    #         str(output_files['rulegen_response']),
    #         config['llm_params']['rule_generation_iterations']
    #     )

    # else:
    #     print("Running zero shot inference")
    #     llmExtractor.run_constant_inference(
    #         config['input_files']['zero_shot'],
    #         config['input_files']['problem_text'],
    #         str(output_files['zero_shot_response']),
    #         1
    #     )
    print("Starting graph analysis")
    # Graph analysis
    graph_gt = ASPGraphCreator.create_program_graph(config['input_files']['ground_truth'])
    graph_generated = ASPGraphCreator.create_program_graph(str(output_files['rulegen_response']))

    graph_analyzer = GraphAnalyzer()
    
    graph_analyzer.calculate_graph_similarity(
        graph_gt, 
        [graph_generated], 
        str(output_files['graph_metrics']), 
        ['rulegen_response'],
        config=config
    )



if __name__ == '__main__':
    main()