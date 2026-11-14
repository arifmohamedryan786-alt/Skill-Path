from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/i18n", tags=["Internationalization"])

TRANSLATIONS = {
    "en": {
        "welcome": "Your Career Path, From Zero to Job-Ready",
        "subtitle": "Discover what fits you, know where to start this week, and track your progress to a high-paying job.",
        "start_discovery": "Discover My Career",
        "start_first_week": "Start My First Week",
        "view_roadmap": "View Complete Roadmap",
        "flight_simulator": "Career Flight Simulator",
        "skill_passport": "Verified Skill Passport",
        "mock_interview": "Mock Interview Coach",
        "career_guide": "Personalized Career Guide",
        "ai_mentor": "AI Career Mentor",
        "readiness_projection": "You are projected to be job-ready by",
        "hours_per_week": "Hours per week"
    },
    "hi": {
        "welcome": "स्किलपाथ – शून्य से जॉब-रेडी तक आपका करियर पथ",
        "subtitle": "जानिए कौन सा करियर आपके लिए सही है, इस हफ्ते कहाँ से शुरुआत करें, और अपनी नौकरी की तैयारी को ट्रैक करें।",
        "start_discovery": "मेरे करियर की खोज करें",
        "start_first_week": "मेरा पहला सप्ताह शुरू करें",
        "view_roadmap": "पूरा रोडमैप देखें",
        "flight_simulator": "करियर फ़्लाइट सिम्युलेटर",
        "skill_passport": "वेरिफाइड स्किल पासपोर्ट",
        "mock_interview": "मॉक इंटरव्यू कोच",
        "career_guide": "व्यक्तिगत करियर गाइड",
        "ai_mentor": "एआई करियर मेंटर",
        "readiness_projection": "आप इस तारीख तक जॉब-रेडी होने का अनुमान है",
        "hours_per_week": "प्रति सप्ताह अध्ययन घंटे"
    },
    "ta": {
        "welcome": "ஸ்கில்பாத் – பூஜ்ஜியத்திலிருந்து வேலைக்குத் தயாராகும் உங்கள் தொழில் பாதை",
        "subtitle": "உங்களுக்கு ஏற்ற தொழில் எதுவென்பதைக் கண்டறிந்து, இந்த வாரம் எங்கு தொடங்குவது என்பதைத் தெரிந்து கொள்ளுங்கள்.",
        "start_discovery": "எனது தொழிலைக் கண்டறியவும்",
        "start_first_week": "முதல் வாரத்தைத் தொடங்குங்கள்",
        "view_roadmap": "முழுமையான வரைபடத்தைக் காண்க",
        "flight_simulator": "தொழில் உருவகப்படுத்தி",
        "skill_passport": "சரிபார்க்கப்பட்ட திறன் பாஸ்போர்ட்",
        "mock_interview": "நேர்காணல் பயிற்சி ஆசிரியர்",
        "career_guide": "தனிப்பயனாக்கப்பட்ட தொழில் வழிகாட்டி",
        "ai_mentor": "செயற்கை நுண்ணறிவு வழிகாட்டி",
        "readiness_projection": "நீங்கள் வேலைக்குத் தயாராகும் உத்தேச தேதி",
        "hours_per_week": "வாராந்திர படிப்பு நேரம்"
    }
}

@router.get("/{lang}")
def get_language_strings(lang: str):
    lang_code = lang.lower()
    if lang_code not in TRANSLATIONS:
        return TRANSLATIONS["en"]
    return TRANSLATIONS[lang_code]

