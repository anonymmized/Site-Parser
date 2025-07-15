import re
import os
import csv
import time
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor



class SiteParser:
    def __init__(self):
        self.visited_urls = set()
        self.results = {}
        self.start_time = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def is_valid_url(self, url, base_domain):
        parsed = urlparse(url)
        return bool(parsed.netloc) and parsed.netloc == base_domain

    def get_all_links(self, soup, base_url, base_domain):
        links = []
        for link in soup.find_all('a', href=True):
            url = urljoin(base_url, link['href'])
            if self.is_valid_url(url, base_domain):
                links.append(url)
        return links

    def export_to_csv(self, filename="results.csv"):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Word', 'URL', 'Location'])
            for word in self.results:
                for url, locations in self.results[word].items():
                    writer.writerow([word, url, '; '.join(locations)])
        print(f"\nResults saved to {filename}")

    def export_to_json(self, filename="results.json"):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.results, file, ensure_ascii=False, indent=4)
        print(f"\nResults saved to {filename}")

    def generate_report(self):
        total_time = time.time() - self.start_time
        report = f"""
=== Scan Report ===
Scan time: {total_time:.2f} seconds
Pages scanned: {len(self.visited_urls)}
Words found: {len(self.results)}
===================
"""
        return report

    def search_words(self, url, words):
        try:
            response = requests.get(url, timeout=5, headers=self.headers)
            response.raise_for_status()

            if 'charset' in response.headers.get('content-type', '').lower():
                response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()

            for script in soup(["script", "style"]):
                script.decompose()

            for word in words:
                word = word.lower()
                if word in text:
                    locations = []
                    for tag in soup.find_all(text=re.compile(word, re.I)):
                        parent = tag.parent.name
                        context = tag.strip()[:50] + "..."
                        locations.append(f"In tag <{parent}>: {context}")

                    if word not in self.results:
                        self.results[word] = {}
                    self.results[word][url] = locations

            return soup
        except requests.RequestException as e:
            print(f"Network error processing {url}: {str(e)}")
            return None
        except Exception as e:
            print(f"General error processing {url}: {str(e)}")
            return None

    def crawl(self, start_url, words, max_pages=50):
        """Улучшенный обход сайта"""
        self.start_time = time.time()
        base_domain = urlparse(start_url).netloc
        urls_to_visit = [start_url]

        with ThreadPoolExecutor(max_workers=3) as executor:
            while urls_to_visit and len(self.visited_urls) < max_pages:
                url = urls_to_visit.pop(0)
                if url not in self.visited_urls:
                    print(f"Scanning: {url}")
                    self.visited_urls.add(url)

                    future = executor.submit(self.search_words, url, words)
                    soup = future.result()

                    if soup:
                        new_links = self.get_all_links(soup, url, base_domain)
                        urls_to_visit.extend(link for link in new_links if link not in self.visited_urls)

                    time.sleep(0.5)


def display_ascii_art():
    print("""
    ╔═══════════════════════════════════════╗
    ║        SITE PARSER v1.0               ║
    ║    ____  ___ _____ ___               ║
    ║   / ___||_ _|_   _| __|             ║
    ║   \\___ \\ | |  | | | _|              ║
    ║    ___) || |  | | | |_              ║
    ║   |____/___| |_| |___|              ║
    ║                                      ║
    ║   PARSER & WORD FINDER              ║
    ╚═══════════════════════════════════════╝
    """)


def main():
    display_ascii_art()
    parser = SiteParser()

    print("Select search mode:")
    print("[1] Search single word")
    print("[2] Search from dictionary")
    print("[3] Load words from file")

    choice = input("Your choice (1/2/3): ")
    url = input("Enter website URL: ")

    words = []
    if choice == "1":
        word = input("Enter word to search: ")
        words = [word]
    elif choice == "2":
        print("Enter words to search (one per line). Press Enter twice to finish:")
        while True:
            word = input()
            if not word:
                break
            words.append(word)
    elif choice == "3":
        filename = input("Enter path to words file: ")
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                words = [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return

    max_pages = int(input("Enter maximum pages to scan (default 50): ") or 50)

    parser.crawl(url, words, max_pages)

    if parser.results:
        print("\nSearch Results:")
        for word in parser.results:
            print(f"\nWord '{word}' found on following pages:")
            for url, locations in parser.results[word].items():
                print(f"\nURL: {url}")
                print("Location:", ", ".join(locations))

        print("\nSelect export format:")
        print("[1] CSV")
        print("[2] JSON")
        print("[3] Both formats")
        export_choice = input("Your choice (1/2/3): ")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if export_choice in ["1", "3"]:
            parser.export_to_csv(f"results_{timestamp}.csv")
        if export_choice in ["2", "3"]:
            parser.export_to_json(f"results_{timestamp}.json")

        print(parser.generate_report())
    else:
        print("\nNothing found")


if __name__ == "__main__":
    main()
