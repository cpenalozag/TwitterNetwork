# Twitter User Network
Scripts for creating a directed network of Twitter followers.

These scripts work in three parts.

1. Taking an initial user, download information about who they follow. Repeat recursively until depth *d*.
2. Generate the files `edges.csv` and `vertices.csv` required to create the directed graph.
3. Create and visualize the network.

## Requirements
* Tweepy
* NetworkX
* Jupyter Notebooks

## Usage

### Extract The Information
* Choose the Twitter user where the program will start e.g. `@NoticiasCaracol`.
* Decide what recursive depth you want to go.  A depth of 1 or 2 should be done in a few hours (depending on how many people they are following), a depth of 5 can take several days.

`python GetFollowing.py -s NoticiasCaracol -d 2`

This will generate a directory structure like
```
.
├── following
│   ├── NoticiasCaracol.csv
│   └── Bogota.csv
└── twitter-users
    ├── 17813487.json
    └── 57664761.json
```

The `following` directory contains a file for every Twitter user name searched. Each file is a `.csv` file showing who they are following.

The `twitter-users` directory contains a `.json` representation of every user. The file name is their Twitter ID.

### Generate The Network Files

This script parses the `.csv` files and creates two new `.csv` which contains the elements of the network.

    python GenerateNetwork.py -s NoticiasCaracol
    
The file `edges.csv` contains the network's edges delimited by commas:

```
source,target
17813487,57664761
```

Column 1 is the Twitter ID of a User. Column 2 is the ID of a User they follow.

The file `vertices.csv` inside the directory network-data/ contains the network's vertices delimited by commas:

```
id,screen_name,followers,friends
17813487,NoticiasCaracol,8321076,1287
```

Column 1 is the Twitter ID. Column 2 is the screen name. Column 3 has the number of followers of the user. Column 4 has the number of users followed by this user.


### Collect tweets

This script gets up to 3200 of each user's latest tweets. 

`python GetStatuses.py`

Results are saved in the `statuses.csv` file inside of the tweets/ directory. 


```
user id,created_at,text,favorite_count,retweet_count,phone,sensitive,hashtags,no_hashtags,mentions,no_mentions,no_urls,no_media
```

The columns are:
* ID of the user who wrote the tweet
* created_at: Date the tweet was created
* text: Extended text of the tweet
* favorite_count: Number of times the tweet has received a 'favorite' from a user
* retweet_count: Number of times the tweet has been retweeted
* phone: Device from which the tweet was posted
* sensitive: Indicator that an URL contained in the Tweet may contain content or media identified as sensitive content
* hashtags: List of all the hashtags in the tweet
* no_hashtags: Number of hashtags in the tweet
* mentions: List of IDs of the users mentioned in the tweet
* no_mentions: Number of mentions in the tweet
* no_urls: Number of URLs in the tweet
* no_media: Number of media elements in the tweet


### Create and visualize the network.

Run jupyter notebooks with the command:

    jupyter notebook
    
Open the `Graph.ipynb` notebook and run it.

![Sample graph](network-data/network.png)