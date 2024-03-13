import openai
import pandas as pd

openai.api_key = ''

import pandas as pd
import openai

# Load the data
try:
    data = pd.read_csv('singlehop_eval_gpt_incontext_yes.csv')
except FileNotFoundError:
    data = pd.read_csv(
        '../../Datasets/Singlehop_question.csv')
    data['Answer_GPT'] = ''
    data['False-Assumption'] = ''

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

# Find the starting index (the first row with an empty Answer_GPT)
start_idx = data[data['Answer_GPT'] ==
                 ''].index[0] if '' in data['Answer_GPT'].values else 0

# Process each question starting from start_idx
for idx in range(start_idx, len(data['question'])):
    question = data['question'].iloc[idx]
    yes_no_question = data['yes_no_question'].iloc[idx]
    # Formulate the contextual questions
    answer_question = answer_context + " New Question: " + question
    yes_no_question = yes_no_context + " New Question: " + yes_no_question
    false_assumption_question = false_premise_context + " New Question: " + question + \
        ' Answer yes if this question contains a false premise, answer no otherwise.'

    answer_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=answer_question,
        temperature=0.9,
        max_tokens=1024
    )

    false_assumption_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=false_assumption_question,
        temperature=0.9,
        max_tokens=1024
    )
    yes_no_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=false_assumption_question,
        temperature=0.9,
        max_tokens=1024
    )

    # Store the answers
    data.loc[idx, 'Answer'] = answer_response.choices[0].text.strip()
    data.loc[idx, 'Yes/No'] = yes_no_response.choices[0].text.strip()
    data.loc[idx, 'False-Assumption'] = false_assumption_response.choices[0].text.strip()

    # Save the data
    data.to_csv('singlehop_eval_gpt_incontext_yes.csv', index=False)

print("Process completed!")



