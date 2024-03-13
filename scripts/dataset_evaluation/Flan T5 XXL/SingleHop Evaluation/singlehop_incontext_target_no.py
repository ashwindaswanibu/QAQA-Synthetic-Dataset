import os
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM

# Contexts for answering the questions
answer_context = """
Answer the following 'wh' questions:

- Question: "When did Julius Caesar conquer Australia?"
  Answer: This question contains a false assumption. Julius Caesar never conquered Australia; he lived long before the European discovery of the continent.

- Question: "What is the color of the invisible cloak in 'Harry Potter'?"
  Answer: This question contains a false assumption. The invisible cloak in 'Harry Potter' is described as making the wearer invisible, so it doesn't have a specific visible color when worn.

- Question: "Who is the author of the play 'Romeo and Juliet'?"
  Answer: The author of the play 'Romeo and Juliet' is William Shakespeare.

- Question: "Where is the Eiffel Tower located?"
  Answer: The Eiffel Tower is located in Paris, France.
"""

# Contexts for identifying false premises
false_premise_context = """
Give answer in the following format. First answer Yes/No on whether the question contains any false premises and then give a rationale behind your answer. Below are few examples

- Question: "When did Julius Caesar conquer Australia? Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: No.
  Rationale: This question contains a false assumption. Julius Caesar never conquered Australia; he lived long before the European discovery of the continent.
  
- Question: "Where is the Eiffel Tower located? Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: Yes.
  Rationale: The Eiffel Tower is located in Paris, France.
  
- Question: "Who is the author of the play 'Romeo and Juliet'? Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: Yes.
  Rationale: The author of the play 'Romeo and Juliet' is William Shakespeare.
  
- Question: "What is the color of the invisible cloak in 'Harry Potter'?Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: No.
  Rationale: This question contains a false assumption. The invisible cloak in 'Harry Potter' is described as making the wearer invisible, so it doesn't have a specific visible color when worn.
  
"""
yes_no_context = """
Answer 'Yes' or 'No' to the following questions:

- Question: "Did Julius Caesar conquer Australia?"
  Answer: No.

- Question: "Is the invisible cloak in 'Harry Potter' visibly colored?"
  Answer: No.

- Question: "Is William Shakespeare the author of the play 'Romeo and Juliet'?"
  Answer: Yes.

- Question: "Is the Eiffel Tower located in Paris, France?"
  Answer: Yes.
"""


def generate_response(model, tokenizer, question):
    inputs = tokenizer.encode(question, return_tensors="pt")
    outputs = model.generate(inputs, max_length=150)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.strip()


def process_data(data, model, tokenizer, model_name):
    # Check if the necessary columns exist and determine the start index
    if model_name + '-Answer' in data.columns and model_name + '-False-Assumption' in data.columns and model_name + '-Yes-No' in data.columns:
        start_index = data[model_name + '-Answer'].isnull().idxmax()
    else:
        start_index = 0
        data[model_name + '-Answer'] = pd.NA
        data[model_name + '-False-Assumption'] = pd.NA
        data[model_name + '-Yes-No'] = pd.NA

    for idx in range(start_index, len(data)):
        question = data['original_question'].iloc[idx]
        false_assumption_question = false_premise_context + " New Question: " + question + \
            ''' Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'.''' + '\n'+ 'Answer: '
        yes_no_question = data['yes_no_question'].iloc[idx]
        # Generate responses
        answer_question = answer_context + " New Question: " + question
        response = generate_response(model, tokenizer, answer_question)
        yes_no_response = generate_response(
            model, tokenizer, yes_no_context + " New Question: " + yes_no_question)
        false_assumption_response = generate_response(
            model, tokenizer, false_assumption_question)

        # Store responses in the respective columns
        data.at[idx, model_name + '-Answer'] = response
        data.at[idx, model_name + '-Yes-No'] = yes_no_response
        data.at[idx, model_name + '-False-Assumption'] = false_assumption_response

        # Save after each response generation
        data.to_csv(
            'singlehop_incontext_responses_flan_target_no_old.csv', index=False)
        print(false_assumption_response)

    print(f"Data processing for {model_name} completed.")


# Try to load the existing data
try:
    data = pd.read_csv('singlehop_incontext_responses_flan_target_no_old.csv')
except (FileNotFoundError, ValueError):
    data = pd.read_csv(
        '../../Datasets/Singlehop_question.csv')


# Flan-UL2
flan_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-xxl")
flan_model = AutoModelForSeq2SeqLM.from_pretrained(
    "google/flan-t5-xxl",  cache_dir='.')
process_data(data, flan_model, flan_tokenizer, 'Flan-UL2')
del flan_model

pip install transformers --upgrade



