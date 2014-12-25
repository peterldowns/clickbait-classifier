# Clickbait Classifier

This is a very naïve attempt at classifying article titles into one of two
groups: "clickbait" (à la [Buzzfeed](http://www.buzzfeed.com/) and
[Clickhole](http://www.clickhole.com/)) or "news" (à la [The New York
Times](http://www.nytimes.com/)). I was curious if this could be done
accurately; I can't think of a good definition for "clickbait" but [I know it
when I see it](http://en.wikipedia.org/wiki/I_know_it_when_I_see_it).

Eventually, I'd like to add a simple REST API and build a chrome extension that
automatically deletes clickbait from my browser as I surf the internet. I truly
cannot stand Buzzfeed.

### Setup / Installation

Theoretically, the only command you need to run is:

```shell
clickbait-classifier/ $ pip install -r requirements.txt
```

Of course, you may want to set up a virtualenv:

```shell
clickbait-classifier/ $ virtualenv env
clickbait-classifier/ $ . env/bin/activate
(env)clickbait-classifier/ $ pip install -r requirements.txt
```

The classifier's dependencies can be found in `requirements.txt`. I'd like to
say that it's a simple `pip install` but depending on your version of Python
and your OS, `scikit-learn` and `lxml` may give you some issues. Be warned:
these issues may take some time to resolve. I think it took me about 3 hours to
get everything set up and I ended up having to start using a new package
manager ([brew](http://brew.sh/)) and a new Python install.

### Usage

The code is pretty messy, but the general idea is that there is some article
data in the `data/` directory, and `classifier.py` uses this for training. You can download more data from Buzzfeed and Clickhole using the tools in `scripts/`.

```shell
clickbait-classifier/ $ ./scripts/scrape_buzzfeed.py > data/buzzfeed2.json  
clickbait-classifier/ $ ./scripts/scrape_clickhole.py > data/clickhole2.json  
```

If you feel like testing a few article titles, you can get a simple testing loop like so:

```shell
clickbait-classifier/ $ ./interactive.py
```

This will load the classifier, train it, and then present you with a simple
loop where you can paste in article titles and see the results. You can quit
using c-C. For example:

```shell
clickbait-classifier/ $ ./interactive.py
Loading classifier (may take time to train.)
Classification report:
             precision    recall  f1-score   support

  clickbait       0.91      0.62      0.74       172
       news       0.90      0.98      0.94       621

avg / total       0.91      0.91      0.90       793


  -9.0500 10 things         -5.3044 new
  -9.0500 11 things         -5.7492 bush
  -9.0500 13 times          -5.8460 overview
  -9.0500 15 times          -5.9519 iraq
  -9.0500 19 puppies        -5.9645 war
  -9.0500 2014              -5.9828 president
  -9.0500 2015              -5.9852 clinton
  -9.0500 21                -6.1021 special
  -9.0500 23 life           -6.1206 nation
  -9.0500 24                -6.1464 report
  -9.0500 25                -6.1778 campaign
  -9.0500 27                -6.2223 china
  -9.0500 33                -6.2880 york
  -9.0500 35                -6.2880 new york
  -9.0500 90s               -6.2994 plan
  -9.0500 90s kid           -6.3191 special report
  -9.0500 90s kids          -6.3523 says
  -9.0500 90s kids rejoice    -6.4277 big
  -9.0500 90s sitcom        -6.4423 challenged
  -9.0500 absolute          -6.4465 house
Done.

Article title: 43 Reasons 2014 Was The Best Year Ever To Be A Nerd
(95.13% clickbait, 4.87% news) -> clickbait

Article title: Protesters And Police Clash In Missouri For A Second Night
(19.32% clickbait, 80.68% news) -> news

Article title: 29 Christmas Vines That Will Make You Laugh Every Time
(88.25% clickbait, 11.75% news) -> clickbait

Article title: New Subprime Boom Ties Risky Loans to Car Titles
(10.98% clickbait, 89.02% news) -> news

Article title: ^C
```
