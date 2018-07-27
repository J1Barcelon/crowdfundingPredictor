import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from pandas import ExcelWriter
from pandas import ExcelFile
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import linear_model

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

df_cons = pd.read_excel('consolidated_lda_dataset_log_wooutliers.xlsx')
y_cons = df_cons.iloc[1:,0].values.tolist()
X_cons = df_cons.iloc[1:,1:].values.tolist()

y_lda = np.array(y_cons)
X_lda = np.array(X_cons)

clf_lda = LinearDiscriminantAnalysis()
clf_lda.fit(X_lda,y_lda)

capital = float(input("How much is your required capital? "
                      "Please convert to USD if otherwise."))
currency = input("What currency will you be using? "
                 "Choose between USD, CAD, EUR, GBP, AUD, or PHP.")
segment = input("What industry would your product belong to? "
                "Choose between Arts, Music, Film, Games, Design & Tech, Publishing, "
                "Food & Crafts, Comics & Illustration")
rewards = float(input("How many reward levels will you be providing?"))
length = float(input("How many days will your campaign last?"))
month = input("On what month will you start the campaign?")
videos = float(input("How many videos will you be uploading?"))
images = float(input("How many images will you be uploading?"))
faqs = float(input("How many FAQs will you be posting?"))
fb = input("Will you be including a link to a Facebook page for the campaign? Yes or No")
updates = float(input("How many updates are you planning to make?"))

#natural log transformation for capital
log_capital = math.log(capital)

#dummy variables for currency
usd = 0
cad = 0
eur = 0
gbp = 0
aud = 0
php = 0

if currency == "USD":
    usd = 1
elif currency == "CAD":
    cad = 1
elif currency == "EUR":
    eur = 1
elif currency == "GBP":
    gbp = 1
elif currency == "AUD":
    aud = 1
elif currency == "PHP":
    php = 1
else:
    pass

#dummy variables for segment
arts = 0
music = 0
film = 0
games = 0
design_tech = 0
publishing = 0
food_crafts = 0
comics_illustration = 0

if segment == "Arts":
    arts = 1
elif segment == "Music":
    music = 1
elif segment == "Film":
    film = 1
elif segment == "Games":
    games = 1
elif segment == "Design & Tech":
    design_tech = 1
elif segment == "Publishing":
    publishing = 1
elif segment == "Food & Crafts":
    food_crafts = 1
elif segment == "Comics & Illustration":
    comics_illustration = 1
else:
    pass

#dummy variables for month
jan = 0
feb = 0
mar = 0
apr = 0
may = 0
jun = 0
jul = 0
aug = 0
sep = 0
oct = 0
nov = 0
dec = 0

if month == "January":
    jan = 1
elif month == "February":
    feb = 1
elif month == "March":
    mar = 1
elif month == "April":
    apr = 1
elif month == "May":
    may = 1
elif month == "June":
    jun = 1
elif month == "July":
    jul = 1
elif month == "August":
    aug = 1
elif month == "September":
    sep = 1
elif month == "October":
    oct = 1
elif month == "November":
    nov = 1
elif month == "December":
    dec = 1
else:
    pass

#dummy variables for fb
if fb == "Yes":
    fb = float(1)
elif fb == "No":
    fb = float(0)
else:
    pass


user_inputC = []
user_inputC.extend((log_capital, rewards, videos, images, faqs, fb, updates, usd, cad, eur, gbp, aud, php,
                    arts, music, film, games, design_tech, publishing, food_crafts, comics_illustration,
                    jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec))
platform = float(clf_lda.predict([user_inputC]))

if platform == 1 and php == 0:
    platform = 0

if platform == 0:
    print("Global Platform")
elif platform == 1:
    print("Local Platform")

df_global = pd.read_excel('global_logit_dataset_log.xlsx')
y_global = df_global.iloc[1:,0].values.tolist()
X_global = df_global.iloc[1:,1:].values.tolist()

df_local = pd.read_excel('local_logit_dataset_log.xlsx')
y_local = df_local.iloc[1:,0].values.tolist()
X_local = df_local.iloc[1:,1:].values.tolist()

y_logitG = np.array(y_global)
X_logitG = np.array(X_global)

y_logitL = np.array(y_local)
X_logitL = np.array(X_local)


if platform == 0:
    clf_logit = linear_model.LogisticRegression()
    clf_logit.fit(X_logitG,y_logitG)

    user_inputG = []
    user_inputG.extend((log_capital, length, videos, images, faqs, fb, updates, usd, cad, eur, gbp,
                        arts, music, film, publishing, apr))
    lorc = float(clf_logit.predict([user_inputG]))

    if lorc == 0:
        print("Low Likelihood of Obtaining Required Capital")
    elif lorc == 1:
        print("High Likelihood of Obtaining Required Capital")
elif platform == 1:
    clf_logit = linear_model.LogisticRegression()
    clf_logit.fit(X_logitL, y_logitL)

    user_inputL = []
    user_inputL.extend((log_capital, rewards, faqs, updates, may, jul))
    lorc = float(clf_logit.predict([user_inputL]))
    if lorc == 0:
        print("Low Likelihood of Obtaining Required Capital")
    elif lorc == 1:
        print("High Likelihood of Obtaining Required Capital")











