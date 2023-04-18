# human-wildlife-interactions 🐘 

Check out the blog for a lot more information:
https://sallyyin.notion.site/Modeling-Social-Interests-In-Wildlife-eb82013e736d4d08ace4eb685149ce28

## Problem Statement
Social media platforms serve as a rich source of information that documents and reflects the range of societal interests in wildlife. This information can often have sizable impact in conserving biodiversity when harnessed. For instance, [literature](https://www.sciencedirect.com/science/article/pii/S0006320719305099?via%3Dihub) shows online sentiment analysis on Twitter can detect prominent conservation events towards iconic species such as rhinos. However, the vast amount of information available on social media platforms presents both an opportunity and a challenge. 

This project hopes to address the challenge of information through data science and provide insight on the landscape of social interest for conservationists. Specifically, advanced machine learning techniques may enable more sustainable ways to keep a pulse on broad social trends of interest and also more focused monitoring of specific interests.

## Problem Break Down
### model social interest through topic modeling

According to SIADS 543 lectures, “topic modeling is an unsupervised machine learning technique for discovering abstract themes that occur in a set of documents”. We leveraged this technique to automate the identification and tracking of key trends in social interest. Specifically, we analyzed the landscape of social interests in wildlife through topic modeling the titles and descriptions of YouTube wildlife videos. 
##### Additional information on topic modeling can be found in the notebooks folder

### find key characteristics around classic social interests

Beyond uncovering latent social interests in wildlife, we used the results of topic modeling as downstream labels for further analysis. Social topics such as hunting are of particular interest to the biodiversity conservation community. Labels produced from topic modeling can help cluster videos of special interests and aid in comparative descriptive analysis among groups. 

##### Additional information about the descriptive analysis can be found in the reports folder

### experiment with automated capture of classic social interest through video

With meaningful interest labels, we explored the feasibility of developing an automated multi-modal classifier based on video and audio features available in the YouTube-8M dataset. This would help generalize the solution to video-based social media platforms beyond YouTube. A classifier of this kind can be integrated with sampled content feeds and serve as a filter for content important to the conservation community at large.

##### Additional information for the classifiers can be found in the reports folder


## Instructions:
- Start by downloading the data (see the Data Access section below).
- Once you have the data, proceed to the notebooks folder and follow the instructions within the README there.
  - Note that in addition to the README instructions, each of the notebooks contains instructions as well as comments to help guide you through the steps.
- After you have completed the steps in the notebooks folder you can proceed to the reports folder and follow the instructions provided there.


## Data Access: 
The YouTube 8 Million dataset is completely free and available to access to anyone at this link: https://research.google.com/youtube8m/download.html <br>
You will need approximately 2 Terabytes of storage space to get all of the data, but there are instructions for accessing a small sample for testing purposes.
Our copy of the data was stored in Professor Neil Carter's Great Lakes' Turbo drive.

In addition to the YouTube 8 Million dataset, you will also need access to the YouTube API located here: https://developers.google.com/youtube/v3 <br> 
This access is completely free, however you will need to follow the instructions to setup your google cloud account and then enable the YouTube API from within that account. We highly recommend setting up two different API accounts / keys so that you can experiment without running into daily rate limiting issues (for the wildlife lookup a single one can do the job, but you won't be able to do more than 1 run per day). 
