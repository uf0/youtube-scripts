youtube-scripts
============

Various scripts to get youtube data

##Installation
Install virtualenv:

``` sh
$ sudo easy_install virtualenv
```

Download git repository:

``` sh
$ git clone https://github.com/uf0/imgs-scripts.git
```

browse to youtube-scripts root folder:

``` sh
$ cd youtube-scripts
```

Create a virtualenv directory `env`, activate the virtualenv and install the requirements:

``` sh
$ virtualenv --no-site-packages env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Copy the config sample file:

``` sh
$ cp config.sample.py config.py
```
open the file add your API key

##Google API key
You need to obtain your google API key and activate the Google+ service from the [Google API Console](https://code.google.com/apis/console).

[Here](https://www.youtube.com/watch?v=69ZwR4o7oGQ) there's a quick video tutorial


##Run scripts

###getComments.py
This script gets in input a `.tsv` file containing the videos ID (in one column named `id`) and outputs a .tsv file with all the comment(s) (text, author, date, ecc) for each video.

Type `$ python getComments.py -h` for usage instructions

**Usage example**

``` sh
$ python -i fileWithID.tsv -o allComments.tsv
```