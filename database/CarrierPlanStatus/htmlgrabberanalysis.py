import requests

def fetch_and_save_html(url, file_name):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Write the content to a file
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"HTML content saved to {file_name}")
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error occurred: {e}")

# URL of the webpage to fetch
url = "https://www.nm.org/patients-and-visitors/billing-and-insurance/insurance-information/accepted-insurance-plans/northwestern-memorial-hospital#commercial"  # Replace with your desired URL

# Name of the file to save the HTML content
file_name = "commercialoutput.html"

fetch_and_save_html(url, file_name)
