import requests
from bs4 import BeautifulSoup
import math

session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}

class Country:

    def __init__(self, _id=None, _url=None):

        self.id = _id
        self.url = _url

        pass

    @staticmethod
    def GetAllCountries():

        countries = []

        countriesJson = session.get("https://images.parkrun.com/events.json").json()["countries"]

        for countryKey in countriesJson:

            country = Country(
                _id=countryKey, 
                _url="https://" + countriesJson[countryKey]["url"]
                )

            countries.append(country)

        return countries

class Event:

    def __init__(self, _id=None, _name=None, _longName=None, _shortName=None, _countryCode=None, _seriesId=None, _location=None, _url=None):

        self.id = _id
        self.name = _name
        self.longName = _longName
        self.shortName = _shortName
        self.countryCode = _countryCode
        self.seriesId = _seriesId
        self.location = _location
        self.url = _url
        
        pass

    @staticmethod
    def GetAllEvents():

        events = []

        eventsJson = session.get("https://images.parkrun.com/events.json").json()["events"]["features"]

        for event in eventsJson:

            event = Event(
                _id=event["id"], 
                _name=event["properties"]["eventname"], 
                _longName=event["properties"]["EventLongName"], 
                _shortName=event["properties"]["EventShortName"], 
                _countryCode=event["properties"]["countrycode"], 
                _seriesId=event["properties"]["seriesid"], 
                _location=event["properties"]["EventLocation"]
                )

            events.append(event)

        return events

    @staticmethod
    def UpdateEventUrls(events, countries):

        for country in countries:

            for event in events:

                if str(event.countryCode) == str(country.id):

                    event.url = f"{country.url}/{event.name}/".replace("//", "/")

        return events

class Result():

    def __init__(self, _name=None, _ageGroup=None, _club=None, _gender=None, _position=None, _runs=None, _ageGrade=None, _achievement=None):

        self.name = _name
        self.ageGroup = _ageGroup
        self.club = _club
        self.gender = _gender
        self.position = _position
        self.runs = _runs
        self.ageGrade = _ageGrade
        self.achievement = _achievement

        pass

    @staticmethod
    def GetResults(event, eventNumber):

        results = []

        resultsHTML = session.get(event.url + "results/{eventNumber}/").text

        resultsSoup = BeautifulSoup(resultsHTML, "html.parser")
        resultRows = resultsSoup.findAll("tr", {"class": "Results-table-row"})

        for resultRow in resultRows:

            result = Result(
                _name=resultRow["data-name"],
                _ageGroup=resultRow["data-agegroup"],
                _club=resultRow["data-club"],
                _gender=resultRow["data-gender"],
                _position=resultRow["data-position"],
                _runs=resultRow["data-runs"],
                _ageGrade=resultRow["data-agegrade"],
                _achievement=resultRow["data-achievement"]
            )

            results.append(result)

        return results

    @staticmethod
    def GetLatestResults(event):

        return Result.GetResults(event, "latestresults")

class EventHistory():

    def __init__(self, _eventNumber=None, _date=None, _finishers=None, _volunteers=None, _male=None, _female=None, _maleTime=None, _femaleTime=None):

        self.eventNumber = _eventNumber
        self.date = _date
        self.finishers = _finishers
        self.volunteers = _volunteers
        self.male = _male
        self.female = _female
        self.maleTime = _maleTime
        self.femaleTime = _femaleTime

        pass

    @staticmethod
    def GetEventHistorys(event):

        eventHistorys = []

        eventHistoryHTML = session.get(event.url + "results/eventhistory/").text

        eventHistorySoup = BeautifulSoup(eventHistoryHTML, "html.parser")
        eventHistoryRows = eventHistorySoup.findAll("tr", {"class": "Results-table-row"})

        for eventHistoryRow in eventHistoryRows:

            eventHistory = EventHistory(
                _eventNumber=eventHistoryRow["data-parkrun"],
                _date=eventHistoryRow["data-date"],
                _finishers=eventHistoryRow["data-finishers"],
                _volunteers=eventHistoryRow["data-volunteers"],
                _male=eventHistoryRow["data-male"],
                _female=eventHistoryRow["data-female"],
                _maleTime=eventHistoryRow["data-maletime"],
                _femaleTime=eventHistoryRow["data-femaletime"],
            )

            eventHistorys.append(eventHistory)

        return eventHistorys

