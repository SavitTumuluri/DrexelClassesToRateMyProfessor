class Professor:
    def __init__(self, id, profName, overallRating, difficulty):
        self.id = id
        self.profname = profName
        self.overallRating = overallRating
        self.difficulty = difficulty

    def SetProfName(self, name):
        self.profname = name

    def SetOverallRating(self, rating):
        self.overallRating = rating

    def SetDifficulty(self, diff):
        self.difficulty = diff