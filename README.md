# Yu Quan's E-commerce Price Tracking Webapp
 This is my Price tracker app to track prices on the 3 popular e-commerce sites in Singapore - Amazon, Lazada and Shopee.
 This project is a work in progress and I am continuously trying to improve it.

### Features:
- Look up prices of products
- Search keywords of the product and select the one that you want to track.
- "Refresh" Page to update the prices
  - ![Refresh](https://github.com/limyuquan/pricetracker/blob/main/ezgif.com-gif-maker.gif)  

- Track prices of products on a graph (Work in Progress)
##### Side Features:
- A proxy tester that tests a list of proxies to find valid ones.
### Technologies used:
- Frontend: HTML, CSS, bootstrap
- Backend: Python and Flask
- SQLite database
- Web Scrapping Tools: Beautifulsoup4 and Selenium / HTML requests

### Installation and Running:
##### To run it both locally and on a dedicated server:
- Insert a list of proxies that you can use into the CSV files.
    - If these proxies are free and unreliable, please run my proxy_tester programme
    - To run:
        ```sh
            cd project
            python proxy_tester.py w
        ```
    - If you already have a list of trusted_proxies and you want to add to the list:
        ```
            python proxy_tester.py a
        ```
- Download Chrome Webdriver and copy paste the executable path into scraper.py inside the shopee_scraper function, in the line of code 
    ```
       browser = webdriver.Chrome(executable_path = r")
    ```
- Update the path of your google chrome file in the same function:
   ```
         chrome_options.add_argument("")
    ```
##### To run it on a server:
- You can follow this [video tutorial](https://www.youtube.com/watch?v=NQP89ish9t8) by freeCodeCamp to learn how to run a server online.

### Requirements:
All libraries required can be located in the [requirements ](https://github.com/limyuquan/yuquanfinance/blob/main/requirements.txt) text file.
Webapp backend is also written in Python 3 and is using the Flask Framework.

### Contributing
##### Bug Reports & Feature Requests

Please use the [issue tracker](https://github.com/limyuquan/pricetracker/issues) to report any bugs or file feature requests.

### Limitations of the Project:
- Due to Beautifulsoup, some e-commerce websites (Lazada, Shopee) may flag the programme and not allow the scrapping functions to work properly.
  - To overcome it as much as possible, we use and test a rotating list of free proxies, but as they are free, most of them also do not work.
- Dynamic Websites like Shopee require use of Selenium to scrape and as a result, a local web browser has to be opened to allow it to function.
- Since I am not hosting and testing on a sever, prices can only be updated on manual click, instead of being on a timer, which increases run times and wait.

If you have any ideas on how these limitations can be solved, please feel free to contact me or use the [issue tracker](https://github.com/limyuquan/pricetracker/issues) to reccommend me some solutions. Thank you so much in advance!

### Possible Improvements to the project:
##### If given ample time, these are the possible improvements I would implement:
- Improve search times and runtimes
##### Bugs and problems reported:
- Website will return errors when list of usable proxies run out. 
    - Problem can be fixed with reliable paid proxies.
    
##### Work In Progress:
- Front End
- Homepage
- Price Tracker History


### What have I learned from the project (So Far):
##### Technical
- Usage of beautifulsoup and selenium for basic webscrapping
- How to overcome the problem of proxies being blocked by websites
- Usage of web frameworks (Flask)

##### Personal
- It takes a really long time to complete a project from the group-up, however throughout the journey I have been enjoying myself, and the process has been very rewarding and I am motivated to continue working on the project as there are still many incomplete features and bugs.
- Things that seem impossible will become possible with enough time and effort (and staring into the code/ problem).



##### Repository History
28 Nov 2022 - Repo created

##### Project Status - Work In Progress

![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)
