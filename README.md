A cross-platform python based utility for export SurveyPlanet.com survey results.
___

### Requirements

* **_A premium Scribd account_**
* Python 3.6
* Python module argparse
* Python module selenium

### Installation:

* clone with ```git clone https://github.com/mrtztg/surveyplanet_result_export.git``` or download the release file
  and extract it.
* install requirements with ```pip install -r requirements.txt```

### Usage:

* Make a text file (e.g:my_links_file.txt) in script folder (alongside scribd_dl.py) and put books
  url in it (one url per line). example:
  ```
  https://www.scribd.com/audiobook/265831522/Elon-Musk-Tesla-Spacex-and-the-Quest-for-a-Fantastic-Future
  https://www.scribd.com/audiobook/366626161/Influence-The-Psychology-of-Persuasion
  https://www.scribd.com/audiobook/237848637/The-Alchemist
  ```
* Download book with script. Sample:
    ```shell
    python surveyplanet.py -u "my_email" -p "my_password" -q "https://app.surveyplanet.com/participants/61050e9876f392908f6c53a8"
    ```

### Advanced usage:

```
usage: surveyplanet.py [-h] [-u USERNAME] [-p PASSWORD] [-q QUESTION_PARTICIPANTS_URL] [--display] [-v]

Export survey results from SurveyPlanet.com.

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Account email/username
  -p PASSWORD, --password PASSWORD
                        Account password
  -q QUESTION_PARTICIPANTS_URL, --question_participants_url QUESTION_PARTICIPANTS_URL
                        participants url. ex: https://app.surveyplanet.com/participants/61a50e9876f392908f6c10a8
  --display             Display the browser to user
  -v, --verbose         Increase output verbosity

```

#### Disclaimer

Exporting results from SurveyPlanet for free maybe prohibited. This tool is meant for educational
purposes only. Please support the authors by buying their titles.