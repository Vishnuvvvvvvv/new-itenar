function EmployeeProfile({ employee }) {
    if (!employee) return null;

    return (
        <div className="profile-card">
            <span>Employee profile</span>
            <h2>{employee.employee_name}</h2>
            <p>{employee.designation}</p>
            <div>{employee.department}</div>
            <div>{employee.employee_location}</div>
            <small>{employee.employee_id}</small>
        </div>
    );
}

export default EmployeeProfile;
