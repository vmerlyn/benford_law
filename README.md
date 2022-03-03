# Benford's law 
> Benford's law, also known as the Newcomb–Benford law, the law of anomalous numbers, or the first-digit law, is an observation that in many real-life sets of numerical data, the leading digit is likely to be small.[1] In sets that obey the law, the number 1 appears as the leading significant digit about 30 % of the time, while 9 appears as the leading significant digit less than 5 % of the time. If the digits were distributed uniformly, they would each occur about 11.1 % of the time.[2] Benford's law also makes predictions about the distribution of second digits, third digits, digit combinations, and so on.

Ref - [Benford's law](https://en.wikipedia.org/wiki/Benford%27s_law)


## Running the app
With Docker -
From the project root folder command line -
  1. `docker build --tag flask-benford-app .`
  2. `docker run --name flask-benford-app -p 5001:5001 flask-benford-app`

Without Docker -
From the project root folder command line -
  1. `pip install -r requirements.txt`
  2. `python app.py`
  3. Paste the displayed url from the console, into a browser

The current version only works for the file provided with this assignment. 
A smaller version of this file is available in the tests\data folder. 

## Running tests
Run pytest from the project root folder. 