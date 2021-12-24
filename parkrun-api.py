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
                _url=countriesJson[countryKey]["url"]
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

                    event.url = "https://" + f"{country.url}/{event.name}/".replace("//", "/")

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
    print("Done")