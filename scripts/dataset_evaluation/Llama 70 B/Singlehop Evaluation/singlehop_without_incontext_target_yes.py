!pip install huggingface_hub transformers BitsAndBytes accelerate

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


def generate_response(question):
    generate_text = transformers.pipeline(
        model=model,
        tokenizer=tokenizer,
        return_full_text=True,
        task='text-generation',
        temperature=0.001,
        max_new_tokens=32,
        repetition_penalty=1.1
    )
    generated_output = generate_text(question)
    return generated_output[0]['generated_text'][len(question):].strip()

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
            'Answer yes if this question contains any false premises, answer no otherwise.'

        response = generate_response(question)
        yes_no_response = generate_response(yes_no_question)
        false_assumption_response = generate_response(
            false_assumption_question)

        data.at[idx, 'LLaMA-Answer'] = response
        data.at[idx, 'LLaMA-Yes/No'] = yes_no_response
        data.at[idx, 'LLaMA-False-Assumption'] = false_assumption_response

        data.to_csv(output_csv, index=False)
        print(idx, question, response, yes_no_response,
              false_assumption_response)

    print("Data processing completed.")

input_csv = '../../Datasets/Singlehop_question.csv'
output_csv = 'singlehop_without_incontext_target_yes.csv'
process_data(input_csv, output_csv)



