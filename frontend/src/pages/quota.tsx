import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { Progress } from "@/components/ui/progress";
import { getQuotaPageData } from "@/lib/api";
import { Calendar, Clock, Coins, Database, MoveRight, PercentDiamond, TrendingDown, TrendingUp, Zap } from "lucide-react";

import { CartesianGrid, Line, LineChart, ResponsiveContainer, XAxis, YAxis } from "recharts";
import { useEffect, useState } from "react";





let weeklyAllowance = 0;
let extraCredits = 0;
let trend = 0;
let daysUntilTopup = 0;
let currentUsage = 0;
let usagePercentage = 0;
let isNearLimit = false;

type UsageTrend = {
  date: string;
  usage: number;
  limit?: number; 
};

let usageTrend: UsageTrend[] = [

];

let refetch = true;
let refetchInterval = 2000; // 2 seconds

function QuotaPage() {
    const [quotaData, setQuotaData] = useState({
        currentUsage: 0,
        weeklyAllowance: 100,
        usageTrend: [] as UsageTrend[],
        trend: 0,
        daysUntilTopup: 7 - new Date().getDay(),
        extraCredits: 0,
        usagePercentage: 0,
        isNearLimit: false,
    });

    useEffect(() => {
        async function fetchQuotaData() {
            const data = await getQuotaPageData();
            if (data) {
                const weeklyAllowance = data.credits || 100;
                const currentUsage = data.used_this_week || 0;
                const usageTrend = data.weekly_usage.map((entry: UsageTrend) => ({
                    ...entry,
                    limit: weeklyAllowance,
                }));
                const usagePercentage = (currentUsage / weeklyAllowance) * 100;
                const isNearLimit = usagePercentage > 80;

                const trend = data.change_percent.toFixed(2);

                setQuotaData({
                    currentUsage,
                    weeklyAllowance,
                    usageTrend,
                    trend: trend,
                    daysUntilTopup: 7 - new Date().getDay(),
                    extraCredits: data.extra_credits || 0,
                    usagePercentage,
                    isNearLimit,
                });
            }
        }

        fetchQuotaData();
        const interval = setInterval(() => {
            if (refetch) {
                fetchQuotaData();
            }
        }, refetchInterval);

    }, []);

    const {
        currentUsage,
        weeklyAllowance,
        usageTrend,
        trend,
        daysUntilTopup,
        extraCredits,
        usagePercentage,
        isNearLimit,
    } = quotaData;

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
                            <ResponsiveContainer>
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
                        <CardTitle className="text-sm flex items-center gap-2">
                            <Calendar className="w-4" />
                            Next Reset
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{daysUntilTopup}</div>
                        <p className="text-xs text-muted-foreground">days remaining</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle className="text-sm flex items-center gap-2">
                            <Coins className="w-4" />
                            Extra Credits
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-green-600">{extraCredits.toLocaleString()}</div>
                        <p className="text-xs text-muted-foreground">bonus credits available</p>
                        <Badge variant="outline" className="mt-2">
                            Never expire! :)
                        </Badge>
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
                            ) : trend === 0 ? (
                                <MoveRight className="h-5 w-5 text-muted-foreground" />
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
                    <CardTitle>How do I get more credits?</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-sm text-muted-foreground">
                        We are an open source project so here are some ways you can get more credits:
                    </p>
                    <ul
                        className="list-disc pl-5 space-y-1 text-sm text-muted-foreground"
                        style={{ listStyleType: "-" }}
                    >
                        <li>Contribute to the codebase on GitHub</li>
                        <li>Report bugs and issues</li>
                        <li>Share HackDB with your friends and community</li>
                        <li>Support @hexagonicalhq or @meepstertron on GitHub</li>
                        <li>Use HackDB in open source projects</li>
                        <li>Beg @meepstertron on the hackclub slack /hj ?</li>
                    </ul>
                </CardContent>
            </Card>
        </div>
    );
}

export default QuotaPage;