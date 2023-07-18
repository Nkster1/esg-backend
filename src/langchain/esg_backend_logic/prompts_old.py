"""
This is the prompt used for the old version of the ESG backend logic.
Instead of topics it uses the GRI Topic Standards, which are used for the reporting, under the likely material topics.
With the new prompt, first the material topics are identified and explained, and then the GRI Topic Standards are
identified and explained for each material topic.
"""


def general_disclosure_json(company_info):
    template = "Given the following description of a company:" + f"{company_info}" \
               + """
            Please generate a response in JSON format that describes the environmental, social, and governance (ESG) aspects of the company's business operation based on the provided GRI input. Include a general description of each aspect, an explanation of its importance, and specific actions the company can take to improve compliance. The JSON should have the following structure:

            {
                "environment": [
                    {
                        "description": "general description of the environmental factor for the specific business operation",
                        "importance": "explanation how the environmental aspect of ESG applies to the specific business operation",
                        "topics": [
                            {
                                "topic_standard": "specific GRI Topic Standard, for example: GRI 302: Energy 2016",
                                "topic_standard_description": "description of the GRI topic standard and how it applies to the business",
                                "topic_actions": [
                                    "Description of a concrete action to improve the company's compliance with this specific action",
                                    "write at least three or more such actions that are the most important for the business given the information",
                                ]
                            }
                            #"define at least three more topics for the specific company that fall under the environment factor"
                        ]
                    }
                ],
                "social": [
                    {
                        "description": "general description of the social factor for the specific business operation",
                        "importance": "explanation how the social aspect of ESG applies to the specific business operation",
                        "topics": [
                            {
                                "topic_standard": "specific GRI Topic Standard, for example: GRI 413: Local Communities 2016",
                                "topic_standard_description": "description of the GRI topic standard and how it applies to the business",
                                "topic_actions": [
                                    "Description of a concrete action to improve the company's compliance with this specific action",
                                    "write at least three or more such actions that are the most important for the business given the information",
                                ]
                            }
                            #"define at least three more topics for the specific company that fall under the social factor"
                        ]
                    }
                ],
                "governance": [
                    {
                        "description": "general description of the governance factor for the specific business operation",
                        "importance": "explanation how the governance aspect of ESG applies to the specific business operation",
                        "topics": [
                            {
                                "topic_standard": "specific GRI Topic Standard, for example: TGRI 205: Anti-corruption 2016",
                                "topic_standard_description": "description of the GRI topic standard and how it applies to the business",
                                "topic_actions": [
                                    "Description of a concrete action to improve the company's compliance with this specific action",
                                    "write at least three or more such actions that are the most important for the business given the information",
                                ]
                            }
                            #"define at least three more topics for the specific company that fall under the governance factor"
                        ]
                    }
                ]
            }
            """
    return template
