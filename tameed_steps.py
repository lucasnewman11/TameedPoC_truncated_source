from app.models import *
import doc_api
from datetime import datetime
from nylasapi import send_email
import pickle

# get data from pickle
def load_data():
    with open("data.pickle", "rb") as f:
         return pickle.load(f)

# store data as pickle
def persist_data(data):
    with open("data.pickle", "wb") as f:
         pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

# update the status of a list of order objects
def update_state(orders, dapi, DATA):
    for o in orders:
        ic(o.step)
        if o.step == 0:
            o.step = 1
            for i in (o.purchaser, o.financier):
                send_email(i.email, "You have documents to sign! (No reply)", f"""An assignment of proceeds and a cover letter have been generated for you to review and sign!  Please log into tameedpoc.ngrok.io.""")
            

        elif o.step == 1:

            if ((dapi.doc_info(o.aop.pid)['recipients'][0]['has_completed']) == True):
                o.aop.signedc=True
                ic(o.aop.signedc)

            if ((dapi.doc_info(o.aop.pid)['recipients'][1]['has_completed']) == True):
                o.aop.signedb=True
                ic(o.aop.signedb)

            if ((dapi.doc_info(o.ccover.pid)['recipients'][0]['has_completed']) == True):
                o.ccover.signedc=True

            if ((dapi.doc_info(o.bcover.pid)['recipients'][0]['has_completed']) == True):
                o.bcover.signedb=True

            if o.aop.signedc and o.aop.signedb and o.ccover.signedc and o.bcover.signedb:
                o.signed = True
                send_email(o.issuer.email, "You have documents to approve! (No reply)", f"An assignment of proceeds and two cover letters have been generated for you to review and approve! Please log into tameedpoc.ngrok.io.")
                o.step = 2
                
    persist_data(DATA)

# properly format company information from the input form for use with the doc API
def format_party_info(company):
    c = company
    return f'''{c.commercial_registry_number}
{c.building_number},  {c.secondary_number}
{c.street_name}, {c.district}
{c.city}, {c.country}, {c.zip_code}
{c.phone_number} {c.email}'''

# create dictionary of tokens from the input form for use with the doc API
def aotp_tokens(order):
    return {"Name of project": order.name_of_project,
            "PO/ Contract Number": order.po_contract_number,
            "Date of PO": str(order.date_of_po),
            "Value of PO": order.value_of_po,
            "PO Issuer": order.issuer.company_name,
            "First Party Name": order.purchaser.company_name,
            "First Party Info and Address": format_party_info(order.purchaser),
            "Second Party Name": order.financier.company_name,
            "Second Party Info and Address": format_party_info(order.financier)}

class OrderW():
    def __init__(self):
        self.name_of_project = ''
        self.po_contract_number  = ''
        self.date_of_po = ''
        self.value_of_po = ''
        self.date_created = ''
        self.purchaser = ''
        self.financier = ''
        self.issuer = ''
        self.aop = ''
        self.ccover = ''
        self.bcover = ''
        self.current_agent = ''
        self.current_doc = ''
        self.current_action = ''
        self.step_text = ''
        self.zero = ''
        self.one = ''
        self.two = ''
        self.three = ''
        self.four = ''
        self.five = ''
        self.six = ''
        self.signed = False

    def data(self):
        dct = {i:self.__dict__[i] for i in ("name_of_project", "po_contract_number", "date_of_po", "value_of_po", "date_created")}
        first_dct = {("first_party_" + i):self.purchaser.__dict__[i] for i in self.purchaser.__dict__}
        second_dct = {("second_party_" + i):self.financier.__dict__[i] for i in self.financier.__dict__}
        dct.update(first_dct)
        dct.update(second_dct)
        return dct

class ActionW():
    def __init__(self, step_number, keyword, name, company, role, status, order, date_activated=None):
        self.step_number = step_number
        self.name = name
        self.keyword = keyword
        self.date_activated = date_activated
        self.date_terminated = None
        self.company = company
        self.role = role
        self.status = status
        self.order = order

class CompanyW():
    def __init__(self,
                 company_name = '',
                 commercial_registry_number  = '',
                 building_number = '',
                 secondary_number = '',
                 street_name = '',
                 district = '',
                 city = '',
                 country = '',
                 zip_code = '',
                 phone_number = '',
                 email = '',
                 iban = '',
                 uuid = ''):
        self.company_name = company_name
        self.commercial_registry_number = commercial_registry_number
        self.building_number = building_number
        self.secondary_number = secondary_number
        self.street_name = street_name
        self.district = district
        self.city = city
        self.country = country
        self.zip_code = zip_code
        self.phone_number = phone_number
        self.email = email
        self.iban = iban
        self.uuid = uuid

class DocumentW():
    def __init__(self, tpid, pid, order, name, purchaser = "", financier = "", issuer= ""):
        self.tpid=tpid
        self.pid=pid
        self.name=name
        self.order=order
        self.signedc=False
        self.signedb=False
        self.approved=False
        self.rejected=False
        self.purchaser = purchaser
        self.financier = financier
        self.issuer = issuer

class TemplateW():
    pid = ''
    folded_pid = ''
    name = ''


