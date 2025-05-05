"use client"

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Database, Table, HardDrive, DollarSign, MoreHorizontal, Pencil } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"

export function DBPage() {
  const databases = [
    {
      id: "2e7e89d8-faff-4c1f-933b-2be43034ff3d",
      name: "Test",
      tables: 3,
      size: "1GB",
      cost: 0.5,
      status: "active",
    },
    {
      id: "2e7e89d8-faff-4c1f-933b-2be43034ff3d",
      name: "Test",
      tables: 3,
      size: "15MB",
      cost: 0.5,
      status: "idle",
    },
    {
      id: "2e7e89d8-faff-4c1f-933b-2be43034ff3d",
      name: "Test",
      tables: 3,
      size: "1GB",
      cost: 0.5,
      status: "active",
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {databases.map((database) => (
        <Card
          key={database.id}
          className="overflow-hidden border border-border/40 transition-all hover:shadow-md hover:border-border/80"
        >
            <CardHeader>
                <div className="w-full text-right h-full">
                    
                </div>
                <CardTitle>
                    {database.name}
                </CardTitle>
                <div className="w-full text-right">

                </div>
            </CardHeader>
        </Card>
      ))}
    </div>
  )
}
