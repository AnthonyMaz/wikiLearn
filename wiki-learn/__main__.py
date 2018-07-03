import argparse
from wikipedia import wikipedia

parser = argparse.ArgumentParser()
parser.add_argument('--slideshow', help='Render a slideshow of the images found on that subject',
                    action='store_true')
parser.add_argument('wikipage', help='Wiki page title',
                    nargs='?', default="Iron Man")
args = parser.parse_args()

if args.slideshow:
    from slideshow import render_slideshow
    render_slideshow(args.wikipage)
else:
    print(wikipedia.summary(args.wikipage))