class FirstFinisher():

    def __init__(self, _parkRunner=None, _firstPlaceFinishes=None, _bestTime=None, _sex=None):

        self.parkRunner = _parkRunner
        self.firstPlaceFinishes = _firstPlaceFinishes
        self.bestTime = _bestTime
        self.sex = _sex

        pass

    @staticmethod
    def GetFirstFinishers(event):

        firstFinishers = []

        firstFinishersHTML = session.get(event.url + "results/firstfinishescount/").text

        firstFinishersSoup = BeautifulSoup(firstFinishersHTML, "html.parser")
        firstFinishersRows = firstFinishersSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for firstFinisherRow in firstFinishersRows:

            rowData = firstFinisherRow.findAll("td")

            firstFinisher = FirstFinisher(
                _parkRunner=rowData[0].find("a").text if rowData[0].find("a") else None,
                _firstPlaceFinishes=rowData[1].text if rowData[1] else None,
                _bestTime=rowData[2].text if rowData[2] else None,
                _sex=rowData[3].text if rowData[3] else None
            )

            firstFinishers.append(firstFinisher)

        return firstFinishers

class AgeCategoryRecord():

    def __init__(self, _ageCategory=None, _eventNumber=None, _date=None, _parkRunner=None, _time=None, _ageGrade=None):

        self.ageCategory = _ageCategory
        self.eventNumber = _eventNumber
        self.date = _date
        self.parkRunner = _parkRunner
        self.time = _time
        self.ageGrade = _ageGrade

        pass

    @staticmethod
    def GetAgeCategoryRecords(event):

        getAgeCategoryRecords = []

        getAgeCategoryRecordsHTML = session.get(event.url + "results/agecategoryrecords/").text

        getAgeCategoryRecordsSoup = BeautifulSoup(getAgeCategoryRecordsHTML, "html.parser")
        getAgeCategoryRecordsRows = getAgeCategoryRecordsSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for ageCategoryRecordRow in getAgeCategoryRecordsRows:

            rowData = ageCategoryRecordRow.findAll("td")

            ageCategoryRecord = AgeCategoryRecord(
                _ageCategory=rowData[0].find("a").find("strong").text if rowData[0].find("a") else None,
                _eventNumber=rowData[2].find("a").text if rowData[2].find("a") else None,
                _date=rowData[3].find("a").text if rowData[3].find("a") else None,
                _parkRunner=rowData[4].text if rowData[4] else None,
                _time=rowData[5].text if rowData[5] else None,
                _ageGrade=rowData[6].text if rowData[6] else None
            )

            getAgeCategoryRecords.append(ageCategoryRecord)

        return getAgeCategoryRecords

class Club():

    def __init__(self, _name=None, _numberOfParkrunners=None, _numberOfRuns=None, _clubHomePage=None):

        self.name = _name
        self.numberOfParkrunners = _numberOfParkrunners
        self.numberOfRuns = _numberOfRuns
        self.clubHomePage = _clubHomePage

        pass

    @staticmethod
    def GetClubs(event):

        clubs = []

        clubsHTML = session.get(event.url + "results/clublist/").text

        clubsSoup = BeautifulSoup(clubsHTML, "html.parser")
        clubRows = clubsSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")
        
        for clubRow in clubRows:

            rowData = clubRow.findAll("td")

            club = Club(
                _name=rowData[0].find("a").text if rowData[0].find("a") else None,
                _numberOfParkrunners=rowData[1].text if rowData[1] else None,
                _numberOfRuns=rowData[2].text if rowData[2] else None,
                _clubHomePage=rowData[3].find("a")["href"] if rowData[3].find("a") else None,
            )

            clubs.append(club)

        return clubs

class Sub20Woman():

    def __init__(self, _rank=None, _parkRunner=None, _numberOfRuns=None, _fastestTime=None, _club=None):

        self.rank = _rank
        self.parkRunner = _parkRunner
        self.numberOfRuns = _numberOfRuns
        self.fastestTime = _fastestTime
        self.club = _club

        pass

    @staticmethod
    def GetSub20Women(event):

        sub20Women = []

        sub20WomenHTML = session.get(event.url + "results/sub20women/").text

        sub20WomenSoup = BeautifulSoup(sub20WomenHTML, "html.parser")
        sub20WomenRows = sub20WomenSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")
        
        for sub20WomenRow in sub20WomenRows:

            rowData = sub20WomenRow.findAll("td")

            sub20Woman = Sub20Woman(
                _rank=rowData[0].text if rowData[0] else None,
                _parkRunner=rowData[1].find("a").text if rowData[1].find("a") else None,
                _numberOfRuns=rowData[2].text if rowData[2] else None,
                _fastestTime=rowData[3].text if rowData[3] else None,
                _club=rowData[4].find("a").text if rowData[4].find("a") else None
            )

            sub20Women.append(sub20Woman)

        return sub20Women

