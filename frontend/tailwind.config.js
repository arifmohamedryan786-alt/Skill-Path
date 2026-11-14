/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: '#F7F6F2',
        surface: '#FFFFFF',
        ink: {
          DEFAULT: '#1C2B2A',
          secondary: '#5E6B69',
          muted: '#8A9694',
        },
        border: {
          DEFAULT: '#E3E1DA',
          light: '#EFECE6',
        },
        primary: {
          DEFAULT: '#0F6E68',
          hover: '#0A534E',
          tint: '#E3F1EF',
          light: '#C9E6E3',
        },
        accent: {
          DEFAULT: '#E8A33D',
          hover: '#C78526',
          tint: '#FDF3E3',
        },
        status: {
          success: '#2F8F5B',
          'success-tint': '#E8F5EE',
          warning: '#D9822B',
          'warning-tint': '#FBF1E6',
          danger: '#C8463D',
          'danger-tint': '#FAEAE9',
        },
      },
      fontFamily: {
        serif: ['"Fraunces"', '"DM Serif Display"', 'Georgia', 'serif'],
        sans: ['"Plus Jakarta Sans"', '"Inter"', 'system-ui', '-apple-system', 'sans-serif'],
      },
      borderRadius: {
        sm: '6px',
        md: '10px',
        lg: '16px',
      },
      boxShadow: {
        soft: '0 2px 8px -2px rgba(28, 43, 42, 0.05), 0 1px 3px -1px rgba(28, 43, 42, 0.03)',
        card: '0 4px 16px -4px rgba(28, 43, 42, 0.07)',
        drawer: '0 8px 30px -4px rgba(28, 43, 42, 0.12)',
      },
    },
  },
  plugins: [],
}

