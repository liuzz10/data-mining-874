# Readme

## All files

Homework files:

- Final paper.docx
- Final project presentation.pptx

Program file:

- `opioid-tweets-exploration-0513.ipynb`: it is the jupyter notebook file for the main program.

Data files:

- `categories.csv`: all terms in DUI lexicons and categories that each term belongs to.
- `opioid_tweets(3rd).csv`: all tweets with at least oneopioid-related keywords (data get from the 1st fetch).
- `dui_filter_tweets_by_keywords(3rd).csv`: all tweets in `opioid_tweets(3rd).csv` sorted by the frequency of DUI terms. It's totally the same with `opioid_tweets(3rd).csv` except that the order is different so that it may benefit data annoation.
- `abuse.csv`: tweets that are most likely posted by opioid-addiected users.
- `recovered.csv`: tweets that are most likely posted by opioid-recovered users who are clean and recovered from previous opioid addiction.

- `recovered_user_tweets.dictionary`: all regular tweets posted by users in `recovered.csv` (data get from the 2nd fetch).
- `abuse_user_tweets.dictionary`: all regular tweets posted by users in `abuse.csv` (data get from the 2nd fetch).

The program takes the above 2 files as input data and does the analysis.

## Dependencies

- VADER: pip install vaderSentiment (https://pypi.org/project/vaderSentiment/)
- matplotlib: pip install matplotlib (https://pypi.org/project/matplotlib/)
- numpy: pip install numpy (https://numpy.org/install/)
- pandas: pip install pandas (https://pypi.org/project/pandas/)
- seaborn pip install seaborn (https://pypi.org/project/seaborn/)
- scipy: python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose (https://scipy.org/install/)
- textblob: pip install textblob (https://pypi.org/project/textblob/)
- nltk: pip install --user -U nltk (https://www.nltk.org/install.html)
- gensim: pip install gensim (https://pypi.org/project/gensim/)
- scikit-learn: pip install scikit-learn (https://pypi.org/project/scikit-learn/)

## Run the program

1. cd to `final_project` directory.
2. Type `jupyter notebook` to launch the Jupyter Notebook App. Click and open `opioid-tweets-exploration-0513.ipynb`.
3. Follow instructions in the .ipynb file to manually run code in each cell. There are 3 sections, the 1st section is not runnable since data have been fetched already and saved into `recovered_user_tweets.dictionary` and `abuse_user_tweets.dictionary`. Runnable program starts from the 2nd section: User-level sentiment analysis using vader. To avoid running the 1st section, I removed Twitter tokens to access the API.
