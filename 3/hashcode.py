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
slideshowsList = chunks(slides, 500)
for ind, _slides in enumerate(slideshowsList):
    print(ind)
    newList = LList()
    newList.head = Node(_slides[0], Node(_slides[1]))

    # print(newList)

    current = newList.head
    _next = current.next
    _previous = None
    sum_of_slideshow = current.value.similarity(_next.value)

    for slide in _slides[2:]:
        current = newList.head
        _next = current.next
        _previous = None
        new_sum = sum_of_slideshow + slide.similarity(current.value)
        max_sum = new_sum
        new_position = current
        new_position_previous = _previous

        while _next != None:
            _previous = current
            current = _next
            new_sum = sum_of_slideshow + _previous.value.similarity(slide) + \
                current.value.similarity(slide)
            if new_sum > max_sum:
                max_sum = new_sum
                new_position = current
                new_position_previous = _previous
            _next = current.next
        new_sum = sum_of_slideshow + slide.similarity(current.value)
        if new_position_previous is None:
            newList.head = Node(slide, newList.head)
        elif new_sum > max_sum:
            current.next = Node(slide)
        else:
            new_position_previous.next = Node(slide, new_position)
    sum_of_slideshow = max(new_sum, max_sum)

    slideshowsList[ind] = []
    current = newList.head
    while current != None:
        slideshowsList[ind].append(current.value)
        current = current.next

    # slideshow = _slides[:2]
    # sum_of_slideshow = slideshow[0].similarity(slideshow[1])
    # for slide in _slides[2:]:
    #     new_sum = sum_of_slideshow + slide.similarity(slideshow[0])
    #     max_sum = new_sum
    #     new_position = 0
    #     for i in range(1, len(slideshow)):
    #         new_sum = sum_of_slideshow + \
    #             slideshow[i-1].similarity(slide) + \
    #             slide.similarity(slideshow[i])
    #         if new_sum > max_sum:
    #             max_sum = new_sum
    #             new_position = i
    #     new_sum = sum_of_slideshow + slide.similarity(slideshow[-1])
    #     if new_sum > max_sum:
    #         slideshow.append(slide)
    #     else:
    #         slideshow.insert(new_position, slide)
    #     sum_of_slideshow = max_sum
    # slideshowsList[ind] = slideshow

slideshow = []
for i in slideshowsList:
    slideshow += i

# for i in range(20):
#     print(i)
#     for j in range(2, len(slideshow)-1):
#         sum1 = slideshow[j-1].similarity(slideshow[j-2]) + \
#             slideshow[j].similarity(slideshow[j-1]) + \
#             slideshow[j].similarity(slideshow[j+1])
#         sum2 = slideshow[j].similarity(slideshow[j-2]) + \
#             slideshow[j].similarity(slideshow[j-1]) + \
#             slideshow[j-1].similarity(slideshow[j+1])
#         if sum2 > sum1:
#             slideshow[j], slideshow[j-1] = slideshow[j-1], slideshow[j]

new_file = open("results.txt", 'w+')
new_file.write(str(len(slideshow)) + '\n')
for i in slideshow:
    if i.type == 'single':
        new_file.write(str(i.photo1.id) + '\n')
    else:
        new_file.write(str(i.photo1.id) + " " + str(i.photo2.id) + '\n')
