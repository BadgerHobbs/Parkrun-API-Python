from flask import Flask, redirect, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import json
import parkrun_api as parkrun

cache = {}

def Setup():

    countries = parkrun.Country.GetAllCountries()
    events = parkrun.Event.GetAllEvents()
    parkrun.Event.UpdateEventUrls(events, countries)
    
    cache["countries"] = countries
    cache["events"] = events

def GetEventById(eventId):

    for event in cache["events"]:
        if str(event.id) == (eventId):
            return event

    return None

def GetCountryById(countryId):

    for country in cache["countries"]:
        if str(country.id) == (countryId):
            return country

    return None

def ObjectListToDictList(objectList):

    objectDictList = []

    for object in objectList:
        objectDictList.append(object.__dict__)

    return objectDictList

def CacheToDict():

    cacheDict = {}
    print(cache)

    for cacheItem in cache:

        cacheDict[cacheItem] = ObjectListToDictList(cache[cacheItem])

    return cacheDict

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["15000 per day", "600 per hour"]
)

@app.route("/")
def GithubRedirect():
    return redirect("https://github.com/BadgerHobbs/Parkrun-API-Python", code=302)

@app.route("/v1/cache")
def GetCache():
    return json.dumps(CacheToDict())

@app.route("/v1/countries")
def GetCountries():

    if "countries" not in cache:
        cache["countries"] = parkrun.Country.GetAllCountries()

    return json.dumps(ObjectListToDictList(cache["countries"]))

# Event Specific Data
@app.route("/v1/events")
def GetEvents():

    if "events" not in cache:
        cache["events"] = parkrun.Event.GetAllEvents()

    return json.dumps(ObjectListToDictList(cache["events"]))

@app.route("/v1/events/<event_id>/history")
def GetEventHistory(event_id):

    if f"events/{event_id}/history" not in cache:
        cache[f"events/{event_id}/history"] = parkrun.EventHistory.GetEventHistorys(GetEventById(event_id))

    return json.dumps(ObjectListToDictList(cache[f"events/{event_id}/history"]))

@app.route("/v1/events/<event_id>/first-finishers")
def GetFirstFinishers(event_id):

    if f"events/{event_id}/first-finishers" not in cache:
        cache[f"events/{event_id}/first-finishers"] = parkrun.FirstFinisher.GetFirstFinishers(GetEventById(event_id))

    return json.dumps(ObjectListToDictList(cache[f"events/{event_id}/first-finishers"]))

@app.route("/v1/events/<event_id>/age-category-records")
def GetAgeCategoryRecords(event_id):

    if f"events/{event_id}/age-category-records" not in cache:
        cache[f"events/{event_id}/age-category-records"] = parkrun.AgeCategoryRecord.GetAgeCategoryRecords(GetEventById(event_id))

    return json.dumps(ObjectListToDictList(cache[f"events/{event_id}/age-category-records"]))

@app.route("/v1/events/<event_id>/clubs")
def GetClubs(event_id):

    if f"events/{event_id}/clubs" not in cache:
        cache[f"events/{event_id}/clubs"] = parkrun.Club.GetClubs(GetEventById(event_id))

    return json.dumps(ObjectListToDictList(cache[f"events/{event_id}/clubs"]))

@app.route("/v1/events/<event_id>/sub-20-women")
def GetSub20Women(event_id):

    if f"events/{event_id}/sub-20-women" not in cache:
        cache[f"events/{event_id}/sub-20-women"] = parkrun.Sub20Woman.GetSub20Women(GetEventById(event_id))

    return json.dumps(ObjectListToDictList(cache[f"events/{event_id}/sub-20-women"]))

@app.route("/v1/events/<event_id>/sub-17-men")
def GetSub17Men(event_id):

    if f"events/{event_id}/sub-17-men" not in cache:
        cache[f"events/{event_id}/sub-17-men"] = parkrun.Sub17Man.GetSub17Men(GetEventById(event_id))

    return json.dumps(ObjectListToDictList(cache[f"events/{event_id}/sub-17-men"]))

@app.route("/v1/events/<event_id>/age-graded-league-ranks")
def GetAgeGradedLeagueRanks(event_id):

    quantity = 1000

    if request.args.get('quantity'):
        quantity = int(request.args.get('quantity'))

    if f"events/{event_id}/age-graded-league-ranks" not in cache:
        cache[f"events/{event_id}/age-graded-league-ranks"] = parkrun.AgeGradedLeagueRank.GetAgeGradedLeagueRanks(GetEventById(event_id), quantity=quantity)

    return json.dumps(ObjectListToDictList(cache[f"events/{event_id}/age-graded-league-ranks"]))

