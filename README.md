# Scholarships scraper

This project helps you get through giant lists of scholarships. In particular, this project handles the following for you:
* Downloading the HTML source of multiple webpages.
* Handling all the files and intermediate conversions.
* Providing a framework to handle the different types of webpages.

However, since each provider/website use their own DOM layout, it is not feasible to provide a standardised interface for all of them. So it is up to you to write code to actually parse the website (and, yes, this is kind of complex).


## Expected website structure and pre-requisites:
* There are several pages of **lists** on the website. These are numbered and the number can be written inside a URL.
*   Each **scholarship** in the list can provide you a name and a link.
*   Following the link will take you to a **page** with more details about that specific scholarship.
*   All this data must be directly embedded in the HTML (and not downloaded through JavaScript, for instance). This does appear to be the common case, thankfully.
*   You'll need to know how to use the [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/doc/) Python module (in addition to knowing Python scripting, of course).
*   A recent Python 3, and all Python dependencies (listed in [requirements file](./requirements.txt)), must be installed. You can use the `pip` tool to install the dependencies using the following command:

    ```shell
    python -m pip install -r requirements.txt
    ```

## How this program works
1. Use [`aiohttp`](https://docs.aiohttp.org/) to download the content of each page of lists.
1. Pull out all the names and links from each page, and store all of it to one JSON file.
1. Read the JSON file and use `aiohttp` again to download the page for each scholarship.
1. Extract the details and store these to another JSON file.
1. Convert the second JSON to CSV, which can then be imported to a spreadsheet software (or wherever).

## Understanding the file structure
| File | Description/purpose | Would you need to edit this? |
| -- | -- | -- |
| `pull.py` | Handle any communication with the internet. | No |
| `fileio.py` | Handle the storage and retrieval of files. (mostly). | No
| `csvify.py` | Handle the JSON to CSV conversion. | No |
| `main.py` | Organise everything and help you run the program. | Yes |
| `data/` | Holds subfolders, each for one specific website. | Yes |
| `data/templates/` | Template for dealing with one website. Duplicate this and rename it to begin (`website_name` is used here as an example). | No |
| `data/website_name/` | Hold all parsers and data about one particular website. | Yes |
| `data/website_name/parsers.py` | Define the parsers and other data for one particular website. | Yes |
| `data/website_name/links.json` | Hold all the links and names pulled from one website. | No |
| `data/website_name/scholarships.json` | Hold all the data about each scholarship pulled form one website. | No |
| `data/website_name/scholarships.csv` | Hold all the data about each scholarship pulled form one website. **Final product.** | No |
| `data/website_name/test_page.html` | Source code for any one scholarship for you to experiment on. | No |
| `data/website_name/test_page_list.html` | Source code for any one page of the lists scholarship for you to experiment on. | No |

## Usage

### Directories and information
1.  Find a website with lists of scholarships. Get the URL of one page of lists, such as:

    ```text
    https://websitename.com/scholarships/page4.html
    ```

    You'll also want to take note of the number/ID of the first and last page.

1.  Go to the page for any one scholarship and take note of its URL as well. For example:

    ```text
    https://websitename.com/scholarship/really-cool-scholarship.html
    ```
1.  Duplicate the `data/template` directory, and rename it (to `data/websitename`, for example).

### Scholarship-specific information
1.  Open `data/websitename/parsers.py` and find the `PARAMETERS` identifier.
   
    ```python
    PARAMETERS = {
        'base_url': None,  # provide a link to a page of lists, and replace the number of the page with an asterisk
        'start': 0,  # the first page of lists
        'end': 0,  # the last page of lists
        'provider_name': None,  # name of the provider
        'page_link': None  # provide a link to a specific scholarship page
    }
    ```
    
    *   Set `'base_url'` to the URL of the page of lists, but replace the number/ID with an asterisk.
    *   Set `'start'` to the number/ID of the first page of lists.
    *   Set `'end'` to the number/ID of the last page of lists.
    *   Set `'provider_name'` to the name of the website (this be the same as the name of the folder `websitename`).
    *   Set `'page_link'` to the URL for the page of a specific scholarship.

    You should be left with something like this:

    ```python
    PARAMETERS = {
        'base_url': "https://websitename.com/scholarships/page*.html",  # provide a link to a page of lists, and replace the number of the page with an asterisk
        'start': 1,  # the first page of lists
        'end': 24,  # the last page of lists
        'provider_name': "websitename",  # name of the provider
        'page_link': "https://websitename.com/scholarship/really-cool-scholarship.html"  # provide a link to a specific scholarship page
    }
    ```

1.  Open `main.py` and find the section with all the imports. Find the import with the `data/template` folder:
    
    ```python
    from data.template.parsers import TEST_PAGE_FILENAME, TEST_PAGE_LIST_FILENAME, PARAMETERS, scholarship_page_parser, scholarships_list_parser
    ```

    Edit this to instead import from the folder specific to the website you are trying to scrape, like (just replace the term `template` with `websitename`):

    ```python
    from data.websitename.parsers import TEST_PAGE_FILENAME, TEST_PAGE_LIST_FILENAME, PARAMETERS, scholarship_page_parser, scholarships_list_parser
    ```

1.  Open `main.py` and find the `main()` function. Edit it so that only the following subroutines run:
    *   `setup()`
    *   `pull_scholarship_page_test()`
    *   `pull_list_page_test()`

    You should be left with something like this:

    ```python
    def main() -> None:
        setup(PARAMETERS)
        pull_scholarship_page_test()
        pull_list_page_test()
        # get_list_of_scholarships()
        # get_all_scholarship_pages()
        # convert_to_csv()
    ```

    Run the `main.py` script from the root of the project. This will download the source for two webpages (one for a list, and another for a specific scholarship). You can then use these two to develop the parsers, as in the next few steps.

    ```shell
    python main.py
    ```

1.  Open `data/websitename/parsers.py`. Your first task is to write code to extract a list of all the scholarships on that page.

    To begin, find the `find_scholarships()` function:

    ```python
    def find_scholarships(soup: Soup) -> list:
        return soup.find_all('div', {'class', 'post clearfix'})
    ```

    The `soup` object is an instance of the `BeautifulSoup` class, which means that you can just begin to write the parser.

    Your goal is to return a `list` of all the scholarships given on that page. Each element of that list must be another `BeautifulSoup` object (such as a `<div>` or a row in a table) from which the name and link of that scholarship can be extracted.

1.  Open `data/websitename/parsers.py`. Your second task is to write code to extract the name and link to a specific scholarship (an element of the list returned by `find_scholarships()`).

    To begin, find the `parse_scholarship()` function:

    ```python
    def parse_scholarship(scholarship: Soup) -> tuple:
        heading = scholarship.find('h2')
        name = None
        link = None

        if heading:
            embedded_link = heading.find('a')
            
            if embedded_link:
                name = embedded_link.text.strip()
                link = embedded_link['href']

        return name, link  # return the name and link of the scholarship
    ```

    The `scholarship` object is an instance of the `BeautifulSoup` class, which means that you can just begin to write the parser.

    Your goal is to extract the name and link to the scholarship in to the two variables `name` and `link`. An example is implemented by default and many websites will adopt an approach that is loosely compatible with this.

    In the `main()` function, there are two functions built in that can help you run your code thus far to test.

    ```python
    def main():
        test(TEST_PAGE_FILENAME, scholarship_page_parser)
        test(TEST_PAGE_LIST_FILENAME, scholarships_list_parser)
    ```

    You can set only the latter to run like this:

    ```python
    def main():
        # test(TEST_PAGE_FILENAME, scholarship_page_parser)
        test(TEST_PAGE_LIST_FILENAME, scholarships_list_parser)
    ```

    Then, run this script from the root of the project.

    ```shell
    python data/websitename/parsers.py
    ```

1.  Open `data/websitename/parsers.py`. Your third (and final for this file) task is to write code to extract the various properties of a particular scholarship from its webpage.

    To begin, find the `scholarship_page_parser()` function:
    
    ```python
    def scholarship_page_parser(html_text: str) -> dict:
        data = {}
        soup = Soup(html_text, 'html.parser')

        return data
    ```

    The `soup` object is an instance of the `BeautifulSoup` class, which means that you can just begin to write the parser.

    Your goal is to find whatever data you deem important (such as the value of the award, eligibility requirements, a link to apply et cetera). You should then store this data in the `data` dictionary.

    Here is an example of what `data` should look like after you're done ([source](https://www.internationalstudent.com/scholarships/3589/MPOWER%20Women%20in%20STEM%20Scholarship/)):

    ```json
    {
        "name": "MPOWER Women in STEM Scholarship",
        "host_countries": "Canada and United States",
        "field_of_study_list": "Biology/Life Sciences, Computer & Information Systems, Engineering, Health Professions, Mathematics, Psychology, Aviation, Nursing, Dental/Orthodontics, Chemistry, Applied Science, Game Design & Development, Computer Animation, Criminal & Forensic Science, Geology, Medicine, Nutrition, Physics and Science",
        "other_criteria": "STEM includes any degree programs related to Science, Technology, Engineering, and Mathematics.",
        "host_institution": "MPOWER Financing",
        "amount": "$5,000",
        "number_of_awards": "3",
        "deadline": "July 20"
    }
    ```

    In the `main()` function, there are two functions built in that can help you run your code thus far to test.

    ```python
    def main():
        test(TEST_PAGE_FILENAME, scholarship_page_parser)
        test(TEST_PAGE_LIST_FILENAME, scholarships_list_parser)
    ```

    You can set only the former to run like this:

    ```python
    def main():
        test(TEST_PAGE_FILENAME, scholarship_page_parser)
        # test(TEST_PAGE_LIST_FILENAME, scholarships_list_parser)
    ```

    Then, run this script from the root of the project.

    ```shell
    python data/websitename/parsers.py
    ```

### Running the program

Open `main.py` and find the `main()` function. Edit it so that only the following subroutines run:
*   `setup()`
*   `get_list_of_scholarships()`
*   `get_all_scholarship_pages()`
*   `convert_to_csv()`

You should be left with something like this:

```python
def main() -> None:
    setup(PARAMETERS)
    # pull_scholarship_page_test()
    # pull_list_page_test()
    get_list_of_scholarships()
    get_all_scholarship_pages()
    convert_to_csv()
```

**Note:** This project uses the built-in [`multiprocesssing`](https://docs.python.org/library/multiprocessing.html) module to concurrently run parsers. As a result, using Ctrl+C or Cmd+C may not abort the script, and you may have to kill the terminal.
Run the `main.py` script from the root of the project.

```shell
python main.py
```

At this point, if all goes well, you should see some status updates in your terminal, and finally you should be left with the file `data/website_name/scholarships.csv`. You can then import this into a spreadsheet editor. Here are some support links for the most common editors:

* Microsoft Excel: https://support.microsoft.com/office/import-or-export-text-txt-or-csv-files-5250ac4c-663c-47ce-937b-339e391393ba
* Apple Numbers: https://support.apple.com/guide/numbers/tan9f3c54bdc/mac
* Google Docs: https://support.google.com/docs/answer/40608
* LibreOffice Calc: https://help.libreoffice.org/6.3/en-US/text/scalc/guide/csv_files.html

However, in my experience, there usually some debugging to do the first time you run this for a given scholarship website. This is mostly due to a lack of standardization, or because some fields may exist only for some awards and not others.
