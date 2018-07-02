import wikipedia
import sys
print (sys.argv)
test = input("Enter Search Term: ")
print (wikipedia.summary(test))
