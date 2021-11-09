import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://tanlab6a.eastus.cloudapp.azure.com:8100/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Blood Pressure</th>
							<th>Heart Rate</th>
						</tr>
						<tr>
							<td># BP: {stats['student_count']}</td>
							<td># HR: {stats['class_count']}</td>
						</tr>
						<tr>
							<td colspan="2">Maximum number of students: {stats['num_students_in_class']}</td>
						</tr>
						<tr>
							<td colspan="2">Most Popular CIT course: {stats['most_popular_cit_class']}</td>
						</tr>
						<tr>
							<td colspan="2">Max HR: {stats['max_bp_sys_reading']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}