import { AppWindow, Clock, Database, DiamondPercent, FileQuestion, MoveRight, TrendingDown, TrendingUp, Workflow } from "lucide-react";
import { useAuth } from "./components/authContext";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "./components/ui/chart";
import { CartesianGrid, Line, ResponsiveContainer, XAxis, YAxis, LineChart } from "recharts";
import { useEffect, useState } from "react";
import { API_URL } from "./lib/api";
import { toast } from "sonner";

function getDaysUntilNextMonday(): number {
  const today = new Date();
  const dayOfWeek = today.getDay(); // Sunday = 0, Monday = 1, ..., Saturday = 6
  const daysUntilMonday = (8 - dayOfWeek) % 7; // Calculate days until next Monday
  return daysUntilMonday === 0 ? 7 : daysUntilMonday; // If today is Monday, return 7
}

function App() {
  const [dashData, setDashData] = useState({
        "user_id": "someuuid",
        "username": "user",
        "email": "user@example.com",
        "credits": 100,
        "unlimited": false,
        "extra_credits": 0,
        "used_this_week": 0,
        "used_last_week": 0,
        "change_percent": 0,
        "weekly_usage": [],
        "requests_today": 0,
        "databases": 0
    });


    useEffect(() => {
        async function fetchData() {
            const response = await fetch(API_URL+"/dash", {
                method: "GET",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
            } );
            const data = await response.json();
            setDashData(data);




            if (!response.ok) {
                console.error("Failed to fetch dashboard data:", data);
                toast.error("Failed to fetch dashboard data. Please try again later.");
            }

            for (const entry of data.weekly_usage) {
                entry.limit = data.unlimited ? 1000000 : data.credits;
            }
        }
        fetchData();
    }, []);

    return (
        <div className="flex-1 space-y-6 p-0 ">
            <h1 className="text-xl">Hi {dashData.username}! Nice to see you</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Databases</CardTitle>
                <Database className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{dashData.databases}</div>
                <p className="text-xs text-muted-foreground">

                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Credits Used</CardTitle>
                <DiamondPercent className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{dashData.used_this_week}</div>
                <p className="text-xs text-muted-foreground">
                  {dashData.change_percent > 0 ? (
                      <TrendingUp className="h-3 w-5 text-orange-500 inline" />
                  ) : dashData.change_percent === 0 ? (
                      <MoveRight className="h-3 w-5 text-muted-foreground inline" />
                  ) : (
                      <TrendingDown className="h-3 w-5 text-green-500 inline" />
                  )} {Math.abs(dashData.change_percent)}% increase this week
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">API Requests Today</CardTitle>
                <AppWindow className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{dashData.requests_today} <span className="text-sm font-medium text-muted-foreground">/ ∞ </span></div>
                <p className="text-xs text-muted-foreground">

                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Days Until Reset</CardTitle>
                <Clock className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{getDaysUntilNextMonday()}</div>
                <p className="text-xs text-muted-foreground">
                  Quota resets weekly
                </p>
              </CardContent>
            </Card>
            <Card className="lg:col-span-2 lg:row-span-2">
              <CardHeader>
                <CardTitle className="text-xl font-bold">Credit Usage</CardTitle>
              </CardHeader>
              <CardContent>
                <ChartContainer
                    config={{
                        usage: {
                            label: "Usage",
                            color: "hsl(var(--chart-1))",
                        },
                        limit: {
                            label: "Limit",
                            color: "hsl(var(--chart-2))",
                        },
                    }}
                    className="h-[300px]"
                >
                    <ResponsiveContainer>
                        <LineChart data={dashData.weekly_usage}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="date" />
                            <YAxis />
                            <ChartTooltip content={<ChartTooltipContent />} />
                            <Line
                                type="monotone"
                                dataKey="usage"
                                stroke="#2a9d90"
                                strokeWidth={3}
                                dot={{ fill: "#2a9d90" }}
                            />
                            <Line
                                type="monotone"
                                dataKey="limit"
                                stroke="#e76e50"
                                strokeWidth={2}
                                strokeDasharray="5 5"
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </ChartContainer>
              </CardContent>
            </Card>
            <Card className="lg:col-span-2 lg:row-span-2">
              <CardHeader>
                <CardTitle className="text-xl font-bold">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col space-y-2">
                  <a href="/databases/create" className="text-blue-600 hover:underline">Create New Database</a>
                  <a href="/editor" className="text-blue-600 hover:underline">Open the editor</a>
                  <a href="/tokens" className="text-blue-600 hover:underline">Manage API Tokens</a>
                  <a href="/quota" className="text-blue-600 hover:underline">View Quota Details</a>

                </div>
              </CardContent>
            </Card>


        </div>

    </div>
  )
}

export default App
