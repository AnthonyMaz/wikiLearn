import argparse
from slideshow import render_slideshow

from wikipedia import wikipedia


global sprite


parser = argparse.ArgumentParser()
parser.add_argument('--slideshow', help='Render a slideshow of the images found on that subject',
                    action='store_true')


parser.add_argument('wikipage', help='Wiki page title',
                    nargs='?', default="Iron Man")

args = parser.parse_args()

if args.slideshow:
    render_slideshow(args.wikipage)
else:
    print(wikipedia.summary(args.wikipage))
