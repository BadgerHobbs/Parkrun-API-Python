# Parkrun-API-Python
Python API for Parkrun data

## Example Usage
```python
def ExampleUsage():

    countries = Country.GetAllCountries()
    events = Event.GetAllEvents()
    Event.UpdateEventUrls(events, countries)

    selectedEvent = events[0]

    eventHistory = EventHistory.GetEventHistorys(selectedEvent)
    firstFinishers = FirstFinisher.GetFirstFinishers(selectedEvent)
    ageCategoryRecords = AgeCategoryRecord.GetAgeCategoryRecords(selectedEvent)
    clubs = Club.GetClubs(selectedEvent)
    sub20Women = Sub20Woman.GetSub20Women(selectedEvent)
    sub17Men = Sub17Man.GetSub17Men(selectedEvent)
    ageGradedLeagueRanks = AgeGradedLeagueRank.GetAgeGradedLeagueRanks(selectedEvent)
    fastest500 = Fastest.GetFastest500(selectedEvent)
    print("Done")
```
