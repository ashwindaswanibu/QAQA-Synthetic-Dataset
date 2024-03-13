import openai
import pandas as pd

openai.api_key = ''

import pandas as pd
import openai

# Load the data
try:
    data = pd.read_csv('singlehop_eval_gpt_without_incontext_yes_old.csv')
except FileNotFoundError:
    data = pd.read_csv(
        '../../Datasets/Singlehop_question.csv')
    data['Answer_GPT'] = ''
    data['False-Assumption'] = ''
    data['Yes/No Response']=''


# Find the starting index
start_idx = data[data['Answer_GPT'] == ''].index[0] if '' in data['Answer_GPT'].values else 0


# Process each question
for idx, row in data.iloc[start_idx:].iterrows():
    question = row['original_question']

    # Formulate the questions for answering and false assumption checking
    answer_question = f"Question: \"{question}\"\n  Answer: "
    false_assumption_question = f"Question: \"{question}\"Answer 'Yes' if this question contains any false premises, answer 'No' otherwise..\nAnswer: "
    yes_no_question = f"Question: \"{question}\"\n  Answer: "
    try:
        # Generate response for answering the question
        answer_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": answer_question}
            ]
        )
        answer = answer_response['choices'][0]['message']['content'].strip()

        # Generate response for checking false assumption
        false_assumption_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": false_assumption_question}
            ]
        )
        false_assumption_answer = false_assumption_response['choices'][0]['message']['content'].strip()
        yes_no_response=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": yes_no_question}
            ]
        )
        yes_no_answer = yes_no_response['choices'][0]['message']['content'].strip()
        # Store the responses
        data.at[idx, 'Answer_GPT'] = answer
        data.at[idx, 'False-Assumption'] = false_assumption_answer
        data.at[idx, 'Yes/No Response'] = yes_no_answer
        
    except Exception as e:
        print(f"Error processing row {idx}: {e}")

    # Save the data periodically
    if idx % 10 == 0:
        data.to_csv('singlehop_eval_gpt_without_incontext_yes_old.csv', index=False)

# Final save
data.to_csv('singlehop_eval_gpt_without_incontext_yes_old.csv', index=False)

print("Process completed!")



