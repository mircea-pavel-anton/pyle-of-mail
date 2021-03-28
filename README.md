![GitHub](https://img.shields.io/github/license/mikeanth-dev/pyle-of-mail?style=for-the-badge)
[![Available on docker](https://img.shields.io/badge/Available%20on-Docker%20Hub-blue?style=for-the-badge&logo=Docker)](https://hub.docker.com/repository/docker/mikeanth/pyle-of-mail)
![Docker Pulls](https://img.shields.io/docker/pulls/mikeanth/pyle-of-mail?style=for-the-badge&logo=Docker)
![GitHub top language](https://img.shields.io/github/languages/top/mikeanth-dev/pyle-of-mail?style=for-the-badge&logo=python&color=yellow&logoColor=yellow)

# pyle-of-mail

A Python script that sorts all read emails from your mailbox.

## How it works

With the information provided in the `config.py` file, this script will connect to your IMAP server of choice, and then start filtering the mailboxes you tell it to.

### How does it log in to the imap server?

In the config file, there are 3 variables of interest:

- `imap_server`: the address of the imap server.  
    For example, if you're using gmail, it will be `imap.gmail.com`.  
    Personally, my main email address is a Yahoo address, so for that, it would be `imap.mail.yahoo.com`
- `username`: the email address for the given IMAP server
- `password`: the password, or access token used to authenticate  
    For gmail, you need to enable insecure app access.  
    For Yahoo, you can generate a dedicated access token for this app.

### How does it filter my emails?

Glad you asked!  
So here's the basic logic behind. The script firstly gets a list of all UNREAD emails from the given mailbox, and then iterates through it.  
In the config file, there is a dictionary, `filters` that basically explains what should happen. The structure of the dictionary is:
`{ 'keyword': 'destination/mailbox' }`. The keyword is NOT case sensitive, and it will look for it in the sender address.  
For example, the following rules should handle all emails from amazon, regardless if they come from `contact@amazon.com` or `noreply@amazon.uk` or whatever else. As long as it has `amazon` in the address somewhere, it will get filtered.

``` python
filters = {
    'amazon'; 'Shopping/Amazon'
}
```

For each email in the list, it checks it against all filters from the config file, until it finds a match or it runs out of options.  

As such, your inbox will eventually just be a place for unread emails, that require your attention. After they have been read, they will automatically get placed into the appropriate directory.

### How often does it filter my emails?

As often as you want!  
In the config file, there is the `sleep_time` variable, along with some sample values, if you want the script to run multiple times a day, daily or even weekly.

### How does it know which mailboxes to filter?

Again, the config file holds all the secrets. There is an array, called `mailboxes`. You simply populate it with the names of all mailboxes you want filtered, and it will go ham at them, one at a time.

### What if it moved an email that it shouldn't have, or I can't find something?

Log files are here to save us!  
Every email that gets moved around, is also logged. The script logs to a file, at the path given in the `config` (`logfile=/var/log/pyle-of-mail.log` by default) and to `stdout`.  
Anything that moves or breathes, gets logged, so you should be able to find anything.

## How to deploy

You can either clone the source code and run it manually whenever you feel like it, but I think the true power of this comes when you deploy it in a Docker Container and allow it to run periodically.

You can find a sample `docker-compose.yml` file in this repo that uses the image pushed to DockerHub. If you so desire, you can also build your own docker image with the provided `Dockerfile` and run that one.

## Feedback, suggestions and help

For feedback, suggestions, bug reports etc., feel free to e-mail me at 'mike.anth99@gmail.com'.

---

_a project by Mircea-Pavel Anton (Mike Anthony)_