class Sub17Man():

    def __init__(self, _rank=None, _parkRunner=None, _numberOfRuns=None, _fastestTime=None, _club=None):

        self.rank = _rank
        self.parkRunner = _parkRunner
        self.numberOfRuns = _numberOfRuns
        self.fastestTime = _fastestTime
        self.club = _club

        pass

    @staticmethod
    def GetSub17Men(event):

        sub17Men = []

        sub17MenHTML = session.get(event.url + "results/sub17men/").text

        sub17MenSoup = BeautifulSoup(sub17MenHTML, "html.parser")
        sub17MenRows = sub17MenSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")
        
        for sub17MenRow in sub17MenRows:

            rowData = sub17MenRow.findAll("td")

            sub17Man = Sub17Man(
                _rank=rowData[0].text,
                _parkRunner=rowData[1].find("a").text if rowData[1].find("a") else None,
                _numberOfRuns=rowData[2].text if rowData[2] else None,
                _fastestTime=rowData[3].text if rowData[3] else None,
                _club=rowData[4].find("a").text if rowData[4].find("a") else None,
            )

            sub17Men.append(sub17Man)

        return sub17Men

class AgeGradedLeagueRank():

    def __init__(self, _rank=None, _parkRunner=None, _ageGrade=None):

        self.rank = _rank
        self.parkRunner = _parkRunner
        self.ageGrade = _ageGrade

        pass

    @staticmethod
    def GetAgeGradedLeagueRanks(event, quantity=1000):

        ageGradedLeagueRanks = []

        resultSet = int(math.ceil(quantity/1000))

        for i in range(1, resultSet+1):

            ageGradedLeagueRanksHTML = session.get(event.url + f"results/agegradedleague/?resultSet={resultSet}").text

            ageGradedLeagueRanksSoup = BeautifulSoup(ageGradedLeagueRanksHTML, "html.parser")
            ageGradedLeagueRanksRows = ageGradedLeagueRanksSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")
            
            for ageGradedLeagueRanksRow in ageGradedLeagueRanksRows:

                rowData = ageGradedLeagueRanksRow.findAll("td")

                ageGradedLeagueRank = AgeGradedLeagueRank(
                    _rank=rowData[0].text if rowData[0] else None,
                    _parkRunner=rowData[1].find("a").text if rowData[1].find("a") else None,
                    _ageGrade=rowData[2].text if rowData[2] else None
                )

                ageGradedLeagueRanks.append(ageGradedLeagueRank)

        return ageGradedLeagueRanks

class Fastest():

    def __init__(self, _rank=None, _parkRunner=None, _numberOfRuns=None, _sex=None, _fastestTime=None, _club=None):

        self.rank = _rank
        self.parkRunner = _parkRunner
        self.numberOfRuns = _numberOfRuns
        self.sex = _sex
        self.fastestTime = _fastestTime
        self.club = _club

        pass

    @staticmethod
    def GetFastest500(event):

        fastest500 = []

        fastest500HTML = session.get(event.url + "results/fastest500/").text

        fastest500Soup = BeautifulSoup(fastest500HTML, "html.parser")
        fastest500Rows = fastest500Soup.find("table", {"id": "results"}).find("tbody").findAll("tr")
        
        for fastest500Row in fastest500Rows:

            rowData = fastest500Row.findAll("td")

            fastest = Fastest(
                _rank=rowData[0].text if rowData[0] else None,
                _parkRunner=rowData[1].find("a").text if rowData[1].find("a") else None,
                _numberOfRuns=rowData[2].text if rowData[2] else None,
                _sex=rowData[3].text if rowData[3] else None,
                _fastestTime=rowData[4].text if rowData[4] else None,
                _club=rowData[5].find("a").text if rowData[5].find("a") else None,
            )

            fastest500.append(fastest)

        return fastest500

