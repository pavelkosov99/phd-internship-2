from owlready2 import *
import os
import json

def load_json_data(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

def clean_ontology(onto):
    for individual in list(onto.individuals()):
        destroy_entity(individual)

def update_ontology_with_json(json_data, onto):
    body_parts = ['WholeBody', 'TopPart', 'BottomPart', 'Feet', 'Hands']
    weather_types = ['Cold', 'Warm', 'Any']
    edge_shapes = ['StraightEdge', 'CurveEdge']

    all_properties = {
        'BodyPart': body_parts,
        'WeatherType': weather_types,
        'EdgeShape': edge_shapes
    }

    inconsistent_individuals = []

    for image_id, properties in json_data.items():
        clothes_class_name = properties["Clothes"]
        properties_present = properties.get("Properties", {})

        clothes_class = getattr(onto, clothes_class_name)
        individual = clothes_class(image_id)

        for prop_category, prop_list in all_properties.items():
            predicate = getattr(onto, f'has{prop_category}')
            if prop_category in properties_present:
                actual_prop = properties_present[prop_category]
                for prop in prop_list:
                    property_class = getattr(onto, prop)
                    if prop == actual_prop:
                        individual.is_a.append(predicate.some(property_class))
                    else:
                        individual.is_a.append(Not(predicate.some(property_class)))
            else:
                for prop in prop_list:
                    property_class = getattr(onto, prop)
                    individual.is_a.append(Not(predicate.some(property_class)))

        # Check consistency
        with onto:
            try:
                sync_reasoner()
            except OwlReadyInconsistentOntologyError:
                # Remove the inconsistent individual
                destroy_entity(individual)
                inconsistent_individuals.append(image_id)

    return inconsistent_individuals


def check_consistency_and_explain(onto, json_data, explanation_file, inconsistent_individuals):
    body_parts = ['WholeBody', 'TopPart', 'BottomPart', 'Feet', 'Hands']
    weather_types = ['Cold', 'Warm', 'Any']
    edge_shapes = ['StraightEdge', 'CurveEdge']

    total_items = len(json_data)
    inconsistent_count = len(inconsistent_individuals)

    with open(explanation_file, 'w') as file:
        first_entry = True  # Track if we're writing the first entry to avoid a newline at the start
        for image_id, properties in json_data.items():
            # Attempt to find the individual in the ontology
            individual = onto.search_one(iri="*" + image_id)

            if individual is None:
                explanation = f"{image_id} could not be found in the ontology. It may have been removed due to inconsistency."
            else:
                explanation = f"{image_id} is a {individual.is_a[0].name}"
                if image_id in inconsistent_individuals:
                    explanation += " and is NOT consistent, hence removed from the ontology."
                else:
                    explanation += " and is consistent in the ontology"

                # Initialize the explanations for properties
                prop_explanations = []

                # Check and explain BodyPart properties
                for prop in body_parts:
                    if prop in properties.get("Properties", {}).get("BodyPart", ""):
                        prop_explanations.append(f"it has {prop} in BodyPart")
                    else:
                        prop_explanations.append(f"does not have {prop} in BodyPart")

                # Check and explain WeatherType properties
                for prop in weather_types:
                    if prop in properties.get("Properties", {}).get("WeatherType", ""):
                        prop_explanations.append(f"it has {prop} in WeatherType")
                    else:
                        prop_explanations.append(f"does not have {prop} in WeatherType")

                # Check and explain EdgeShape properties
                for prop in edge_shapes:
                    if prop in properties.get("Properties", {}).get("EdgeShape", ""):
                        prop_explanations.append(f"it has {prop} in EdgeShape")
                    else:
                        prop_explanations.append(f"does not have {prop} in EdgeShape")

                explanation += ". It " + ", ".join(prop_explanations) + "."

            if first_entry:
                # Calculate and write the percentage of inconsistent and consistent items
                consistent_count = total_items - inconsistent_count
                inconsistent_percentage = (inconsistent_count / total_items) * 100
                consistent_percentage = (consistent_count / total_items) * 100

                summary = (f"Summary:\nTotal Items: {total_items}\n"
                           f"Inconsistent Items: {inconsistent_count} ({inconsistent_percentage:.2f}%)\n"
                           f"Consistent Items: {consistent_count} ({consistent_percentage:.2f}%)\n\n")
                file.write(summary)

                file.write(explanation)
                first_entry = False
            else:
                file.write("\n" + explanation)


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ontology_path = os.path.join(current_dir, "../data/ontology/ontology.owl")
    json_file_path = os.path.join(current_dir, '../data/json/compound_output.json')
    explanation_file = os.path.join(current_dir, "../explanation.txt")

    # Load the ontology
    onto = get_ontology(ontology_path).load()

    # Clean the ontology from existing individuals
    clean_ontology(onto)

    # Load and parse JSON data
    json_data = load_json_data(json_file_path)

    # Update ontology with JSON data and get list of inconsistent individuals
    inconsistent_individuals = update_ontology_with_json(json_data, onto)

    # Check consistency for each individual and write explanations
    check_consistency_and_explain(onto, json_data, explanation_file, inconsistent_individuals)

    # Save the updated ontology
    onto.save(file=ontology_path, format="rdfxml")

if __name__ == "__main__":
    main()
