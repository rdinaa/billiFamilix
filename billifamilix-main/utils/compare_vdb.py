from utils.prompts import CODE_COMPARAISON,CODE_EXPLANATION
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import os

from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock

from langchain.chains import LLMChain


region = "eu-central-1"
service = "aoss"
billi_host = "a4pkevhrjfw0pasvcu18.eu-central-1.aoss.amazonaws.com"
fam_host = "ezfuwmpse0avly7gwq9h.eu-central-1.aoss.amazonaws.com"

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

awsauth = AWS4Auth(AWS_ACCESS_KEY_ID,
                   AWS_SECRET_ACCESS_KEY,
                   region,
                   service)


bedrock = boto3.client(service_name='bedrock-runtime', region_name=region)
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock, region_name=region)


billi_vector = OpenSearchVectorSearch(
  embedding_function = bedrock_embeddings,
  index_name = 'billi-index',
  http_auth = awsauth,
  use_ssl = True,
  verify_certs = True,
  http_compress = True, # enables gzip compression for request bodies
  connection_class = RequestsHttpConnection,
  opensearch_url="https://" + billi_host
)


fam_vector = OpenSearchVectorSearch(
  embedding_function = bedrock_embeddings,
  index_name = 'fam-index',
  http_auth = awsauth,
  use_ssl = True,
  verify_certs = True,
  http_compress = True, # enables gzip compression for request bodies
  connection_class = RequestsHttpConnection,
  opensearch_url="https://" + fam_host
)



def compare_code_based_on_description(description):
  

    embedding_vector = bedrock_embeddings.embed_query(description)

    fam_docs = fam_vector.similarity_search_by_vector(
        embedding_vector,
        vector_field="nominee_vector",
        text_field="text",
        metadata_field="metadata",
    )    
    
    billi_docs = billi_vector.similarity_search_by_vector(
        embedding_vector,
        vector_field="nominee_vector",
        text_field="text",
        metadata_field="metadata",
    )

    docs_dict = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in fam_docs]
    fam_data = ""
    for doc in docs_dict:
        fam_data += doc['page_content'] + "\n\n"

    
    docs_dict = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in billi_docs]
    billi_data = ""
    for doc in docs_dict:
        billi_data += doc['page_content'] + "\n\n"

    ### creating the LLM

    llm = Bedrock(model_id="anthropic.claude-v2", client=bedrock, model_kwargs={'max_tokens_to_sample':200})



    chain = LLMChain(llm=llm, prompt=CODE_EXPLANATION)
    fam_description = chain.run({'context': fam_data})

    chain = LLMChain(llm=llm, prompt=CODE_EXPLANATION)
    billi_description = chain.run({'context': billi_data})

    chain = LLMChain(llm=llm, prompt=CODE_COMPARAISON)
    code_comparaion = chain.run({'billi_code': billi_data, 'fam_code': fam_data})



    print(fam_description)

    print(billi_description)

    print(code_comparaion)

    return fam_description, billi_description, code_comparaion


# compare_code_based_on_description("Bonus malus")