class WeekFirstFinisher:

    def __init__(self, _event=None, _maleParkRunner=None, _maleClub=None, _femaleParkRunner=None, _femaleClub=None):

        self.event = _event
        self.maleParkRunner = _maleParkRunner
        self.maleClub = _maleClub
        self.femaleParkRunner = _femaleParkRunner
        self.femaleClub = _femaleClub

        pass

    @staticmethod
    def GetWeekFirstFinishersForCountry(country):

        weekFirstFinishers = []

        weekFirstFinisherHTML = session.get(country.url + "/results/firstfinishers/").text

        weekFirstFinisherSoup = BeautifulSoup(weekFirstFinisherHTML, "html.parser")
        weekFirstFinisherRows = weekFirstFinisherSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for weekFirstFinisherRow in weekFirstFinisherRows:

            rowData = weekFirstFinisherRow.findAll("td")

            weekFirstFinisher = WeekFirstFinisher(
                _event=rowData[0].find("a").text if rowData[0].find("a") else None,
                _maleParkRunner=rowData[2].find("a").text if rowData[2].find("a") else None,
                _maleClub=rowData[3].find("a").text if rowData[3].find("a") else None,
                _femaleParkRunner=rowData[5].find("a").text if rowData[5].find("a") else None,
                _femaleClub=rowData[6].find("a").text if rowData[6].find("a") else None,
            )

            weekFirstFinishers.append(weekFirstFinisher)

        return weekFirstFinishers

    @staticmethod
    def GetWeekFirstFinishersGlobally():

        weekFirstFinishers = []

        weekFirstFinisherHTML = session.get("https://www.parkrun.com/results/firstfinishers/").text

        weekFirstFinisherSoup = BeautifulSoup(weekFirstFinisherHTML, "html.parser")
        weekFirstFinisherRows = weekFirstFinisherSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for weekFirstFinisherRow in weekFirstFinisherRows:

            rowData = weekFirstFinisherRow.findAll("td")

            weekFirstFinisher = WeekFirstFinisher(
                _event=rowData[0].find("a").text if rowData[0].find("a") else None,
                _maleParkRunner=rowData[1].find("a").text if rowData[1].find("a") else None,
                _maleClub=rowData[2].text if rowData[2] else None,
                _femaleParkRunner=rowData[3].find("a").text if rowData[3].find("a") else None,
                _femaleClub=rowData[4].text if rowData[4] else None,
            )

            weekFirstFinishers.append(weekFirstFinisher)

        return weekFirstFinishers

class WeekSub17Run:

    def __init__(self, _event=None, _parkRunner=None, _time=None, _club=None):

        self.event = _event
        self.parkRunner = _parkRunner
        self.time = _time
        self.club = _club

        pass

    @staticmethod
    def GetWeekSub17RunsForCountry(country):

        weekSub17Runs = []

        weekSub17RunHTML = session.get(country.url + "/results/sub17/").text

        weekSub17RunSoup = BeautifulSoup(weekSub17RunHTML, "html.parser")
        weekSub17RunRows = weekSub17RunSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for weekSub17RunRow in weekSub17RunRows:

            rowData = weekSub17RunRow.findAll("td")

            weekSub17Run = WeekSub17Run(
                _event=rowData[0].find("a").text if rowData[0].find("a") else None,
                _parkRunner=rowData[2].find("a").text if rowData[2].find("a") else None,
                _time=rowData[3].text if rowData[3] else None,
                _club=rowData[4].find("a").text if rowData[4].find("a") else None,
            )

            weekSub17Runs.append(weekSub17Run)

        return weekSub17Runs

    @staticmethod
    def GetWeekSub17RunsGlobally():

        weekSub17Runs = []

        weekSub17RunHTML = session.get("https://www.parkrun.com/results/sub17/").text

        weekSub17RunSoup = BeautifulSoup(weekSub17RunHTML, "html.parser")
        weekSub17RunRows = weekSub17RunSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for weekSub17RunRow in weekSub17RunRows:

            rowData = weekSub17RunRow.findAll("td")

            weekSub17Run = WeekSub17Run(
                _event=rowData[0].find("a").text if rowData[0].find("a") else None,
                _parkRunner=rowData[1].find("a").text if rowData[1].find("a") else None,
                _time=rowData[2].text if rowData[2] else None,
                _club=rowData[3].text if rowData[3] else None,
            )

            weekSub17Runs.append(weekSub17Run)

        return weekSub17Runs

