import os 
import re

class FileManager():
    def __init__(self) -> None:
        pass

    def load_file(self, input_file:str) -> str:
        with open(input_file, 'r', encoding='utf-8') as f:
            file_text = f.read()
        return file_text

    def save_file(self, input_text:str, output_file:str) -> None:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(input_text)
            f.close()
        print(f"Saved response to {output_file}")
    

    
    def extract_unique_constants(self, input_file, output_file):
        # Dictionary to store category: set of unique values
        constants = {}
        
        with open(input_file, 'r') as f:
            content = f.read()
            # Split into iterations
            iterations = content.split('---------------Iteration')
            
            for iteration in iterations:
                # Skip empty iterations
                if not iteration.strip():
                    continue
                    
                # Look for Constants section more flexibly
                if 'Constants:' not in iteration:
                    continue
                
                try:
                    # Get the content after "Constants:"
                    constants_section = iteration.split('Constants:')[1].strip()
                    
                    # Process each line
                    for line in constants_section.split('\n'):
                        # Skip empty lines or lines without ':'
                        if not line.strip() or ':' not in line:
                            continue
                        
                        # Split category and values
                        category, values = line.split(':', 1)
                        category = category.strip()
                        
                        # Skip if category is empty
                        if not category:
                            continue
                            
                        # Clean up values and extract quoted strings
                        values = values.strip(' ;.')
                        # Extract strings within quotes, handling both single and double quotes
                        quoted_values = re.findall(r'[""]([^""]*)[""]', values)
                        
                        # Initialize set if category doesn't exist
                        if category not in constants:
                            constants[category] = set()
                        # Add values to set
                        constants[category].update(quoted_values)
                        
                except IndexError:
                    continue  # Skip malformed sections
        
        # Write to output file
        with open(output_file, 'w') as f:
            f.write("Constants:\n")
            for category, values in sorted(constants.items()):
                # Skip empty categories
                if not values:
                    continue
                # Sort values for consistent output
                sorted_values = sorted(values)
                values_str = '"; "'.join(sorted_values)
                f.write(f'{category}: "{values_str}".\n')


    def extract_unique_predicates(self, input_file:str, output_file:str) -> None:
        # Extract unique predicates
        print("Processing the predicates")
        # Regex pattern to match predicates
        # predicate_pattern = re.compile(r"^\d+\.\s(.+)") # for patterns like 1. **
        predicate_pattern = re.compile(r"^\s*-\s*([^)]*\))")
        unique_predicates = set()
        
        with open(input_file, 'r') as infile:
            for line in infile:
                match = predicate_pattern.match(line.strip())
                if match:
                    predicate = match.group(1)
                    unique_predicates.add(predicate)

        # Write unique predicates to the output file
        with open(output_file, 'w') as outfile:
            for predicate in sorted(unique_predicates):  # Sorted for consistent output
                outfile.write(f"{predicate}\n")
        
    