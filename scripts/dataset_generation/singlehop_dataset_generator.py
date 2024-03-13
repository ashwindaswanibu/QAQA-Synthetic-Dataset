from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import csv
import time
import random

class WikidataHelper:
    def __init__(self):
        self.endpoint = "https://query.wikidata.org/sparql"

    def execute_query(self, query):
        sparql = SPARQLWrapper(self.endpoint)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        try:
            return sparql.query().convert()
        except Exception as e:
            time.sleep(5)  # Wait before retrying
            print(f"Query execution error: {e}")
            return None

    def find_similar_individuals(self, wikidata_id, ignored_properties):
        properties = ['P106', 'P19', 'P69', 'P800', 'P101', 'P102', 'P166']
        properties = [p for p in properties if p not in ignored_properties]

        shared_counts = {}
        for prop in properties:
            query = f"""
                SELECT ?person (COUNT(?value) as ?valueCount) WHERE {{
                    wd:{wikidata_id} wdt:{prop} ?value .
                    ?person wdt:{prop} ?value .
                    FILTER (?person != wd:{wikidata_id})
                }} GROUP BY ?person
            """
            results = self.execute_query(query)
            if results:
                for result in results["results"]["bindings"]:
                    person_id = result["person"]["value"].split('/')[-1]
                    count = int(result["valueCount"]["value"])
                    if person_id not in shared_counts:
                        shared_counts[person_id] = 0
                    shared_counts[person_id] += count

        if not shared_counts:
            return None, "No similar individual found"

        most_similar_person_id = max(shared_counts, key=shared_counts.get)
        return most_similar_person_id, self.fetch_label(most_similar_person_id)

    def fetch_label(self, wikidata_id):
        response = requests.get(f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={wikidata_id}&languages=en&format=json").json()
        try:
            return response["entities"][wikidata_id]["labels"]["en"]["value"]
        except KeyError:
            return "Label not found"

    def generate_and_save_questions(self, properties, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Wikidata ID", "Label", "Similar Person ID", "Similar Person Label", "Property", "Generated Question"])

            for prop in properties:
                ignored_properties = ["P31"]  # Example of ignored properties
                wikidata_id, label = random.choice(self.fetch_entities_with_property(prop))
                similar_person_id, similar_person_label = self.find_similar_individuals(wikidata_id, ignored_properties)
                question = f"How does {label} compare to {similar_person_label} in the context of {prop}?"
                writer.writerow([wikidata_id, label, similar_person_id, similar_person_label, prop, question])

    def fetch_entities_with_property(self, prop, limit=100):
        query = f"""
            SELECT ?entity ?entityLabel WHERE {{
                ?entity wdt:{prop} ?value.
                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
            }}
            LIMIT {limit}
        """
        results = self.execute_query(query)
        return [(result['entity']['value'].split('/')[-1], result['entityLabel']['value']) for result in results["results"]["bindings"]]

def main():
    wikidata_helper = WikidataHelper()
    properties = ["P106", "P27"]
    wikidata_helper.generate_and_save_questions(properties, "wikidata_questions.csv")

if __name__ == "__main__":
    main()