class WeekTopAgeGrade:

    def __init__(self, _event=None, _parkRunner=None, _time=None, _ageGroup=None, _ageGrade=None, _club=None):

        self.event = _event
        self.parkRunner = _parkRunner
        self.time = _time
        self.ageGroup = _ageGroup
        self.ageGrade = _ageGrade
        self.club = _club

        pass

    @staticmethod
    def GetWeekTopAgeGradesForCountry(country):

        weekTopAgeGrades = []

        weekTopAgeGradeHTML = session.get(country.url + "/results/topagegrade/").text

        weekTopAgeGradeSoup = BeautifulSoup(weekTopAgeGradeHTML, "html.parser")
        weekTopAgeGradeRows = weekTopAgeGradeSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for weekTopAgeGradeRow in weekTopAgeGradeRows:

            rowData = weekTopAgeGradeRow.findAll("td")

            weekTopAgeGrade = WeekTopAgeGrade(
                _event=rowData[0].find("a").text if rowData[0].find("a") else None,
                _parkRunner=rowData[2].find("a").text if rowData[2].find("a") else None,
                _time=rowData[3].text if rowData[3] else None,
                _ageGroup=rowData[4].text if rowData[4] else None,
                _ageGrade=rowData[5].text if rowData[5] else None,
                _club=rowData[6].find("a").text if rowData[6].find("a") else None,
            )

            weekTopAgeGrades.append(weekTopAgeGrade)

        return weekTopAgeGrades

    @staticmethod
    def GetWeekTopAgeGradesGlobally():

        weekTopAgeGrades = []

        weekTopAgeGradeHTML = session.get("https://www.parkrun.com/results/topagegrade/").text

        weekTopAgeGradeSoup = BeautifulSoup(weekTopAgeGradeHTML, "html.parser")
        weekTopAgeGradeRows = weekTopAgeGradeSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for weekTopAgeGradeRow in weekTopAgeGradeRows:

            rowData = weekTopAgeGradeRow.findAll("td")

            weekTopAgeGrade = WeekTopAgeGrade(
                _event=rowData[0].find("a").text if rowData[0].find("a") else None,
                _parkRunner=rowData[1].find("a").text if rowData[1].find("a") else None,
                _time=rowData[2].text if rowData[2] else None,
                _ageGroup=rowData[3].text if rowData[3] else None,
                _ageGrade=rowData[4].text if rowData[4] else None,
                _club=rowData[5].text if rowData[5] else None,
            )

            weekTopAgeGrades.append(weekTopAgeGrade)

        return weekTopAgeGrades

class WeekNewCategoryRecord:

    def __init__(self, _event=None, _parkRunner=None, _time=None, _ageGroup=None, _ageGrade=None, _club=None):

        self.event = _event
        self.parkRunner = _parkRunner
        self.time = _time
        self.ageGroup = _ageGroup
        self.ageGrade = _ageGrade
        self.club = _club

        pass

    @staticmethod
    def GetWeekNewCategoryRecordsForCountry(country):

        weekNewCategoryRecords = []

        weekNewCategoryRecordHTML = session.get(country.url + "/results/newcategoryrecords/").text

        weekNewCategoryRecordSoup = BeautifulSoup(weekNewCategoryRecordHTML, "html.parser")
        weekNewCategoryRecordRows = weekNewCategoryRecordSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for weekNewCategoryRecordRow in weekNewCategoryRecordRows:

            rowData = weekNewCategoryRecordRow.findAll("td")

            weekNewCategoryRecord = WeekNewCategoryRecord(
                _event=rowData[0].find("a").text if rowData[0].find("a") else None,
                _parkRunner=rowData[2].find("a").text if rowData[2].find("a") else None,
                _time=rowData[3].text if rowData[3] else None,
                _ageGroup=rowData[4].text if rowData[4] else None,
                _ageGrade=rowData[5].text if rowData[5] else None,
                _club=rowData[6].find("a").text if rowData[6].find("a") else None
            )

            weekNewCategoryRecords.append(weekNewCategoryRecord)

        return weekNewCategoryRecords
        
    @staticmethod
    def GetWeekNewCategoryRecordsGlobally():

        weekNewCategoryRecords = []

        weekNewCategoryRecordHTML = session.get("https://www.parkrun.com/results/newcategoryrecords/").text

        weekNewCategoryRecordSoup = BeautifulSoup(weekNewCategoryRecordHTML, "html.parser")
        weekNewCategoryRecordRows = weekNewCategoryRecordSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for weekNewCategoryRecordRow in weekNewCategoryRecordRows:

            rowData = weekNewCategoryRecordRow.findAll("td")

            weekNewCategoryRecord = WeekNewCategoryRecord(
                _event=rowData[0].find("a").text if rowData[0].find("a") else None,
                _parkRunner=rowData[1].find("a").text if rowData[1].find("a") else None,
                _time=rowData[2].text if rowData[2] else None,
                _ageGroup=rowData[3].text if rowData[3] else None,
                _ageGrade=rowData[4].text if rowData[4] else None,
                _club=rowData[5].text if rowData[5] else None
            )

            weekNewCategoryRecords.append(weekNewCategoryRecord)

        return weekNewCategoryRecords

