class Photo:
    def __init__(self, id, orientation, tags):
        self.id, self.orientation, self.tags = id, orientation, set(tags)

    def __repr__(self):
        a = str(self.id) + " " + self.orientation + " " + "tags: "
        a += str([i + ' ' for i in self.tags])
        return a

class Slide:
    def __init__(self, photo1, photo2=None):
        if photo2 is None:
            self.type = 'single'
        else:
            self.type = 'double'
        self.photo1 = photo1
        self.photo2 = photo2

        if self.type == 'single':
            self.tags = photo1.tags
        else:
            self.tags = photo1.tags.union(photo2.tags)

    def __repr__(self):
        a = " Photo a:" + self.photo1.__repr__() + " Photo b: "
        if self.photo2 is not None:
            a += self.photo2.__repr__();
        return a
        

    def similarity(self, slide_b):
        common_tags = len(self.tags.intersection(slide_b.tags))
        tags_in_a_not_in_b = len(self.tags.difference(slide_b.tags))
        tags_in_b_not_in_a = len(slide_b.tags.difference(self.tags))
        # print(self.__repr__(), slide_b.__repr__(), common_tags, tags_in_a_not_in_b, 
        # tags_in_b_not_in_a, min(common_tags, tags_in_a_not_in_b, tags_in_b_not_in_a))
        return min(common_tags, tags_in_a_not_in_b, tags_in_b_not_in_a)