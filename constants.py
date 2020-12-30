## CONSTANTS
from pathlib import Path

DEFAULT_QUESTION = {
    'type'            : 'quiz',
    'question'        : '',
    'time'            : 20000,
    'points'          : True,
    'pointsMultiplier': 1,
    'choices'         : [],
    'layout'          : 'CLASSIC',
    'resources'       : '',
    'video'           : {
        'startTime': 0.0,
        'endTime'  : 0.0,
        'service'  : 'youtube',
        'fullUrl'  : ''},
    'questionFormat'  : 0}
DEFAULT_KAHOOT = {
    "id"          : None,
    "kahootExists": False,
    "kahoot"      : {
        "cover"           : "",
        "coverMetadata"   : None,
        "created"         : None,
        "creator_username": "",
        "description"     : "",
        "folderId"        : "",
        "introVideo"      : "",
        "language"        : "English",
        "lobby_video"     : {
            "youtube": {
                "id"       : "",
                "fullUrl"  : "",
                "startTime": 0
            }
        },
        "metadata"        : {
            "resolution"           : "",
            "duplicationProtection": False,
            "moderation"           : {
                "flaggedTimestamp"   : 0,
                "timestampResolution": 0
            },
            "resolution"           : ""
        },
        "organisation"    : None,
        "questions"       : [
            {
                "question"        : "",
                "type"            : "quiz",
                "layout"          : "CLASSIC",
                "image"           : None,
                "imageMetadata"   : None,
                "choices"         : [],
                "numberOfAnswers" : 0,
                "pointsMultiplier": 1,
                "question"        : "",
                "questionFormat"  : 0,
                "resources"       : "",
                "time"            : 20000,
                "type"            : "quiz",
                "video"           : {
                    "id"       : None,
                    "endTime"  : 0,
                    "startTime": 0,
                    "service"  : None,
                    "fullUrl"  : ""
                }
            }
        ],
        "quizType"        : "quiz",
        "resources"       : "",
        "themeId"         : None,
        "title"           : "",
        "type"            : "quiz",
        "uuid"            : None,
        "visibility"      : 0
    }
}

base_folder_path = Path(__file__).parent