class CourseRecord:

    def __init__(self, _event=None, _femaleParkRunner=None, _femaleTime=None, _femaleDate=None, _maleParkRunner=None, _maleTime=None, _maleDate=None):

        self.event = _event
        self.femaleParkRunner = _femaleParkRunner
        self.femaleTime = _femaleTime
        self.femaleDate = _femaleDate
        self.maleParkRunner = _maleParkRunner
        self.maleTime = _maleTime
        self.maleDate = _maleDate

        pass

    @staticmethod
    def GetCourseRecordsForCountry(country):

        courseRecords = []

        courseRecordHTML = session.get(country.url + "/results/courserecords/").text

        courseRecordSoup = BeautifulSoup(courseRecordHTML, "html.parser")
        courseRecordRows = courseRecordSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for courseRecordRow in courseRecordRows:

            rowData = courseRecordRow.findAll("td")

            courseRecord = CourseRecord(
                _event=rowData[0].find("a").text if rowData[0].find("a") else None,
                _femaleParkRunner=rowData[2].find("a").text if rowData[2].find("a") else None,
                _femaleTime=rowData[3].text if rowData[3] else None,
                _femaleDate=rowData[4].text if rowData[4] else None,
                _maleParkRunner=rowData[6].find("a").text if rowData[6].find("a") else None,
                _maleTime=rowData[7].text if rowData[7] else None,
                _maleDate=rowData[8].text if rowData[8] else None,
            )

            courseRecords.append(courseRecord)

        return courseRecords

    @staticmethod
    def GetCourseRecordsGlobally():

        courseRecords = []

        courseRecordHTML = session.get("https://www.parkrun.com/results/courserecords/").text

        courseRecordSoup = BeautifulSoup(courseRecordHTML, "html.parser")
        courseRecordRows = courseRecordSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for courseRecordRow in courseRecordRows:

            rowData = courseRecordRow.findAll("td")

            courseRecord = CourseRecord(
                _event=rowData[0].find("a").text if rowData[0].find("a") else None,
                _femaleParkRunner=rowData[1].find("a").text if rowData[1].find("a") else None,
                _femaleTime=rowData[2].text if rowData[2] else None,
                _femaleDate=rowData[3].text if rowData[3] else None,
                _maleParkRunner=rowData[4].find("a").text if rowData[4].find("a") else None,
                _maleTime=rowData[5].text if rowData[5] else None,
                _maleDate=rowData[6].text if rowData[6] else None,
            )

            courseRecords.append(courseRecord)

        return courseRecords

class AttendanceRecord:

    def __init__(self, _event=None, _attendance=None, _week=None, _thisWeek=None):

        self.event = _event
        self.attendance = _attendance
        self.week = _week
        self.thisWeek = _thisWeek

        pass

    @staticmethod
    def GetAttendanceRecordsForCountry(country):

        attendanceRecords = []

        attendanceRecordHTML = session.get(country.url + "/results/attendancerecords/").text

        attendanceRecordSoup = BeautifulSoup(attendanceRecordHTML, "html.parser")
        attendanceRecordRows = attendanceRecordSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for attendanceRecordRow in attendanceRecordRows:

            rowData = attendanceRecordRow.findAll("td")

            attendanceRecord = AttendanceRecord(
                _event=rowData[0].find("a").text if rowData[0].find("a") else None,
                _attendance=rowData[2].text if rowData[2] else None,
                _week=rowData[3].text if rowData[3] else None,
                _thisWeek=rowData[4].text if rowData[4] else None,
            )

            attendanceRecords.append(attendanceRecord)

        return attendanceRecords

class MostEvent:

    def __init__(self, _parkRunner=None, _events=None, _totalParkRuns=None, _totalParkRunsWorldwide=None):

        self.parkRunner = _parkRunner
        self.events = _events
        self.totalParkRuns = _totalParkRuns
        self.totalParkRunsWorldwide = _totalParkRunsWorldwide

        pass

    @staticmethod
    def GetMostEventsForCountry(country):

        mostEvents = []

        mostEventHTML = session.get(country.url + "/results/mostevents/").text

        mostEventSoup = BeautifulSoup(mostEventHTML, "html.parser")
        mostEventRows = mostEventSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for mostEventRow in mostEventRows:

            rowData = mostEventRow.findAll("td")

            mostEvent = MostEvent(
                _parkRunner=rowData[0].find("a").text if rowData[0].find("a") else None,
                _events=rowData[3].text if rowData[3] else None,
                _totalParkRuns=rowData[4].text if rowData[4] else None,
                _totalParkRunsWorldwide=rowData[5].text if rowData[5] else None,
            )

            mostEvents.append(mostEvent)

        return mostEvents

