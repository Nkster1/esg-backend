from jsonschema import validate


# Define a function to validate JSON data
def validate_esg_report(data):
    # Define the JSON schema
    e_s_g_subschma = {"type": "object",
                      "properties": {
                          "explanation": {
                              "type": "string"
                          },
                          "topics": {
                              "type": "array",
                              "items": {
                                  "type": "object",
                                  "properties": {
                                      "topic": {
                                          "type": "object",
                                          "properties": {
                                              "name": {
                                                  "type": "string"
                                              },
                                              "description": {
                                                  "type": "string"
                                              },
                                              "actions": {
                                                  "type": "array",
                                                  "items": {
                                                      "type": "string"
                                                  }
                                              },
                                              "disclosures": {
                                                  "type": "array",
                                                  "items": {
                                                      "type": "object",
                                                      "properties": {
                                                          "name": {
                                                              "type": "string"
                                                          },
                                                          "description": {
                                                              "type": "string"
                                                          }
                                                      },
                                                      "required": ["name", "description"]
                                                  }
                                              }
                                          },
                                          "required": ["name", "description", "actions", "disclosures"]
                                      }
                                  },
                                  "required": ["topic"]
                              }
                          }
                      },
                      "required": ["explanation", "topics"]
                      }

    schema = {
        "type": "object",
        "properties": {
            "general": {
                "type": "object",
                "properties": {
                    "general_compliance": {"type": "string"},
                },
                "required": ["general_compliance"],
            },
            "environmental": e_s_g_subschma,
            "social": e_s_g_subschma,
            "governance": e_s_g_subschma,
            "rating": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string"},
                        "rating": {"type": "string"},
                    },
                    "required": ["topic", "rating"],
                },
            },
        },
        "required": ["general", "environmental", "social", "governance", "rating"],
    }

    # Validate the data
    validate(instance=data, schema=schema)
    print("JSON data is valid")


