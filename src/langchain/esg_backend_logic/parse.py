import json


def combine_json_strings(json_str1, json_str2):
    # Replace newline characters
    json_str1 = json_str1.replace('\n', ' ')
    json_str2 = json_str2.replace('\n', ' ')

    # Load the JSON strings into Python dictionaries
    dict1 = json.loads(json_str1)
    dict2 = json.loads(json_str2)

    # Combine the dictionaries
    for topic in dict2:
        if topic['topic'] in [item['topic']['name'] for category in dict1['relevant_topics'] for item in
                              dict1['relevant_topics'][category]]:
            for category in dict1['relevant_topics']:
                for item in dict1['relevant_topics'][category]:
                    if item['topic']['name'] == topic['topic']:
                        item['topic']['disclosures'] = topic['disclosures']
                        break

    # Dump the combined dictionary back into a JSON string
    combined_json_str = json.dumps(dict1, indent=2)

    return combined_json_str

def convert_the_shit_to_json(json_str1, json_str2, rating, general):
    # Convert JSON strings to dictionaries
    json_data1 = json.loads(json_str1)
    json_data2 = json.loads(json_str2)
    json_data3 = json.loads(rating)
    json_data4 = json.loads(general)

    # Merge the JSON structures
    merged_data = {}

    # Merge environmental category
    environmental_data1 = json_data1.get("environmental", {})
    environmental_data2 = json_data2["relevant_topics"]["environmental"]

    merged_environmental = {
        "explanation": environmental_data1.get("explanation"),
        "topics": []
    }

    for topic1, topic2 in zip(environmental_data1.get("topics", []), environmental_data2):
        topic_data1 = topic1.get("topic", {})
        topic_data2 = topic2.get("topic", {})
        topic_merged = {
            "name": topic_data1.get("name"),
            "description": topic_data2.get("description"),
            "actions": topic_data1.get("actions"),
            "disclosures": topic_data2.get("disclosures")
        }
        merged_environmental["topics"].append({"topic": topic_merged})

    merged_data["environmental"] = merged_environmental

    # Merge social category
    social_data1 = json_data1.get("social", {})
    social_data2 = json_data2["relevant_topics"]["social"]

    merged_social = {
        "explanation": social_data1.get("explanation"),
        "topics": []
    }

    for topic1, topic2 in zip(social_data1.get("topics", []), social_data2):
        topic_data1 = topic1.get("topic", {})
        topic_data2 = topic2.get("topic", {})
        topic_merged = {
            "name": topic_data1.get("name"),
            "description": topic_data2.get("description"),
            "actions": topic_data1.get("actions"),
            "disclosures": topic_data2.get("disclosures")
        }
        merged_social["topics"].append({"topic": topic_merged})

    merged_data["social"] = merged_social

    # Merge governance category
    governance_data1 = json_data1.get("governance", {})
    governance_data2 = json_data2["relevant_topics"]["governance"]

    merged_governance = {
        "explanation": governance_data1.get("explanation"),
        "topics": []
    }

    for topic1, topic2 in zip(governance_data1.get("topics", []), governance_data2):
        topic_data1 = topic1.get("topic", {})
        topic_data2 = topic2.get("topic", {})
        topic_merged = {
            "name": topic_data1.get("name"),
            "description": topic_data2.get("description"),
            "actions": topic_data1.get("actions"),
            "disclosures": topic_data2.get("disclosures")
        }
        merged_governance["topics"].append({"topic": topic_merged})

    merged_data["governance"] = merged_governance

    merged_data['general'] = json_data4

    merged_data['rating'] = json_data3


    # Convert merged data back to JSON string
    merged_json_str = json.dumps(merged_data, indent=4)
    return merged_json_str
