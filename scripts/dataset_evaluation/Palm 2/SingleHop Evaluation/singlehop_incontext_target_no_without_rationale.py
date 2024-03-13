import google.generativeai as palm
import pandas as pd
palm.configure(api_key='')

#To list the available models, we write the below code:

models = [model for model in palm.list_models()]

for model in models:
  print(model.name)

def get_content_from_author1(chat_response):
    try:
        # Get the list of candidates
        candidates = chat_response.candidates
        
        # Extract content for author '1' from candidates
        content = next((c['content'] for c in candidates if c['author'] == '1'), None)
        return content
    except AttributeError:
        print("Error: ChatResponse object structure unexpected or missing 'candidates' attribute.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

data= pd.read_csv('../../Datasets/Singlehop_question.csv')

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

- Question: "When did Julius Caesar conquer Australia? Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: No.
  
- Question: "Where is the Eiffel Tower located?Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: Yes.
  
- Question: "Who is the author of the play 'Romeo and Juliet'? Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'."
  Answer: Yes.
  
- Question: "What is the color of the invisible cloak in 'Harry Potter'? Is every statement or assumption in this previous question accurate? Please answer with a simple 'Yes' or 'No'."
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

data['Answer_Palm'] = ''

data['False-Assumption'] = ''
data['Yes/No_Answer'] = ''
for idx in range(len(data)):
    question = data['question'].iloc[idx]
    yes_no_question = data['yes_no_question'].iloc[idx]
    false_assumption_question =  question + ''' Is every statement or assumption in this question accurate? Please answer with a simple 'Yes' or 'No'.''' + '\n' + "Answer: "
    response = palm.chat(messages=answer_context + question, temperature=0.1, context="QA")
    yes_no_response = palm.chat(messages=yes_no_context + yes_no_question, temperature=0.9, context="QA")
    false_assumption_response = palm.chat(messages=false_premise_context + false_assumption_question, temperature=0.9, context="QA")
    
    # Extract content for author '1'
    answer_content = get_content_from_author1(response)
    
    false_assumption_content = get_content_from_author1(false_assumption_response)
    yes_no_content = get_content_from_author1(yes_no_response)
    # Store extracted content in the DataFrame
    data.loc[idx, 'Answer_Palm'] = answer_content
    data.loc[idx, 'Yes/No_Answer'] = yes_no_content
      # Note: Corrected column name from 'Yes/No' to 'Yes/No_Answer'
    data.loc[idx, 'False-Assumption'] = false_assumption_content
    
    # Print extracted content
    print(idx,    false_assumption_content)
    
    if idx % 10 == 0:
        data.to_csv('singlehop_after_eval_palm_with_incontext_no_without_rationale.csv', index=False)
        print(f"Saved {idx+1} rows to CSV")




