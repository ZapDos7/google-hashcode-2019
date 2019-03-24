import sys
from photo import *

inputfile = sys.argv[1]

file = open(inputfile, 'r')

numberOfPhotos = int(file.readline())
photos = []
vertical_photos = []
horizontal_photos = []
tags = {}
slides = []

for i in range(numberOfPhotos):
    newLine = file.readline().split()
    photo = Photo(i, newLine[0], newLine[2:])
    photos.append(photo)

    if photo.orientation == "V":
        vertical_photos.append(photo)
    else:
        horizontal_photos.append(photo)

    # Add tags to dictionary, with the values being the photo ids
    for tag in newLine[2:]:
        if tag not in tags:
            tags[tag] = [i]
        else:
            tags[tag].append(i)


# Set up vertical slides:
vertical_photos = sorted(vertical_photos, key=lambda x: len(x.tags))
for i in range(int(len(vertical_photos)/2)):
    newSlide = Slide(vertical_photos[i], vertical_photos[-(i+1)])
    slides.append(newSlide)

# Add horizontal slides:
for i in horizontal_photos:
    newSlide = Slide(i)
    slides.append(newSlide)

# Start making the slideshow
# slideshow = slides[:2]
# sum_of_slideshow = slideshow[0].similarity(slideshow[1])
# for slide in slides[2:]:
#     new_sum = sum_of_slideshow + slide.similarity(slideshow[0])
#     max_sum = new_sum
#     new_position = 0 
#     for i in range(1, len(slideshow)):
#         new_sum = sum_of_slideshow + slideshow[i-1].similarity(slide) + slide.similarity(slideshow[i])
#         if(new_sum > max_sum):
#             max_sum = new_sum
#             new_position = i 
#     new_sum = sum_of_slideshow + slide.similarity(slideshow[-1])
#     if(new_sum > max_sum):
#         slideshow.append(slide)
#     else:
#         slideshow.insert(new_position, slide)    
#     sum_of_slideshow = max_sum

def mergesort(slides):
    if len(slides) > 1:
        mid = len(slides) // 2
        left = slides[:mid]
        right = slides[mid:]

        mergesort(left)
        mergesort(right)

        a = b = c = 0
        while a < len(left) - 1 and b < len(right):
            if left[a].similarity(right[b]) > left[a].similarity(left[a+1]):
                slides[c] = left[a]
                a += 1
            else:
                slides[c] = right[b]
                b += 1
            c += 1

        while a < len(left):
            slides[c] = left[a]
            a += 1
            c += 1
        while b < len(right):
            slides[c] = right[b]
            b += 1
            c += 1

new_file = open("results.txt", 'w+')
new_file.write(str(len(slides)) + '\n')
for i in slides:
    if i.type == 'single':
        new_file.write(str(i.photo1.id) + '\n')
    else:
        new_file.write(str(i.photo1.id) + " " + str(i.photo2.id) + '\n')