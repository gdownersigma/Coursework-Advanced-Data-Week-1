The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

Solution

# make a dict for the grid - make the key a tuple of (x,y) location
# build each rectangle and fill in all of the positions (x,y) co-ord with 1
# if a position already has 1 then set it to 2
# return the amount of values in the dict greater than 1.  