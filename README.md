# Parkrun-API-Python
Python API for Parkrun data, currently live at parkrun-api.rggs.xyz. This is a light-weight and unofficial API.

## Python Requirements
```python
# General
pip install requests
pip install beautifulsoup4

# For running web API
pip install flask
pip install flask-limiter
```
## Example Usage (see also example.py)
```python
import parkrun_api as parkrun

def ExampleUsage():

    # General Setup Data
    countries = parkrun.Country.GetAllCountries()
    events = parkrun.Event.GetAllEvents()
    parkrun.Event.UpdateEventUrls(events, countries)

    selectedEvent = parkrun.events[0]

    # Event Specific Data
    eventHistory = parkrun.EventHistory.GetEventHistorys(selectedEvent)
    firstFinishers = parkrun.FirstFinisher.GetFirstFinishers(selectedEvent)
    ageCategoryRecords = parkrun.AgeCategoryRecord.GetAgeCategoryRecords(selectedEvent)
    clubs = parkrun.Club.GetClubs(selectedEvent)
    sub20Women = parkrun.Sub20Woman.GetSub20Women(selectedEvent)
    sub17Men = parkrun.Sub17Man.GetSub17Men(selectedEvent)
    ageGradedLeagueRanks = parkrun.AgeGradedLeagueRank.GetAgeGradedLeagueRanks(selectedEvent)
    fastest500 = parkrun.Fastest.GetFastest500(selectedEvent)

    # Country Specific Data
    weekFirstFinishers = parkrun.WeekFirstFinisher.GetWeekFirstFinishersForCountry(countries[0])
    weekSub17Runs = parkrun.WeekSub17Run.GetWeekSub17RunsForCountry(countries[0])
    weekTopAgeGrades = parkrun.WeekTopAgeGrade.GetWeekTopAgeGradesForCountry(countries[0])
    weekNewCategoryRecords = parkrun.WeekNewCategoryRecord.GetWeekNewCategoryRecordsForCountry(countries[0])
    courseRecords = parkrun.CourseRecord.GetCourseRecordsForCountry(countries[0])
    attendanceRecords = parkrun.AttendanceRecord.GetAttendanceRecordsForCountry(countries[0])
    mostEvents = parkrun.MostEvent.GetMostEventsForCountry(countries[0])
    largestClubs = parkrun.LargestClub.GetLargestClubsForCountry(countries[0])
    joined100Clubs = parkrun.Joined100Club.GetJoined100ClubsForCountry(countries[0])
    mostFirstFinishes = parkrun.MostFirstFinish.GetMostFirstFinishesForCountry(countries[0])
    freedomRuns = parkrun.FreedomRun.GetFreedomRunsForCountry(countries[0])
    historicNumbers = parkrun.HistoricNumber.GetHistoricNumbersForCountry()

    # Global Results Data
    globalWeekFirstFinishers = parkrun.WeekFirstFinisher.GetWeekFirstFinishersGlobally()
    globalNewCategoryRecords = parkrun.WeekNewCategoryRecord.GetWeekNewCategoryRecordsGlobally()
    globalSub17Runs = parkrun.WeekSub17Run.GetWeekSub17RunsGlobally()
    globalTopAgeGrades = parkrun.WeekTopAgeGrade.GetWeekTopAgeGradesGlobally()
    globalCourseRecords = parkrun.CourseRecord.GetCourseRecordsGlobally()
    globalFreedomRuns = parkrun.FreedomRun.GetFreedomRunsGlobally()

    # Global Stats Data
    globalLargestClubs = parkrun.Club.GetLargestClubsGlobally()
    globalAttendanceRecords = parkrun.AttendanceRecord.GetAttendanceRecordsGlobally()
    globalMostEvents = parkrun.MostEvent.GetMostEventsGlobally()
    globalMostFirstFinishes = parkrun.MostFirstFinish.GetMostFirstFinishesGlobally()

    print("Done")

ExampleUsage()
```

## Docker Deployment

### Build Docker Container
```
docker build -t parkrun-api:latest .
```

### Run Docker Container
```
docker run -d \
    --name parkrun-api \
    -p 5000:5000 \
    --restart on-failure \
    parkrun-api:latest
```

## API Documentation

### General Data

```/```
```
Redirect to https://github.com/BadgerHobbs/Parkrun-API-Python
```


