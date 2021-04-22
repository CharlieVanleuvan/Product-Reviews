#import packages for web scraping
import bs4 as bs
import urllib.request
import lxml

#import packages for web browser driving
from selenium import webdriver
from time import sleep
from webdrivermanager import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

#import packages for the GUI and plotting
import PySimpleGUI as sg 
import numpy as np
import matplotlib.pyplot as plt 

#import packages for wordcloud
from wordcloud import WordCloud, STOPWORDS
import pandas as pd

#import tokenizer packages
from nltk.tokenize import word_tokenize 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize



def rei_link(product):
    """Takes a product name and creates a REI search URL from it"""
    product = product.replace(' ','+')
    rei_url = 'https://www.rei.com/search?q=' + product
    return(rei_url)

#REI base url link
rei_base_url = 'https://www.rei.com'




#empty list to append all product models found in search
product_models = []
#empty list to append all URLs 
product_urls = []

def products_found(soup_object):
    """A function that returns the products found on search page. Requires a soup object"""
    for item in soup_object.find_all('a', class_ = "_1A-arB0CEJjk5iTZIRpjPs"):
        #This initial find_all() only returns 1 item. Product tags are nested in here

        #return the model names found in search results
        for div in item.find_all('div', class_ = "r9nAQ5Ik_3veCKyyZkP0b"):
            product_models.append(div.text)
        
        #return the URLs found in search results
        for span in item.find_all('span', class_ = "_2xZVXKL4Bd0pJyQCumYi9P"):
            product_urls.append(rei_base_url + item.get('href'))
    return("Successfully searched.")        



def selected_product_url(soup, index):
    for item in soup.find_all('a', class_ = "_1A-arB0CEJjk5iTZIRpjPs"):
        for div in item.find_all('div', class_ = "r9nAQ5Ik_3veCKyyZkP0b"):
            if div.text == index:
                return(rei_base_url + item.get('href'))




#set global Options to get headless browsing to be used in webdriver.Firefox()
options = Options()
options.headless = True

def word_cloud(reviews):
    """A Function that generates a word cloud from a web page containing product reviews"""

    #create a text string to add all words to
    review_words = ''
    #stop words
    stopwords = set(STOPWORDS)
    #iterate through the reviews
    for item in reviews:
        #tokenize the text
        tokens = word_tokenize(item.text)    
        #convert the tokens into lower case
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
    
        #append to review_words
        review_words += " ".join(tokens) + " "
    #generate word cloud
    wordcloud = WordCloud(width = 800,
                         height = 800,
                         background_color = 'white',
                         stopwords = stopwords,
                         min_font_size = 10).generate(review_words)
    
    #plot the word cloud object
    plt.figure(figsize = (8,8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    return(plt.show(block=False))


def sentiment_plot(sentences):
    """A function that takes list of sentences and gets sentiment scores"""

    y = [SentimentIntensityAnalyzer().polarity_scores(sentence)['compound'] for sentence in sentences if SentimentIntensityAnalyzer().polarity_scores(sentence)['compound'] != 0]
    x = np.linspace(0, len(y), len(y))

    plt.figure()
    plt.scatter(x,y, c=y, cmap='coolwarm')
    plt.xlabel('Sentences (backwards in time)')
    plt.ylabel('Compound Rating')
    plt.title('Sentiment Compund Ratings')
    return(plt.show(block=False))


def sentiment_compound_score(sentence_list):
    #A function that calculates the average compound score for all sentences in a product review listing
    compound_scores = []

    for sentence in sentence_list:
        compound_scores.append(SentimentIntensityAnalyzer().polarity_scores(sentence)['compound'])
    
    #return the average value
    return(sum(compound_scores) / len(compound_scores))

def print_reviews(reviews):
    #A function that takes a reviews object and prints them

    review_list = []

    for item in reviews:
        review_list.append(item.text)

    return(review_list)



#create GUI
sg.theme('DarkBlue17')

layout = [  [sg.Text('Enter a product name:'),sg.InputText(key = '_INPUT_'),sg.Button('Search')],
            [sg.Text('The following products match your search. Click one to see reviews.'), sg.Button('Clear results')],
            [sg.Listbox([], enable_events=True, key='_PRODUCTS_',size=(60,20)),sg.Multiline(key = '_REVIEW_TEXT_',size=(50,10))],
            [sg.Text('# of Reviews:'), sg.InputText(key = '_REVIEWS_'), sg.Text('Sentiment Rating Score'), sg.InputText(key = '_RATING_')],
            [sg.Button('Sentiment Rating Plot'), sg.Button('Word Cloud')],
            [sg.Button('Exit')]]

window = sg.Window('Product Reviews', layout)


while True:
    event, values = window.read()

    #check if window is closed
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear results':
        window.FindElement('_PRODUCTS_').Update('')

    if event == 'Search':
        #create the search results source object
        source = urllib.request.urlopen(rei_link(values['_INPUT_'])).read()
        #create soup object from the source link
        soup = bs.BeautifulSoup(source, 'html.parser')
        sleep(3)
        
        #clear product_models and product_urls
        product_models = []
        product_urls = []

        #scrape the website search results
        products_found(soup)
        print("Found products")
        for product in product_models:
            print(product)
        for url in product_urls:
            print(url)

        #for the products returned into product_models, add each to the listbox 
        for product in product_models:
            window.FindElement('_PRODUCTS_').Update(values = product_models)

    if event == '_PRODUCTS_':
        #take the selected index, grab the URL, and put URL into headless selenium browser

        #Grab the selected product name
        index = values['_PRODUCTS_'][0]
        print("Index selected")

        #open firefox browser in Selenium   
        browser = webdriver.Firefox()
        sleep(5)
        print("Browser opened")

        #navigate to product page
        try:
            browser.get(selected_product_url(soup = soup, index = index))
            sleep(10)
            print("Opened product page. Waiting 10 seconds.")
            print(selected_product_url(soup = soup,index = index))
        except:
            print("Could not load url.")
            print(selected_product_url(soup = soup,index = index))

        #load more comments, if exists
        try:
            browser.find_element_by_xpath('/html[1]/body[1]/div[2]/div[2]/div[3]/div[2]/div[9]/div[10]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/button[1]').click()
            print("Loading extra reviews. Waiting 10 seconds.")
            sleep(10)
        except:
            print("No extra comments to load.")
        
        #get reviews from web page
        reviews = browser.find_elements_by_class_name('bv-content-summary-body-text')
        sleep(10)

        #display review text in GUI
        window.FindElement('_REVIEW_TEXT_').Update('\n\nComment:\n'.join(print_reviews(reviews)))
        print("Displayed review text.")
        sleep(12)

        window.FindElement('_REVIEWS_').Update(len(reviews))
        print("Found {} reviews.".format(len(reviews)))
        print("End product search")

    if event == 'Word Cloud':
        word_cloud(reviews)
        print("Displayed word cloud.")

    if event == 'Sentiment Rating Plot':
        #sentences list to be appended to
        sentences = []

        #loop through reviews and pull out sentences
        for item in reviews:
            sentence_tokens = sent_tokenize(item.text)

            #append to sentences list
            for sentence in sentence_tokens:
                sentences.append(sentence)
        
        #calculate average sentiment rating and display it
        window.FindElement('_RATING_').Update(sentiment_compound_score(sentences))
        #return sentiment plot
        sentiment_plot(sentences)      

        print("Displayed sentiment plot.")

try:
    browser.quit()
except:
    pass
window.Close()