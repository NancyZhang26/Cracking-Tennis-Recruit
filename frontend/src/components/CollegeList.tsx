import { getColleges, type College } from '../services/api';
import { useState, useEffect } from 'react';

function CollegeList() {
    const [colleges, setColleges] = useState<College[]>([]);

    const [selectedGender, setSelectedGender] = useState<string>('');
    const [selectedDivision, setSelectedDivision] = useState<string>('');

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchColleges = async() => {
            try { 
                setLoading(true);
                const data = await getColleges({});
                setColleges(data)// source of truth
                setError(null);
            } catch(err) {
                setError(err instanceof Error? err.message: 'Failed to fetch colleges.');
            } finally {
                setLoading(false);
            }
        }

        fetchColleges(); // useEffect does not accpet async functions for effect callback
    
    }, [])

    const filteredColleges = colleges.filter((e) => {
        const genderOk = selectedGender? e.gender === selectedGender: true;
        const divisionOk = selectedDivision? e.division === selectedDivision: true;
        return genderOk && divisionOk;
    })

    if (loading) return <p>Loading...</p>
    if (error) return <p>Error: {error}</p>

    return (<>
        <h1>Colleges</h1>

        <div>
            <label>
                Gender: 
                <select value={selectedGender} onChange={(e) => setSelectedGender(e.target.value)}>
                    <option value="">All</option>
                    <option value="f">Women</option>
                    <option value="m">Men</option>
                </select>
            </label>

            <br/>

            <label>
                Division:
                <select value={selectedDivision} onChange={(e) => setSelectedDivision(e.target.value)}>
                    <option value="">All</option>
                    <option value="i">Division I</option>
                    <option value="ii">Division II</option>
                    <option value="iii">Division III</option>
                </select>
            </label>
        </div>

        <br/>

        <div>Showing {filteredColleges.length} colleges out of {colleges.length} colleges.</div>

        <ol>
            {filteredColleges.map((college, index) => (
                <li key={index}>
                    <strong>{college.school_name} - Division {college.division?.toUpperCase()} - {college.gender==='m'? "Men's Tennis Team": "Women's Tennis Team"}</strong>
                    <br/>
                    <small>{college.location}, {college.conference}</small>
                </li>
            ))}
        </ol>
    </>)

}

export default CollegeList;