```/v1/cache```
```json
{
  "countries": [
        {
            "id": "3",
            "url": "https://www.parkrun.com.au"
        },
    ],
    "events": [
        {
            "id": 193,
            "name": "newfarm",
            "longName": "New Farm parkrun",
            "shortName": "New Farm",
            "countryCode": 3,
            "seriesId": 1,
            "location": "New Farm, Brisbane",
            "url": "https://www.parkrun.com.au/newfarm/"
        },
    ],
    "countries/3/historic-numbers": [],
    "global/results/week-first-finishers": [],
    "...": [],
}
```


```/v1/countries```
```json
[
    {
        "id": "3",
        "url": "https://www.parkrun.com.au"
    },
    {
        "id": "4",
        "url": "https://www.parkrun.co.at"
    },
]
```

### Event Specific Data

```/v1/events```
```json
[
    {
        "id": 2761,
        "name": "centralplymouth",
        "longName": "Central parkrun, Plymouth",
        "shortName": "Central, Plymouth",
        "countryCode": 97,
        "seriesId": 1,
        "location": "Central Park",
        "url": "https://www.parkrun.org.uk/centralplymouth/"
    },
]
```


```/v1/events/<event_id>/history```
```json
[
    {
        "eventNumber": "5",
        "date": "18/12/2021",
        "finishers": "169",
        "volunteers": "21",
        "male": "John SMITH",
        "female": "Jasmine KING",
        "maleTime": "1647",
        "femaleTime": "2029"
    },
]
```


```/v1/events/<event_id>/first-finishers```
```json
[
    {
        "parkRunner": "John SMITH",
        "firstPlaceFinishes": "2",
        "bestTime": "16:47",
        "sex": "M"
    },
]
```


```/v1/events/<event_id>/age-category-records```
```json
[
    {
        "ageCategory": "JM10",
        "eventNumber": "4",
        "date": "11/12/2021",
        "parkRunner": "John SMITH",
        "time": "00:24:16",
        "ageGrade": "70.12 %"
    },
]
```


```/v1/events/<event_id>/clubs```
```json
    {
        "name": "Plymouth Musketeers RC",
        "numberOfParkrunners": "53",
        "numberOfRuns": "110",
        "clubHomePage": "http://www.plymouthmusketeers.org.uk/"
    },
```


```/v1/events/<event_id>/sub-20-women```
```json
[
    {
        "rank": "1",
        "parkRunner": "Molly SMITH",
        "numberOfRuns": "2",
        "fastestTime": "18:36",
        "club": null
    }
]
```


```/v1/events/<event_id>/sub-17-men```
```json
[
    {
        "rank": "1",
        "parkRunner": "Matt SMITH",
        "numberOfRuns": "1",
        "fastestTime": "16:43",
        "club": "Egdon Heath Harriers"
    },
]
```


```/v1/events/<event_id>/age-graded-league-ranks?quantity=<quantity>```
```json
[
    {
        "rank": "1",
        "parkRunner": "Molly SMITH",
        "ageGrade": "84.50 %"
    },
]
```


```/v1/events/<event_id>/fastest-500```
```json
[
    {
        "rank": "1",
        "parkRunner": "Matt SMITH",
        "numberOfRuns": "1",
        "sex": "M",
        "fastestTime": "00:16:43",
        "club": "Egdon Heath Harriers"
    },
]
```

### Country Specific Data

```/v1/countries/<country_id>/week-first-finishers```
```json
[
    {
        "event": "Airlie Beach",
        "maleParkRunner": "William SMITH",
        "maleClub": "Run Crew",
        "femaleParkRunner": "Aimee KING",
        "femaleClub": null
    },
]
```


```/v1/countries/<country_id>/week-sub-17-runs```
```json
[
    {
        "event": "Goolwa",
        "parkRunner": "Unknown ATHLETE",
        "time": "14:55",
        "club": null
    },
]
```


```/v1/countries/<country_id>/week-top-age-grades```
```json
[
    {
        "event": "Devonport",
        "parkRunner": "Xavier SMITH",
        "time": "18:08",
        "ageGroup": "JM10",
        "ageGrade": "93.84 %",
        "club": null
    },
]
```


```/v1/countries/<country_id>/week-new-category-records```
```json
[
    {
        "event": "Applecross",
        "parkRunner": "Jen SMITH",
        "time": "19:59",
        "ageGroup": "VW50-54",
        "ageGrade": "83.90 %",
        "club": "Frontrunner TRC"
    },
]
```


