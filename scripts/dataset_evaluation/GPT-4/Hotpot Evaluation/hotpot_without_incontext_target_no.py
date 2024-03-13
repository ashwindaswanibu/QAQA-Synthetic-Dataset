import openai
import pandas as pd

# Set OpenAI API key
openai.api_key = ''

import pandas as pd
import openai

# Load the data
try:
    data = pd.read_csv('Hotpot_questions_after_eval_gpt_without_incontext_target_no_old.csv')
except FileNotFoundError:
    data = pd.read_csv('../../Datasets/Hotpot_Questions.csv')
    data['Answer_GPT'] = ''
    data['False-Assumption'] = ''

# Contexts for answering the questions
# Contexts for answering the questions
answer_context = """ """

# Contexts for identifying false premises
false_premise_context = """ """

# Find the starting index
start_idx = data[data['Answer_GPT'] == ''].index[0] if '' in data['Answer_GPT'].values else 0


# Process each question
for idx, row in data.iloc[start_idx:].iterrows():
    question = row['Old Question']

    # Formulate the questions for answering and false assumption checking
    answer_question = f"{answer_context}\n- Question: \"{question}\"\n  Answer: "
    false_assumption_question = f"{false_premise_context}\n- Question: \"{question}\" Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'.\nAnswer: "

    try:
        # Generate response for answering the question
        answer_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": answer_question}
            ]
        )
        answer = answer_response['choices'][0]['message']['content'].strip()

        # Generate response for checking false assumption
        false_assumption_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": false_assumption_question}
            ]
        )
        false_assumption_answer = false_assumption_response['choices'][0]['message']['content'].strip()

        # Store the responses
        data.at[idx, 'Answer_GPT'] = answer
        data.at[idx, 'False-Assumption'] = false_assumption_answer
        print(false_assumption_answer)
    except Exception as e:
        print(f"Error processing row {idx}: {e}")

    # Save the data periodically
    if idx % 10 == 0:
        data.to_csv('Hotpot_questions_after_eval_gpt_without_incontext_target_no_old.csv', index=False)

# Final save
data.to_csv('Hotpot_questions_after_eval_gpt_without_incontext_target_no_old.csv', index=False)

print("Process completed!")

import pandas as pd
import openai

# Load the data
try:
    data = pd.read_csv('Hotpot_questions_after_eval_gpt_without_incontext_target_no.csv')
except FileNotFoundError:
    data = pd.read_csv('../../Datasets/Hotpot_Questions.csv')
    data['Answer_GPT'] = ''
    data['False-Assumption'] = ''

# Contexts for answering the questions
# Contexts for answering the questions
answer_context = """ """

# Contexts for identifying false premises
false_premise_context = """ """

# Find the starting index
start_idx = data[data['Answer_GPT'] == ''].index[0] if '' in data['Answer_GPT'].values else 0


# Process each question
for idx, row in data.iloc[start_idx:].iterrows():
    question = row['New Question']

    # Formulate the questions for answering and false assumption checking
    answer_question = f"{answer_context}\n- Question: \"{question}\"\n  Answer: "
    false_assumption_question = f"{false_premise_context}\n- Question: \"{question}\" Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'.\nAnswer: "

    try:
        # Generate response for answering the question
        answer_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": answer_question}
            ]
        )
        answer = answer_response['choices'][0]['message']['content'].strip()

        # Generate response for checking false assumption
        false_assumption_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": false_assumption_question}
            ]
        )
        false_assumption_answer = false_assumption_response['choices'][0]['message']['content'].strip()

        # Store the responses
        data.at[idx, 'Answer_GPT'] = answer
        data.at[idx, 'False-Assumption'] = false_assumption_answer
        print(false_assumption_answer)
    except Exception as e:
        print(f"Error processing row {idx}: {e}")

    # Save the data periodically
    if idx % 10 == 0:
        data.to_csv('Hotpot_questions_after_eval_gpt_without_incontext_target_no.csv', index=False)

# Final save
data.to_csv('Hotpot_questions_after_eval_gpt_without_incontext_target_no.csv', index=False)

print("Process completed!")