if __name__ == '__main__':
    test_string = {
        "general": {
            "general_compliance": "The data you provided was insufficient for our algorithms to derive concrete measures, hence we provide you with an overview over general ESG rules."
        },
        "environmental": {
            "explanation": "The environmental category includes topics related to the impact of a company's activities on the natural environment. These topics are important. To address the material topics in this category, a company should consider actions such as implementing biodiversity conservation measures, promoting soil health management practices, and minimizing natural ecosystem conversion.",
            "topics": [
                {
                    "topic": {
                        "name": "Topic 13.3 Biodiversity",
                        "description": "The biodiversity topic focuses on the organization's impacts on biodiversity, including the conservation and restoration of ecosystems, the protection of endangered species, and the management of invasive species. It also includes the organization's efforts to minimize the negative impacts of its activities on biodiversity and promote sustainable practices.",
                        "actions": [
                            "Implement biodiversity conservation measures",
                            "Conduct biodiversity impact assessments",
                            "Support habitat restoration initiatives"
                        ],
                        "disclosures": [
                            {
                                "name": "GRI 303: Water 2018",
                                "description": "This disclosure provides information on the organization's water usage and management practices, including water sources, water consumption, and water efficiency measures."
                            },
                            {
                                "name": "GRI 304: Biodiversity 2016",
                                "description": "This disclosure focuses on the organization's impacts on biodiversity, including the protection and restoration of habitats, the assessment of significant impacts on biodiversity, and the use of operational sites in or adjacent to protected areas."
                            },
                            {
                                "name": "GRI 305: Emissions 2018",
                                "description": "This disclosure addresses the organization's greenhouse gas emissions, including the measurement and reporting of emissions, emission reduction initiatives, and the use of renewable energy sources."
                            }
                        ]
                    }
                },
                {
                    "topic": {
                        "name": "Topic 13.5 Soil health",
                        "description": "The soil health topic addresses the organization's impacts on soil quality and fertility. It includes the organization's efforts to prevent soil erosion, promote sustainable soil management practices, and protect soil health from contamination. It also covers the organization's initiatives to restore degraded soils and enhance soil biodiversity.",
                        "actions": [
                            "Adopt sustainable soil management practices",
                            "Monitor soil health indicators",
                            "Implement erosion control measures"
                        ],
                        "disclosures": [
                            {
                                "name": "GRI 416: Customer Health and Safety 2018",
                                "description": "This disclosure focuses on the organization's efforts to ensure customer health and safety, including product labeling, safety information, and customer communication channels."
                            },
                            {
                                "name": "GRI 417: Marketing and Labeling 2018",
                                "description": "This disclosure addresses the organization's marketing and labeling practices, including advertising standards, product claims, and compliance with labeling regulations."
                            },
                            {
                                "name": "GRI 418: Customer Privacy 2018",
                                "description": "This disclosure focuses on the organization's protection of customer privacy, including data collection and storage practices, data security measures, and compliance with privacy laws and regulations."
                            }
                        ]
                    }
                },
                {
                    "topic": {
                        "name": "Topic 13.4 Natural ecosystem conversion",
                        "description": "The natural ecosystem conversion topic focuses on the organization's impacts on natural ecosystems, including the conversion of natural habitats for agricultural or industrial purposes. It includes the organization's efforts to minimize the conversion of natural ecosystems, protect critical habitats, and promote the restoration and conservation of natural ecosystems.",
                        "actions": [
                            "Avoid or minimize conversion of natural ecosystems",
                            "Implement land use planning strategies",
                            "Support reforestation and afforestation projects"
                        ],
                        "disclosures": [
                            {
                                "name": "GRI 303: Water 2018",
                                "description": "This disclosure provides information on the organization's water usage and management practices, including water sources, water consumption, and water efficiency measures."
                            },
                            {
                                "name": "GRI 304: Biodiversity 2016",
                                "description": "This disclosure focuses on the organization's impacts on biodiversity, including the protection and restoration of habitats, the assessment of significant impacts on biodiversity, and the use of operational sites in or adjacent to protected areas."
                            },
                            {
                                "name": "GRI 305: Emissions 2016",
                                "description": "This disclosure addresses the organization's greenhouse gas emissions, including the measurement and reporting of emissions, emission reduction initiatives, and the use of renewable energy sources."
                            }
                        ]
                    }
                }
            ]
        },
        "social": {
            "explanation": "The social category includes topics related to a company's impact on people and society.To address the material topics in this category, a company should consider actions such as ensuring animal health and welfare, promoting non-discrimination and equal opportunity, and implementing supply chain traceability measures.",
            "topics": [
                {
                    "topic": {
                        "name": "Topic 13.11 Animal health and welfare",
                        "description": "The animal health and welfare topic addresses the organization's impacts on animal welfare, including the treatment and care of animals used in agricultural or aquaculture activities. It includes the organization's efforts to ensure the humane treatment of animals, prevent animal cruelty, and promote responsible animal husbandry practices.",
                        "actions": [
                            "Implement animal welfare standards",
                            "Provide veterinary care for animals",
                            "Promote responsible animal handling practices"
                        ],
                        "disclosures": [
                            {
                                "name": "GRI 403: Occupational Health and Safety 2018",
                                "description": "This disclosure focuses on the organization's efforts to ensure the health and safety of its employees, including occupational health and safety policies, training programs, and incident reporting procedures."
                            },
                            {
                                "name": "GRI 404: Training and Education 2016",
                                "description": "This disclosure addresses the organization's training and education programs for employees, including skills development, career advancement opportunities, and employee performance evaluations."
                            },
                            {
                                "name": "GRI 405: Diversity and Equal Opportunity 2016",
                                "description": "This disclosure focuses on the organization's commitment to diversity and equal opportunity, including policies and practices to promote diversity, prevent discrimination, and ensure equal access to employment opportunities."
                            }
                        ]
                    }
                },
                {
                    "topic": {
                        "name": "Topic 13.21 Living income and living wage",
                        "description": "The living income and living wage topic focuses on the organization's impacts on the income and wages of workers in the agriculture, aquaculture, and fishing sectors. It includes the organization's efforts to ensure fair and equitable compensation for workers, promote living wages, and address income inequality and poverty in the sector.",
                        "actions": [
                            "Ensure fair wages for employees",
                            "Promote income equality",
                            "Support initiatives for living wage standards"
                        ],
                        "disclosures": [
                            {
                                "name": "GRI 202: Market Presence 2016",
                                "description": "This disclosure provides information on the organization's market presence, including market share, market growth strategies, and market competition analysis."
                            },
                            {
                                "name": "GRI 204: Procurement Practices 2016",
                                "description": "This disclosure addresses the organization's procurement practices, including supplier selection criteria, supplier relationship management, and responsible sourcing initiatives."
                            },
                            {
                                "name": "GRI 205: Anti-corruption 2016",
                                "description": "This disclosure focuses on the organization's efforts to prevent and address corruption, including anti-corruption policies, training programs, and mechanisms for reporting and investigating corruption incidents."
                            }
                        ]
                    }
                },
                {
                    "topic": {
                        "name": "Topic 13.23 Supply chain traceability",
                        "description": "The supply chain traceability topic addresses the organization's efforts to trace and track its products and inputs throughout the supply chain. It includes the organization's initiatives to ensure transparency and accountability in its supply chain, prevent illegal or unethical practices, and promote responsible sourcing and production.",
                        "actions": [
                            "Implement traceability systems for supply chain",
                            "Monitor and audit suppliers for compliance",
                            "Promote transparency in the supply chain"
                        ],
                        "disclosures": [
                            {
                                "name": "GRI 204: Procurement Practices 2016",
                                "description": "This disclosure addresses the organization's procurement practices, including supplier selection criteria, supplier relationship management, and responsible sourcing initiatives."
                            },
                            {
                                "name": "GRI 308: Supplier Environmental Assessment 2016",
                                "description": "This disclosure focuses on the organization's assessment of suppliers' environmental performance, including environmental criteria for supplier selection, supplier environmental audits, and collaboration with suppliers to improve environmental performance."
                            },
                            {
                                "name": "GRI 414: Supplier Social Assessment 2016",
                                "description": "This disclosure addresses the organization's assessment of suppliers' social performance, including social criteria for supplier selection, supplier social audits, and collaboration with suppliers to improve social performance."
                            }
                        ]
                    }
                },
                {
                    "topic": {
                        "name": "Topic 13.15 Non-discrimination and equal opportunity",
                        "description": "The non-discrimination and equal opportunity topic focuses on the organization's efforts to promote diversity, inclusion, and equal opportunities in its operations and workforce. It includes the organization's initiatives to prevent discrimination based on race, gender, age, disability, or other protected characteristics, and promote a fair and inclusive work environment.",
                        "actions": [
                            "Establish non-discrimination policies",
                            "Promote diversity and inclusion",
                            "Provide equal opportunities for all employees"
                        ],
                        "disclosures": [
                            {
                                "name": "GRI 405: Diversity and Equal Opportunity 2016",
                                "description": "This disclosure focuses on the organization's commitment to diversity and equal opportunity, including policies and practices to promote diversity, prevent discrimination, and ensure equal access to employment opportunities."
                            },
                            {
                                "name": "GRI 406: Non-discrimination 2016",
                                "description": "This disclosure addresses the organization's efforts to prevent discrimination, including non-discrimination policies, training programs, and mechanisms for reporting and addressing discrimination incidents."
                            },
                            {
                                "name": "GRI 408: Child Labor 2016",
                                "description": "This disclosure focuses on the organization's efforts to prevent and address child labor, including policies and practices to ensure compliance with child labor laws, age verification mechanisms, and remediation measures for child labor violations."
                            }
                        ]
                    }
                }
            ]
        },
        "governance": {
            "explanation": f"The governance category includes topics related to the company's governance structure and practices. To address the material topics in this category, a company should consider actions such as implementing effective governance mechanisms, ensuring transparency in decision-making processes, and promoting ethical business practices.",
            "topics": []
        },

        "rating": [
            {
                "topic": "Environmental",
                "rating": "0"
            },
            {
                "topic": "Social",
                "rating": "0"
            },
            {
                "topic": "Governance",
                "rating": "0"
            }
        ]
    }

    # Test the function
    #json_data = json.loads(json_data_string)  # assuming json_data_string is your JSON data in string format
    validate_esg_report(test_string)
