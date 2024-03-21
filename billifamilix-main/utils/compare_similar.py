import json
from compare_vdb import compare_codes
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import os

from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock

from langchain.chains import LLMChain


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


json_file_path = 'data/FAM_BILLI_similarity.json'
data_dictionary = read_json_file(json_file_path)

FAM_dir = "/Users/maximegillot/Desktop/Hackathon/Cleaned_FAM/"
BILLI_dir = "/Users/maximegillot/Desktop/Hackathon/Cleaned_BILLI/"

Output_folder = "/Users/maximegillot/Desktop/Projects/AudioTranscriptAndSynthesis/Hackathon/MD_Comparaison/"

similarity_list = []
dic = {}


for fam_funct, billi_classes in data_dictionary.items():
    for billi_class, similarity in billi_classes.items():

        if(similarity in similarity_list):
            print(similarity, "already in list")
        else:
            similarity_list.append(similarity)
            dic[similarity] = [fam_funct,billi_class]

        # print(similarity)
            

similarity_list.sort(reverse=True)
# print(similarity_list)


for i in range(50):
    similarity = similarity_list[i]
    # print(similarity)
    print(similarity, "-", dic[similarity])


for i in range(5):
    similarity = similarity_list[i]
    # print(similarity)
    print(similarity, "-", dic[similarity])

    fam_path = FAM_dir + dic[similarity][0] + ".java"
    billi_path = BILLI_dir + dic[similarity][1]


    with open(fam_path, 'r') as fam:
            fam_code = fam

    with open(billi_path, 'r') as billi:
            billi_code = billi

    fam_description, billi_description, code_comparaion = compare_codes(fam_code, billi_code)

    # print(fam_description)

    # print(billi_description)

    # print(code_comparaion)

    result = "## FAM DESCRIPTION\n\n" + dic[similarity][0] + ".java" + "\n\n" + fam_description + "\n\n"
    result += "## BILLI DESCRIPTION\n\n" + dic[similarity][1] + "\n\n" + billi_description + "\n\n"
    result += "## COMPARAISON\n\n" + code_comparaion

    file_path = Output_folder + dic[similarity][0] + ".md"

    f = open(file_path,"a")
    f.write(result)
    f.close()