class LargestClub:

    def __init__(self, _club=None, _numberOfParkRunners=None, _numberOfRuns=None, _clubHomePage=None):

        self.club = _club
        self.numberOfParkRunners = _numberOfParkRunners
        self.numberOfRuns = _numberOfRuns
        self.clubHomePage = _clubHomePage

        pass

    @staticmethod
    def GetLargestClubsForCountry(country):

        largestClubs = []

        largestClubHTML = session.get(country.url + "/results/largestclubs/").text

        largestClubSoup = BeautifulSoup(largestClubHTML, "html.parser")
        largestClubRows = largestClubSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for largestClubRow in largestClubRows:

            rowData = largestClubRow.findAll("td")

            largestClub = LargestClub(
                _club=rowData[0].find("a").text if rowData[0].find("a") else None,
                _numberOfParkRunners=rowData[2].text if rowData[2] else None,
                _numberOfRuns=rowData[3].text if rowData[3] else None,
                _clubHomePage=rowData[4].find("a")["href"] if rowData[4].find("a") else None,
            )

            largestClubs.append(largestClub)

        return largestClubs

class Joined100Club:

    def __init__(self, _parkRunner=None, _numberOfRuns=None):

        self.parkRunner = _parkRunner
        self.numberOfRuns = _numberOfRuns

        pass

    @staticmethod
    def GetJoined100ClubsForCountry(country):

        joined100Clubs = []

        joined100ClubHTML = session.get(country.url + "/results/100clubbers/").text

        joined100ClubSoup = BeautifulSoup(joined100ClubHTML, "html.parser")
        joined100ClubRows = joined100ClubSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for joined100ClubRow in joined100ClubRows:

            rowData = joined100ClubRow.findAll("td")

            joined100Club = Joined100Club(
                _parkRunner=rowData[0].find("a").text if rowData[0].find("a") else None,
                _numberOfRuns="100" if rowData[1].find("img") else rowData[1].text,
            )

            joined100Clubs.append(joined100Club)

        return joined100Clubs

class MostFirstFinish:

    def __init__(self, _parkRunner=None, _numberOfRuns=None):

        self.parkRunner = _parkRunner
        self.numberOfRuns = _numberOfRuns

        pass

    @staticmethod
    def GetMostFirstFinishesForCountry(country):

        mostFirstFinishes = []

        mostFirstFinishHTML = session.get(country.url + "/results/mostfirstfinishes/").text

        mostFirstFinishSoup = BeautifulSoup(mostFirstFinishHTML, "html.parser")
        mostFirstFinishRows = mostFirstFinishSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for mostFirstFinishRow in mostFirstFinishRows:

            rowData = mostFirstFinishRow.findAll("td")

            mostFirstFinish = MostFirstFinish(
                _parkRunner=rowData[0].find("a").text if rowData[0].find("a") else None,
                _numberOfRuns=rowData[1].text if rowData[1] else None,
            )

            mostFirstFinishes.append(mostFirstFinish)

        return mostFirstFinishes

class FreedomRun:

    def __init__(self, _parkRunner=None, _date=None, _location=None, _runTime=None):

        self.parkRunner = _parkRunner
        self.date = _date
        self.location = _location
        self.runTime = _runTime

        pass

    @staticmethod
    def GetFreedomRunsForCountry(country):

        freedomRuns = []

        freedomRunHTML = session.get(country.url + "/results/freedom/").text

        freedomRunSoup = BeautifulSoup(freedomRunHTML, "html.parser")
        freedomRunRows = freedomRunSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for freedomRunRow in freedomRunRows:

            rowData = freedomRunRow.findAll("td")

            freedomRun = FreedomRun(
                _parkRunner=rowData[0].find("a").text if rowData[0].find("a") else None,
                _date=rowData[1].text if rowData[1] else None,
                _location=rowData[2].text if rowData[2] else None,
                _runTime=rowData[3].text if rowData[3] else None,
            )

            freedomRuns.append(freedomRun)

        return freedomRuns

    @staticmethod
    def GetFreedomRunsGlobally():

        freedomRuns = []

        freedomRunHTML = session.get("https://www.parkrun.com/results/freedom/").text

        freedomRunSoup = BeautifulSoup(freedomRunHTML, "html.parser")
        freedomRunRows = freedomRunSoup.find("table", {"id": "results"}).find("tbody").findAll("tr")

        for freedomRunRow in freedomRunRows:

            rowData = freedomRunRow.findAll("td")

            freedomRun = FreedomRun(
                _parkRunner=rowData[0].find("a").text if rowData[0].find("a") else None,
                _date=rowData[1].text if rowData[1] else None,
                _location=rowData[2].text if rowData[2] else None,
                _runTime=rowData[3].text if rowData[3] else None,
            )

            freedomRuns.append(freedomRun)

        return freedomRuns

