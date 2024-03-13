!pip install huggingface_hub transformers BitsAndBytes accelerate

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

false_premise_context = """
Give an answer in the following format. First answer Yes/No on whether all the premises in the questions are true and then give a rationale behind your answer. Below are a few examples:

- Question: "When did Julius Caesar conquer Australia? Is every statement or assumption in this question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: No.
  Rationale: Julius Caesar never conquered Australia; this is a false assumption as he lived long before the European discovery of the continent.

- Question: "What is the color of the invisible cloak in 'Harry Potter'? Is every statement or assumption in this question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: No.
  Rationale: The invisible cloak in 'Harry Potter' is described as making the wearer invisible, hence it does not have a specific visible color when worn.

- Question: "Who is the author of the play 'Romeo and Juliet'? Is every statement or assumption in this question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: Yes.
  Rationale: The author of the play 'Romeo and Juliet' is correctly identified as William Shakespeare.

- Question: "Where is the Eiffel Tower located? Is every statement or assumption in this question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: Yes.
  Rationale: The Eiffel Tower is correctly stated to be located in Paris, France.
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

import torch
import pandas as pd
import transformers

# Setup model configuration and tokenizer
model_id = 'meta-llama/Llama-2-70b-chat-hf'
hf_auth = ''

bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

model_config = transformers.AutoConfig.from_pretrained(
    model_id, use_auth_token=hf_auth)
model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config=model_config,
    quantization_config=bnb_config,
    device_map='auto',
    use_auth_token=hf_auth,
    cache_dir="."
)

tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_id, use_auth_token=hf_auth, cache_dir=".")


def generate_response(question, context):
    full_prompt = context + "\n- Question: \"" + question + "\""
    generate_text = transformers.pipeline(
        model=model,
        tokenizer=tokenizer,
        return_full_text=True,
        task='text-generation',
        temperature=0.7,
        max_new_tokens=50,
        repetition_penalty=1.1
    )
    generated_output = generate_text(full_prompt)
    return generated_output[0]['generated_text'][len(full_prompt):].strip()


# Process data

def process_data(input_csv, output_csv):
    try:
        data = pd.read_csv(output_csv)
        start_index = data['LLaMA-Answer'].isnull().idxmax()
    except (FileNotFoundError, ValueError):
        data = pd.read_csv(input_csv)
        start_index = 0

    for idx in range(start_index, len(data)):
        question = data['question'].iloc[idx]
        yes_no_question = data['yes_no_question'].iloc[idx]
        false_assumption_question = question + \
            ''' Is every statement or assumption in this question accurate? Please answer with a simple 'Yes' or 'No'.'''

        response = generate_response(question, answer_context)
        yes_no_response = generate_response(yes_no_question, yes_no_context)
        false_assumption_response = generate_response(
            false_assumption_question, false_premise_context)

        data.at[idx, 'LLaMA-Answer'] = response
        data.at[idx, 'LLaMA-Yes/No'] = yes_no_response
        data.at[idx, 'LLaMA-False-Assumption'] = false_assumption_response

        data.to_csv(output_csv, index=False)
        print(idx, question, response, yes_no_response,
              false_assumption_response)

    print("Data processing completed.")

input_csv = '../../Datasets/Singlehop_question.csv'
output_csv = 'singlehop_incontext_target_no_old.csv'
process_data(input_csv, output_csv)





