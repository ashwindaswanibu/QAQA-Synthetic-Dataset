import openai
import pandas as pd

openai.api_key = ''



# Load the data
try:
    data = pd.read_csv('singlehop_eval_gpt_without_incontext_no_unperturbed.csv')
except FileNotFoundError:
    data = pd.read_csv(
        '../../Datasets/singlehop_unperturbed.csv')
    data['Answer_GPT'] = ''
    data['False-Assumption'] = ''
    data['Yes/No Response']=''


# Find the starting index
start_idx = data[data['Answer_GPT'] == ''].index[0] if '' in data['Answer_GPT'].values else 0


# Process each question
for idx, row in data.iloc[start_idx:].iterrows():
    question = row['question']
    yes_no_question = row['unperturbed_yes_no_question']
    # Formulate the questions for answering and false assumption checking
    answer_question = f"Question: \"{question}\"\n  Answer: "
    false_assumption_question = f"Question: \"{question}\" Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'.\nAnswer: "
    yes_no_question = f"Question: \"{yes_no_question}\"\n  Answer: "
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
        yes_no_response=openai.ChatCompletion.create(
            model="gpt-4",
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
        data.to_csv('singlehop_eval_gpt_without_incontext_no_unperturbed.csv', index=False)

# Final save
data.to_csv('singlehop_eval_gpt_without_incontext_no_unperturbed.csv', index=False)

print("Process completed!")



