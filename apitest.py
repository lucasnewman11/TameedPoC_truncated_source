############################# LIST TEMPLATES ############################
from pprint import pprint

import pandadoc_client
from pandadoc_client.api import templates_api

# Configure API key authorization: apiKey
api_key = "1b99b4eb8318ffaf22de8c2defecb5707f8933bc"

# Defining the host is optional and defaults to https://api.pandadoc.com
# See configuration.py for a list of all supported configuration parameters.
cfg = pandadoc_client.Configuration(
    host = "https://api.pandadoc.com",
    api_key={"apiKey": f"API-Key {api_key}"},
)

# Enter a context with an instance of the API client
with pandadoc_client.ApiClient(cfg) as api_client:
    # Create an instance of the API class
    api_instance = templates_api.TemplatesApi(api_client)

    try:
        resp = api_instance.list_templates(tag=["Tameed"])
        pprint(resp)
    except pandadoc_client.ApiException as e:
        pprint("Exception when calling TemplatesApi->list_templates: %s\n" % e)

###################### CREATE DOC FROM TEMPLATE ########################
import pandadoc_client
from pandadoc_client.api import documents_api
from pandadoc_client.model.document_create_response import DocumentCreateResponse
from pandadoc_client.model.document_create_request import DocumentCreateRequest
from pandadoc_client.model.document_create_request_recipients import DocumentCreateRequestRecipients
from pandadoc_client.model.document_create_by_template_request_tokens import \
    DocumentCreateByTemplateRequestTokens
from pprint import pprint

# Defining the host is optional and defaults to https://api.pandadoc.com
# See configuration.py for a list of all supported configuration parameters.
configuration = pandadoc_client.Configuration(
    host="https://api.pandadoc.com",
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = '1b99b4eb8318ffaf22de8c2defecb5707f8933bc'
configuration.api_key_prefix['apiKey'] = 'API-Key'

# Configure OAuth2 access token for authorization: oauth2
# configuration = pandadoc_client.Configuration(
#    host="https://api.pandadoc.com",
# )
# configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with pandadoc_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = documents_api.DocumentsApi(api_client)
    document_create_request = DocumentCreateRequest(
        name="Assignment of Proceeds Between Purchaser and Bank/FinTech",
        template_uuid="5eGxZRfEgdstvt8TDwFhnW",
        folder_uuid="XEyXdjeid3uW7GxqmJyhtc",
        recipients=[
            DocumentCreateRequestRecipients(
                email="lucasnewman11@gmail.com",
                first_name="Lucas",
                last_name="Newman",
                role="Client",
                signing_order=1,
            ),
            DocumentCreateRequestRecipients(
                email="lucasnewman11+1@gmail.com",
                first_name="Bobby",
                last_name="Brown",
                role="Bank/FinTech",
                signing_order=2,
            ),
        ],
        tokens=[
            DocumentCreateByTemplateRequestTokens(
                name="Name of project",
                value="This is my test value",
            ),
        ],
    )
                
          # DocumentCreateRequest | Use a PandaDoc template or an existing PDF to create a document. See the creation request examples [by template](/schemas/DocumentCreateByTemplateRequest) and [by pdf](/schemas/DocumentCreateByPdfRequest) 
    editor_ver = "ev2"  # str | Set this parameter as `ev1` if you want to create a document from PDF with Classic Editor when both editors are enabled for the workspace. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create document
        api_response = api_instance.create_document(document_create_request)
        pprint(api_response)
    except pandadoc_client.ApiException as e:
        print("Exception when calling DocumentsApi->create_document: %s\n" % e)

    # # example passing only required values which don't have defaults set
    # # and optional values
    # try:
    #     # Create document
    #     api_response = api_instance.create_document(
    #         document_create_request,
    #         editor_ver=editor_ver,
    #     )
    #     pprint(api_response)
    # except pandadoc_client.ApiException as e:
    #     print("Exception when calling DocumentsApi->create_document: %s\n" % e)

################################# SEND DOCUMENT ###############################################

import pandadoc_client
from pandadoc_client.api import documents_api
from pandadoc_client.model.document_send_response import DocumentSendResponse
from pandadoc_client.model.document_send_request import DocumentSendRequest
from pprint import pprint

# Defining the host is optional and defaults to https://api.pandadoc.com
# See configuration.py for a list of all supported configuration parameters.
configuration = pandadoc_client.Configuration(
    host="https://api.pandadoc.com",
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = '1b99b4eb8318ffaf22de8c2defecb5707f8933bc'
configuration.api_key_prefix['apiKey'] = 'API-Key'

# Configure OAuth2 access token for authorization: oauth2
# configuration = pandadoc_client.Configuration(
#    host="https://api.pandadoc.com",
# )
# configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with pandadoc_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = documents_api.DocumentsApi(api_client)
    id = "infXYh4HqJXk6X2uL85Yw6"  # str | Document ID
    document_send_request = DocumentSendRequest(
        message="Assignment of Proceeds Document Test",
        subject="Please sign!",
        silent=True,
    )  # DocumentSendRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Send Document
        api_response = api_instance.send_document(id, document_send_request)
        pprint(api_response)
    except pandadoc_client.ApiException as e:
        print("Exception when calling DocumentsApi->send_document: %s\n" % e)

######################### SHARE DOCUMENT ################################

import pandadoc_client
from pandadoc_client.api import documents_api
from pandadoc_client.model.document_create_link_response import DocumentCreateLinkResponse
from pandadoc_client.model.document_create_link_request import DocumentCreateLinkRequest
from pprint import pprint

# Defining the host is optional and defaults to https://api.pandadoc.com
# See configuration.py for a list of all supported configuration parameters.
configuration = pandadoc_client.Configuration(
    host="https://api.pandadoc.com",
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = '1b99b4eb8318ffaf22de8c2defecb5707f8933bc'
configuration.api_key_prefix['apiKey'] = 'API-Key'

# Configure OAuth2 access token for authorization: oauth2
# configuration = pandadoc_client.Configuration(
#    host="https://api.pandadoc.com",
# )
# configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with pandadoc_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = documents_api.DocumentsApi(api_client)
    id = "infXYh4HqJXk6X2uL85Yw6"  # str | Document ID
    document_create_link_request = DocumentCreateLinkRequest(
        recipient="lucasnewman11+1@gmail.com",
        lifetime=float(10000),
    )  # DocumentCreateLinkRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create a Document Link
        api_response = api_instance.create_document_link(id, document_create_link_request)
        pprint(api_response)
    except pandadoc_client.ApiException as e:
        print("Exception when calling DocumentsApi->create_document_link: %s\n" % e)
