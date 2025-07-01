from LLM_Inferencer import LLMInferencer
import subprocess
import tempfile
import os
import re


def collect_unique_patient_data(file_path):
    """
    Process a file containing patient data from multiple iterations and
    collect all unique constants for each patient.
    
    Args:
        file_path: Path to the file containing patient data
        
    Returns:
        Dictionary mapping patient numbers to sets of unique constants
    """
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split the content by iterations
    # Split by iterations and filter out the headers
    iterations = content.split('---------------Iteration')
    iterations = [it.split('\n', 1)[1] if '\n' in it else it for it in iterations if it.strip()]
    # Dictionary to store unique constants for each patient
    patient_data = {}
    
    # Process each iteration
    for iteration in iterations:
        # Split by patient
        patients = iteration.split('Patient ')
        patients = [p for p in patients if p.strip()]
        
        for patient in patients:
            # Extract patient number
            lines = patient.strip().split('\n')
            patient_num = int(lines[0].split(':')[0])
            
            # Initialize patient entry if not exists
            if patient_num not in patient_data:
                patient_data[patient_num] = set()
            
            # Extract constants (lines ending with period)
            for line in lines[1:]:
                line = line.strip()
                if line.endswith('.'):
                    patient_data[patient_num].add(line)
    
    return patient_data

