import React from 'react';

export const CompassIllustration: React.FC<{ className?: string }> = ({ className = 'w-32 h-32' }) => (
  <svg viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
    <circle cx="60" cy="60" r="50" stroke="#E3E1DA" strokeWidth="2" strokeDasharray="3 3" />
    <circle cx="60" cy="60" r="42" fill="#E3F1EF" fillOpacity="0.4" stroke="#0F6E68" strokeWidth="2.5" />
    <path d="M60 25V33M60 87V95M25 60H33M87 60H95" stroke="#0F6E68" strokeWidth="2" strokeLinecap="round" />
    <polygon points="60,35 68,57 60,85 52,57" fill="#E8A33D" />
    <polygon points="60,35 52,57 60,60" fill="#C78526" />
    <polygon points="60,85 68,57 60,60" fill="#0F6E68" />
    <polygon points="60,85 52,57 60,60" fill="#0A534E" />
    <circle cx="60" cy="60" r="4" fill="#FFFFFF" stroke="#1C2B2A" strokeWidth="2" />
  </svg>
);

export const MountainSummitIllustration: React.FC<{ className?: string }> = ({ className = 'w-36 h-28' }) => (
  <svg viewBox="0 0 140 100" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
    <path d="M10 90L60 25L85 60L105 35L135 90H10Z" fill="#E3F1EF" stroke="#0F6E68" strokeWidth="2" strokeLinejoin="round" />
    <path d="M60 25L45 45L60 40L75 48L60 25Z" fill="#FFFFFF" stroke="#0F6E68" strokeWidth="1.5" />
    <path d="M105 35L95 50L105 46L115 52L105 35Z" fill="#FFFFFF" stroke="#0F6E68" strokeWidth="1.5" />
    <path d="M60 25V12M60 12L72 17L60 22V12Z" fill="#E8A33D" stroke="#E8A33D" strokeWidth="1.5" strokeLinejoin="round" />
    <path d="M25 90H125" stroke="#E3E1DA" strokeWidth="3" strokeLinecap="round" />
    <circle cx="28" cy="72" r="3" fill="#2F8F5B" />
    <circle cx="50" cy="52" r="3" fill="#0F6E68" />
    <circle cx="78" cy="38" r="3" fill="#E8A33D" />
  </svg>
);

export const FlightSimulatorIllustration: React.FC<{ className?: string }> = ({ className = 'w-36 h-28' }) => (
  <svg viewBox="0 0 140 100" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
    <path d="M15 85C45 85 60 70 85 45C105 25 120 20 130 18" stroke="#0F6E68" strokeWidth="2.5" strokeLinecap="round" strokeDasharray="4 4" />
    <circle cx="85" cy="45" r="5" fill="#E8A33D" stroke="#FFFFFF" strokeWidth="2" />
    <circle cx="130" cy="18" r="6" fill="#2F8F5B" stroke="#FFFFFF" strokeWidth="2" />
    <path d="M20 90H130V92H20V90Z" fill="#E3E1DA" />
    <path d="M110 32L125 18L132 30L122 28L110 32Z" fill="#0F6E68" />
    <rect x="25" y="35" width="40" height="28" rx="6" fill="#FFFFFF" stroke="#E3E1DA" strokeWidth="1.5" />
    <path d="M32 45H58M32 52H48" stroke="#5E6B69" strokeWidth="1.5" strokeLinecap="round" />
  </svg>
);

export const PassportBadgeIllustration: React.FC<{ className?: string }> = ({ className = 'w-24 h-28' }) => (
  <svg viewBox="0 0 100 120" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
    <path d="M50 10L85 24V60C85 82 70 102 50 110C30 102 15 82 15 60V24L50 10Z" fill="#E3F1EF" stroke="#0F6E68" strokeWidth="2.5" strokeLinejoin="round" />
    <circle cx="50" cy="55" r="22" fill="#FFFFFF" stroke="#0F6E68" strokeWidth="2" />
    <path d="M42 55L48 61L60 48" stroke="#2F8F5B" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M50 22V28M50 82V88" stroke="#E8A33D" strokeWidth="2" strokeLinecap="round" />
  </svg>
);

export const MentorLightIllustration: React.FC<{ className?: string }> = ({ className = 'w-28 h-28' }) => (
  <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
    <circle cx="50" cy="46" r="24" fill="#E3F1EF" stroke="#0F6E68" strokeWidth="2" />
    <path d="M42 70H58M45 76H55" stroke="#1C2B2A" strokeWidth="2" strokeLinecap="round" />
    <path d="M44 64V70H56V64" stroke="#1C2B2A" strokeWidth="2" fill="#E3E1DA" />
    <path d="M50 32V24M28 46H20M72 46H80M34 30L28 24M66 30L72 24" stroke="#E8A33D" strokeWidth="2" strokeLinecap="round" />
    <path d="M46 48C46 45 54 45 54 48C54 52 48 53 48 56" stroke="#0F6E68" strokeWidth="2" strokeLinecap="round" />
    <circle cx="50" cy="60" r="1.5" fill="#0F6E68" />
  </svg>
);

