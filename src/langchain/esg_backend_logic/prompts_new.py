def get_sector(company_info, company_sector):
    template = f"""
    {{
      "role": "ESG consultant",
      "task": "Identify the relevant GRI Sector Standard based on the provided company information and sector using the GRI Framework.",
      "choices": [
        {{"label": "1", "value": "GRI 11: Oil and Gas Sector 2021"}},
        {{"label": "2", "value": "GRI 12: Coal Sector 2022"}},
        {{"label": "3", "value": "GRI 13: Agriculture, Aquaculture and Fishing Sectors 2022"}}
      ],
      "input": {{"company_info": "{company_info}", "company_sector": "{company_sector}"}}
    }}
    ONLY OUTPUT THE GRI SECTOR YOU DETERMINED, FOR EXAMPLE "GRI 11: Oil and Gas Sector 2021"
    """

    return template


def grouped_topics(sector) -> str:
    template1_2 = f"""
    Given the {sector} from the GRI Framework, list all the Topics from that sector in a JSON format and also consult the definition of these topics. Categorize them under the keys 'environmental,' 'social,' and 'governance'. 

    Give your output in this json format: 
    ----
    {{
        "categories": {{
            "environmental": [
                //... topics categorized under environmental
            ],
            "social": [
                //... topics categorized under social
            ], 
            "governance": [
                //... topics categorized under governance
            ]
        }}
    }}
    ----

    Example:
    ----
    {{input}}: GRI 11: Oil and Gas Sector 2021
    {{output}}: 
    {{
        "categories": {{
            "environmental": [
                "Topic 11.1 GHG emissions",
                "Topic 11.2 Climate adaptation, resilience, and transition",
                "Topic 11.3 Air emissions",
                "Topic 11.4 Biodiversity",
                "Topic 11.5 Waste",
                "Topic 11.6 Water and effluents",
                "Topic 11.7 Closure and rehabilitation"
            ],
            "social": [
                "Topic 11.9 Occupational health and safety",
                "Topic 11.10 Employment practices",
                "Topic 11.11 Non-discrimination and equal opportunity",
                "Topic 11.12 Forced labor and modern slavery",
                "Topic 11.13 Freedom of association and collective bargaining",
                "Topic 11.15 Local communities",
                "Topic 11.16 Land and resource rights",
                "Topic 11.17 Rights of indigenous peoples"
            ], 
            "governance": [
                "Topic 11.8 Asset integrity and critical incident management",
                "Topic 11.14 Economic impacts",
                "Topic 11.18 Conflict and security",
                "Topic 11.19 Anti-competitive behavior",
                "Topic 11.20 Anti-corruption",
                "Topic 11.21 Payments to governments",
                "Topic 11.22 Public policy"
            ]
        }}
    }}
    ----
    """
    return template1_2


# gpt 3.5 has trouble with this one (can't handle amounts, e.g. "at most three topics")

def filter_topics(grouped_topics_, company_info):
    template = f"""
    You are given this information about a company: {company_info} and a set of GRI Topics in json format, 
    that are grouped by 'environmental', 'social' and 'governance': {grouped_topics_}.
    Your task is to consult the GRI Framework and determine which of the topics in the input json under the keys 'environmental', 'social' and 'governance'
    are relevant for the specific company. Give your output in this json format: 
    {{
        "categories": {{
            "environmental": [

            ],
            "social": [

            ], 
            "governance": [

            ]
        }}
    }}
    USE AT MOST THREE TOPICS FOR EACH CATEGORY!
    It is important that you USE the PROVIDED COMPANY INFORMATION to determine which topics are relevant!
    """
    return template


def topics_description(sector: str, company_info: str, topics: str) -> str:
    template3_4 = f"""
    You are given the following information about a company: {company_info} and a set of GRI Topics from {sector}, grouped under the keys 'environmental,' 'social,' and 'governance': {topics}. 

    Summarize the description of each topic from the input-json with roughly 200 words. 
    Only use the topics from the input-json!

    Give your output in this json format:

    {{
      "relevant_topics": {{
          "environmental": [
            {{
              "topic": {{
                "name": "name of the topic from the input json (for example: "Topic 12.5 Biodiversity")",
                "description": "summarized description of the topic from the GRI Topic description in the GRI Framework"
              }}
            }},
            // ... repeat the above structure for the remaining topics under the key "environmental"
          ]}},
          "social": [
            {{
              "topic": {{
                "name": "name of the topic",
                "description": "summarized description of the topic from the GRI Topic description in the GRI Framework"
              }}
            }},
            // ... repeat the above structure for the remaining topics under the key "social"
          ]}},
          "governance": [
            {{
              "topic": {{
                "name": "name of the topic",
                "description": "summarized description of the topic from the GRI Topic description in the GRI Framework"
              }}
            }},
            // ... repeat the above structure for the remaining topics under the key "governance"
          ]}}
    }}
    """
    return template3_4


def get_disclosures_from_gri(topic, sector):
    prompt = f"""

    Given the topic: '{topic}' from the sector: '{sector}', 

    - identify the relevant GRI Topic Standard and output it in a list.

    - GRI that are under Environmental always start with 'GRI 3XX', GRI that are under Social with 'GRI 4XX', and GRI that are under Governance with 'GRI 2XX'.

    - Give no more than three Topic Standards per topic.

    - The List should have the following format: ['GRI XXX: Name of the Topic Standard', ...]

    ----
    Example 1:
    ----
    {{your input:}}
    topic:  'Topic 11.21 Payments to governments'
    sector: 'GRI 11: Oil and Gas Sector 2021'
    {{your output:}}
    ["GRI 201: Economic Performance 2016", "GRI 207: Tax 2019"]
    ----
    Example 2:
    ----
    {{your input:}}
    topic:  'Topic 11.10 Employment practices'
    sector: 'GRI 11: Oil and Gas Sector 2021'
    {{your output:}}
    ["GRI 401: Employment 2016", "GRI 402: Labor/Management Relations 2016", "GRI 404: Training and Education 2016"]
    ----

    Only give the output in the format specified above.
    """

    return prompt


