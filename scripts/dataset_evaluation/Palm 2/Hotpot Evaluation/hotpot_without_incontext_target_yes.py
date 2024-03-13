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


data= pd.read_csv('../../Datasets/Hotpot_Questions.csv')

data['Answer_Palm'] = ''

data['False-Assumption'] = ''
for idx, question in enumerate(data['New Question']):
    
    false_assumption_question = question + 'Does this question contain any false premises? Please answer with only Yes/No. Dont elaborate at all'
    
    response = palm.chat(messages=question, temperature=0.1, context="QA")
    
    false_assumption_response = palm.chat(messages=false_assumption_question, temperature=0.9, context="QA")
    
    # Extract content for author '1'
    answer_content = get_content_from_author1(response)
    
    false_assumption_content = get_content_from_author1(false_assumption_response)

    # Store extracted content in the DataFrame
    data.loc[idx, 'Answer_Palm'] = answer_content
      # Note: Corrected column name from 'Yes/No' to 'Yes/No_Answer'
    data.loc[idx, 'False-Assumption'] = false_assumption_content
    
    # Print extracted content
    print(idx,    false_assumption_content)
    
    if idx % 10 == 0:
        data.to_csv('hotpot_after_eval_palm_without_incontext_target_yes.csv', index=False)
        print(f"Saved {idx+1} rows to CSV")




