# Campuswire Data Scraper

This script downloads group info, posts, and comments from Campuswire.


## Usage

1. Install the requirements
```bash
pip install -r requirements.txt
```
1. Get headers from browser

   1. Login to campuswire and open dev tools (F12)
   2. Go to the class that you want to get data from and click on any post in that class
   3. In the Network tab, enable filter to show only Fetch/XHR requests. This is not necessary but useful
   4. If you now refresh the page, you should see a bunch of requests that campuswire makes to get data
   5. Find the request having the url: `https://campuswire.com/courses/<group_id>/posts` or having name `posts?number=<n>`
   6. Go to context menu for that request and click on `Copy > Copy as cURL(bash)`
   7. Paste the clipboard content into `curl.txt`

2. Run the script
```bash
py main.py
```

## Notes

* On Windows, run the script in administrator Command Prompt or PowerShell if you get permission error
* On Linux, provide permission to read, write and execute
* Script is tested on python version 3.11