@app.route("/v1/events/<event_id>/fastest-500")
def GetFastest500(event_id):

    if f"events/{event_id}/fastest-500" not in cache:
        cache[f"events/{event_id}/fastest-500"] = parkrun.Fastest.GetFastest500(GetEventById(event_id))

    return json.dumps(ObjectListToDictList(cache[f"events/{event_id}/fastest-500"]))

# Country Specific Data
@app.route("/v1/countries/<country_id>/week-first-finishers")
def GetWeekFirstFinishersForCountry(country_id):

    if f"countries/{country_id}/week-first-finishers" not in cache:
        cache[f"countries/{country_id}/week-first-finishers"] = parkrun.WeekFirstFinisher.GetWeekFirstFinishersForCountry(GetCountryById(country_id))

    return json.dumps(ObjectListToDictList(cache[f"countries/{country_id}/week-first-finishers"]))

@app.route("/v1/countries/<country_id>/week-sub-17-runs")
def GetWeekSub17RunsForCountry(country_id):

    if f"countries/{country_id}/week-sub-17-runs" not in cache:
        cache[f"countries/{country_id}/week-sub-17-runs"] = parkrun.WeekSub17Run.GetWeekSub17RunsForCountry(GetCountryById(country_id))

    return json.dumps(ObjectListToDictList(cache[f"countries/{country_id}/week-sub-17-runs"]))

@app.route("/v1/countries/<country_id>/week-top-age-grades")
def GetWeekTopAgeGradesForCountry(country_id):

    if f"countries/{country_id}/week-top-age-grades" not in cache:
        cache[f"countries/{country_id}/week-top-age-grades"] = parkrun.WeekTopAgeGrade.GetWeekTopAgeGradesForCountry(GetCountryById(country_id))

    return json.dumps(ObjectListToDictList(cache[f"countries/{country_id}/week-top-age-grades"]))

@app.route("/v1/countries/<country_id>/week-new-category-records")
def GetWeekNewCategoryRecordsForCountry(country_id):

    if f"countries/{country_id}/week-new-category-records" not in cache:
        cache[f"countries/{country_id}/week-new-category-records"] = parkrun.WeekNewCategoryRecord.GetWeekNewCategoryRecordsForCountry(GetCountryById(country_id))

    return json.dumps(ObjectListToDictList(cache[f"countries/{country_id}/week-new-category-records"]))

@app.route("/v1/countries/<country_id>/course-records")
def GetCourseRecordsForCountry(country_id):

    if f"countries/{country_id}/course-records" not in cache:
        cache[f"countries/{country_id}/course-records"] = parkrun.CourseRecord.GetCourseRecordsForCountry(GetCountryById(country_id))

    return json.dumps(ObjectListToDictList(cache[f"countries/{country_id}/course-records"]))

@app.route("/v1/countries/<country_id>/attendance-records")
def GetAttendanceRecordsForCountry(country_id):

    if f"countries/{country_id}/attendance-records" not in cache:
        cache[f"countries/{country_id}/attendance-records"] = parkrun.AttendanceRecord.GetAttendanceRecordsForCountry(GetCountryById(country_id))

    return json.dumps(ObjectListToDictList(cache[f"countries/{country_id}/attendance-records"]))

@app.route("/v1/countries/<country_id>/most-events")
def GetMostEventsForCountry(country_id):

    if f"countries/{country_id}/most-events" not in cache:
        cache[f"countries/{country_id}/most-events"] = parkrun.MostEvent.GetMostEventsForCountry(GetCountryById(country_id))

    return json.dumps(ObjectListToDictList(cache[f"countries/{country_id}/most-events"]))

@app.route("/v1/countries/<country_id>/largest-clubs")
def GetLargestClubsForCountry(country_id):

    if f"countries/{country_id}/largest-clubs" not in cache:
        cache[f"countries/{country_id}/largest-clubs"] = parkrun.LargestClub.GetLargestClubsForCountry(GetCountryById(country_id))

    return json.dumps(ObjectListToDictList(cache[f"countries/{country_id}/largest-clubs"]))

@app.route("/v1/countries/<country_id>/joined-100-club")
def GetJoined100ClubsForCountry(country_id):

    if f"countries/{country_id}/joined-100-club" not in cache:
        cache[f"countries/{country_id}/joined-100-club"] = parkrun.Joined100Club.GetJoined100ClubsForCountry(GetCountryById(country_id))

    return json.dumps(ObjectListToDictList(cache[f"countries/{country_id}/joined-100-club"]))

@app.route("/v1/countries/<country_id>/most-first-finishes")
def GetMostFirstFinishesForCountry(country_id):

    if f"countries/{country_id}/most-first-finishes" not in cache:
        cache[f"countries/{country_id}/most-first-finishes"] = parkrun.MostFirstFinish.GetMostFirstFinishesForCountry(GetCountryById(country_id))

    return json.dumps(ObjectListToDictList(cache[f"countries/{country_id}/most-first-finishes"]))

