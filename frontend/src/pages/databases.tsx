import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function DBPage(){
    const databases = [
        {
            id: "2e7e89d8-faff-4c1f-933b-2be43034ff3d",
            name: "Test",
            tables: 3,
            size: "1GB"
        },
        {
            id: "2e7e89d8-faff-4c1f-933b-2be43034ff3d",
            name: "Test",
            tables: 3,
            size: "15MB"
        },
        {
            id: "2e7e89d8-faff-4c1f-933b-2be43034ff3d",
            name: "Test",
            tables: 3,
            size: "1GB"
        },
    ]
    return(
      <>
        {databases.map((database) => (
            <Card>
                <CardHeader>
                    <CardTitle>
                        {database.name}
                    </CardTitle>
                </CardHeader>
                <CardContent>

                    <p>Tables: {database.tables}</p>
                    <p>Size: {database.size}</p>
                </CardContent>
            </Card>
        ))}
      </>  
    )
}
