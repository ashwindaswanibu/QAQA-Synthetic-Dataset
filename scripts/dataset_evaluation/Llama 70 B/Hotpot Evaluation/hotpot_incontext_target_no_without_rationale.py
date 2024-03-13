!pip install huggingface_hub transformers BitsAndBytes accelerate

answer_context = """ """

false_premise_context = """ """

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
    full_prompt =  "\n- Question: \"" + question + "\""
    generate_text = transformers.pipeline(
        model=model,
        tokenizer=tokenizer,
        return_full_text=True,
        task='text-generation',
        temperature=0.001,
        max_new_tokens=50,
        repetition_penalty=1.1
    )
    generated_output = generate_text(full_prompt)
    return generated_output[0]['generated_text'][len(full_prompt):].strip()


# Process data

def process_data(input_csv, output_csv):
    try:
        data = pd.read_csv(output_csv)
        start_index = data['LLaMA-Answer-Old'].isnull().idxmax()
    except (FileNotFoundError, ValueError):
        data = pd.read_csv(input_csv)
        start_index = 0

    for idx in range(start_index, len(data)):
        question = data['Old Question'].iloc[idx]
        # yes_no_question = data['yes_no_question'].iloc[idx]
        false_assumption_question = question + \
            ''' Is every statement or assumption in this question accurate? Please answer with a simple 'Yes' or 'No'.'''

        response = generate_response(question, answer_context)
        # yes_no_response = generate_response(yes_no_question, yes_no_context)
        false_assumption_response = generate_response(
            false_assumption_question, false_premise_context)

        data.at[idx, 'LLaMA-Answer-Old'] = response
        # data.at[idx, 'LLaMA-Yes/No'] = yes_no_response
        data.at[idx, 'LLaMA-False-Assumption-Old'] = false_assumption_response

        data.to_csv(output_csv, index=False)
        print(idx, question, response, false_assumption_response)

    print("Data processing completed.")

input_csv = '../../Datasets/Hotpot_Questions.csv'
output_csv = 'hotpot_incontext_target_no_without_rationale.csv'
process_data(input_csv, output_csv)



