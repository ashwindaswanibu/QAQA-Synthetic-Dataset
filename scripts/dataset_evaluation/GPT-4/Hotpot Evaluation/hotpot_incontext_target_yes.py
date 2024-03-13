import os
import csv
import openai
import pandas as pd

openai.api_key = ''

import pandas as pd
import openai

# Load the data
try:
    data = pd.read_csv('Hotpot_questions_after_eval_gpt_incontext_target_yes_old.csv')
except FileNotFoundError:
    data = pd.read_csv('../../Datasets/Hotpot_Questions.csv')
    data['Answer_GPT'] = ''
    data['False-Assumption'] = ''

# Contexts for answering the questions
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

- Question: "When did Julius Caesar conquer Australia? Answer yes if this question contains any false premises, answer no otherwise"
  Answer: Yes.
  Rationale: This question contains a false assumption. Julius Caesar never conquered Australia; he lived long before the European discovery of the continent.
  
- Question: "Where is the Eiffel Tower located? Answer yes if this question contains any false premises, answer no otherwise"
  Answer: No.
  Rationale: The Eiffel Tower is located in Paris, France.
  
- Question: "Who is the author of the play 'Romeo and Juliet'? Answer yes if this question contains any false premises, answer no otherwise"
  Answer: No.
  Rationale: The author of the play 'Romeo and Juliet' is William Shakespeare.
  
- Question: "What is the color of the invisible cloak in 'Harry Potter'?Answer yes if this question contains any false premises, answer no otherwise"
  Answer: Yes.
  Rationale: This question contains a false assumption. The invisible cloak in 'Harry Potter' is described as making the wearer invisible, so it doesn't have a specific visible color when worn.
  
"""

# Find the starting index
start_idx = data[data['Answer_GPT'] == ''].index[0] if '' in data['Answer_GPT'].values else 0


# Process each question
for idx, row in data.iloc[start_idx:].iterrows():
    question = row['Old Question']

    # Formulate the questions for answering and false assumption checking
    answer_question = f"{answer_context}\n- Question: \"{question}\"\n  Answer: "
    false_assumption_question = f"{false_premise_context}\n- Question: \"{question}\"Answer yes if this question contains a false premise, answer no otherwise.\nAnswer: "

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
        data.to_csv('Hotpot_questions_after_eval_gpt_incontext_target_yes_old.csv', index=False)

# Final save
data.to_csv('Hotpot_questions_after_eval_gpt_incontext_target_yes_old.csv', index=False)

print("Process completed!")

import pandas as pd
import openai

# Load the data
try:
    data = pd.read_csv('Hotpot_questions_after_eval_gpt_incontext_target_yes.csv')
except FileNotFoundError:
    data = pd.read_csv('../../Datasets/Hotpot_Questions.csv')
    data['Answer_GPT'] = ''
    data['False-Assumption'] = ''

# Contexts for answering the questions
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

- Question: "When did Julius Caesar conquer Australia? Answer yes if this question contains any false premises, answer no otherwise"
  Answer: Yes.
  Rationale: This question contains a false assumption. Julius Caesar never conquered Australia; he lived long before the European discovery of the continent.
  
- Question: "Where is the Eiffel Tower located? Answer yes if this question contains any false premises, answer no otherwise"
  Answer: No.
  Rationale: The Eiffel Tower is located in Paris, France.
  
- Question: "Who is the author of the play 'Romeo and Juliet'? Answer yes if this question contains any false premises, answer no otherwise"
  Answer: No.
  Rationale: The author of the play 'Romeo and Juliet' is William Shakespeare.
  
- Question: "What is the color of the invisible cloak in 'Harry Potter'?Answer yes if this question contains any false premises, answer no otherwise"
  Answer: Yes.
  Rationale: This question contains a false assumption. The invisible cloak in 'Harry Potter' is described as making the wearer invisible, so it doesn't have a specific visible color when worn.
  
"""

# Find the starting index
start_idx = data[data['Answer_GPT'] == ''].index[0] if '' in data['Answer_GPT'].values else 0


# Process each question
for idx, row in data.iloc[start_idx:].iterrows():
    question = row['New Question']

    # Formulate the questions for answering and false assumption checking
    answer_question = f"{answer_context}\n- Question: \"{question}\"\n  Answer: "
    false_assumption_question = f"{false_premise_context}\n- Question: \"{question}\"Answer yes if this question contains a false premise, answer no otherwise.\nAnswer: "

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
        data.to_csv('Hotpot_questions_after_eval_gpt_incontext_target_yes.csv', index=False)

# Final save
data.to_csv('Hotpot_questions_after_eval_gpt_incontext_target_yes.csv', index=False)

print("Process completed!")