```/v1/countries/<country_id>/course-records```
```json
[
    {
        "event": "Airlie Beach",
        "femaleParkRunner": "Alex KING",
        "femaleTime": "18:56",
        "femaleDate": "11/12/2021",
        "maleParkRunner": "Tony SMITH",
        "maleTime": "15:55",
        "maleDate": "13/11/2021"
    },
]
```


```/v1/countries/<country_id>/attendance-records```
```json
[
    {
        "event": "Airlie Beach",
        "attendance": "120",
        "week": "16/02/2019",
        "thisWeek": "61"
    },
]
```


```/v1/countries/<country_id>/most-events```
```json
[
    {
        "parkRunner": "Neil SMITH",
        "events": "316",
        "totalParkRuns": "444",
        "totalParkRunsWorldwide": "444"
    },
]
```


```/v1/countries/<country_id>/largest-clubs```
```json
[
    {
        "club": "Derek Zoolander Centre for Kids Who Can't Run Good",
        "numberOfParkRunners": "1535",
        "numberOfRuns": "75993",
        "clubHomePage": "https://www.facebook.com/groups/650499288335106/"
    },
]
```


```/v1/countries/<country_id>/joined-100-club```
```json
[
    {
        "parkRunner": "Adeline KING",
        "numberOfRuns": "100"
    },
]
```


```/v1/countries/<country_id>/most-first-finishes```
```json
[
    {
        "parkRunner": "Cory SMITH",
        "numberOfRuns": "270"
    },
]
```


```/v1/countries/<country_id>/freedom-runs```
```json
[
    {
        "parkRunner": "David SMITH",
        "date": "24/12/2021",
        "location": "Blue Gum Hills",
        "runTime": "00:46:20"
    },
]
```


```/v1/countries/<country_id>/historic-numbers```
```json
[
    {
        "date": "2011-04-02",
        "events": "1",
        "athletes": "108",
        "volunteers": "7"
    },
]
```

### Global Results Data

```/v1/global/results/week-first-finishers```
```json
[
    {
        "event": "Aberbeeg",
        "maleParkRunner": "Martin SMITH",
        "maleClub": "Parc Bryn Bach Running Club",
        "femaleParkRunner": "Lisa KING",
        "femaleClub": "Pont-y-pwl and District Runners"
    },
]
```


```/v1/global/results/new-category-records```
```json
[
    {
        "event": "Aberdeen",
        "parkRunner": "Kirsty SMITH",
        "time": "18:22",
        "ageGroup": "SW18-19",
        "ageGrade": "81.49 %",
        "club": "Aberdeen AAC"
    },
]
```


```/v1/global/results/sub-17-runs```
```json
[
    {
        "event": "Hull",
        "parkRunner": "Kris SMITH",
        "time": "14:50",
        "club": "City of Hull AC"
    },
]
```


```/v1/global/results/top-age-grades```
```json
[
    {
        "event": "Rickmansworth",
        "parkRunner": "Sarah SMITH",
        "time": "22:34",
        "ageGroup": "VW70-74",
        "ageGrade": "101.99 %",
        "club": "Dacorum AC"
    },
]
```


```/v1/global/results/course-records```
```json
[
    {
        "event": "Aachener Weiher",
        "femaleParkRunner": "Hannah KING",
        "femaleTime": "18:44",
        "femaleDate": "14/12/2019",
        "maleParkRunner": "Declan SMITH",
        "maleTime": "16:37",
        "maleDate": "06/11/2021"
    },
]
```


```/v1/global/results/freedom-runs```
```json
[
    {
        "parkRunner": "Maria KING",
        "date": "24/12/2021",
        "location": "Whangarei",
        "runTime": "00:28:55"
    },
]
```

### Global Stats Data

```/v1/global/stats/largest-clubs```
```json
[
    {
        "name": "Lonely Goat RC",
        "numberOfParkrunners": "4443",
        "numberOfRuns": "170799",
        "clubHomePage": "https://lonelygoat.com"
    },
]
```


```/v1/global/stats/attendance-records```
```json
[
    {
        "event": "Aberbeeg",
        "attendance": "364",
        "week": "01/01/2020",
        "thisWeek": "30"
    },
]
```


```/v1/global/stats/most-events```
```json
[
    {
        "parkRunner": "Paul SMITH",
        "events": "541",
        "totalParkRuns": "585",
        "totalParkRunsWorldwide": null
    },
]
```


```/v1/global/stats/most-first-finishes```
```json
[
    {
        "parkRunner": "Hannah SMITH",
        "numberOfRuns": "368"
    },
]
```
