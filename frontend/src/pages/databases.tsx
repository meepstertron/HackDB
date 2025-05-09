"use client"

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { getUsersDatabases } from "@/lib/api"
import { Plus } from "lucide-react"
import { useNavigate } from "react-router-dom"
import { useEffect, useState } from "react"

interface Database {
  id: string;
  name: string;
  tables: number;
}

export function DBPage() {
  const navigate = useNavigate()
  const [databases, setDatabases] = useState<Database[]>([])

  useEffect(() => {
    const fetchDatabases = async () => {
        try {
            const dbs = await getUsersDatabases();
            if (dbs && dbs.databases) {
                setDatabases(dbs.databases);
            } else {
                setDatabases([]); 
            }
        } catch (error) {
            console.error("Error fetching databases:", error);
            setDatabases([]);
        }
    };
    fetchDatabases();
}, []);



  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {databases.map((database) => (
        <Card
          onClick={() => (
            navigate(`/databases/${database.id}`)
          )}
          key={database.id}
          className="overflow-hidden border shadow-none border-border/40 transition-all hover:border-border/80"
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
      <Card onClick={() => (
        navigate("/databases/create")
      )}className="overflow-hidden border shadow-none border-border/40 transition-all hover:border-border/80 cursor-pointer">
        <CardContent className="flex flex-col items-center justify-center h-full">
          <Plus className="h-8 w-8 text-gray-500" />
          <span className="text-gray-500">Create new database</span>
          </CardContent>

      </Card>
    </div>
  )
}
