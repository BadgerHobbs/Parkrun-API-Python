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