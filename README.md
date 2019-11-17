# Twitter_plotbot
Tweepy, vaderSentiment, Heroku


Look at results: https://twitter.com/UCR_Jason_Wu
Test account: https://twitter.com/projecttestonly
Problem: Sometimes tweets may not show using the search function, unfortunately there is no easy solution to resolve this, but to either deactivate and remake the account or use another account to provide the commands.

Build a twitter bot that sends sentiment analysis for tweets by another twitter user. The pattern used will be "@projecttestonly Analyze: @CNN". Tweets like this will trigger the bot to perform a sentiment analysis on the target user (@CNN). The outputs should look similar to:
![cnn](analysis/@CNN.png)
![nytimes](analysis/@nytimes.png)

Heroku Deployment:
For the twitter API keys, use config vars and os.get() to retrieve global variables. 
Automatic deploys is enabled. 
Remember to enable the free Dyno, under resources.
Check logs on the upper right under 'more' to view activity. 
