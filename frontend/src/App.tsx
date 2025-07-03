import { AppWindow, Clock, Database, DiamondPercent, FileQuestion, LineChart, TrendingUp, Workflow } from "lucide-react";
import { useAuth } from "./components/authContext";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "./components/ui/chart";
import { CartesianGrid, Line, ResponsiveContainer, XAxis, YAxis } from "recharts";



function App() {

  return (
    <div className="flex-1 space-y-6 p-0 ">

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Databases</CardTitle>
                <Database className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{4}</div>
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
                <div className="text-2xl font-bold">{4}</div>
                <p className="text-xs text-muted-foreground">
                  <TrendingUp className="inline h-3 w-3 text-red-500" /> 12% increase this week
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">API Requests Today</CardTitle>
                <AppWindow className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{0} <span className="text-sm font-medium text-muted-foreground">/ ∞ </span></div>
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
                <div className="text-2xl font-bold">{4}</div>
                <p className="text-xs text-muted-foreground">
                  Quota resets weekly
                </p>
              </CardContent>
            </Card>
            <Card className="lg:col-span-2 lg:row-span-2">

            </Card>
            <Card className="lg:col-span-2 lg:row-span-2">
              <CardHeader>
                <CardTitle className="text-xl font-bold">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col space-y-2">
                  <a href="/databases/create" className="text-blue-600 hover:underline">Create New Database</a>
                  <a href="/tokens" className="text-blue-600 hover:underline">Manage API Tokens</a>
                  <a href="/flow" className="text-blue-600 hover:underline">Flow Editor</a>
                </div>
              </CardContent>
            </Card>


        </div>

    </div>
  )
}

export default App
