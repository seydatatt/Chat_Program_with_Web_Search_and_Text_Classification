#!/usr/bin/env python
# coding: utf-8

import sqlite3
from transformers import pipeline
import requests
import random

class TextClassifier:
    def __init__(self, model_name='joeddav/xlm-roberta-large-xnli'):
        self.classifier = pipeline('zero-shot-classification', model=model_name, framework='tf')
        self.candidate_labels = ["Eğitim", "Teknoloji", "Sağlık", "Spor", "Moda", "Seyahat", "Yemek", "Finans"]

    def classify(self, text):
        result = self.classifier(text, self.candidate_labels)
        main_topic = result['labels'][0]  # En yüksek olasılıklı etiket
        return main_topic

#Veritabanı oluşturma kod bloğu
class DatabaseManager:
    def __init__(self, db_name='chat_program.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS topics (
                                id INTEGER PRIMARY KEY,
                                main_topic TEXT NOT NULL,
                                sub_topics TEXT NOT NULL
                                );''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS search_results (
                                id INTEGER PRIMARY KEY,
                                topic_id INTEGER,
                                link TEXT,
                                FOREIGN KEY(topic_id) REFERENCES topics(id)
                                );''')

    def save_topic(self, main_topic, sub_topics):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO topics (main_topic, sub_topics) VALUES (?, ?)', 
                           (main_topic, ','.join(sub_topics)))
            return cursor.lastrowid

    def save_search_results(self, topic_id, search_results):
        with self.conn:
            self.conn.executemany('INSERT INTO search_results (topic_id, link) VALUES (?, ?)',
                                  [(topic_id, link) for link in search_results])

#Web araması yapma kod bloğu 
class WebSearcher:
    def __init__(self, api_key, cx):
        self.api_key = api_key
        self.cx = cx

    def search(self, query):
        search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.api_key}&cx={self.cx}"
        try:
            response = requests.get(search_url)
            response.raise_for_status()
            search_results = response.json()
            links = []
            if 'items' in search_results:
                for item in search_results['items']:
                    links.append(item['link'])
            return links
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return []

class ChatProgram:
    def __init__(self, api_key, cx):
        self.classifier = TextClassifier()
        self.db_manager = DatabaseManager()
        self.web_searcher = WebSearcher(api_key, cx)

    def run(self):
        previous_main_topic = None
        while True:
            user_input = input("Lütfen bir metin girin (çıkmak için 'q' tuşlayın): ")
            if user_input.lower() == 'q':
                break
            
            main_topic = self.classifier.classify(user_input)
            sub_topics = self.get_sub_topics(main_topic)
            topic_id = self.db_manager.save_topic(main_topic, sub_topics)
            self.print_to_console(main_topic, sub_topics)
            search_results = self.web_searcher.search(main_topic)
            self.db_manager.save_search_results(topic_id, search_results)
            self.print_general_topic(main_topic, search_results)

            previous_main_topic = main_topic

    def get_sub_topics(self, main_topic):
        # Alt konular için bir örnek listesi
        sub_topics_pool = {
            "Eğitim": ["Edebiyat", "Tarih", "Felsefe"],
            "Teknoloji": ["Yapay Zeka", "Blok Zinciri", "Nesnelerin İnterneti"],
            "Sağlık": ["Diyet", "Spor Beslenmesi", "Zihinsel Sağlık"],
            "Spor": ["Futbol", "Basketbol", "Yüzme"],
            "Moda": ["Giyim", "Aksesuarlar", "Moda Trendleri"],
            "Seyahat": ["Avrupa", "Asya", "Amerika"],
            "Yemek": ["Mediterranean", "Uzak Doğu Mutfağı", "Vegan Yemekler"],
            "Finans": ["Yatırım", "Kripto Para", "Borsa"]
        }
        
        if main_topic in sub_topics_pool:
            sub_topics = random.sample(sub_topics_pool[main_topic], 3)
        else:
            # Genel konu listede yoksa, rastgele alt konular seç
            sub_topics = random.sample(list(sub_topics_pool.values())[0], 3)
        
        return sub_topics

    def print_to_console(self, main_topic, sub_topics):
        print(f"Genel Konu: {main_topic}")
        print("Alt Konular:")
        for topic in sub_topics:
            print(f"- {topic}")

    def print_general_topic(self, main_topic, search_results):
        print(f"Genel Sohbet Konusu: {main_topic}")
        print("Arama Sonuçları:")
        for link in search_results:
            print(link)

if __name__ == "__main__":
    API_KEY = 'Your_API_KEY'  
    CX = 'Your_CX' 
    chat_program = ChatProgram(API_KEY, CX)
    chat_program.run()


# In[ ]:




