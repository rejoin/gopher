#A script used to populate the sqlite database used for the COMP2541 coursework
#Author Alexandar Dimitrov <sc12avd@leeds.ac.uk>
#Version 0.1 Created on 18/02/2014
import sys
from imdb import IMDb
import sqlite3

#Connect to the database and create the cursor

conn = sqlite3.connect('imdb')
c = conn.cursor()

#Create the API handler
i = IMDb()

#Get the movie from the command line
movie_list = i.search_movie(sys.argv[1])

#We only need the first one
pro = movie_list[0]

#Get all the info about it
i.update(pro)

#Get only the parameters we need
imdbid = int(pro.movieID)
title = str(pro['title'])

#Join the list for multiple genres
genre = str(', '.join(pro['genres']))
rating= float(pro['rating'])
plot_outline = str(pro.get('plot outline'))
plot = str(', '.join(pro.get('plot')))
allcert = pro.get('certificates')
cert = str(', '.join([x for x in allcert if x.startswith('UK')]))
duration = str(', '.join(pro.get('runtimes')))
country = str(', '.join(pro.get('countries')))
year = int(pro.get('year'))
image = str(pro.get('full-size cover url'))


#Create a neat list which is to be inserted into the database
table = (imdbid, title, genre, rating, plot, plot_outline, cert, duration, country, year, image)

#for item in table:
#	print type(item) 
#	print item

#Populate the data into the table
#Keep in mind that the table was created using the following SQL statement
#create TABLE movies (id INTEGER PRIMARY KEY, title TEXT, genre TEXT, rating FLOAT, plot TEXT, cert TEXT, duration TEXT, country TEXT, year INTEGER, image TEXT);
c.execute("INSERT INTO universal_gopher_movie VALUES (?,?,?,?,?,?,?,?,?,?,?)", table)

#Disconnect from the database.
conn.commit()
conn.close()

