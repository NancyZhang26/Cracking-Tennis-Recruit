export interface College {
    school_id?: number;
    club_id?: number;
    gender?: string;
    location?: string;
    division?: string;
    p6high?: number | null;
    p6low?: number | null;
    conference?: string | null;
    url?: string | null;
    school_name?: string;
    line_up_utr?: number[];  
    roster_utr?: number[];  
    line_up_utr_avg?: number;   
    roster_utr_avg?: number;
    conference_id?: number;
    type?: string | null;
    official_url?: string | null;
}

export interface Player {
    player_name?: string;
    gender?: string | null;
    player_id?: number;
    singles_utr?: number | null;
    doubles_utr?: number | null;
    location?: string | null;
    school_id?: number | null;
}

export interface CollegeTemp {
    school_name?: string;
    gender?: string;
    division?: string;
    conference?: string;
    location?: string;
    url?: string;
    type?: string | null;
}
