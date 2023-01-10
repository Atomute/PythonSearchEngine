from robotexclusionrulesparser import RobotExclusionRulesParser

robot = RobotExclusionRulesParser()
url = "https://www.azlyrics.com/a/aaronwatson.html"

robot.fetch("https://www.azlyrics.com/robots.txt")

allowed = robot.is_allowed("*", url)

print(allowed)