@app.route("/v1/countries/<country_id>/freedom-runs")
def GetFreedomRunsForCountry(country_id):

    if f"countries/{country_id}/freedom-runs" not in cache:
        cache[f"countries/{country_id}/freedom-runs"] = parkrun.FreedomRun.GetFreedomRunsForCountry(GetCountryById(country_id))

    return json.dumps(ObjectListToDictList(cache[f"countries/{country_id}/freedom-runs"]))

@app.route("/v1/countries/<country_id>/historic-numbers")
def GetHistoricNumbersForCountry(country_id):

    if f"countries/{country_id}/historic-numbers" not in cache:
        cache[f"countries/{country_id}/historic-numbers"] = parkrun.HistoricNumber.GetHistoricNumbersForCountry(GetCountryById(country_id))

    return json.dumps(ObjectListToDictList(cache[f"countries/{country_id}/historic-numbers"]))

# Global Results Data
@app.route("/v1/global/results/week-first-finishers")
def GetWeekFirstFinishersGlobally():

    if f"global/results/week-first-finishers" not in cache:
        cache[f"global/results/week-first-finishers"] = parkrun.WeekFirstFinisher.GetWeekFirstFinishersGlobally()

    return json.dumps(ObjectListToDictList(cache[f"global/results/week-first-finishers"]))

@app.route("/v1/global/results/new-category-records")
def GetWeekNewCategoryRecordsGlobally():

    if f"global/results/new-category-records" not in cache:
        cache[f"global/results/new-category-records"] = parkrun.WeekNewCategoryRecord.GetWeekNewCategoryRecordsGlobally()

    return json.dumps(ObjectListToDictList(cache[f"global/results/new-category-records"]))

@app.route("/v1/global/results/sub-17-runs")
def GetWeekSub17RunsGlobally():

    if f"global/results/sub-17-runs" not in cache:
        cache[f"global/results/sub-17-runs"] = parkrun.WeekSub17Run.GetWeekSub17RunsGlobally()

    return json.dumps(ObjectListToDictList(cache[f"global/results/sub-17-runs"]))

@app.route("/v1/global/results/top-age-grades")
def GetWeekTopAgeGradesGlobally():

    if f"global/results/top-age-grades" not in cache:
        cache[f"global/results/top-age-grades"] = parkrun.WeekTopAgeGrade.GetWeekTopAgeGradesGlobally()

    return json.dumps(ObjectListToDictList(cache[f"global/results/top-age-grades"]))

@app.route("/v1/global/results/course-records")
def GetCourseRecordsGlobally():

    if f"global/results/course-records" not in cache:
        cache[f"global/results/course-records"] = parkrun.CourseRecord.GetCourseRecordsGlobally()

    return json.dumps(ObjectListToDictList(cache[f"global/results/course-records"]))

@app.route("/v1/global/results/freedom-runs")
def GetFreedomRunsGlobally():

    if f"global/results/freedom-runs" not in cache:
        cache[f"global/results/freedom-runs"] = parkrun.FreedomRun.GetFreedomRunsGlobally()

    return json.dumps(ObjectListToDictList(cache[f"global/results/freedom-runs"]))

# Global Stats Data
@app.route("/v1/global/stats/largest-clubs")
def GetLargestClubsGlobally():

    if f"global/stats/largest-clubs" not in cache:
        cache[f"global/stats/largest-clubs"] = parkrun.Club.GetLargestClubsGlobally()

    return json.dumps(ObjectListToDictList(cache[f"global/stats/largest-clubs"]))

@app.route("/v1/global/stats/attendance-records")
def GetAttendanceRecordsGlobally():

    if f"global/stats/attendance-records" not in cache:
        cache[f"global/stats/attendance-records"] = parkrun.AttendanceRecord.GetAttendanceRecordsGlobally()

    return json.dumps(ObjectListToDictList(cache[f"global/stats/attendance-records"]))

@app.route("/v1/global/stats/most-events")
def GetMostEventsGlobally():

    if f"global/stats/most-events" not in cache:
        cache[f"global/stats/most-events"] = parkrun.MostEvent.GetMostEventsGlobally()

    return json.dumps(ObjectListToDictList(cache[f"global/stats/most-events"]))

@app.route("/v1/global/stats/most-first-finishes")
def GetMostFirstFinishesGlobally():

    if f"global/stats/most-first-finishes" not in cache:
        cache[f"global/stats/most-first-finishes"] = parkrun.MostFirstFinish.GetMostFirstFinishesGlobally()

    return json.dumps(ObjectListToDictList(cache[f"global/stats/most-first-finishes"]))

if __name__ == '__main__':

    Setup()
    app.run(host='0.0.0.0', port=5000)