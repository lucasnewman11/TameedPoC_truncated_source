from pprint import pprint
import pandadoc_client
from pandadoc_client.api import documents_api
from pandadoc_client.model.document_create_response import DocumentCreateResponse
from pandadoc_client.model.document_create_request import DocumentCreateRequest
from pandadoc_client.model.document_create_request_recipients import DocumentCreateRequestRecipients
from pandadoc_client.model.document_create_by_template_request_tokens import \
    DocumentCreateByTemplateRequestTokens
from pandadoc_client.model.document_create_link_response import DocumentCreateLinkResponse
from pandadoc_client.model.document_create_link_request import DocumentCreateLinkRequest
from pandadoc_client.model.document_send_response import DocumentSendResponse
from pandadoc_client.model.document_send_request import DocumentSendRequest
from pandadoc_client.model.document_details_response import DocumentDetailsResponse
from pandadoc_client.model.document_status_response import DocumentStatusResponse
from icecream import ic

def format_recipient(company, role, signing_order):
    return {'email': company.email,
            'first_name': company.company_name,
            'last_name': "Hamilton",
            'role': role}

def format_recipients(tuples):
    return [format_recipient(company, role, signing_order) for \
                      (company, role, signing_order) in tuples]

def format_tokens(token_dict):
    return [{"name": i, "value": token_dict[i]} for i in token_dict]

class DocApi():

    configuration = pandadoc_client.Configuration(
    host="https://api.pandadoc.com",
    )
    configuration.api_key['apiKey'] = '1b99b4eb8318ffaf22de8c2defecb5707f8933bc'
    configuration.api_key_prefix['apiKey'] = 'API-Key'

    api_client = pandadoc_client.ApiClient(configuration) 
    api_instance = documents_api.DocumentsApi(api_client)

    def create_document(self, name, template_uuid, folder_uuid, recipients, tokens):
        ic(tokens)
        recipients = [DocumentCreateRequestRecipients(**recipient) for recipient in recipients]
        tokens = [DocumentCreateByTemplateRequestTokens(**token) for token in tokens]
        document_create_request = DocumentCreateRequest(name=name,
                                                        template_uuid=template_uuid,
                                                        folder_uuid=folder_uuid,
                                                        recipients=recipients,
                                                        tokens=tokens)
        try:
            # Create document
            api_response = DocApi.api_instance.create_document(document_create_request)
            pprint(api_response)
            return api_response
        except pandadoc_client.ApiException as e:
            print("Exception when calling DocumentsApi->create_document: %s\n" % e)

    def send_document(self, pid, message='', subject='', silent=True):
        document_send_request = DocumentSendRequest(message=message,
                                                    subject=subject,
                                                    silent=silent)
        try:
            # Send Document
            api_response = DocApi.api_instance.send_document(pid, document_send_request)
            pprint(api_response)
            return api_response
        except pandadoc_client.ApiException as e:
            print("Exception when calling DocumentsApi->send_document: %s\n" % e)

    def doc_info(self, pid):
        try:
            api_response = DocApi.api_instance.details_document(pid)
            pprint(api_response)
            return api_response
        except pandadoc_client.ApiException as e:
            print("Exception when calling DocumentsApi->doc_info: %s\n" % e)

    def doc_status(self, pid):
        try:
            # Document status
            api_response = DocApi.api_instance.status_document(pid)
            pprint(api_response)
            return api_response
        except pandadoc_client.ApiException as e:
            print("Exception when calling DocumentsApi->status_document: %s\n" % e)

    def embed_link(self, pid, recipient_email, lifetime=10000):
        document_create_link_request = DocumentCreateLinkRequest(
            recipient=recipient_email,
            lifetime=float(10000),
        )  
        try:
            # Create a Document Link
            api_response = DocApi.api_instance.create_document_link(pid, document_create_link_request)
            pprint(api_response)
            return f"https://app.pandadoc.com/s/{api_response['id']}"
        except pandadoc_client.ApiException as e:
            print("Exception when calling DocumentsApi->create_document_link: %s\n" % e)

                                                
    

        
                
