import openai
import pandas as pd

openai.api_key = ''

import pandas as pd
import openai

# Load the data
try:
    data = pd.read_csv('singlehop_eval_unperturbed_target_no_without_rationale.csv')
except FileNotFoundError:
    data = pd.read_csv(
        '../../Datasets/singlehop_unperturbed.csv')
    data['Answer_GPT'] = ''
    data['False-Assumption'] = ''
    data['Yes/No Response']=''

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
  
- Question: "Where is the Eiffel Tower located? Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: Yes.
  
- Question: "Who is the author of the play 'Romeo and Juliet'? Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: Yes.
  
- Question: "What is the color of the invisible cloak in 'Harry Potter'?Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: No.
  
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

# Find the starting index
start_idx = data[data['Answer_GPT'] == ''].index[0] if '' in data['Answer_GPT'].values else 0


# Process each question
for idx, row in data.iloc[start_idx:].iterrows():
    question = row['original_question']
    yes_no_question = row['unperturbed_yes_no_question']

    # Formulate the questions for answering and false assumption checking
    answer_question = f"{answer_context}\n- Question: \"{question}\"\n  Answer: "
    false_assumption_question = f"{false_premise_context}\n- Question: \"{question}\" Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'.\nAnswer: "
    yes_no_question = f"{yes_no_context}\n- Question: \"{yes_no_question}\"\n  Answer: "
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
        data.to_csv('singlehop_eval_gpt_incontext_no_without_rationale_old.csv', index=False)

# Final save
data.to_csv('singlehop_eval_gpt_incontext_no_without_rationale_old.csv', index=False)

print("Process completed!")




