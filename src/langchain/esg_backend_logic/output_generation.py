from .company_definition import *
from .prompts_old import *
from .prompts_new import *
from .chains import *
from .parse import combine_json_strings, convert_the_shit_to_json
import textwrap
import json
import ast
import random

def wrap_text_preserve_newlines(text, width=110):
    # Split the input text into lines based on newline characters
    lines = text.split('\n')

    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

    # Join the wrapped lines back together using newline characters
    wrapped_text = '\n'.join(wrapped_lines)

    return wrapped_text


def process_llm_response(llm_response):
    return wrap_text_preserve_newlines(llm_response['result'])


def extract_topic(s):
    return " ".join(s.split()[2:])


def extract_sector(s):
    return " ".join(s.split()[2:-1]).lower()


def generate_disclosures(input_json, sector, chain):
    categories = json.loads(input_json)["categories"]

    results = {
        "categories": {
            "environmental": [],
            "social": [],
            "governance": []
        }
    }

    for category in categories:
        for topic in categories[category]:
            disclosures_string = run_local(get_disclosures_from_gri(topic, sector), chain)

            try:
                disclosures = ast.literal_eval(disclosures_string)
            except (ValueError, SyntaxError):
                disclosures = [disclosures_string]

            formatted_disclosures = []
            for disclosure in disclosures:
                if isinstance(disclosure, str):
                    formatted_disclosures.extend([x.strip() for x in disclosure.split(',') if x.strip() != ''])
                elif isinstance(disclosure, dict) and "result" in disclosure:
                    formatted_disclosures.append(disclosure["result"])

            results["categories"][category].append({
                "name": topic,
                "disclosures": formatted_disclosures
            })

    return json.dumps(results, indent=2)


def select_topics(input_json):
    output_json = {"categories": {}}
    for category, topics in input_json["categories"].items():
        random.shuffle(topics)
        selected_topics = topics[:random.randint(3, 4)]
        output_json["categories"][category] = selected_topics
    return json.dumps(output_json, indent=4)


def ensure_brackets(s):
    if not s.startswith('['):
        s = '[' + s
    if not s.endswith(']'):
        s = s + ']'
    return s

def combine_jsons2(json1, json2):
    # Load JSON strings into dictionaries if they are not
    if isinstance(json1, str):
        json1 = json.loads(json1)
    if isinstance(json2, str):
        json2 = json.loads(json2)

    # Modify the structure of json1 to match json2
    json1_mod = {}
    for category in json1["relevant_topics"]:
        topics_dict = {topic["topic"]["name"]: topic for topic in json1["relevant_topics"][category]}
        json1_mod[category] = {"topics": list(topics_dict.values())}

    # Now, json1_mod and json2 have the same structure and can be merged
    for category in json1_mod:
        if category in json2:
            for topic2 in json2[category]["topics"]:
                topic_name = topic2["topic"]["name"]
                topics_dict = {topic["topic"]["name"]: topic for topic in json1_mod[category]["topics"]}
                if topic_name in topics_dict:
                    # Add actions to the matching topic in json1_mod
                    topics_dict[topic_name]["topic"]["actions"] = topic2["topic"]["actions"]
                else:
                    # Add the whole topic from json2 if it does not exist in json1_mod
                    json1_mod[category]["topics"].append(topic2)

            # Add explanation to the category in json1_mod
            json1_mod[category]["explanation"] = json2[category]["explanation"]

    return json1_mod


def get_esg_reporting(company_info_: CompanyInfo, company_: Company):

    sector = process_llm_response(
        run_local(get_sector(company_info=company_info_.generate_company_description(), company_sector=company_.sector), chain_sector))

    if sector.__eq__("GRI 11: Oil and Gas Sector 2021"):
        chain = chain_oil_gas_sector

    elif sector.__eq__("GRI 12: Coal Sector 2022"):
        chain = chain_coal_sector

    else:
        chain = chain_agrar_aqua_sector


    topics = process_llm_response(run_local(grouped_topics(sector=sector), chain))
    filtered = select_topics(json.loads(topics))
    topics_with_description = process_llm_response(
        run_local(topics_description(sector=sector, company_info=company_info_.generate_company_description(), topics=filtered), chain))
    res1 = generate_disclosures(filtered, sector, chain)
    res2 = process_llm_response(run_local(disclosures_with_descriptions(topic=res1, sector=sector), chain))
    gri = ensure_brackets(res2)
    res3 = run_standard(get_actions_json(filtered, sector, company_info_.generate_company_description()))
    rating = run_standard(get_rating(company_info_.generate_company_description()))
    general = run_standard(get_general_compliance(company_info_.generate_company_description(), sector=sector, rating=rating))
    final = convert_the_shit_to_json(res3, combine_json_strings(topics_with_description, gri), rating, general)

    return final
