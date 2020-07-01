# Pair Programming

## Features to Pair Program:

   Querying the data (part 3) and returning/displaying the data (part 4).
    
## Explanation of process:
 
Our initial process was to have 2 sessions to pair program part 3 and part 4. We had to stop in the session for part 4 since it ran much longer than we anticipated due to coding errors. We then decided to split off the error fix we were facing and testing into a third session to regroup. We split up the checkpoints into small enough tasks so that we could switch the role of driver and navigator roughly every two checkpoints (more or less depending on how long it actually took us to implement).

### Process Steps and Checkpoints
#### 1. Querying (25/6/2020)

-   (Driver: Emily, Navigator: Da Eun) 
	- Checkpoint 1: Check which query to do (countries, states, combined keys) and return documents that match the query.
	-   Checkpoint 2: Check that document was retrieved correctly by getting just the start date

-   (Driver: Da Eun, Navigator: Emily)
	-   Checkpoint 3: Iterate through the returned documents above to get the specific dates
	-   Checkpoint 4: Put dates we want and key(s) that were queried into some data structure that will be used for part 4
    
### 2. Displaying  (26/6/2020)
-   (Driver: Da Eun, Navigator: Emily)
	-   Checkpoint 1: Change html file to have “choose export file format option”
-   (Driver: Emily, Navigator: Da Eun)
	-   Checkpoint 2: Get the data structure from querying (part 3) and display it as JSON or a line plot depending on user input
-   (Driver: Da Eun, Navigator: Emily)
	-   Checkpoint 3: Get the data structure from querying (part 3) and display it as csv and text
	-   Fix bug that returns number of cases incorrectly for queries involving states/provinces with multiple combined keys

### 3. Testing/Error Fix (27/6/2020)
-   (Driver: Emily, Navigator: Da Eun) 
	-   Checkpoint 1: Fix the way matplotlib displays the data when multiple locations are queried
-   Driver: Da Eun, Navigator: Emily
	-   Check point 2: Implement unit tests for home, upload and search
	-   Check point 3: Implement unit tests for uploader
	-   Check point 4: Implement unit tests for query
	    

  

##  Reflection:

During our pair programming sessions the major positives that we saw were an increased understanding of different solutions of our mini tasks and a reinforcement of what we were learning. Having the ability to have a conversation with your partner about possible implementations helped you understand not only the solutions available but the problem as w
ell. Planning checkpoints, discussing solutions and constantly explaining the code reinforced our understanding of what we were doing and also helped us come up with a greater variety of solutions and points of view than had we done the tasks alone. We also noticed that since we were planning out tests before we implemented solutions, we were more test driven when coding part 3 and 4. Additionally, having immediate feedback helped us with catching overly complicated code, syntax errors and debugging any errors we were having much quicker than normal. The negatives of pair programming mostly revolved around errors, time constraints and schedule flexibility. Pair programming required the tasks to be done at specific times, which was not hard for this session, but it did restrict when we could implement part 3 and part 4. During the sessions we noticed that if one partner had technical difficulties, then it was hard for the task to continue which led to longer than expected sessions. This was also observed when we ran into errors or bugs that we couldn't immediately fix. The longer sessions resulted in splitting the remaining tasks into a third session. We did some research on the advantages and disadvantages of pair programming, and we agreed with most of the advantages (multiple perspectives, quickly spotting and fixing bugs, better productivity and concentration, etc.) We did, however, disagree with some of the disadvantes we saw online. For example, some people noted a decrease in productivity, but we felt we were very productive and accomplished a lot in a short time span while pair programming. Also, we read that some people experience conflicts with their partner and disagreement over how the code should be written, but we worked together well and considered each other's suggestions without conflict. This was a new experience for both of us and there was a bit of a learning curve when we first started, but as we got more comfortable we saw our productivity increase. We see a big benefit in having a few pair programming sessions when working on a project as part of a team, and we will definitely consider implementing pair programming into future projects. 

#### Pros:
-   Able to explore solutions together and choose how to implement a solution quicker than messaging back and forth.

