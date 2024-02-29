import requests
import openai
from bs4 import BeautifulSoup

#set openai key
openai.api_key = "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" 

def generate_openai_summary(url):
    response = requests.get(url)
    #check if the website can be accessed
    print(response.status_code)
    if response.status_code == 200:
        content = response.text
        #parse the content just for text
        soup = BeautifulSoup(content, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # print (text)
        main_content = soup.text
    
        #since the OpenAi api has a 4067 token limit, we have to set a limit to read from the webpage
        chunk = main_content[0:4000]
       
        # Call the OpenAI API to generate a summary
        prompt_request = chunk + ".\n\nreturn a Tl;dr summary of this snippet of a webpage. Make the summary give a breif overview about what the page is about."
        response = openai.Completion.create(
            #Define the OpenAI parameters
            engine="text-davinci-003",  # Replace with your desired OpenAI engine
            prompt=prompt_request,
            max_tokens=60,  # Adjust the desired length of the summary
            temperature=0.9,  # Control the randomness of the generated text
            n=1,  # Set the number of completions to generate
            stop=None,  # Specify a custom stop condition if needed
            timeout=None,  # Set a timeout if desired
        )
        print('here:',response.choices[0].text.strip())
        return response.choices[0].text.strip()
        #return response
    else:
        print(f"Error: Failed to retrieve the webpage. Status code: {response.status_code}")
        return None
    

# Sample function usage
#url = "https://www.ics.uci.edu/" 
#summary = generate_summary(url)
#print(summary)