def write_consolidated_patient_data(input_file, output_file):
    """
    Process patient data from input file and write consolidated unique data to output file.
    
    Args:
        input_file: Path to the input file with iterations
        output_file: Path to write the consolidated output
    """
    patient_data = collect_unique_patient_data(input_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(output_file, 'w') as file:
        file.write("---------------Consolidated Patient Data----------------\n\n")
        
        for patient_num in sorted(patient_data.keys()):
            file.write(f"Patient {patient_num}:\n")
            for constant in sorted(patient_data[patient_num]):
                file.write(f"{constant}\n")
            file.write("\n")

def run_clingo_for_ground_truth(lp_file_path, gt_file_path, output_file_path=None):
    """
    For each patient in the ground truth file:
    1. Extract patient facts from the ground truth file
    2. Append the facts to the .lp file
    3. Run clingo on the combined file
    4. Record the output
    
    Args:
        lp_file_path (str): Path to the ASP logic program (.lp file)
        gt_file_path (str): Path to the ground truth file with patient descriptions
        output_file_path (str, optional): Path to save the results. If None, results are only printed.
    
    Returns:
        dict: Dictionary mapping patient IDs to clingo outputs
    """
    
    # Read the original .lp file content
    with open(lp_file_path, 'r') as f:
        lp_content = f.read()
    
    # Read the ground truth file
    with open(gt_file_path, 'r') as f:
        gt_content = f.read()
    
    # Dictionary to store results
    results = {}
    
    # Split the content into patient sections
    patient_sections = re.split(r'Patient \d+:', gt_content)[1:]  # Skip the first empty section
    patient_ids = re.findall(r'Patient (\d+):', gt_content)
    
    # Process each patient
    for patient_id, section in zip(patient_ids, patient_sections):
        print(f"Processing Patient {patient_id}...")
        
        # Extract facts from the section
        facts = []
        for line in section.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('%'):  # Skip empty lines and comments
                facts.append(line)
        
        # Create a temporary file with the combined content
        with tempfile.NamedTemporaryFile(suffix='.lp', delete=False) as temp_file:
            temp_file_path = temp_file.name
            # Write original .lp content
            temp_file.write(lp_content.encode())
            # Add a newline if needed
            if not lp_content.endswith('\n'):
                temp_file.write(b'\n')
            # Write patient facts
            temp_file.write(('\n'.join(facts) + '\n').encode())
            
            # Print temp file contents]
            
            # temp_file.seek(0)
            # print(f"\nTemporary file contents for Patient {patient_id}:")
            # print(temp_file.read().decode())
            # print("-" * 50)
        
        try:
            # Run clingo on the temporary file
            result = subprocess.run(
                ['clingo', '--warn=no-atom-undefined', temp_file_path, '0'],
                capture_output=True, 
                text=True
            )
            
            # Store the output
            results[patient_id] = result.stdout
            
        except subprocess.CalledProcessError as e:
            # Handle clingo errors
            results[patient_id] = f"ERROR: {e.stderr}"
            print(f"Error running clingo for Patient {patient_id}:")
            print(e.stderr)
            print("-" * 50)
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
    
    # Save results to file if requested
    if output_file_path:
        with open(output_file_path, 'w') as f:
            for patient_id, output in results.items():
                f.write(f"=== Patient {patient_id} ===\n")
                f.write(output)
                f.write("\n" + "=" * 50 + "\n\n")
        print(f"Results saved to {output_file_path}")
    
    return results

def filter_clingo_results(clingo_results_path, facts_path, output_path=None):
    """
    For each patient and each answer set in the clingo results:
    1. Extract the facts from the facts file for that patient
    2. Remove those facts from each answer set
    3. Print or save the filtered answer sets showing only new inferences
    
    Args:
        clingo_results_path (str): Path to the clingo results file
        facts_path (str): Path to the facts file containing patient data
        output_path (str, optional): Path to save the filtered results. If None, results are only printed.
    """
    # Read the facts file and organize by patient
    with open(facts_path, 'r') as f:
        facts_content = f.read()
    
    # Parse patient facts
    patient_facts = {}
    current_patient = None
    
    for line in facts_content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Check for patient header
        if line.startswith('Patient '):
            current_patient = line.split(' ')[1].rstrip(':')
            patient_facts[current_patient] = set()
        elif current_patient and line.endswith('.'):
            # Remove the trailing period for comparison
            fact = line[:-1]
            patient_facts[current_patient].add(fact)
    
    # Read the clingo results file
    with open(clingo_results_path, 'r') as f:
        clingo_content = f.read()
    
    # Split by patient sections
    patient_sections = clingo_content.split('=== Patient ')
    
    # Prepare output
    output_text = []
    
    # Process each patient section (skip the first empty section if it exists)
    for i, section in enumerate(patient_sections):
        # print(section)
        if not section.strip():
            continue
            
        # Extract patient ID and content
        parts = section.split(' ===\n', 1)
        parts2 = parts[1].split('\nSATISFIABLE', 1)
        parts3 = [parts[0], parts2[0]]

        if len(parts3) < 2:
            continue
            
        patient_id = parts3[0]
        content = parts3[1]
        
        # Get the facts for this patient
        patient_fact_set = patient_facts.get(patient_id, set())
        
        # Process each answer set
        answer_sets = []
        for answer_block in content.split('Answer: '):
            if not answer_block.strip():
                continue
                
            # Extract answer number and atoms
            lines = answer_block.strip().split('\n', 1)
            if len(lines) < 2:
                continue
                
            answer_num = lines[0]
            atoms = lines[1].strip()
            
            # Skip if this is not an answer set
            if 'SATISFIABLE' in atoms or 'UNSATISFIABLE' in atoms:
                continue
                
            # Split atoms and filter out those in the facts file
            atom_list = atoms.split()
        
            filtered_atoms = [atom for atom in atom_list if atom not in patient_fact_set]
            
            # Add to answer sets if there are any atoms left
            if filtered_atoms:
                answer_sets.append(f"Answer: {answer_num}\n{' '.join(filtered_atoms)}")
        
        # Add to output if there are any filtered answer sets
        if answer_sets:
            output_text.append(f"=== Patient {patient_id} ===\n" + "\n\n".join(answer_sets))
    
    # Join all output sections
    final_output = "\n\n" + "="*50 + "\n\n".join(output_text)
    
    # Save to file or print
    if output_path:
        with open(output_path, 'w') as f:
            f.write(final_output)
        print(f"Filtered results saved to {output_path}")
    else:
        print(final_output)
    
    return final_output


if __name__ == "__main__":
    # Initialise the LLM Inferencer
    llm_inferencer = LLMInferencer(model="llama-3.3-70b-versatile", temperature=0.0001)

    # Extract the atoms from the ground truth
    llm_inferencer.extract_atoms(
        prompt_template="input_files/K2P/setupProgram.txt",
        rules="input_files/ground_truths/GT_PC.lp",
        descriptions="input_files/K2P/PC_descriptions.txt",
        output_file="output_files/K2P/PC/PC_descriptions_gt.txt",
        iterations=1
    )
    write_consolidated_patient_data("output_files/K2P/PC/PC_descriptions_gt.txt", "output_files/K2P/PC/PC_facts_gt.txt")

    # Extract the atoms from the generated rules
    llm_inferencer.extract_atoms(
        prompt_template="input_files/K2P/setupProgram.txt",
        rules="output_files/PC/PC_D2K_Claude/1/rulegen_raw.lp",
        descriptions="input_files/K2P/PC_descriptions.txt",
        output_file="output_files/K2P/PC/PC_descriptions_gen.txt",
        iterations=1
    )
    write_consolidated_patient_data("output_files/K2P/PC/PC_descriptions_gen.txt", "output_files/K2P/PC/PC_facts_gen.txt")


    print("Running clingo for ground truth (PC)")
    results_gt = run_clingo_for_ground_truth(
        lp_file_path="input_files/ground_truths/GT_PC.lp",
        gt_file_path="output_files/K2P/PC/PC_facts_gt.txt",
        output_file_path="output_files/K2P/PC/PC_gt_clingo_results.txt"
    )
    print("Running clingo for generated rules (PC)")
    results_generated = run_clingo_for_ground_truth(
        lp_file_path="output_files/PC/PC_D2K_Claude/1/rulegen_raw.lp",
        gt_file_path="output_files/K2P/PC/PC_facts_gen.txt",
        output_file_path="output_files/K2P/PC/PC_gen_clingo_results.txt"
    )
    print('\n')

    print("Filtering clingo results for ground truth (PC)")
    filter_clingo_results(
        "output_files/K2P/PC/PC_gt_clingo_results.txt",
        "output_files/K2P/PC/PC_facts_gt.txt",
        "output_files/K2P/PC/PC_filtered_clingo_results_gt.txt"
    )
    print("Filtering clingo results for generated rules (PC)")
    filter_clingo_results(
        "output_files/K2P/PC/PC_gen_clingo_results.txt",
        "output_files/K2P/PC/PC_facts_gen.txt",
        "output_files/K2P/PC/PC_filtered_clingo_results_gen.txt"
    )




