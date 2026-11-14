import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

export const resources = {
  en: {
    translation: {
      appName: 'SkillPath',
      tagline: 'Your Career Path, From Zero to Job-Ready',
      nav: {
        dashboard: 'Overview',
        discovery: 'Career Discovery',
        careers: 'Career Explorer',
        roadmap: 'My Roadmap',
        skills: 'Skill Gap Analysis',
        assessments: 'Checkpoint Tests',
        simulator: 'Flight Simulator',
        passport: 'Verified Passport',
        interview: 'Mock Interview',
        guide: 'Career Guide',
        mentor: 'AI Mentor',
        progress: 'My Progress',
        glossary: 'Glossary Terms',
        profile: 'Profile',
        admin: 'Admin Analytics',
        logout: 'Sign Out'
      },
      common: {
        back: 'Back',
        next: 'Next',
        save: 'Save Changes',
        loading: 'Loading...',
        completed: 'Completed',
        inProgress: 'In Progress',
        locked: 'Locked',
        verify: 'Verify',
        search: 'Search...',
        readiness: 'Job Readiness'
      },
      onboarding: {
        question: 'Do you already know the career you want?',
        optionKnown: 'Yes, I know my goal',
        optionRough: 'I have a rough idea',
        optionUnknown: 'I have no idea yet',
        step1Title: 'About You',
        step2Title: 'What do you enjoy doing?',
        step3Title: 'Current Skills & Coursework',
        step4Title: 'Weekly Study Schedule'
      }
    }
  },
  hi: {
    translation: {
      appName: 'स्किलपाथ',
      tagline: 'शून्य से नौकरी तक, आपका करियर मार्ग',
      nav: {
        dashboard: 'अवलोकन',
        discovery: 'करियर खोज',
        careers: 'करियर एक्सप्लोरर',
        roadmap: 'मेरा रोडमैप',
        skills: 'कौशल विश्लेषण',
        assessments: 'चेकपॉइंट टेस्ट',
        simulator: 'फ्लाइट सिम्युलेटर',
        passport: 'सत्यापित पासपोर्ट',
        interview: 'मॉक इंटरव्यू',
        guide: 'करियर गाइड',
        mentor: 'एआई मेंटर',
        progress: 'मेरी प्रगति',
        glossary: 'शब्दावली',
        profile: 'प्रोफाइल',
        admin: 'एडमिन विश्लेषण',
        logout: 'लॉग आउट'
      },
      common: {
        back: 'पीछे',
        next: 'आगे बढ़ें',
        save: 'बदलाव सहेजें',
        loading: 'लोड हो रहा है...',
        completed: 'पूर्ण',
        inProgress: 'जारी है',
        locked: 'लॉक्ड',
        verify: 'सत्यापित करें',
        search: 'खोजें...',
        readiness: 'नौकरी की तैयारी'
      },
      onboarding: {
        question: 'क्या आप पहले से जानते हैं कि आप कौन सा करियर चाहते हैं?',
        optionKnown: 'हाँ, मुझे मेरा लक्ष्य पता है',
        optionRough: 'मुझे एक मोटा अंदाजा है',
        optionUnknown: 'मुझे अभी बिल्कुल अंदाजा नहीं है',
        step1Title: 'आपके बारे में',
        step2Title: 'आपको क्या करना पसंद है?',
        step3Title: 'मौजूदा कौशल और पढ़ाई',
        step4Title: 'साप्ताहिक अध्ययन समय'
      }
    }
  },
  ta: {
    translation: {
      appName: 'ஸ்கில்பாத்',
      tagline: 'பூஜ்ஜியத்திலிருந்து வேலை வரை உங்கள் தொழில் பாதை',
      nav: {
        dashboard: 'கண்ணோட்டம்',
        discovery: 'தொழில் கண்டுபிடிப்பு',
        careers: 'தொழில் உலாவல்',
        roadmap: 'எனது கற்றல் பாதை',
        skills: 'திறன் இடைவெளி',
        assessments: 'சரிபார்ப்பு தேர்வுகள்',
        simulator: 'வேலை திட்டமிடல்',
        passport: 'சான்றளிக்கப்பட்ட கடவுச்சீட்டு',
        interview: 'போலி நேர்காணல்',
        guide: 'தொழில் வழிகாட்டி',
        mentor: 'AI வழிகாட்டி',
        progress: 'எனது முன்னேற்றம்',
        glossary: 'சொற்களஞ்சியம்',
        profile: 'சுயவிவரம்',
        admin: 'நிர்வாக பகுப்பாய்வு',
        logout: 'வெளியேறு'
      },
      common: {
        back: 'பின்செல்',
        next: 'அடுத்து',
        save: 'மாற்றங்களைச் சேமி',
        loading: 'ஏற்றப்படுகிறது...',
        completed: 'முடிந்தது',
        inProgress: 'நடைபெறுகிறது',
        locked: 'பூட்டப்பட்டது',
        verify: 'சரிபார்',
        search: 'தேடுக...',
        readiness: 'வேலை தயார்நிலை'
      },
      onboarding: {
        question: 'நீங்கள் விரும்பும் தொழில் பற்றி உங்களுக்குத் தெரியுமா?',
        optionKnown: 'ஆம், எனது இலக்கு எனக்குத் தெரியும்',
        optionRough: 'எனக்கு ஒரு தோராயமான யோசனை உள்ளது',
        optionUnknown: 'எனக்கு இன்னும் தெரியவில்லை',
        step1Title: 'உங்களைப் பற்றி',
        step2Title: 'நீங்கள் என்ன செய்ய விரும்புகிறீர்கள்?',
        step3Title: 'தற்போதைய திறன்கள்',
        step4Title: 'வாராந்திர படிப்பு நேரம்'
      }
    }
  }
};

i18n.use(initReactI18next).init({
  resources,
  lng: localStorage.getItem('skillpath_language') || 'en',
  fallbackLng: 'en',
  interpolation: {
    escapeValue: false
  }
});

export default i18n;