def disclosures_with_descriptions(topic, sector):
    prompt = f"""
    For the topics: '{topic}' from the sector: '{sector}', return a JSON object of each disclosure with their description. Use at least 50 words for each description. Structure your output as follows:

    Start with '{{"topic": "{topic}", "disclosures": [', and then for each disclosure, include '{{"name": "(disclosure name)", "description": "(description)"}}'. Close the array with ']}}'. Repeat this for each topic.

    For example:
    '{{"topic": "Topic 11.1 GHG emissions", "disclosures": [{{"name": "GRI 305: Emissions 2020", "description": "This disclosure provides information on nitrogen oxides (NO), sulfur oxides (SO), and other significant air emissions."}}]}}'

    Make sure to separate each disclosure with a comma!

    Do this for as many disclosures under each topic as you can provide.
    """

    return prompt


def get_actions_json(topics, sector, company_info):
    prompt = f"""
You are given this json object that contains all the relevant material topics for a company, grouped under the keys 'environmental,' 'social,' and 'governance': {topics}. and a set of GRI Topics from {sector}
Your task is to determine which actions the company should take to address the material topics. Use the company information: {company_info} to determine the actions.
For the keys environmental, social and governance include a general description with rougly 100 words of its meaning, and an explanation of its importance for the specific company.
Give your output in this json format:
{{
    "environmental": 
    {{
      "explanation": "general description of the environmental category",
      "topics" : [
        {{
          "topic": {{
            "name": "name of the topic from the input json (for example: "Topic 12.5 Biodiversity")",
            "actions": [
              "action 1",
              "action 2",
              "action 3"
            ]
          }}
        }},
        // ... repeat the above structure for the remaining topics under the key "environmental"
      ]
    }},
    "social": 
      {{
        "explanation": "general description of the social category",
        "topics": [
          {{
            "topic": {{
              "name": "name of the topic",
              "actions": [
                "action 1",
                "action 2",
                "action 3"
              ]
            }}
        }},
        // ... repeat the above structure for the remaining topics under the key "social"
      ]
    }},
    "governance": 
    {{
      "explanation": "general description of the governance category",
      "topics": [
        {{
          "topic": {{
            "name": "name of the topic",
            "actions": [ 
              "action 1",
              "action 2",
              "action 3"
            ]
          }}
        }},
        // ... repeat the above structure for the remaining topics under the key "governance"
    ]
  }}
}}
"""
    return prompt


def get_rating(company_information):
    prompt = f"""
"prompt": "Based on the specific details provided about a company: {company_information}, your task is to evaluate the level of significance of the environmental, social, and governance (ESG) aspects for their operations. Your evaluation should be expressed in scores ranging from 0 to 5, with 0 being the least significant and 5 the most. Provide a score for each ESG aspect, substantiated by the unique attributes of the company. Always provide a rating for each topic, even if you are not sure!

The output should be in this JSON format:

[
    {{
        "topic": "Environmental",
        "rating": "evaluated score reflecting the importance of environmental considerations for the company, based on the provided information"
    }},
    {{
        "topic": "Social",
        "rating": "evaluated score reflecting the importance of social considerations for the company, based on the provided information"
    }},
    {{
        "topic": "Governance",
        "rating": "evaluated score reflecting the importance of governance considerations for the company, based on the provided information"
    }}
]
Your output should only be the JSON, and nothing else!
"""
    return prompt


def get_general_compliance(company_information, sector, rating):
    prompt = f"""
"prompt": "Given the company's information, sector, and ESG ratings, produce a detailed explanation as to why the environmental, social, and governance (ESG) aspects have received their respective scores. Draw on the company's unique profile and sector attributes to explain the rationale behind these scores. Make sure to provide a thorough explanation. Do not respond with uncertainty or inability to generate a summary.

company details: 
----------------
{company_information}
----------------
company sector: 
----------------
{sector}
----------------
company ESG ratings: 
----------------
{rating}
----------------

example output: 
----------------
{{
  "general_compliance" : "In the context of PetroRefine Co.'s operations within the energy sector and the provided ESG ratings, each ESG component presents varying degrees of significance. The environmental score of 4 reflects the importance of environmental adaptation and sustainability for PetroRefine Co., given the inherent environmental implications of oil refining. This score emphasizes the critical nature of environmental stewardship for the company's future sustainability and reputation. A social score of 5 underscores the significance of strong stakeholder relationships in the company's widespread operations across North America, Europe, and Asia. The necessity of maintaining excellent employee welfare, community involvement, and customer relations is highlighted. Governance, with a score of 3, is vital for PetroRefine Co., but its direct impact is not as observable as the environmental and social elements due to the specifics of the company's operations. Nevertheless, adherence to ethical business conduct, regulatory compliance, and sustainable business practices is essential, as reflected in the governance score."
}}
----------------
Only produce the json as output, nothing else!
Please adhere to this exact json format: 
{{
  "general_compliance" : "your analysis"
}}

Write your output string in one line, and do not include any newlines or line breaks. It has to be in a valid json format!
"""
    return prompt
