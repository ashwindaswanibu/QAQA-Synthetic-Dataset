#FLAN_INCONTEXT 

#HOTPOT-INCONTEXT-NO

import pandas as pd
import matplotlib.pyplot as plt
import re
# Read the latest CSV file into a DataFrame again
df_latest = pd.read_csv('hotpot_incontext_responses_flan_target_yes_without_rationale_old.csv')

# The correct column name is 'False-Assumption'
false_assumption_column = 'Flan-UL2-False-Assumption'

yes_responses = df_latest[false_assumption_column].str.startswith('Yes').sum()
no_responses = df_latest[false_assumption_column].str.startswith('No').sum()
other_responses = len(df_latest) - yes_responses - no_responses

# Let's create a bar chart with this data
response_counts = pd.Series({
    'Yes': yes_responses,
    'No': no_responses,
    'Other': other_responses,
})

# Recalculate percentages
total = len(df_latest)
yes_percentage = (yes_responses / total) * 100
no_percentage = (no_responses / total) * 100
others_percentage = (other_responses/ total) * 100

print(yes_percentage)
print(no_percentage)
print(others_percentage)

# Plotting the bar chart
response_counts.plot(kind='bar', figsize=(10, 5), color=['blue'])
plt.title('Response Counts in False-Assumption Column')
plt.xlabel('Response Type')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

#HOTPOT-INCONTEXT-NO-WITHOUT-RATIONALE

import pandas as pd
import matplotlib.pyplot as plt
import re
# Read the latest CSV file into a DataFrame again
df_latest = pd.read_csv('hotpot_incontext_responses_flan_target_no_without_rationale.csv')

# The correct column name is 'False-Assumption'
false_assumption_column = 'Flan-UL2-False-Assumption'

yes_responses = df_latest[false_assumption_column].str.startswith('Yes').sum()
no_responses = df_latest[false_assumption_column].str.startswith('No').sum()
other_responses = len(df_latest) - yes_responses - no_responses

# Let's create a bar chart with this data
response_counts = pd.Series({
    'Yes': yes_responses,
    'No': no_responses,
    'Other': other_responses,
})

# Recalculate percentages
total = len(df_latest)
yes_percentage = (yes_responses / total) * 100
no_percentage = (no_responses / total) * 100
others_percentage = (other_responses/ total) * 100

print(yes_percentage)
print(no_percentage)
print(others_percentage)

# Plotting the bar chart
response_counts.plot(kind='bar', figsize=(10, 5), color=['blue'])
plt.title('Response Counts in False-Assumption Column')
plt.xlabel('Response Type')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

#HOTPOT-INCONTEXT-YES

import pandas as pd
import matplotlib.pyplot as plt
import re
# Read the latest CSV file into a DataFrame again
df_latest = pd.read_csv('hotpot_incontext_responses_flan_target_yes.csv')

# The correct column name is 'False-Assumption'
false_assumption_column = 'Flan-UL2-False-Assumption'

yes_responses = df_latest[false_assumption_column].str.startswith('Yes').sum()
no_responses = df_latest[false_assumption_column].str.startswith('No').sum()
other_responses = len(df_latest) - yes_responses - no_responses

# Let's create a bar chart with this data
response_counts = pd.Series({
    'Yes': yes_responses,
    'No': no_responses,
    'Other': other_responses,
})

# Recalculate percentages
total = len(df_latest)
yes_percentage = (yes_responses / total) * 100
no_percentage = (no_responses / total) * 100
others_percentage = (other_responses/ total) * 100

print(yes_percentage)
print(no_percentage)
print(others_percentage)

# Plotting the bar chart
response_counts.plot(kind='bar', figsize=(10, 5), color=['blue'])
plt.title('Response Counts in False-Assumption Column')
plt.xlabel('Response Type')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

#HOTPOT-INCONTEXT-YES-WITHOUT-RATIONALE

import pandas as pd
import matplotlib.pyplot as plt
import re
# Read the latest CSV file into a DataFrame again
df_latest = pd.read_csv('hotpot_incontext_responses_flan_target_yes_without_rationale.csv')

# The correct column name is 'False-Assumption'
false_assumption_column = 'Flan-UL2-False-Assumption'

yes_responses = df_latest[false_assumption_column].str.startswith('Yes').sum()
no_responses = df_latest[false_assumption_column].str.startswith('No').sum()
other_responses = len(df_latest) - yes_responses - no_responses

# Let's create a bar chart with this data
response_counts = pd.Series({
    'Yes': yes_responses,
    'No': no_responses,
    'Other': other_responses,
})

# Recalculate percentages
total = len(df_latest)
yes_percentage = (yes_responses / total) * 100
no_percentage = (no_responses / total) * 100
others_percentage = (other_responses/ total) * 100

print(yes_percentage)
print(no_percentage)
print(others_percentage)

# Plotting the bar chart
response_counts.plot(kind='bar', figsize=(10, 5), color=['blue'])
plt.title('Response Counts in False-Assumption Column')
plt.xlabel('Response Type')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

