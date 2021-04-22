# Product-Reviews

The objective of this task is to create a graphical user interface that does some quite basic analysis or information retrieval. This program is for educational purpose only.

Product_Reviews was developed to aggregate product reviews on a popular hiking gear website in a simple to use GUI. This GUI displays a Word Cloud, compound sentiment score scatter plots, and an average compound sentiment score for the product that you search. 

## Under the Hood
4 key libraries make up this program. In order of use, they are:
1. **BeautifulSoup**
    - to create a soup object to search retailer's website and return the products for sale
2. **Selenium**
    - used as a navigation tool to load dynamic content, such as product reviews
3. **Matplotlib**
    - for graphing word clouds and scatter plots
4. **NLTK**
    - used to tokenize words and sentences and generating compound sentiment scores

## GUI Choice
**PySimpleGUI** was chosen for this task, due to simplicity of setup. PSG is built from a few other popular Python GUI libraries (including tkinter), which gives it enough functionality to provide the features needed for this task. 
![image](https://user-images.githubusercontent.com/53887674/115645163-db973200-a2ed-11eb-9128-e5cdadb6b101.png)

## Graphing Sentiment
Combining NLTK's `SentimentIntensityAnalyzer()` with Matplotlib and embedding within the GUI allows the user to view that product's review sentiment and the trend over time.

![image](https://user-images.githubusercontent.com/53887674/115645430-5c562e00-a2ee-11eb-9eeb-ab3e1fa4a0b6.png)

A scatterplot of Product Rating vs. Compound Sentiment score can also be shown. This is the relationship between a product's reviews and the rating it has on the retailer site:

![image](https://user-images.githubusercontent.com/53887674/115645466-6e37d100-a2ee-11eb-832a-e8f1bb93f884.png)
