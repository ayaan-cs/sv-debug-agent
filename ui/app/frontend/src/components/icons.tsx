import type { SVGProps } from "react";

/* Simple 16/24px line glyphs for the workbench chrome. */

const base = (props: SVGProps<SVGSVGElement>) => ({
  viewBox: "0 0 16 16",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.3,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  "aria-hidden": true,
  ...props,
});

export const FilesIcon = (props: SVGProps<SVGSVGElement>) => (
  <svg {...base(props)} viewBox="0 0 24 24" strokeWidth={1.5}>
    <path d="M13.5 3H6.5A1.5 1.5 0 0 0 5 4.5v15A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5V8.5z" />
    <path d="M13.5 3v5.5H19" />
  </svg>
);

export const BugIcon = (props: SVGProps<SVGSVGElement>) => (
  <svg {...base(props)} viewBox="0 0 24 24" strokeWidth={1.5}>
    <rect x="7.5" y="7" width="9" height="11" rx="4.5" />
    <path d="M12 7V4.5M8 10.5H4.5M8 14.5H4.5M16 10.5H19.5M16 14.5H19.5M9.5 18.5 8 21M14.5 18.5 16 21" />
  </svg>
);

export const ThemeIcon = (props: SVGProps<SVGSVGElement>) => (
  <svg {...base(props)} viewBox="0 0 24 24" strokeWidth={1.5}>
    <circle cx="12" cy="12" r="5" />
    <path d="M12 4V2M12 22v-2M4 12H2M22 12h-2M5.6 5.6 4.2 4.2M19.8 19.8l-1.4-1.4M18.4 5.6l1.4-1.4M4.2 19.8l1.4-1.4" />
  </svg>
);

export const ChevronIcon = (props: SVGProps<SVGSVGElement>) => (
  <svg {...base(props)}>
    <path d="M5 6.5 8 9.5l3-3" />
  </svg>
);

export const SvFileIcon = (props: SVGProps<SVGSVGElement>) => (
  <svg {...base(props)}>
    <path d="M9.5 2H4.5A1 1 0 0 0 3.5 3v10a1 1 0 0 0 1 1h7a1 1 0 0 0 1-1V5z" />
    <path d="M9.5 2v3h3" />
  </svg>
);

export const PlayIcon = (props: SVGProps<SVGSVGElement>) => (
  <svg {...base(props)} fill="currentColor" stroke="none">
    <path d="M4.5 3.2 12.5 8l-8 4.8z" />
  </svg>
);

export const CloseIcon = (props: SVGProps<SVGSVGElement>) => (
  <svg {...base(props)}>
    <path d="M4 4l8 8M12 4l-8 8" />
  </svg>
);

export const ErrorIcon = (props: SVGProps<SVGSVGElement>) => (
  <svg {...base(props)}>
    <circle cx="8" cy="8" r="6" />
    <path d="M8 5v4M8 11h.01" />
  </svg>
);

export const SplitIcon = (props: SVGProps<SVGSVGElement>) => (
  <svg {...base(props)}>
    <rect x="2.5" y="3" width="11" height="10" rx="1" />
    <path d="M8 3v10" />
  </svg>
);
