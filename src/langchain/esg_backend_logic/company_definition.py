from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Company:
    legal_name: str
    ownership: str
    legal_form: str
    location: str
    sector: str
    activities: str
    products: str
    markets: str
    supply_chain: str
    num_employees: str


class CompanyInfo:

    def __init__(self, c_i: Company):
        self._company_info = c_i

    def generate_company_description(self):
        company_description = f"The specific company information about the company is delimited by <>\n" \
                              f"- the company name is <{self._company_info.legal_name}>\n" \
                              f"- the ownership structure of the company" \
                              f"is defined as <{self._company_info.ownership}>\n" \
                              f"- the legal form of the company is defined as <{self._company_info.legal_form}>\n" \
                              f"- the location of the company headquarter is in <{self._company_info.location}>\n" \
                              f"- the industry sector the company operates in is <{self._company_info.sector}>\n" \
                              f"- the activities that are performed by the company " \
                              f"are defined as <{self._company_info.activities}>\n" \
                              f"- the products that are produced by the company " \
                              f"are defined as <{self._company_info.products}>\n" \
                              f"- the industry-markets the company operates " \
                              f"in are defined as <{self._company_info.markets}>\n" \
                              f"- the supply-chain of the company is defined as <{self._company_info.supply_chain}>\n" \
                              f"- the number of employees in the company is <{self._company_info.num_employees}>\n"
        return company_description


# for testing, set default companies.
# Using companies that aren't in agriculture/fishing; oil/gas; coal -> perhaps nothing will work
# potential work-around, should this behaviour occur: Just assign every company to one of these sectors

coal_company = Company(
    legal_name="Coal Mining Co.",
    ownership="Private",
    legal_form="Limited Liability Company",
    location="Freising, Bavaria, Germany",
    sector="Coal Mining",
    activities="Exploration, extraction, and processing of coal",
    products="Coal",
    markets="Germany, Europe",
    supply_chain="Mining equipment suppliers, transportation companies, power plants",
    num_employees="500"
)

oil_company = Company(
    legal_name="PetroRefine Co.",
    ownership="Public",
    legal_form="Corporation",
    location="Houston, Texas, USA",
    sector="Energy",
    activities="Oil refining and marketing for big ship motors",
    products="Gasoline, diesel, jet fuel, heating oil, lubricants",
    markets="North America, Europe, Asia",
    supply_chain="Crude oil suppliers, transportation companies, retail outlets",
    num_employees="500"
)

test_company = Company(
    legal_name="Shell LLC",
    ownership="Stock Company",
    legal_form="LLC",
    location="USA",
    sector="Energy",
    activities="we refine oil to gasoline",
    products="Oil Refinement",
    markets="we operate globally",
    supply_chain="we do everything ourselves",
    num_employees="10000"
)

company_2 = Company(
markets="europe",
products="luxury automobiles",
supply_chain="outsourced manufacturing",
activities="designing and producing high-end cars",
legal_name="xyz motors",
ownership="publicly traded",
legal_form="corporation",
num_employees="2000",
location="Germany",
sector="Automotive"
)
