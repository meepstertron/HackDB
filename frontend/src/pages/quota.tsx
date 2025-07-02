import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { Progress } from "@/components/ui/progress";
import { Calendar, Clock, Coins, Database, PercentDiamond, TrendingDown, TrendingUp, Zap } from "lucide-react";
import { CartesianGrid, Line, LineChart, ResponsiveContainer, XAxis, YAxis } from "recharts";


const currentUsage = 3000 
const weeklyAllowance = 6000
const extraCredits = 2500
const trend = -23
let daysUntilTopup = 4
let usagePercentage = (currentUsage / weeklyAllowance) * 100
let isNearLimit = usagePercentage > 80


type UsageTrend = {
  date: string;
  usage: number;
  limit?: number; 
};

let usageTrend: UsageTrend[] = [
  { date: "Jan 1", usage: 2400 },
  { date: "Jan 8", usage: 1398 },
  { date: "Jan 15", usage: 9800 },
  { date: "Jan 22", usage: 3908 },
  { date: "Jan 29", usage: 4800 },
  { date: "Feb 5", usage: 10900 },
  { date: "Feb 12", usage: 4300 },
];

for (let i = 0; i < usageTrend.length; i++) {
    usageTrend[i].limit = weeklyAllowance; 
}

function QuotaPage() {

    return ( 
        <div className="container mx-auto p-0 space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold">Quota</h1>
                    <p className="text-muted-foreground">Monitor your credit usage and limits</p>

                </div>
                {isNearLimit && <Badge>Near Limit</Badge>}
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

                <Card className="lg:col-span-2 lg:row-span-2">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                        <Database className="h-5 w-5" />
                        Weekly Usage
                        </CardTitle>
                        <CardDescription>Your database usage over the past weeks</CardDescription>
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
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={usageTrend}>
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
                <Card>
                    <CardHeader>
                        <CardTitle className="text-sm flex items-center gap-2">Weekly Allowance</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{currentUsage.toLocaleString()}</div>
                        <p className="text-xs text-muted-foreground">of {weeklyAllowance.toLocaleString()} credits</p>
                        <Progress className="mt-3" value={usagePercentage} max={100} />
                        <div className="flex items-center pt-2">
                            <PercentDiamond className="h-4 w-4" />
                            <span className="text-xs text-muted-foreground ml-1"> {usagePercentage}% used</span>
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle className="text-sm flex items-center gap-2"><Calendar className="w-4"/>Next Reset</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{daysUntilTopup}</div>
                        <p className="text-xs text-muted-foreground">days remaining</p>
                        

                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle className="text-sm flex items-center gap-2"><Coins className="w-4"/>Extra Credits</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-green-600">{extraCredits.toLocaleString()}</div>
                        <p className="text-xs text-muted-foreground">bonus credits available</p>
                        <Badge variant="outline" className="mt-2">Never expire! :)</Badge>

                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium flex items-center gap-2">
                        <Zap className="h-4 w-4" />
                        Usage Trend
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center gap-2">
                        {trend > 0 ? (
                            <TrendingUp className="h-5 w-5 text-orange-500" />
                        ) : (
                            <TrendingDown className="h-5 w-5 text-green-500" />
                        )}
                        <span className="text-2xl font-bold">{trend}%</span>
                        </div>
                        <p className="text-xs text-muted-foreground">vs last week</p>

                    </CardContent>
                </Card>
            </div>
            <Card>
                <CardHeader>
                    <CardTitle>
                        How do I get more credits?
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-sm text-muted-foreground">
                        We are a open source project so here are some ways you can get more credits:


                        <ul className="list-disc pl-5 space-y-1">
                            <li>Contribute to the codebase on GitHub</li>
                            <li>Report bugs and issues</li>
                            <li>Share HackDB with your friends and community</li>
                            <li>Support @hexagonicalhq or @meepstertron on GitHub</li>
                            <li>Use HackDB in open source projects</li>
                            <li>Beg @meepstertron on the hackclub slack /hj ?</li>
                        </ul>
                    </p>
                </CardContent>
            </Card>
        </div>

     );
}

export default QuotaPage;