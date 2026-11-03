  
Initial Schema Design   
  ┌─────────────────┐             ┌──────────────────┐
  │  competitions   │             │      clubs       │
  ├─────────────────┤             ├──────────────────┤
  │ competition_id  │◄──┐         │ club_id          │◄──┐
  │ competition_name│   │         │ club_name        │   │
  └─────────────────┘   │         └──────────────────┘   │
                        │                   ▲            │
                        │                   │            │
                        │                   │ (home)     │ (away)
                        │                   │            │
                        │         ┌─────────┴────────────┴─────────┐
                        │         │            matches             │
                        │         ├────────────────────────────────┤
                        └─────────┤ competition_id                 │
                                  │ home_club_id                   │
                                  │ away_club_id                   │
                                  └─────────┬──────────────────────┘
                                            │
                                            │ (match_id)
                                            ▼
                                  ┌────────────────────────────────┐
                                  │       club_elo_history         │
                                  ├────────────────────────────────┤
                                  │ club_id ──► (links to clubs)   │
                                  │ match_id ──► (links to matches)│
                                  └────────────────────────────────┘