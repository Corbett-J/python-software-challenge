# welcome
Hi! I hope you're well. I'll try to stick to key point here as there are already lots of code comments for guidance. I've also implement 'documentation through typing' where reasonably possible.
I had the afternoon free and I was enjoying the task a lot, so I went relatively in-depth into laying the groundwork for this project to (theoretically) be fast, efficient, and scalable. This mostly centers around avoiding heavier scraping tools (sticking exlusivly to http requests), and setting up consistant data structures. Where there are currently issues in this project due to time constraints, I belieive there are also clear paths towards improvment for all of them.

If there are any questions or issues, please feel welcome to reach out! I'll be happy to discuss things further.

## navigating the code
I would recommend staring with runner.py, and following through the logic from there for a cohesive overview.


### how to run code
form root directory:

    `python test.py`

from 'python_challenge' directory:

    `python runner.py`

## (Theoretical) futue improvements
- I took an approach with this project of laying groundwork quickly, so I'm sure there are some typos, inconsistancies in naming schemes, and other small mistakes. With more time given to the project, they could be fixed.
- For the sake of time and not overcomplicating a software-challenge, nothing here is async, meaning the code currently takes a while to complete searches. Switching the searches to be async would be fairly easy, but I believe testing and bug fixing would take more time as it would add a layer of complexity, so I considered it a stretch-goal given the timeframe.
- I had trouble keeping some of the typing DRY while also needing the same types across various levels of the code. I'd like to personally know how to handle that better, so it's something I'll look into.
- To meet the basic task requirements I started out by scraping the product pages. This is the approach I took until the end, but it seems like it could be possible to get all the data we want from www.wollplatz.de directly from http requests to save complexity, although the current solution works well enough.
- I thought in this case it made sense to leave the test until the end so that I could work more on the structure of the project before implementing tests based on that structure. But I ended up not having enough time to write more than simple tests to meet the basic requirements. If this project were to continue, I would consider a few additional testinng factors 
  - writing tests for falure states to ensure good error handling.
  - future tests could mock responses from scraper and intercept http requests, so that we can test functions that interact with external services without relying on third-party services being up.
  - Have tests be run as pre-commit tests.
- I realised as I was writing tests that I've used mostly defs, and not many classes. I thought it's worth pointing out that this was just out of habit from working with Typescript a lot recently, and that I am also perfectly happy using classes which I think can somewhat be seen in places thoughout the code (mostly the unit tests).

## time taken
basic core task, including set-up and investigation into subverting cloudflare's bot-protection, and writing tests: 2-2.5 hours
Additional features such as collecting data for all product variants, setting up infrascructure for more sites to be added, and (time-limited attempt at) accepting custom searches: 3-4 hours

## (some of my notes from the begining of the project, in case they're interesting)
When trying to recreate the call through postman, I got block by cloudflare's bot protection returning a 403 containing

```
<span class="icon-wrapper"><div class="heading-icon warning-icon"></div></span><span id="challenge-error-text">Enable JavaScript and cookies to continue</span>
```
Researching this seems to leave two options, using a non-headless browser to run the request or bypassing the cloudflare protection.
For a small project, I think having a non-headless browser run would be fine, but at scale this would cause significant slowdown compared to running a headless browser or simply making http requests. Since I want this project to scale well, I will try subverting the bot protection. It seems there's already a very popular python library for this called cloudscraper, https://pypi.python.org/pypi/cloudscraper/. There's always risk when using a tool like this that it may break in the future, but I'm not too concerned about that in this case for the following reasons:
- There seems to be a big enough comunity around this resources that if it should break, it will likely be fixed again soon after
- During the time it is broken, we can switch to using an automated non-headless browser like Selenium, which will be a lot less performant but is still a viable back-up solution given that it could relatively quickly be set up to make the same calls as we already make using cloudscraper, just in a non-headless browser environment.
cloudscraper works, I'll set up a test call in python using the exact headers and body as the call the website makes.
After some testing to see which info from the body and headers need to be excluded in order for the call to both work and not trigger the bot detection, the http call is working. In the future I would conduct more testing here to see if variables in the body change after time, and include them to further avoid bot detection. Both to keep to a resonable time limit and because in my experience it's almost never an issue to exclude these data entries for the forseeable future, I have simply commented them out in this example.
Got the calls and data collection working for one product, now to test with another and fix any issues