def step_zero(form, dapi, DATA):
        purchaser = CompanyW()
        financier = CompanyW()
        issuer = CompanyW()
        issuer.email = form.po_issuer.data
        issuer.company_name = "Joseph"
        for key in form.first_fields:
            setattr(purchaser, key[6:], getattr(form, key).data)

        for key in form.second_fields:
            setattr(financier, key[7:], getattr(form, key).data)

        COMPANIES[purchaser.email] = purchaser
        COMPANIES[financier.email] = financier
        COMPANIES[issuer.email] = issuer

        order = OrderW()

        order.name_of_project=form.name_of_project.data
        order.po_contract_number=form.po_contract_number.data
        order.date_of_po=form.date_of_po.data
        order.value_of_po=form.value_of_po.data
        order.date_created=datetime.today()
        order.purchaser=purchaser
        order.financier=financier
        order.issuer=issuer
        recipient_tuples_1 = ((purchaser, "Client", 2),
                              (financier, "Bank/FinTech", 1),
                              (issuer, "Issuer", 3))

        recipient_tuples_3 = ((purchaser, "Client", 1),
                              (issuer, "Issuer", 2))
                          
        recipient_tuples_2 = ((financier, "Bank/Fintech", 1),
                              (issuer, "Issuer", 2))

        recipients1 = doc_api.format_recipients(recipient_tuples_1)
        recipients2 = doc_api.format_recipients(recipient_tuples_2)
        recipients3 = doc_api.format_recipients(recipient_tuples_3)

        tokens = doc_api.format_tokens(aotp_tokens(order))
        

        response1 = dapi.create_document("Joint Assignment of Proceeds", TEMPLATES['AoP_BoFt_Client'][0], TEMPLATES['AoP_BoFt_Client'][1], recipients1, tokens)
        response2 = dapi.create_document("Bank/Fintech Cover Letter", TEMPLATES['BoFt_Cover'][0], TEMPLATES['BoFt_Cover'][1], recipients2, tokens)
        response3 = dapi.create_document("Client Cover Letter", TEMPLATES['Client_Cover'][0], TEMPLATES['Client_Cover'][1], recipients3, tokens)
        

        order.aop = DocumentW(pid=response1['id'], tpid=TEMPLATES['AoP_BoFt_Client'][0], order=order, name="Assignment of Proceeds")
        order.bcover = DocumentW(pid=response2['id'], tpid=TEMPLATES['BoFt_Cover'][0], order=order, name="Bank/FinTech Cover Letter")
        order.ccover = DocumentW(pid=response3['id'], tpid=TEMPLATES['Client_Cover'][0], order=order, name="Client Cover Letter")

        order.zero = ActionW(step_number="0",
                             name="Initation of Assignment of Proceeds",
                             date_activated=datetime.now(),
                             company=purchaser,
                             keyword="automatic",
                             role="Purchaser",
                             order=order,
                             status="Complete")

        order.one = ActionW(step_number="1",
                            name="Bank/Fintech Signature of Assignment of Proceeds",
                            date_activated=datetime.now(),
                            company=financier,
                            keyword="signature",
                            role="Financier",
                            order=order,
                            status="Active")

        order.two = ActionW(step_number="2",
                            name="Client Signature of Assignment of Proceeds",
                            company=purchaser,
                            keyword="signature",
                            role="Purchaser",
                            order=order,
                            status="Inactive")

        order.three = ActionW(step_number="3",
                              name="Client Signature of Cover Letter",
                              company=purchaser,
                              keyword="signature",
                              role="Purchaser",
                              order=order,
                              status="Inactive")

        order.four = ActionW(step_number="4",
                             name="Bank/Fintech Signature of Cover Letter",
                             company=financier,
                             keyword="signature",
                             role="Financier",
                             order=order,
                             status="Inactive")

        order.five = ActionW(step_number="5",
                             name="Digital Verification and Approval of PO Issuer",
                             company=issuer,
                             keyword="verification and approval",
                             role="Issuer",
                             order=order,
                             status="Inactive")

        order.approve = ActionW(step_number="COMPLETE",
                             name="Transaction Accepted By PO Issuer",
                             company=issuer,
                             keyword= "",
                             role="Issuer",
                             order=order,
                             status="Inactive")

        order.reject = ActionW(step_number="FAILED",
                             name="Transaction Rejected By PO Issuer",
                             company=issuer,
                             keyword="",
                             role="Issuer",
                             order=order,
                             status="Inactive")
        order.step = 0
        order.current_action = order.zero
        DATA["ORDERS"].append(order)
        persist_data(DATA)
        ORDERS.append(order)
        return order

DOCS = {}
PROGRESS = {}
ROLE_BY_STEP = [None, "Bank/FinTech", "Client", "Client", "Bank/Fintech", "Issuer", "Issuer"]
TEMPLATES = {"AoP_BoFt_Client": ('5eGxZRfEgdstvt8TDwFhnW', 'XEyXdjeid3uW7GxqmJyhtc'), "Client_Cover": ('RQnuFiYws3MWz2te32jTnh', 'XEyXdjeid3uW7GxqmJyhtc'), "BoFt_Cover": ('VsUxCPEQSuswkNs7rTraxJ', 'XEyXdjeid3uW7GxqmJyhtc') }
ORDERS = []
COMPANIES = {}

# awaiting = Company.query.get(order.awaiting)

        
