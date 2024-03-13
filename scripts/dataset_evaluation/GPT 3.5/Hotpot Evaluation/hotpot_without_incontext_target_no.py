import openai
import pandas as pd

# Set OpenAI API key
openai.api_key = ''



# Load the data
try:
    data = pd.read_csv('Hotpot_gpt_eval_without_incontext_no.csv')
except FileNotFoundError:
    data = pd.read_csv('../../Datasets/Hotpot_Questions.csv')
    data['Answer_GPT'] = ''
    data['False-Assumption'] = ''

# Find the starting index (the first row with an empty Answer_GPT)
start_idx = data[data['Answer_GPT'] ==
                 ''].index[0] if '' in data['Answer_GPT'].values else 0

# Process each question starting from start_idx
for idx in range(start_idx, len(data['New Question'])):
    question = data['New Question'].iloc[idx]

    # Formulate the false assumption question
    false_assumption_question = question + \
        ''' Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'.'''

    # Fetch the answers from the model
    answer_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        temperature=0.9,
        max_tokens=1024
    )

    false_assumption_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=false_assumption_question,
        temperature=0.9,
        max_tokens=1024
    )

    # Store the answers
    data.loc[idx, 'Answer_GPT'] = answer_response.choices[0].text.strip()
    data.loc[idx, 'False-Assumption'] = false_assumption_response.choices[0].text.strip()

    # Print the progress
    print(idx, question, answer_response.choices[0].text.strip(
    ), false_assumption_response.choices[0].text.strip())

    # Save the data after each question
    data.to_csv('Hotpot_gpt_eval_without_incontext_no.csv', index=False)

print("Process completed!")



