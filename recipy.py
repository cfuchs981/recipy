from __future__ import print_function
import httplib2
import os

import sys
from bs4 import BeautifulSoup, SoupStrainer
import urllib2
import re
import random
import time 

def main():
  
    #connect to allrecipes.com and parse 15 min recipes, store them in a list 
    http = httplib2.Http()
    status, response = http.request('http://allrecipes.com/recipes/454/everyday-cooking/more-meal-ideas/15-minute-meals/')
    recipeList = []
    for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            if '/recipe' in link['href']:
                recipeList.append(link['href'])

    #user enters ingredient, we'll just trust in their ability without checking for valid syntax
    print("Type an ingredient:")
    ingredientChoice = raw_input()

    if recipeList == None : 
        print("Original parse failed. Run program again.")
        return

    #begin the recipe search 
    loop = 1
    while loop != 0 :

        #find a random recipe and ensure the http:// doesn't double up 
        recipeChoice = random.choice(recipeList)
        if recipeChoice.startswith('http://'):
            recipeChoice = recipeChoice[4:]
        recipeChoice = 'http://allrecipes.com' + recipeChoice

        #but if we search 20 recipes, it's best to quit while you're ahead. increment BEFORE search in case we find a recipe and break the while 
        loop += 1 
        if loop == 21 : 
            print("It'd be quicker just to google it. Returning last found recipe.")
            break

        #search random choice for ingredient list, then search for chosen ingredient 
        status, response = http.request(recipeChoice)
        for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('span', {'class': 'recipe-ingred_txt added'})):
            recipeData = link.text
            recipeData.encode('ascii', 'ignore')

            #if the ingredient is somewhere in the text, break out, else continue to search random recipes 
            if ingredientChoice.encode('ascii', 'ignore') in recipeData: 
                loop = 0
                break

        #wait between each parse one second, httpd will get mad if you spam too fast 
        time.sleep(1); 

    print("Your recipe is " + recipeChoice + "\n")


if __name__ == '__main__':
    main()