class HistoricNumber:

    def __init__(self, _date=None, _events=None, _athletes=None, _volunteers=None):

        self.date = _date
        self.events = _events
        self.athletes = _athletes
        self.volunteers = _volunteers

        pass

    @staticmethod
    def GetHistoricNumbersForCountry(country=None):

        historicNumbers = []
        historicNumberHTML = None

        if country:

            historicNumberHTML = session.get("https://results-service.parkrun.com/resultsSystem/App/globalChartNumRunnersAndEvents.php?CountryNum=" + country.id).text

        else:

            historicNumberHTML = session.get("https://results-service.parkrun.com/resultsSystem/App/globalChartNumRunnersAndEvents.php").text

        searchString = "data.addRows(["
        contentStartIndex = historicNumberHTML.find(searchString) + len(searchString)
        contentEndIndex = historicNumberHTML.find("]);", contentStartIndex)
        contentString = historicNumberHTML[contentStartIndex:contentEndIndex].replace("\n","").replace("\r","").replace("\t","").replace(" ","")

        contentList = contentString.split("],")

        for contentRow in contentList:

            if contentRow.strip() == "":

                continue

            splitContentRow = contentRow.split(",")
            dateStart = splitContentRow[0].find("(")
            dateEnd = splitContentRow[0].find(")")
            date = splitContentRow[0][dateStart + 1:dateEnd]

            historicNumber = HistoricNumber(
                _date=date,
                _events=splitContentRow[1],
                _athletes=splitContentRow[2],
                _volunteers=splitContentRow[3],
            )

            historicNumbers.append(historicNumber)

        return historicNumbers
    
def ExampleUsage():

    countries = Country.GetAllCountries()
    events = Event.GetAllEvents()
    Event.UpdateEventUrls(events, countries)

    selectedEvent = events[0]

    eventHistory = EventHistory.GetEventHistorys(selectedEvent)
    firstFinishers = FirstFinisher.GetFirstFinishers(selectedEvent)
    AgeCategoryRecords = AgeCategoryRecord.GetAgeCategoryRecords(selectedEvent)
    clubs = Club.GetClubs(selectedEvent)
    sub20Women = Sub20Woman.GetSub20Women(selectedEvent)
    sub17Men = Sub17Man.GetSub17Men(selectedEvent)
    ageGradedLeagueRanks = AgeGradedLeagueRank.GetAgeGradedLeagueRanks(selectedEvent)
    fastest500 = Fastest.GetFastest500(selectedEvent)

    weekFirstFinishers = WeekFirstFinisher.GetWeekFirstFinishersForCountry(countries[0])
    weekSub17Runs = WeekSub17Run.GetWeekSub17RunsForCountry(countries[0])
    weekTopAgeGrades = WeekTopAgeGrade.GetWeekTopAgeGradesForCountry(countries[0])
    weekNewCategoryRecords = WeekNewCategoryRecord.GetWeekNewCategoryRecordsForCountry(countries[0])
    courseRecords = CourseRecord.GetCourseRecordsForCountry(countries[0])
    attendanceRecords = AttendanceRecord.GetAttendanceRecordsForCountry(countries[0])
    mostEvents = MostEvent.GetMostEventsForCountry(countries[0])
    largestClubs = LargestClub.GetLargestClubsForCountry(countries[0])
    joined100Clubs = Joined100Club.GetJoined100ClubsForCountry(countries[0])
    mostFirstFinishes = MostFirstFinish.GetMostFirstFinishesForCountry(countries[0])
    freedomRuns = FreedomRun.GetFreedomRunsForCountry(countries[0])
    historicNumbers = HistoricNumber.GetHistoricNumbersForCountry()

    globalWeekFirstFinishers = WeekFirstFinisher.GetWeekFirstFinishersGlobally()
    globalNewCategoryRecords = WeekNewCategoryRecord.GetWeekNewCategoryRecordsGlobally()
    globalSub17Runs = WeekSub17Run.GetWeekSub17RunsGlobally()
    globalTopAgeGrades = WeekTopAgeGrade.GetWeekTopAgeGradesGlobally()
    globalCourseRecords = CourseRecord.GetCourseRecordsGlobally()
    globalFreedomRuns = FreedomRun.GetFreedomRunsGlobally()

    print("Done")