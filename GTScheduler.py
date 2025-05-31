# TODO: Given a class name, be able to return relevant class metadata (waitlist size, etc.)
from bs4 import BeautifulSoup
import requests

def get_enrollment_metadata(crn):
    try:
        res = requests.get(f'https://gt-scheduler.azurewebsites.net/proxy/class_section?term=202502&crn={crn}')
        res = res.text

        soup = BeautifulSoup(res, "html.parser")
        span = soup.findAll("span")
        
        metadata = []

        for i in range(0, len(span), 2):
            key = span[i].text
            key = key[:-1].replace(" ", "")
            key = key[0].lower() + key[1:] + ": "
            metadata.append(key)
            metadata.append(str(span[i + 1].text) + ". ")
        return ' '.join(metadata)
    except:
        return f"Couldn't find data regarding CRN {crn}. Prompt the user for the correct CRN."

if __name__ == '__main__':
    print(get_enrollment_metadata(30312))