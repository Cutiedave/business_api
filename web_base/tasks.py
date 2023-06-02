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
    
    
    
    prompt2 = ('Based on the research conducted on the prospective client, ' + business_data['lead_full_name'] + ', the analysis conducted on the prospective buisness, ' + business_data['company']
               + 
               ', and the recomended sales process, all provided in the previous response, create an introductory sales message to convince ' 
               + 
               business_data['lead_full_name'] + ' to schedule a meeting to discuss purchasing ' + business_data['services_sold']
               + 
               ' for ' + business_data['company']+ ' from the salesperson, ' + business_data['seller_name'] + ', '
               + 
               business_data['seller_overview']
               +
               ' This message should get straight to the point and not include a salutation.'
               + 
               ' This message should be at maximum 10 sentences and 150 words. ' 
               + 
               business_data['seller_name']+ "'s phone number is " + business_data['seller_phone'] 
               + 
               '. Do not claim to have worked with any local/similar companies, ask prospects to contact via social media, or include social media as part of the proposed solution. ' 
               + 
               " Also include a pain point specific to the " + business_data['lead_full_name'] + ' or ' + business_data['company']+ " that " + business_data['services_sold']+ " will solve." 
               + 
               ' This message should be written as if were written in first person by ' + business_data['seller_name'] + ', ' 
               +  
               business_data['seller_name'] 
               + 
               ' This message should be straight to the point.' 
               + 
               ' The message should not include marketing or technical jargon or provide any guarantees.' 
               + 
               ' Do not offer to help the prospective client or buisness expand into new industries.' 
               + 
               ' This message should not include any placeholder text, or any of the following charachters: "<", ">", "[", "]".'
               + 
               ' This message should not include the phrase "pain point", "insert", "industry-specific", "consultative selling", "the challenger sale" or "pain points".'
               +
               'If you have any questions, ask before generating the message.' 
               + 
               ' Do not state which sales approach is being used in the message.' 
               +
               " Include the prospective client's name and the prospective buisness' name in the message."
               +
               " For social proof reference the fact that the salesperson " 
               + 
               business_data['social_proof']
               +
               " Let the prospective client know that the saleperson has research them and the prospective business by including an example from the research previously conducted."
               +
               ' This message should ask the prospective client for their availablility to schedule a call with the salesperson.'
               +
               ' This message should use contraction words when possible.'
               +
               ' This message should be structured as follows: '
               +
               'first paragraph - greet the prospective client by their first name only (do not include last name or prospective buisness in greeting), '
               +
               'second paragraph - highlight the research conducted on the prospective client'
               +
               'third paragraph - show how the service(s) provide by the salesperson solves a problem that the prospective buisness currently has, '
               +
               'fourth paragraph - highlight the reasons why the salesperson is the right partner for the prospective client '
               + 
               " and reference the salesperson's offer/guarantee: " + business_data['seller_offer'] + ", "
               +
               'and fifth paragraph - request a meeting with the prospective client. '
               +
               ' Each sentence in this message should be direct, concise, and written in easy to understand language.'
               +
               ' This message MUST include 5 different paragraphs and 10 sentences at maximum.'
               +
               ' This message cannot guarantee to make the prospective client or prospective business any amount of money.'
               )
    
    text_prompt = ('You are a copywriting expert with 20 years of experience helping B2B companies convert leads to customers. With 100 words or less, rewrite and reformat the sales message to be sent via sms text message, with the goal of having the prospect schedule a call. ' + 
                   'This text should as introduce the salesperson, ' + business_data['seller_name'] 
                   + 
                   ', who has not yet met or been introduced to the prospective client, ' 
                   + 
                   business_data['lead_full_name'] + ' or the prospective business, ' + business_data['company'] 
                   + 
                   '. This sms text message should highlight that ' 
                   + 
                   business_data['seller_name'] + ' ' + business_data['short_social_proof']
                   + 
                   ' This sms text should be written as if were written in first person by the salesperson, ' 
                   + 
                   business_data['seller_name'] + '.' 
                   + 
                   " Be sure to include a problem specific to " + business_data['company'] + "'s industry and provide an example of how " 
                   + 
                   business_data['seller_name'] + " will solve " + business_data['lead_full_name_possesive'] + ' and ' + business_data['company'] + "'s problems." 
                   + 
                   ' Do not ask for a generic "yes" or similar response. This text message should be written as if it were sent directly from the salesperson, ' 
                   + 
                   business_data['seller_name'] + '. This text message should not include any placeholder text, or any of the following charachters: "<", ">", "[", "]".' 
                   + 
                   ' This text message should not ask anyone to respond by calling.' + 'If you have any questions ask before generating the text.' 
                   + 
                   ' This text message should ask the prospective client for their availablility to schedule a call with the salesperson.' 
                   + 
                   ' This text message should not include a phone number.'
                   +
                   ' This text message should not include the phrase "pain point", "insert", "industry-specific", "consultative selling", "the challenger sale" or "pain points".'
                   +
                   ' This text message should use contraction words when possible.'
                   +
                   ' This text message should be structured as follows: first sentence greet ' + business_data['lead_full_name'] + ' and introduce ' + business_data['seller_name'] 
                   + 
                   ', second senetence highlight the research conducted on '
                   +
                   business_data['lead_full_name'] + ' in the initial prompt/response, third senetence show how ' + business_data['services_sold'] + ' proverided by ' + business_data['seller_name'] + ' solve a problem that ' + business_data['lead_full_name'] + ' or ' + business_data['company'] + ' is likely experiencing currently, '
                   +
                   "fourth sentence should include the salesperson's guarantee, "
                   +
                   'and final sentence should request a meeting with ' + business_data['lead_full_name'] + '.'
                   +
                   ' This text message cannot guarantee to make the prospective client or prospective business any amount of money.'
                   +
                   " This text message must have atleast 2 paragraphs."
                  )



    conversation = []
    print('Generating Prospect Report...')
    try:
        time.sleep(35)
        conversation.append({'role': 'system', 'content': prompt1})
        conversation = ChatGPT_conversation(conversation, model_id)
        background = conversation[-1]['content']
        obj = Business_case_data.objects.get(email=business_data['email'])
        obj.prospect_report=background
        obj.save()
    except Exception as e:
        print(e)
        time.sleep(50)

    try:
        time.sleep(35)
        conversation.append({'role': 'system', 'content': prompt2})
        conversation = ChatGPT_conversation(conversation, model_id)
        background = conversation[-1]['content']
        obj = Business_case_data.objects.get(email=business_data['email'])
        obj.background_email=background
        obj.save()
    except Exception as e:
        print(e)
        time.sleep(50)

    try:
        time.sleep(35)
        conversation.append({'role': 'system', 'content': text_prompt})
        conversation = ChatGPT_conversation(conversation, model_id)
        background = conversation[-1]['content']
        obj = Business_case_data.objects.get(email=business_data['email'])
        obj.background_text=background
        obj.save()
    except Exception as e:
        print(e)
        time.sleep(50)