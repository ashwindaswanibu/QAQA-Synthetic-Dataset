import google.generativeai as palm
import pandas as pd
palm.configure(api_key='')

#To list the available models, we write the below code:

models = [model for model in palm.list_models()]

for model in models:
  print(model.name)

data = pd.read_csv('../../Datasets/Hotpot_Questions.csv')

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

data['Answer_Palm'] = ''

data['False-Assumption'] = ''
for idx, question in enumerate(data['Old Question']):
    contextual_question= answer_context + "New Question: " + question
    false_assumption_question = question + "Answer yes if this question contains a false premise, answer no otherwise." + '\n' + "Answer: "
    
    response = palm.chat(messages=contextual_question, temperature=0.1, context=answer_context)
    
    false_assumption_response = palm.chat(messages=false_assumption_question, temperature=0.2, context=false_premise_context)
    
    # Extract content for author '1'
    answer_content = get_content_from_author1(response)
    
    false_assumption_content = get_content_from_author1(false_assumption_response)

    # Store extracted content in the DataFrame
    data.loc[idx, 'Answer_Palm'] = answer_content
      # Note: Corrected column name from 'Yes/No' to 'Yes/No_Answer'
    data.loc[idx, 'False-Assumption'] = false_assumption_content
    
    # Print extracted content
    print(idx, false_assumption_content)
    
    if idx % 10 == 0:
        data.to_csv('hotpot_incontext_after_eval_palm_target_yes_old.csv', index=False)
        print(f"Saved {idx+1} rows to CSV")





