#!/usr/bin/env python3
import json
from typing import Dict, Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.auth.crud import get_user_by_email, create_esg_report
from src.auth.utils import get_db
from src.langchain.data_model import ChatRequest
from src.langchain.default_output import default_response
from src.langchain.esg_backend_logic.company_definition import Company, CompanyInfo
from src.langchain.esg_backend_logic.output_generation import get_esg_reporting
from src.langchain.langchain_application_code import chat
from src.langchain.validate_response import validate_esg_report

router_langchain = APIRouter(prefix="/langchain")

esg_report_cache = {}


@router_langchain.get("/")
async def health():
    return {"status": "success"}


@router_langchain.post("/chat")
async def basic_prompt(chat_request: ChatRequest):
    # Here you might use a language model to generate a response.
    # In this example, we'll simply echo back the user's message.

    response = chat(chat_request)
    print(f"RESPONE: {response}")
    return {"message": response, "sender": "ai"}


@router_langchain.post("/esg_report")
async def esg_report(company: Company, db: Session = Depends(get_db)):
    # company = Company("OilRefinery", "CEO", "Business Corporation", "America", "Oil refinement",
    #                   "we refine oil to gasoline",
    #                   "gasoline", "we operate globally", "we do everything ourselves", "100000")

    h_c = hash(company)
    if h_c in esg_report_cache:
        return {"message": esg_report_cache[h_c]}


    company_info = CompanyInfo(company)
    try:
        esg_report_json_str = get_esg_reporting(company_info_=company_info, company_=company)
        # test that data is valid JSON
        json_data = json.loads(esg_report_json_str)  # assuming json_data_string is your JSON data in string format
        validate_esg_report(json_data)
    except Exception as e:
        print(e)
        esg_report_json_str = default_response
    # super basic basic
    # user_mail = "a@b.com"
    # user = get_user_by_email(db, user_mail)
    # create_esg_report(db, user=user, esg_report=esg_report_json_str)
    #

    esg_report_cache[h_c] = esg_report_json_str
    print(f"RESPONSE: {esg_report_json_str}")
    return {"message": esg_report_json_str}
