# Description
Simple project to try to pinpoint the position of Jason Bourne based on report records(border, duty free, police etc.)
# Usage
1. setup venv (ex. `python -m venv venv`)
2. install requirements (`pip install -r requirements.txt`)
3. run `python main.py testInp/border_01.csv testInp/duty_free_02.csv testInp/police_03.json`
4. sample output:
    ```
   2022-04-25T00:00:00 Jason Bourne border_01.csv
   2022-04-25T00:00:00 James Bond border_01.csv 
   2022-04-25T00:00:00 Ne Jason Bourne2 border_01.csv 
   2022-04-25T00:00:00 Ne Jason Bourne border_01.csv
   2022-04-25T00:00:00 Foma Kinaev duty_free_02.csv
   2022-04-25T00:00:00 James Bond duty_free_02.csv 
   2022-04-25T00:00:00 Jason Bourne police_03.json 
   2022-04-25T00:00:00 Ne Jason Bourne4 police_03.json
   ```
5. Sample input files included in `testInp` directory
   
# Note
Required python3.8 and higher due to `walrus` operator