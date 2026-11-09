// Site-wide singletons (identity, contact, social, navigation).
// Kept here rather than in a content collection so layout components can
// import them directly.
//
// ⚙️  EDIT THIS FIRST: replace every placeholder below with your lab's details.
//    (Tip: ask Claude to "fill in src/data/site.ts for my lab" and paste your
//    name, institution, and a one-line mission.)

export interface NavItem {
  label: string;
  href: string;
}

export interface SiteConfig {
  name: string;
  shortName: string;
  pi: string;
  institution: string;
  university: string;
  url: string;
  description: string;
  email: string;
  phone: string;
  address: string[];
  mapQuery: string;
  social: {
    scholar?: string;
    twitter?: string;
    github?: string;
  };
  nav: NavItem[];
}

export const site: SiteConfig = {
  name: "SwarmsLab — Robotics Laboratory",
  shortName: "SwarmsLab",
  pi: "David Saldaña",
  institution: "Computer Science & Engineering",
  university: "Lehigh University",
  url: "https://swarmslab.com",
  description: "We develop cooperative aerial robots that assemble, manipulate, and work together. Exploring what becomes possible when robots act as a swarm.",
  email: "saldana@lehigh.edu",
  phone: "",
  address: ["SwarmsLab · Building C", "113 Research Drive", "Mountaintop Campus, Lehigh University", "Bethlehem, PA 18015"],
  mapQuery: "113 Research Drive, Bethlehem, PA 18015",
  social: { scholar: "https://scholar.google.com/citations?user=VU1s_Z8AAAAJ", twitter: "https://twitter.com/dsaldana1", github: "https://github.com/LehighBlimpGroup" },
  nav: [
    { label: "Research", href: "/research/" },
    { label: "Our Robots", href: "/robots/" },
    { label: "Team", href: "/people/" },
    { label: "Publications", href: "/publications/" },
    { label: "Videos", href: "/videos/" },
    { label: "Club", href: "/club/" },
    { label: "Contact", href: "/contact/" },
  ],
};
