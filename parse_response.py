import re


def parse_response(response_text):
    """
    Usage Note:
    This function is designed to parse JSON outputs from large language models (LLMs).
    It cleans the input text by removing these elements, then reconstructs a valid JSON structure.

    An example prompt of LLM to generate Json-format output:

        '''Analyze the following doctor-patient dialogue and complete the following tasks:

        1. **Understand the Patient's Description**: Carefully read the symptoms, behaviors, or situations described by the patient.
        2. **Understand the Patient's Condition**: Based on the dialogue, understand the current condition of the patient.
        3. **Decompose the Condition into Atomic Conditions**: Decompose the patient's condition into multiple atomic conditions based solely on the patient's relevant statements to capture different aspects. Convert any questions into statements.
        4. **Extract Entities and Labels**:
           - From the atomic conditions, identify key entities (symptoms, conditions, descriptions, etc.), without identifying the doctor's advice or medications.
           - Assign a clear label to each entity (e.g., "Symptom" for symptoms, "Condition" for conditions, etc.).
           - Ensure no duplicate entities, do not fabricate or guess, and avoid regenerating existing entities.

        Description:
        {Input}

        Your response should be in JSON format with the following structure:
        {{
          "entities": [
            {{
              "entity": "Symptom, condition, description, etc.",
              "label": "Label type (e.g., Symptom, Condition, etc.)"
            }},
            ...
          ]
        }}'''

    - response_text: str, the raw JSON-formatted output from an LLM.

    Returns:
    Completed JSON format output.
    """

    # Step 1: Remove all {} and []
    cleaned_data = re.sub(r'[{$$}]', '', response_text)

    # Step 2: Reformat the cleaned data back into JSON
    # First, split the data into lines and remove any extra spaces
    lines = [line.strip() for line in cleaned_data.splitlines() if line.strip()]

    # Build a new JSON data structure
    new_entities = []
    current_entity = {}

    for line in lines:
        if 'entity' in line:
            # If encountering a new entity, save the previous one and start a new one
            if current_entity:
                new_entities.append(current_entity)
                current_entity = {}

            # Extract the value of the entity
            entity_value = line.split(':')[-1].strip().strip('"').split('"')[0]
            current_entity['entity'] = entity_value
        elif 'label' in line:
            # Extract the value of the label
            description_value = line.split(':')[-1].strip().strip('"')
            current_entity['label'] = description_value

    # Add the last entity
    if current_entity:
        new_entities.append(current_entity)

    # Construct the final JSON object
    final_json = {'entities': new_entities}

    return final_json