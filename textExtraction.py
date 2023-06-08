#extracting the reviews from the reviews.xlsx file into a directory
import pandas as pd
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
import os, json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate




os.environ["OPENAI_API_KEY"] = "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"

chat = ChatOpenAI(temperature=0.0)

# Read the Excel file
excel_file = pd.ExcelFile('reviews.xlsx')

feature_prompt = "Extract any features that the customer liked from the game review.\
      Look for specific details about the game's mechanics, graphics, sound, storyline, characters, or any other aspects that stood out to the customer as particularly enjoyable or well-done if there is any in the review. \
      Please provide these features in a JSON with the feature as the key and a list of descriptions as the value.\
      Each description (if there is) should be a full sentence that provides context and explains why the feature was liked. \
      If the feature was mentioned before, append the new description to the list of existing descriptions for that key. \
      If the review does not mention any features or being too general, please return an empty JSON."

sentiment_prompt = "What is the sentiment of the review?\
        If the review is positive, return 'positive'.\
        If the review is negative, return 'negative'.\
        "
sentiment_schema = ResponseSchema(name='sentiment', description=sentiment_prompt)
feature_schema = ResponseSchema(name='features', description=feature_prompt)
response_schemas = [sentiment_schema, feature_schema]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()
review_template = """\
For the following text, extract the following information:

sentiment: What is the sentiment of the review?\
        If the review is positive, return 'positive'.\
        If the review is negative, return 'negative'.\
        
features: Extract any features that the customer liked from the game review.\
      If the review does not mention any features or being too general, please return an empty JSON.

text: {text}

{format_instructions}
"""
prompt = ChatPromptTemplate.from_template(template=review_template)

def getAIReview(reviewText):
    messages = prompt.format_messages(text = reviewText, format_instructions=format_instructions) # format the messages
    response = chat(messages) # send the messages to the chatbot
    output_dict = output_parser.parse(response.content)
    return output_dict # return the response





# Loop through each sheet in the Excel file
for sheet_name in excel_file.sheet_names:
    # Read the sheet into a DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    
    # Loop through each row of the DataFrame
    for index, row in df.iterrows():
        # Extract the 'review' column from the current row and save it to a text file
        review_text = str(row['review'])
        author_info = json.loads(row['author'].replace("'", '"'))
        steamid = author_info['steamid']
        review_extraction = {
            'steamid': steamid,
            'description': getAIReview(review_text),
        }
        with open(f'Reviews/{sheet_name}.json', 'a') as file:
            json.dump(review_extraction, file)
            file.write(',\n')

        
