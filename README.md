# Shakeal-H.github.io

This project is not yet formed but I intend it do be a can hold some of my projects from class.

Let's Go Pokedex
* Cheikhouna Gueye
* Shakeal Hodge
* Luke Mager

2/18/2022 Revisions:
We performed the following changes:

- Aligned text to the left and centered and left aligned other elements
- Increased text size
- updated color scheme from black text to white to improve contrasting issues
- changed header and button background colour from grey to light blue
- Added information about attributes to help beginner users


## 3/7/2022 Revisions:
We performed the following changes:

- Our helper functions now return parts of a parametrized query
- We instantiated another instance variable to keep track of these parameters
- As pointed out in the grade for our last assignment, there are a lot of methods, but this is as simple as we can make our API considering the amount of freedom we give to the users
- We changed some variable names and method signatures to standardize everything in snake case and to clarify some variables

## Revisions for Flask Integration Team Deliverable
- We removed the function create_base_stats_radar_plot() and instead generated the plots on our own computer and uploaded them
- We added a feature to search for partial names
- We changed our CSS to be more cascading
- We couldn't make this site work without GET and POST methods so we kept them both in

## Final Commit Message:
Ignore the final commit message that has "git add" in it. I input "git commit -m finished!!!!" and the exclamation marks got changed to say git add.

## Addtional Updates

General Pokemon Information Page 

Start postges server
sudo service postgresql start

Clear any running python webapps with:
kill -9 $(ps -A | grep python | awk '{print $1}')
    
Run this to launch the website
python3 webapp.py localhost 5000
