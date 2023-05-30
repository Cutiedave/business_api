import os
import sys
import openai
import time 
from celery import shared_task
from base.models import Business_case_data
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get('oai_sk', '8888')
#model_id = 'gpt-3.5-turbo'
model_id = os.environ.get('ai_model', 'gpt-3.5-turbo')
def ChatGPT_conversation(conversation,model_id):
    response = openai.ChatCompletion.create(model=model_id,messages=conversation)
    # api_usage = response['usage']
    # print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    # stop means complete
    # print(response['choices'][0].finish_reason)
    # print(response['choices'][0].index)
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return(conversation)



tone = 'an agressive & direct tone'

@shared_task()
def send_email(business_data):
    prompt1 = ('You are a top-performing B2B sales professional conducting research to assist ' 
            +
            business_data['seller_name'] + ' in selling ' + business_data['services_sold'] + ' to a prospective client and business. '
            +
            'Create 3 paragraphs to compile your research. The first paragraph should be written as a biography of the prospective client, ' 
            + 
            str(business_data['lead_full_name']) + ', who is ' + str(business_data['lead_position']) 
            + 
            ' at ' + str(business_data['company']) 
            + 
            '. This biography should include information on their interests, education, a psychographic analysis, approximate income level, and professional accomplishments based on their social media and the internet at large.' 
            + 
            ' Based on the information already gathered on ' + str(business_data['lead_full_name']) 
            + 
            ' from a B2B database, ' +  business_data['lead_full_name_possesive'] + ' interests include: ' + str(business_data['lead_interest']) + ', ' + business_data['lead_full_name_possesive'] + ' skills include: ' + str(business_data['lead_skills']) 
            + 
            ', ' + business_data['lead_full_name_possesive'] + ' work experience includes: ' + str(business_data['lead_experience']) + ', and ' + business_data['lead_full_name_possesive'] + ' social media profiles are found at: ' + str(business_data['lead_social_links']) 
            + 
            '. This biography should be written in a way that helps ' + business_data['seller_name'] + ' sell to the prospective client.'
            + 
            ' This biography should only include information explicitly stated in the information and links provided. Do not make any assumptions.'
            +
            '\n\n' 
            +
            'The second paragraph should provide an analysis of the prospective business, ' + str(business_data['company']) + '. Which is located in ' 
            + 
            str(business_data['company_city']) + ', ' + str(business_data['company_state']) 
            + 
            '. This analysis should include a SWOT analysis and identify probable pain points for the business based on reviewing & analyzing the company website: ' 
            + 
            str(business_data['company_site']) + ', as well as the loacl market/industry and revelvant news published within the last 90 days. ' 
            + 
            "Based exclusively on the prospective buisness' website, this analysis should also identify the prospective business' target market, ideal client and include relevant information regarding their ideal client. "
            +
            " Based exclusively on the prospective buisness' website, this analysis should also identify if the prospective business sells its products/services to individuals (B2C) or other buisnesses (B2B). If prospective business is a B2B organization, list their target industry."
            +
            ' Both paragraphs 1 & 2 should be written in a way that helps ' + business_data['seller_name'] + ' sell to the prospective buisness.' 
            + 
            ' Both paragraghs 1 & 2 should only include information explicitly stated in the information and links provided. Do not make any assumptions.' 
            + 
            ' Do not include non-conclusive information in your response.'
            + 
            '\n\n'
            +
            'In paragraph 3, make a professional recommendation including the best sales process and tactics (including examples) that ' 
            + 
            business_data['seller_name'] + ' can use to convert ' + business_data['lead_full_name'] + ' and ' + business_data['company'] +', into an interested party and then paying customer.' 
            +
            ' List the top 5 solutions that will add value to ' + business_data['lead_full_name'] + ' and ' + business_data['company'] + '.'
            +
            ' List the top 5 objections that will likely arise, including ways for ' + business_data['seller_name'] + ' overcome them.'
            +
            ' List the top 5 reasons that ' + business_data['lead_full_name'] + ' would decide to become a paying customer.'
            + 
            " The entire response must be less than 30,000 characters and fit within Openai's single response character limits."
            + 
            ' If you have any questions regarding either of these paragraphs, ask before generating them.')

    #print(prompt1)
    #print('\n\n')

    conversation = []
    print('Generating Prospect Report...')

    # try:
    time.sleep(25)
    conversation.append({'role': 'system', 'content': prompt1})
    conversation = ChatGPT_conversation(conversation, model_id)
    #print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
    background = conversation[-1]['content']
    # print(background)
    obj = Business_case_data.objects.get(user=business_data['email'])
    obj.background_email=background
    obj.save()

    # except Exception as e:
    #     print(e)
    #     # exc_type, exc_obj, exc_tb = sys.exc_info()
    #     # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     # print(exc_type, fname, exc_tb.tb_lineno)
    #     time.sleep(300)