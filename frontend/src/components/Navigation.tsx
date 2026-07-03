export type PageName = "home" | "play" | "lab" | "history" | "architecture";

type NavigationProps = {
  activePage: PageName;
  onNavigate: (page: PageName) => void;
};

const navItems: { label: string; page: PageName }[] = [
  { label: "Home", page: "home" },
  { label: "Play Arena", page: "play" },
  { label: "AI Lab", page: "lab" },
  { label: "History", page: "history" },
  { label: "Architecture", page: "architecture" },
];

export function Navigation({ activePage, onNavigate }: NavigationProps) {
  return (
    <nav className="top-nav">
      <button className="brand-button" onClick={() => onNavigate("home")}>
        <span className="brand-mark">♠</span>
        <div>
          <strong>PokerMind</strong>
          <small>Arena</small>
        </div>
      </button>

      <div className="nav-links">
        {navItems.map((item) => (
          <button
            key={item.page}
            className={activePage === item.page ? "nav-link active" : "nav-link"}
            onClick={() => onNavigate(item.page)}
          >
            {item.label}
          </button>
        ))}
      </div>
    </nav>
  );
}