#SINGLEHOP-INCONTEXT-NO

import pandas as pd
import matplotlib.pyplot as plt
import re
# Read the latest CSV file into a DataFrame again
df_latest = pd.read_csv('singlehop_eval_gpt_incontext_no.csv')

# The correct column name is 'False-Assumption'
false_assumption_column = 'False-Assumption'

yes_responses = df_latest[false_assumption_column].str.startswith('Yes').sum()
no_responses = df_latest[false_assumption_column].str.startswith('No').sum()
other_responses = len(df_latest) - yes_responses - no_responses

# Let's create a bar chart with this data
response_counts = pd.Series({
    'Yes': yes_responses,
    'No': no_responses,
    'Other': other_responses,
})

# Recalculate percentages
total = len(df_latest)
yes_percentage = (yes_responses / total) * 100
no_percentage = (no_responses / total) * 100
others_percentage = (other_responses/ total) * 100

print(yes_percentage)
print(no_percentage)
print(others_percentage)

# Plotting the bar chart
response_counts.plot(kind='bar', figsize=(10, 5), color=['blue'])
plt.title('Response Counts in False-Assumption Column')
plt.xlabel('Response Type')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

#SINGLEHOP-INCONTEXT-NO-WITHOUT-RATIONALE

import pandas as pd
import matplotlib.pyplot as plt
import re
# Read the latest CSV file into a DataFrame again
df_latest = pd.read_csv('singlehop_eval_gpt_incontext_no_without_rationale.csv')

# The correct column name is 'False-Assumption'
false_assumption_column = 'False-Assumption'

yes_responses = df_latest[false_assumption_column].str.startswith('Yes').sum()
no_responses = df_latest[false_assumption_column].str.startswith('No').sum()
other_responses = len(df_latest) - yes_responses - no_responses

# Let's create a bar chart with this data
response_counts = pd.Series({
    'Yes': yes_responses,
    'No': no_responses,
    'Other': other_responses,
})

# Recalculate percentages
total = len(df_latest)
yes_percentage = (yes_responses / total) * 100
no_percentage = (no_responses / total) * 100
others_percentage = (other_responses/ total) * 100

print(yes_percentage)
print(no_percentage)
print(others_percentage)

# Plotting the bar chart
response_counts.plot(kind='bar', figsize=(10, 5), color=['blue'])
plt.title('Response Counts in False-Assumption Column')
plt.xlabel('Response Type')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

#SINGLEHOP-INCONTEXT-YES

import pandas as pd
import matplotlib.pyplot as plt
import re
# Read the latest CSV file into a DataFrame again
df_latest = pd.read_csv('singlehop_eval_gpt_incontext_yes.csv')

# The correct column name is 'False-Assumption'
false_assumption_column = 'False-Assumption'

yes_responses = df_latest[false_assumption_column].str.startswith('Answer: Yes').sum()
no_responses = df_latest[false_assumption_column].str.startswith('Answer: No').sum()
other_responses = len(df_latest) - yes_responses - no_responses

# Let's create a bar chart with this data
response_counts = pd.Series({
    'Yes': yes_responses,
    'No': no_responses,
    'Other': other_responses,
})

# Recalculate percentages
total = len(df_latest)
yes_percentage = (yes_responses / total) * 100
no_percentage = (no_responses / total) * 100
others_percentage = (other_responses/ total) * 100

print(yes_percentage)
print(no_percentage)
print(others_percentage)

# Plotting the bar chart
response_counts.plot(kind='bar', figsize=(10, 5), color=['blue'])
plt.title('Response Counts in False-Assumption Column')
plt.xlabel('Response Type')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

#SINGLEHOP-INCONTEXT-YES-WITHOUT-RATIONALE

import pandas as pd
import matplotlib.pyplot as plt
import re
# Read the latest CSV file into a DataFrame again
df_latest = pd.read_csv('singlehop_eval_gpt_incontext_yes_without_rationale.csv')

# The correct column name is 'False-Assumption'
false_assumption_column = 'False-Assumption'

yes_responses = df_latest[false_assumption_column].str.startswith('Answer: Yes').sum()
no_responses = df_latest[false_assumption_column].str.startswith('Answer: No').sum()
other_responses = len(df_latest) - yes_responses - no_responses

# Let's create a bar chart with this data
response_counts = pd.Series({
    'Yes': yes_responses,
    'No': no_responses,
    'Other': other_responses,
})

# Recalculate percentages
total = len(df_latest)
yes_percentage = (yes_responses / total) * 100
no_percentage = (no_responses / total) * 100
others_percentage = (other_responses/ total) * 100

print(yes_percentage)
print(no_percentage)
print(others_percentage)

# Plotting the bar chart
response_counts.plot(kind='bar', figsize=(10, 5), color=['blue'])
plt.title('Response Counts in False-Assumption Column')
plt.xlabel('Response Type')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()



