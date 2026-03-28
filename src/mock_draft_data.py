import pandas as pd

# Standard 2026 Draft Order (Pre-Trade)
DEFAULT_ORDER = {
    1: "LV", 2: "NYJ", 3: "ARI", 4: "TEN", 5: "NYG",
    6: "CLE", 7: "WAS", 8: "NO", 9: "KC", 10: "CIN",
    11: "MIA", 12: "DAL", 13: "ATL", 14: "BAL", 15: "TB"
}

# Mock Draft Metadata Registry
MOCK_REGISTRY = {
    "NFL_DJ": {"source": "NFL.com", "author": "Daniel Jeremiah", "version": "Mock 3.0", "date": "2026-03-18", "context": "Post-Combine", "url": "https://www.nfl.com/author/daniel-jeremiah", "last_checked": "2026-03-26"},
    "NFL_BB": {"source": "NFL.com", "author": "Bucky Brooks", "version": "Mock 3.0", "date": "2026-03-24", "context": "Post-Pro Day", "url": "https://www.nfl.com/author/bucky-brooks", "last_checked": "2026-03-26"},
    "ESPN_JR": {"source": "ESPN", "author": "Jordan Reid", "version": "Post-FA Mock", "date": "2026-03-03", "context": "Post-Initial Free Agency", "url": "https://www.espn.com/college-football/insider/index/_/name/jordan-reid", "last_checked": "2026-03-26"},
    "RING_DK": {"source": "The Ringer", "author": "Danny Kelly", "version": "Mock 2.0", "date": "2026-03-04", "context": "Post-Combine", "url": "https://www.theringer.com/authors/danny-kelly", "last_checked": "2026-03-26"},
    "ESPN_FY": {"source": "ESPN", "author": "Field Yates", "version": "Post-FA Mock", "date": "2026-03-24", "context": "Post-Free Agency Wave 2", "url": "https://www.espn.com/college-football/insider/index/_/name/field-yates", "last_checked": "2026-03-26"},
    "ATH_DB": {"source": "The Athletic", "author": "Dane Brugler", "version": "Post-Combine", "date": "2026-03-15", "context": "Post-Combine", "url": "https://www.nytimes.com/athletic/author/dane-brugler/", "last_checked": "2026-03-26"},
    "PFF_TS": {"source": "PFF", "author": "Trevor Sikkema", "version": "Post-FA Mock", "date": "2026-03-16", "context": "Post-FA Analytics", "url": "https://www.pff.com/author/trevor-sikkema", "last_checked": "2026-03-26"},
    "CBS_RW": {"source": "CBS Sports", "author": "Ryan Wilson", "version": "Mock 5.0", "date": "2026-03-26", "context": "Trade SZN", "url": "https://www.cbssports.com/writers/ryan-wilson/", "last_checked": "2026-03-26"},
    "RING_DL": {"source": "The Ringer", "author": "Diante Lee", "version": "Post-FA Mock", "date": "2026-03-13", "context": "Deep Dive", "url": "https://www.theringer.com/authors/diante-lee", "last_checked": "2026-03-26"},
    "ATH_BW": {"source": "The Athletic", "author": "Beat Writers", "version": "Mock 2.0", "date": "2026-03-19", "context": "Team Insider Insights", "url": "https://www.nytimes.com/athletic/tag/nfl-mock-draft/", "last_checked": "2026-03-26"}
}

