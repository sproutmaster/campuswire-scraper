# Campuswire Data Scraper

This script downloads group info, posts, and comments from Campuswire.


## Usage

1. Install dependencies
```bash
pip install -r requirements.txt
```
2. Get headers from the browser

   1. Login to Campuswire and open browser dev tools (F12)
   2. Go to the class that you want to get data from and click on any post in that class
   3. In the Network tab, enable the filter to show only Fetch/XHR requests
   4. If you now refresh the page, you should see a bunch of requests to Campuswire API
   5. Find the request having the URL: `https://campuswire.com/courses/<group_id>/posts` or `posts?number=<n>`
   6. Go to the context menu (right-click) for that request and click on `Copy -> Copy as cURL(bash)`
   7. Paste the clipboard content into `curl.txt`

3. Run the script
```bash
py main.py
```

## Notes

* On Windows, run the script in administrator Command Prompt or PowerShell if you get a permission error
* On Linux, provide permission to read, write and execute
* Script is tested on Python version 3.11
* cURL text was pasted from Microsoft Edge

