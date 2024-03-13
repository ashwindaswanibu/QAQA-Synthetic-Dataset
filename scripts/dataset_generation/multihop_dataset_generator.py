import wikipedia
import csv
import os
import json

def get_wikipedia_categories(title):
    try:
        page = wikipedia.page(title)
        return page.categories
    except:
        return []

def compute_similarity(categories1, categories2):
    tokens1 = {token for category in categories1 for token in category.lower().split()}
    tokens2 = {token for category in categories2 for token in category.lower().split()}
    shared_tokens = tokens1.intersection(tokens2)
    denominator = max(len(tokens1), len(tokens2))
    return len(shared_tokens) / denominator if denominator else 0

def find_most_similar_distraction(title, context, supporting_facts_titles):
    title_categories = get_wikipedia_categories(title)
    max_similarity = 0
    best_distraction = None
    for distraction_data in context:
        distraction = distraction_data[0]
        if distraction not in [title] + supporting_facts_titles:
            distraction_categories = get_wikipedia_categories(distraction)
            similarity = compute_similarity(title_categories, distraction_categories)
            if similarity > max_similarity:
                max_similarity, best_distraction = similarity, distraction
    return best_distraction

class QuestionProcessor:
    def __init__(self, data_file, output_file):
        self.data_file = data_file
        self.output_file = output_file
        self.headers = ["Old Question", "New Question", "Answer", "Supporting Facts", "Context Titles"]

    def create_csv_if_not_exists(self):
        if not os.path.exists(self.output_file):
            with open(self.output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.headers)

    def save_to_csv(self, data_list):
        with open(self.output_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data_list)

    def get_last_processed_question(self):
        try:
            with open(self.output_file, 'r', newline='') as csvfile:
                return list(csv.reader(csvfile))[-1][1]
        except:
            return None

    def process_and_save(self):
        self.create_csv_if_not_exists()
        last_question = self.get_last_processed_question()
        start_processing = last_question is None

        with open(self.data_file, 'r') as file:
            data = json.load(file)

        processed_data, counter = [], 0
        for entry in data:
            if entry['type'] == 'bridge':
                question = entry['question']
                if not start_processing:
                    start_processing = question == last_question
                    continue
                answer = entry['answer']
                supporting_facts_titles = [fact[0] for fact in entry['supporting_facts']]
                context_titles = [context_item[0] for context_item in entry['context']]
                modified_question = question
                for title in supporting_facts_titles:
                    distraction = find_most_similar_distraction(title, entry['context'], supporting_facts_titles)
                    if distraction:
                        modified_question = modified_question.replace(title, distraction, 1)
                processed_data.append([question, modified_question, answer, '; '.join(supporting_facts_titles), '; '.join(context_titles)])
                counter += 1
                if counter % 50 == 0:
                    self.save_to_csv(processed_data)
                    processed_data = []
        if processed_data:
            self.save_to_csv(processed_data)

if __name__ == "__main__":
    processor = QuestionProcessor('hotpot_dev_distractor_v1.json', 'questions_data.csv')
    processor.process_and_save()