# Verified (Pick, Team, Player, SourceID, Position)
DRAFT_DATA = [
    # Pick 1 - LV
    (1, "LV", "Fernando Mendoza", "NFL_DJ", "QB"), (1, "LV", "Fernando Mendoza", "NFL_BB", "QB"),
    (1, "LV", "Fernando Mendoza", "ESPN_JR", "QB"), (1, "LV", "Fernando Mendoza", "RING_DK", "QB"),
    (1, "LV", "Fernando Mendoza", "ESPN_FY", "QB"), (1, "LV", "Fernando Mendoza", "ATH_DB", "QB"),
    (1, "LV", "Fernando Mendoza", "PFF_TS", "QB"), (1, "LV", "Fernando Mendoza", "CBS_RW", "QB"),
    (1, "LV", "Fernando Mendoza", "RING_DL", "QB"), (1, "LV", "Fernando Mendoza", "ATH_BW", "QB"),

    # Pick 2 - NYJ
    (2, "NYJ", "Arvell Reese", "NFL_DJ", "EDGE"), (2, "NYJ", "David Bailey", "NFL_BB", "EDGE"),
    (2, "NYJ", "Arvell Reese", "ESPN_JR", "EDGE"), (2, "NYJ", "Arvell Reese", "RING_DK", "EDGE"),
    (2, "NYJ", "David Bailey", "ESPN_FY", "EDGE"), (2, "NYJ", "Arvell Reese", "ATH_DB", "EDGE"),
    (2, "NYJ", "Arvell Reese", "PFF_TS", "EDGE"), (2, "NYJ", "Arvell Reese", "CBS_RW", "EDGE"),
    (2, "NYJ", "Arvell Reese", "RING_DL", "EDGE"), (2, "NYJ", "Arvell Reese", "ATH_BW", "EDGE"),

    # Pick 3 - ARI
    (3, "ARI", "Spencer Fano", "NFL_DJ", "OT"), (3, "ARI", "Arvell Reese", "NFL_BB", "EDGE"),
    (3, "ARI", "David Bailey", "ESPN_JR", "EDGE"), (3, "ARI", "David Bailey", "RING_DK", "EDGE"),
    (3, "ARI", "Arvell Reese", "ESPN_FY", "EDGE"), (3, "ARI", "David Bailey", "ATH_DB", "EDGE"),
    (3, "ARI", "Sonny Styles", "PFF_TS", "LB"), (3, "ARI", "Peter Woods", "CBS_RW", "DT"),
    (3, "ARI", "David Bailey", "RING_DL", "EDGE"), (3, "ARI", "Spencer Fano", "ATH_BW", "OT"),

    # Pick 4 - TEN
    (4, "TEN", "Francis Mauigoa", "NFL_DJ", "OT"), (4, "TEN", "Jeremiyah Love", "NFL_BB", "RB"),
    (4, "TEN", "Rueben Bain Jr.", "ESPN_JR", "EDGE"), (4, "TEN", "Rueben Bain Jr.", "RING_DK", "EDGE"),
    (4, "TEN", "Sonny Styles", "ESPN_FY", "LB"), (4, "TEN", "Rueben Bain Jr.", "ATH_DB", "EDGE"),
    (4, "TEN", "Jeremiyah Love", "PFF_TS", "RB"), (4, "TEN", "David Bailey", "CBS_RW", "EDGE"),
    (4, "TEN", "Rueben Bain Jr.", "RING_DL", "EDGE"), (4, "TEN", "Carnell Tate", "ATH_BW", "WR"),

    # Pick 5 - NYG
    (5, "NYG", "Mansoor Delane", "NFL_DJ", "CB"), (5, "NYG", "Sonny Styles", "NFL_BB", "LB"),
    (5, "NYG", "Sonny Styles", "ESPN_JR", "LB"), (5, "NYG", "Francis Mauigoa", "RING_DK", "OT"),
    (5, "NYG", "Caleb Downs", "ESPN_FY", "S"), (5, "NYG", "Sonny Styles", "ATH_DB", "LB"),
    (5, "NYG", "Carnell Tate", "PFF_TS", "WR"), (5, "NYG", "Carnell Tate", "CBS_RW", "WR"),
    (5, "NYG", "Francis Mauigoa", "RING_DL", "OT"), (5, "NYG", "Jordyn Tyson", "ATH_BW", "WR"),

    # Pick 6 - CLE
    (6, "CLE", "David Bailey", "NFL_DJ", "EDGE"), (6, "CLE", "Carnell Tate", "NFL_BB", "WR"),
    (6, "CLE", "Monroe Freeling", "ESPN_JR", "OT"), (6, "CLE", "Spencer Fano", "RING_DK", "OT"),
    (6, "CLE", "Carnell Tate", "ESPN_FY", "WR"), (6, "CLE", "Monroe Freeling", "ATH_DB", "OT"),
    (6, "CLE", "Monroe Freeling", "PFF_TS", "OT"), (6, "CLE", "Francis Mauigoa", "CBS_RW", "OT"),
    (6, "CLE", "Spencer Fano", "RING_DL", "OT"), (6, "CLE", "Monroe Freeling", "ATH_BW", "OT"),

    # Pick 7 - WAS
    (7, "WAS", "Sonny Styles", "NFL_DJ", "LB"), (7, "WAS", "Caleb Downs", "NFL_BB", "S"),
    (7, "WAS", "Caleb Downs", "ESPN_JR", "S"), (7, "WAS", "Sonny Styles", "RING_DK", "LB"),
    (7, "WAS", "Jeremiyah Love", "ESPN_FY", "RB"), (7, "WAS", "Caleb Downs", "ATH_DB", "S"),
    (7, "WAS", "Caleb Downs", "PFF_TS", "S"), (7, "WAS", "Keldric Faulk", "CBS_RW", "EDGE"),
    (7, "WAS", "Sonny Styles", "RING_DL", "LB"), (7, "WAS", "Caleb Downs", "ATH_BW", "S"),

    # Pick 8 - NO
    (8, "NO", "Jeremiyah Love", "NFL_DJ", "RB"), (8, "NO", "Jordyn Tyson", "NFL_BB", "WR"),
    (8, "NO", "Jeremiyah Love", "ESPN_JR", "RB"), (8, "NO", "Jeremiyah Love", "RING_DK", "RB"),
    (8, "NO", "Rueben Bain Jr.", "ESPN_FY", "EDGE"), (8, "NO", "Jeremiyah Love", "ATH_DB", "RB"),
    (8, "NO", "Jordyn Tyson", "PFF_TS", "WR"), (8, "NO", "Jeremiyah Love", "CBS_RW", "RB"),
    (8, "NO", "Jeremiyah Love", "RING_DL", "RB"), (8, "NO", "Carnell Tate", "ATH_BW", "WR"),

    # Pick 9 - KC
    (9, "KC", "Rueben Bain Jr.", "NFL_DJ", "EDGE"), (9, "KC", "Francis Mauigoa", "NFL_BB", "OT"),
    (9, "KC", "Carnell Tate", "ESPN_JR", "WR"), (9, "KC", "Kenyon Sadiq", "RING_DK", "TE"),
    (9, "KC", "Jordyn Tyson", "ESPN_FY", "WR"), (9, "KC", "Carnell Tate", "ATH_DB", "WR"),
    (9, "KC", "Kenyon Sadiq", "PFF_TS", "TE"), (9, "KC", "Caleb Downs", "CBS_RW", "S"),
    (9, "KC", "Kenyon Sadiq", "RING_DL", "TE"), (9, "KC", "Kenyon Sadiq", "ATH_BW", "TE"),

    # Pick 10 - CIN
    (10, "CIN", "Jermod McCoy", "NFL_DJ", "CB"), (10, "CIN", "Mansoor Delane", "NFL_BB", "CB"),
    (10, "CIN", "Mansoor Delane", "ESPN_JR", "CB"), (10, "CIN", "Caleb Downs", "RING_DK", "S"),
    (10, "CIN", "Mansoor Delane", "ESPN_FY", "CB"), (10, "CIN", "Mansoor Delane", "ATH_DB", "CB"),
    (10, "CIN", "David Bailey", "PFF_TS", "EDGE"), (10, "CIN", "David Bailey", "CBS_RW", "EDGE"),
    (10, "CIN", "Caleb Downs", "RING_DL", "S"), (10, "CIN", "Mansoor Delane", "ATH_BW", "CB"),

    # Pick 11 - MIA
    (11, "MIA", "Caleb Downs", "NFL_DJ", "S"), (11, "MIA", "Olaivavega Ioane", "NFL_BB", "G"),
    (11, "MIA", "Francis Mauigoa", "ESPN_JR", "OT"), (11, "MIA", "Carnell Tate", "RING_DK", "WR"),
    (11, "MIA", "Francis Mauigoa", "ESPN_FY", "OT"), (11, "MIA", "Francis Mauigoa", "ATH_DB", "OT"),
    (11, "MIA", "Francis Mauigoa", "PFF_TS", "OT"), (11, "MIA", "Emmanuel McNeil-Warren", "CBS_RW", "S"),
    (11, "MIA", "Carnell Tate", "RING_DL", "WR"), (11, "MIA", "Francis Mauigoa", "ATH_BW", "OT"),

    # Pick 12 - DAL
    (12, "DAL", "Carnell Tate", "NFL_DJ", "WR"), (12, "DAL", "Rueben Bain Jr.", "NFL_BB", "EDGE"),
    (12, "NYJ", "Makai Lemon", "ESPN_JR", "WR"), (12, "DAL", "Keldric Faulk", "RING_DK", "EDGE"),
    (12, "DAL", "Olaivavega Ioane", "ESPN_FY", "G"), (12, "DAL", "Keldric Faulk", "ATH_DB", "EDGE"),
    (12, "DAL", "Dillon Thieneman", "PFF_TS", "S"), (12, "DAL", "Mansoor Delane", "CBS_RW", "CB"),
    (12, "DAL", "Keldric Faulk", "RING_DL", "EDGE"), (12, "DAL", "Keldric Faulk", "ATH_BW", "EDGE"),

    # Pick 13 - LAR
    (13, "LAR", "Makai Lemon", "NFL_DJ", "WR"), (13, "LAR", "Emmanuel McNeil-Warren", "NFL_BB", "S"),
    (13, "LAR", "Kenyon Sadiq", "ESPN_JR", "TE"), (13, "LAR", "Mansoor Delane", "RING_DK", "CB"),
    (13, "LAR", "Kenyon Sadiq", "ESPN_FY", "TE"), (13, "LAR", "Kenyon Sadiq", "ATH_DB", "TE"),
    (13, "LAR", "Makai Lemon", "PFF_TS", "WR"), (13, "LAR", "Kenyon Sadiq", "CBS_RW", "TE"),
    (13, "LAR", "Mansoor Delane", "RING_DL", "CB"), (13, "LAR", "Makai Lemon", "ATH_BW", "WR"),

    # Pick 14 - BAL
    (14, "BAL", "Olaivavega Ioane", "NFL_DJ", "G"), (14, "BAL", "Keldric Faulk", "NFL_BB", "EDGE"),
    (14, "BAL", "Olaivavega Ioane", "ESPN_JR", "G"), (14, "BAL", "Olaivavega Ioane", "RING_DK", "G"),
    (14, "BAL", "Keldric Faulk", "ESPN_FY", "EDGE"), (14, "BAL", "Kayden McDonald", "ATH_DB", "DT"),
    (14, "BAL", "Olaivavega Ioane", "PFF_TS", "G"), (14, "BAL", "Olaivavega Ioane", "CBS_RW", "G"),
    (14, "BAL", "Olaivavega Ioane", "RING_DL", "G"), (14, "BAL", "Jeremiyah Love", "ATH_BW", "RB"),

    # Pick 15 - TB
    (15, "TB", "Keldric Faulk", "NFL_DJ", "EDGE"), (15, "TB", "Brandon Cisse", "NFL_BB", "CB"),
    (15, "TB", "Keldric Faulk", "ESPN_JR", "EDGE"), (15, "TB", "Akheem Mesidor", "RING_DK", "EDGE"),
    (15, "TB", "Akheem Mesidor", "ESPN_FY", "EDGE"), (15, "TB", "Akheem Mesidor", "ATH_DB", "EDGE"),
    (15, "TB", "Keldric Faulk", "PFF_TS", "EDGE"), (15, "TB", "Akheem Mesidor", "CBS_RW", "EDGE"),
    (15, "TB", "Akheem Mesidor", "RING_DL", "EDGE"), (15, "TB", "Akheem Mesidor", "ATH_BW", "EDGE")
]

def get_draft_dataframe():
    df_picks = pd.DataFrame(DRAFT_DATA, columns=["pick", "team", "player", "source_id", "position"])
    df_meta = pd.DataFrame.from_dict(MOCK_REGISTRY, orient='index').reset_index().rename(columns={'index': 'source_id'})
    df = df_picks.merge(df_meta, on="source_id")
    
    # Identify trades
    df['is_trade'] = df.apply(lambda x: x['team'] != DEFAULT_ORDER.get(x['pick']), axis=1)
    df['default_team'] = df['pick'].map(DEFAULT_ORDER)
    return df
