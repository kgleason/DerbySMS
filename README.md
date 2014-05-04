#Derby SMS
This was written as an experiment to replace a paper based bidding system at a party. The main development happens at [BitBucket](https://bitbucket.org/kgleason/derbysms), which is where I track my issues. The code is also posted to [GitHub](https://github.com/kgleason/DerbySMS) as a convenience, but the issues are tracked at [BitBucket](https://bitbucket.org/kgleason/derbysms/issues?status=new&status=open).

##The rules

 * Each horse in the race is available to bid on.
 * Once the bidding is open, everyone can bid on any horse they want in whole dollar amounts.
 * Each bid must be higher than the previous bid.
 * At the close of betting, the highest bidder on that horse get's the winings if their horse wins.
 
 
##Usage
There are 2 components to using this. The web interface, and the SMS interface.

###The web UI
The web interface is provided to show the status of the bidding, as well as to keep the bidding process transparent. The web interface, currently, is made up of 5 sections:

  * Current bids: this page will show the current status of the bidding. Right now it auto-refreshes every 5 seconds. I plan to make that a little better.
  * Horses: This page shows some detail about the horses, including their names, shortcodes for texting purposes, and the position. 
  * Bidders: This pages shows all of the bidders.
  * All bids: This page shows a complete history of all of the bidding. 
  * Help: This page is an attempt to explain what the various SMS commands are.
  
  Clicking on any horse's name will take you to the bidding history for that horse. Clicking on any bidder's name will take you to the bidding history for that person.
  
###The SMS interface
The SMS interface is where most of the fun happens. There are several commands that are available to all bidders. Since the SMS interface is currently sessionless, each SMS needs to begin with the command in order to provide context. Someday perhaps I will add sessions and try to beef up the SMS parser a bit.

  * name: This command is used to add a name to go along with your mobile number. By default, if there is no name for you recorded in the database, you will show up in the web interface as your mobile number. If you add your name, then your name will be avilable in the web interface. The format of this command is __name firstname lastname__
  * status: This command has a couple of different options. Sending it through by itself will return a list of all of the horses for which you are the current high bidder. Sending the shortname of a horse will return the current high bid and bidder for that horse. The format of this command is one of: __status__ or __status HorseShortName__
  * bid: This command is used to place a bid on a horse. If your bid is higher than the current highest bid, then you will be notified that your bid was accepted. If your bid is not higher than the current high bid, you will be informed that your bid has been rejected and told what the current high bid is. The format of this command is __bid HorseShortName amount__
  * bet: This command is an alias for bid. It works exactly the same way.
  
In addition to those commands, if you have been set up as an administrator (see below), then the following commands are also available to you. If you attempt these commands but are not an administrator, then you will be informed.

  * horse add: This command is used to add a new horse to the list. This command requires you to indicate the position that the horse is in, and the shortname of the horse. The SMS parser is rather unintelligent at this point, and it assumes that all information has been provided. The first "word" that is presented after the command is taken as the position, and the second word after the command is taken as the shortname. The rest of the words are recorded as the full name. The format of this command is __horse add PostPosition HorseShortName Full Name__
  * horse mod: This command is used to modify an existing horse in the line up. It works exactly the same was as the add command, but checks to make sure that the horse exists first. the format of this command is __horse mod PostPosition HorseShortName Full Name__
  * horse new: This command is an alias for "horse add". It works exactly the same way.
  * turn: This command takes a required parameter of either _on_ or _off_. The __turn on__ command will begin the bidding. The __turn off__ command will end the bidding.
 
##Requirements
If this all sounds interesting for you, then you will need a few things to get started:

  * access to some sort of system when you can run a Flask application. I'm going to assume some sort of debian linux derivative, but I'm doing my development on OS X. If you know what you are doing, then you should be able to get it to run pretty much anywhere.
  * A [Twilio](www.twilio.com) account. [Twilio](www.twilio.com) is the services that enables the text messaging portion of this whole thing.
  * Some patience. My installation process is pretty borked right now. I'll be getting it cleaned up, but for now ...   

##Installation
The installation process right now isn't great. Sorry. I'm still learning Python and Flask, and so far everything has been run from my dev machine with an ngrok tunnel for external connectivity. This is my first attempt at actually installing something I've written somewhere more permanent, and I've realized that I need to work on these processes. Have a look at my issues on [BitBucket](https://bitbucket.org/kgleason/derbysms/issues?status=new&status=open) to see what I am planing on getting fixed.

Right now it is out there and running, and controlled via `supervisor`, so start with `sudo apt-get install supervisor`. I am assuming that you are using some sort of debian derivative. Next you have 2 choices: either set up a virtual environment or install of the dependencies on the host system. For the sake of simplicity, I'm going to skip the virtualenv piece, and jump right to `sudo pip install -r requirements.txt`. I know it isn't ideal, so feel free to submit a pull request to help me make it better.

Right now, the code checks for a row in the database before it starts, but on the initial installation, the database doesn't exist. For the time being, the work around is to comment out a couple of line of code. (Another thing that I want to improve.) Open up `manage.py` and comment out the 3 lines that begin with

``` 
if not TwilioConfig.query.all()
```
Save the file and exit out. 

Next set an environment variable: `export DERBYSMS_CONFIG="/path/to/your/config.file"` This file is used to override the default config that is set up for development. My current production file looks very similar to this:

```
DEBUG = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mysqlusername:SuperSecretPassword@localhost/mysqldatabasename'
```

Since DerbySMS uses [SQLAlchemy](http://www.sqlalchemy.org/) as an ORM, you can easily substitue in a URI for PostgreSQL or SQLite, or any other database that [SQLAlchemy](http://www.sqlalchemy.org/) supports.

With the config file set up, and the DERBYSMS_CONFIG environment variable set up, you can run `python manage.py db update` to create the database. Please note that if you are using SQLite you will get a wanring about not being able to drop a column from a table. SQLite doesn't support that, so a warning is thrown. It is harmless.

Once that is created, you'll need to connect to the database and make a couple of manual insertions. 

```
// Set up the Twilio config information
INSERT INTO twilio_config (account_sid, auth_token) VALUES ('your twilio account_sid', 'your twilio auth token'); //Both of these values can be obtained from your Twilio account page.

// Set up the first person
INSERT INTO person (firstname, lastname, mobile) VALUES ('your first name', 'your last name', 'your mobile number'); // your mobile number must be in the format +1AAAXXXNNNN where A is your area code, X is your exchange, and N is your number. +18005551212

// Set up the first admin
INSERT INTO admin(mobile) VALUES ('your mobile number'); // your mobile number needs to match exactly what is in your 'Person' record.
```

With that out of the way, go ahead an uncomment the lines that you commented in `manage.py`.

If you want to test, you can now start the server with `python manage.py runserver`, but be sure to run it in a shell that has access to the environment variable that you set up previously.

If you are satisfied with how it is running, then create `/etc/supervisor/conf.d/derbysms.conf` with contents along these lines:

```
[program:derbysms]
command = python manage.py runserver
directory = /path/to/where/ever/you/cloned/derbysms
user = REPLACE WITH AN UNPRIVILEGED USER
autostart = true
autorestart = true
stdout_logfile = /var/log/supervisor/derbysms.log
stderr_logfile = /var/log/supervisor/derbysms.log
environment = DERBYSMS_CONFIG="/path/to/your/config.file"
```

Be sure to update the `directory`, `user`, and `environment` lines with the values that are correct for you. After you issue these commands

```
sudo supervisorctl reread
sudo supervisorctl update
```
your DerbySMS should be up and running.