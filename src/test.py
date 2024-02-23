def check_consistency_and_explain(onto, json_data, explanation_file, inconsistent_individuals):
    total_items = len(json_data)
    inconsistent_count = len(inconsistent_individuals)

    with open(explanation_file, 'w') as file:
        first_entry = True  # Track if we're writing the first entry to avoid a newline at the start
        for image_id, properties in json_data.items():
            # Attempt to find the individual in the ontology
            individual = onto.search_one(iri="*" + image_id)

            # Prepare the explanation string
            if individual is None:
                explanation = f"{image_id} could not be found in the ontology. It may have been removed due to inconsistency."
            else:
                explanation = f"{image_id} is a {individual.is_a[0].name}"
                if image_id in inconsistent_individuals:
                    explanation += " and is NOT consistent, hence removed from the ontology."
                else:
                    explanation += " and is consistent in the ontology."

                prop_explanations = []
                for prop_category in ['BodyPart', 'WeatherType', 'EdgeShape']:
                    prop_values = [prop.name for prop in onto[prop_category].instances() if prop in individual.is_a]
                    if prop_values:
                        prop_explanations.append(f"has {', '.join(prop_values)} in {prop_category}")
                    else:
                        prop_explanations.append(f"does not have specified properties in {prop_category}")

                explanation += " It " + ", and ".join(prop_explanations) + "."

            # Write the explanation to the file, prepending a newline for all but the first entry
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