-   Planning out the check points helped us get a clearer idea of what we wanted and how we were going to do it. Having that before implementation helped with cleaner code and think of what we would want as tests while we were coding.
    
-   Able to see and give immediate feedback on what the driver is doing such as catching syntax errors or giving solutions to errors and bugs.
    
-   Debug and catch bugs much quicker than when working alone and benefit from each other’s knowledge.
    
-   Ability to explain the code you’re writing to partner as you’re writing it. This allowed us to fill in knowledge gaps, have a back and forth on possible solutions as well as reinforce material while explaining to your partner.
    
-   Having to explain your code also made you think about your process and why you implemented a solution in such a way.
    
#### Cons:
    
-   Doing the same task meant that if you ran into a problem it would be a blocker for both persons, which prolonged the pair programming sessions.
    
-   If one person runs into technical difficulties (which happened to us when one of our python interpreters stopped working) the other person is paused or slowed down from continuing the task.
    
-   If the session runs longer than expected you need to plan another session. Unlike working alone you can’t freely choose when to code.
    

# Design Patterns

### Pattern 1:  Builder Design Pattern
We used a builder design pattern for the file exporting process. The builder design pattern is a useful pattern that takes in a common input to create a variety of outputs. For file querying, we find and parse a collection of data using the same key(s) but required a different output package. Since the initial data was the same between all file types, we chose a builder to create different types of output files using the same data to export the files.

[Builder Pattern Diagram](https://imgur.com/9i9bkWb)
### Pattern 2 : Strategy Design Pattern
We used a strategy design pattern for the file importing process. The strategy design pattern is useful when different algorithms or behaviour is required depending on the context that is given to the program. For our file importing process, our context was the type of file, (daily or time series) and we needed to parse the file differently depending on said context. While the input is the same (the file) the algorithm for parsing the data to the database differs based on the file type. We also required the end result to be the same, which is to update the database using the data. Since we were parsing a common data source using different algorithms to achieve the same end result (update the database) we used the strategy design pattern.

[Strategy Pattern Diagram](https://i.imgur.com/K9mX5jO.png)
  

### Code Craftsmanship

-   Tools: Linters (flake8), IDEs (PyCharm, Visual Studio with Python add on)
    

  

# Instructions:

### Instructions for Initial Setup:

1.  Install the packages/modules/frameworks: pymongo, matplotlib, and pandas.
    
2.  Install MongoDB according to your OS: [https://docs.mongodb.com/manual/administration/install-community/](https://docs.mongodb.com/manual/administration/install-community/)
    

### Instructions for Use:
#### Before running `main.py`:
1.  Connect to MongoDB by running `mongo` in terminal.
    
2.  Use the command `use a2test` in the mongodb shell to create the database a2test. 
    
3. Run main.test and open the locally served program in chrome.

#### Begin by uploading a Time Series or Daily file:

1.  Click Upload from home page.
    
2.  Click Choose File and upload the desired file (must be .csv extension).
    
3.  Select Time Series or Daily format type.
    
4.  Select the information type (confirmed, deaths, recovered, active, choose All if the format type is Daily) of data in the file. Only one type can be chosen.
5.  Click Upload File.

Next, you can continue uploading more files (Time Series or Daily Report), or query data from the uploaded file(s).

#### To query data:

1.  Click Search from home page.
    
2.  Select the information type of data to query (confirmed, deaths, recovered, active). Only one type can be chosen.
    
3.  Input the Countries/Regions, States/Provinces, or Combined Keys to query. Only one type can be chosen. For multiple inputs separate the inputs using '/'. For example, for querying Canada and Mexico, input `Canada/Mexico`.
    
4.  Input the dates for your desired date range.
    
5.  Select the format for the data to be returned. Text type will return an html file.

6. Click Submit and save file.

### Testing Instructions
1.  The mongodb database and a2test must be running for the tests to run correctly. To set up the database see the beginning of Instructions section above. 
2. Run tests.
