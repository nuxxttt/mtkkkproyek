import requests
from bs4 import BeautifulSoup

# Function to scrape the information for each university
def scrape_university_info(url, ptn, file):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 0:
            if "infor" not in cells[2].text.lower() and "(Prodi Baru)" not in cells[5].text:
                jurusan = cells[2].text.strip()
                jenjang = cells[3].text.strip()
                # Check if cells[5] contains a numeric value
                if cells[5].text.strip().replace(".", "").replace(",", "").isdigit():
                    ketat = float(cells[5].text.strip().replace(".", "").replace(",", ".")) / float(cells[4].text.strip().replace(".", "").replace(",", "."))
                    result = f"JURUSAN : {jurusan}\nJENJANG : {jenjang}\nKEKETATAN : {ketat}\n\n"
                    print(result)
                    file.write(result)


# Main function to scrape the university names and hrefs
def main():
    url = "https://sidata-ptn-snpmb.bppp.kemdikbud.go.id/ptn_sb.php?ptn=-2"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    with open("result.txt", "w") as file:
        for row in soup.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) > 0:
                university_name = cells[2].text.strip()
                university_href = cells[2].find("a")["href"]
                result = f"University Name: {university_name}\nUniversity Href: {university_href}\n\n"
                print(result)
                file.write(result)
                # Construct the full URL for the university
                university_url = f"https://sidata-ptn-snpmb.bppp.kemdikbud.go.id/ptn_sb.php{university_href}"
                # Extract the ptn from the href
                ptn = university_href.split("=")[1]
                # Scrape the information for the university
                scrape_university_info(university_url, ptn, file)

if __name__ == "__main__":
    main()
