const API_BASE_URL = "http://localhost:3000/api";

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

export interface CollegeParam {
    division?: string;
    gender?: string;
}

export const getColleges = async (params: CollegeParam = {}): Promise<College[]> => {
    const queryParams = new URLSearchParams();
    if (params.division) queryParams.append('division', params.division);
    if (params.gender) queryParams.append('gender', params.gender);

    const url = `${API_BASE_URL}/colleges${queryParams.toString()? "?"+queryParams.toString(): ""}`;
    console.log(url)
    
    const res = await fetch(url);

    if (!res.ok) {
        throw new Error(`HTTP Error: ${res.status}`);
    }

    return res.json();
};

console.log(getColleges({'division':'i', 'gender':'f'}))

