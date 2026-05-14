import { useState } from "react";

function LoginPage({ onLogin, loading, error }) {
    const [employeeId, setEmployeeId] = useState("EMP001");
    const [password, setPassword] = useState("demo");

    const handleSubmit = (event) => {
        event.preventDefault();
        onLogin({
            employee_id: employeeId,
            password
        });
    };

    return (
        <div className="login-page">
            <form className="login-card" onSubmit={handleSubmit}>
                <div className="brand-mark large">AI</div>
                <h1>Enterprise Travel Copilot</h1>
                <p>Sign in with your employee profile to plan policy-aware business travel.</p>

                <label>
                    Employee ID
                    <input
                        value={employeeId}
                        onChange={(event) => setEmployeeId(event.target.value)}
                        placeholder="EMP001"
                    />
                </label>

                <label>
                    Password
                    <input
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        placeholder="Any demo password"
                        type="password"
                    />
                </label>

                {error && (
                    <div className="form-error">
                        {error}
                    </div>
                )}

                <button disabled={loading}>
                    {loading ? "Signing in..." : "Sign in"}
                </button>
            </form>
        </div>
    );
}

export default LoginPage;
